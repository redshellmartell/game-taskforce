"""Heavenly Bodies rules engine (standard library only). Built from games/heavenly-bodies/rules.md + cards.json.
Every place where the rules are silent and an interpretation was chosen is tagged  # INTERP Gn  (see playtest-report.md).
Positions: 0=N 1=E 2=S 3=W. Rotation is clockwise (N->E->S->W->N)  # INTERP G1.
"""
import json, os, random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, "..", "cards.json")))
CARDS = {c["id"]: c for c in DATA["cards"]}
STARS = {s["id"]: s for s in DATA["stars"]}
PN = "NESW"
RESTRICT = {"CO02": {2}, "CO05": {0}, "CO10": {3}, "CO28": {1}, "CO32": {0, 2}}
AUG_IDS = [c["id"] for c in DATA["cards"] if c["subtype"] == "Augmentation"]


class Config:
    def __init__(self, n=2, stars=None, log=False, round_cap=60, extra_dmg=0, swap_dmg=0, first=None, deck_ids=None, first_draw=2):
        self.n, self.stars, self.log, self.round_cap = n, stars, log, round_cap
        self.extra_dmg = extra_dmg      # experiment: +N damage on every direct-damage AE
        self.swap_dmg = swap_dmg        # experiment: replace N low-value AEs with plain 1-damage copies
        self.first = first
        self.deck_ids = deck_ids; self.first_draw = first_draw


class CO:
    def __init__(self, card):
        self.card, self.id = card, card["id"]
        self.owner = None; self.pos = None; self.augs = []; self.temps = []

    def __repr__(self): return "%s(%d/%d)" % (self.id, self.card["size"], self.card["stability"])


class Aug:
    def __init__(self, card, host, src): self.card, self.id, self.host, self.src = card, card["id"], host, src


class Player:
    def __init__(self, i, star):
        self.i, self.star, self.sid = i, star, star["id"]
        self.hp = self.maxhp = star["hp"]
        self.hand, self.orbit = [], [None] * 4
        self.alive = True; self.cm = False; self.dmg_flag = False
        self.entered = 0; self.used = set(); self.plays = 0
        self.st12 = -1; self.st06 = -1
        self.thr = 13 if self.sid == "ST10" else 15
        self.turns = 0


class State:
    def __init__(self, cfg, seed):
        self.cfg, self.rng = cfg, random.Random(seed)
        self.log = []; self.winner = None; self.reason = None; self.over = False
        self.turn_no = 0; self.round = 0; self.cur = 0; self.bots = None
        self.stats = dict(cm_announce=0, cm_cancel=0, cm_retrigger=0, cm_started_by=[], stuck=0, turns=0, collisions=0,
                          reclaims=0, knockouts=0, plays=0, no_play_turns=0, cap_blocked=0)
        self.first_dead = []     # (card id) unplayable cards seen on turn-1 hands
        self.history = []        # per turn: leading player indices (lead-change tracking)
        self.lead_changes = 0; self.cm_cancelled_players = set(); self.cm_ever = set()
        self.cm_starts = {}
        self.card_plays = {}; self.pc = {}; self.interact = 0; self.cm_cancel_by = []; self.turn_plays = []

    # ------------------------------------------------------------------ small helpers
    def say(self, s):
        if self.cfg.log: self.log.append("R%d T%d: %s" % (self.round, self.turn_no, s))

    def alive(self): return [p for p in self.P if p.alive]
    def opps(self, i): return [p.i for p in self.P if p.alive and p.i != i]

    def cos(self, i): return [c for c in self.P[i].orbit if c]
    def all_cos(self): return [c for p in self.P if p.alive for c in p.orbit if c]


# ================================================================== stats
def has_aug(co, aid): return any(a.id == aid for a in co.augs)


def can_reduce(co, src):
    """INTERP: AE04 'opponents' effects cannot reduce Size or Stability' blocks any negative modifier whose source is not the CO's owner."""
    return not (has_aug(co, "AE04") and src is not None and src != co.owner)


def eff_size(st, co):
    s = co.card["size"]; n = len(co.augs); p = st.P[co.owner]
    if co.id in ("CO04", "CO17") and n >= 1: s += 1
    for a in co.augs:
        i = a.id
        if i == "AE02" or i == "AE03": s += 1
        elif i == "AE06" or i == "AE21": s += 2
        elif i == "AE08" and n >= 3: s += 2
        elif i == "AE13" and can_reduce(co, a.src): s -= 1
    if p.sid == "ST08" and n >= 2: s += 1
    for t in co.temps:
        if t["size"] and (t["size"] > 0 or can_reduce(co, t["src"])): s += t["size"]
    return max(0, s)   # INTERP G15: floor applied to the final total; G19: values above 5 are allowed


def total_size(st, i): return sum(eff_size(st, c) for c in st.P[i].orbit if c)


def eff_stab(st, co):
    s = co.card["stability"]; n = len(co.augs); p = st.P[co.owner]; pos = co.pos
    if co.id == "CO01": s += n
    elif co.id == "CO07" and pos == 1: s += 2
    elif co.id == "CO12" and n >= 1: s += 2
    elif co.id == "CO16" and pos == 3: s += 2
    elif co.id == "CO17" and n >= 1: s += 1
    for a in co.augs:
        i = a.id
        if i == "AE01": s += 2
        elif i == "AE03" or i == "AE21": s += 1
        elif i == "AE05": s += 2 if pos == 2 else 1
        elif i == "AE07" and n >= 2: s += 2
        elif i == "AE12" and can_reduce(co, a.src): s -= 1
        elif i == "AE22" and pos == 0 and can_reduce(co, a.src): s -= 2
    for o in p.orbit:
        if o is None or o is co: continue
        if o.id == "CO24" and (o.pos - pos) % 4 in (1, 3): s += 1
        elif o.id == "CO25" and o.pos == 0: s += 1
        elif o.id == "CO35" and o.augs: s += 1
    if p.sid == "ST04" and total_size(st, co.owner) >= 10: s += 1
    for t in co.temps:
        if t["stab"] and (t["stab"] > 0 or can_reduce(co, t["src"])): s += t["stab"]
    return max(0, s)


# ================================================================== core mutations
def draw(st, i, n=1):
    p = st.P[i]; got = 0
    for _ in range(n):
        if not st.deck:
            if not st.discard: break           # INTERP G35: empty deck AND discard -> draw skipped
            st.rng.shuffle(st.discard); st.deck, st.discard = st.discard, []   # reshuffle immediately
            st.say("deck reshuffled")
        p.hand.append(st.deck.pop()); got += 1
    return got


def dmg(st, src, tgt, n, kind="other"):
    t = st.P[tgt]
    if not t.alive or n <= 0 or st.over: return 0
    if kind == "AE" and n > 1 and any(c.id == "CO31" for c in st.cos(tgt)): n = max(1, n - 1)
    t.hp -= n; t.dmg_flag = True
    st.say("P%d (%s) takes %d (hp %d)" % (tgt, t.sid, n, t.hp))
    if t.hp <= 0: eliminate(st, tgt)
    return n


def eliminate(st, i):
    p = st.P[i]
    if not p.alive: return
    p.alive = False
    for c in p.orbit:
        if c:
            st.discard.append(c.card)
            for a in c.augs: st.discard.append(a.card)
    p.orbit = [None] * 4
    st.discard.extend(p.hand); p.hand = []
    # INTERP G31: Augmentations the eliminated player attached to other players' COs stay in place
    st.say("P%d (%s) ELIMINATED" % (i, p.sid))
    al = st.alive()
    if len(al) == 1:
        st.winner, st.reason, st.over = al[0].i, "star", True
    elif not al:
        st.over = True   # INTERP G33: nobody left (cannot happen with sequential resolution)
    if i == st.cur: st.turn_over = True    # INTERP G30: active player eliminated -> turn ends at once


def pick_opp(st, i, why="dmg"):
    ops = st.opps(i)
    if len(ops) == 1: return ops[0]
    return st.bots[i].pick_opp(st, i, ops, why)


def remove_co(st, co, dest, cause=None):
    i = co.owner; p = st.P[i]
    p.orbit[co.pos] = None
    for a in co.augs: st.discard.append(a.card)
    co.augs = []; co.temps = []
    if dest == "ooo": st.ooo.append(co.card)
    elif dest == "discard": st.discard.append(co.card)
    elif dest == "hand": p.hand.append(co.card)
    st.stats["knockouts"] += 1
    st.say("%s leaves P%d orbit -> %s" % (co.id, i, dest))
    co.owner = None
    leave_triggers(st, i, dest, cause)


def leave_triggers(st, i, dest, cause):
    p = st.P[i]
    if not p.alive or st.over: return
    if dest == "ooo" and p.sid == "ST03":
        draw(st, i, 1)       # may -> always yes
    if p.sid == "ST12" and p.st12 != st.turn_no:   # INTERP G27: 'once per turn' counts every player's turn (resets each turn); G17: any removal from orbit
        p.st12 = st.turn_no
        ops = st.opps(i)
        if ops: dmg(st, i, pick_opp(st, i, "dmg") if len(ops) > 1 else ops[0], 1)
    if p.sid == "ST06" and cause is not None and cause != i and p.st06 != st.turn_no and st.P[cause].alive:
        p.st06 = st.turn_no
        dmg(st, i, cause, 1)


def settle(st):
    """Knock out COs at effective Size 0 (discard) or Stability 0 (Out of Orbit), repeat; then monitor Critical Mass cancels."""
    for _ in range(12):
        ch = False
        for p in st.P:
            if not p.alive: continue
            for c in list(p.orbit):
                if c is None or st.over: continue
                if eff_size(st, c) == 0:       # INTERP G18: Size 0 beats Stability 0 (discard)
                    remove_co(st, c, "discard", st.actor); ch = True
                elif eff_stab(st, c) == 0:     # INTERP G16: any time effective Stability is 0 it is knocked out (also if a bonus ends)
                    remove_co(st, c, "ooo", st.actor); ch = True
        if not ch: break
    for p in st.P:
        if p.alive and p.cm and total_size(st, p.i) < p.thr:   # INTERP G8: continuous check; a dip inside one resolution cancels
            p.cm = False; st.stats["cm_cancel"] += 1; st.cm_cancelled_players.add(p.i); st.cm_cancel_by.append("opp" if st.actor not in (None, p.i) else "self")
            st.say("P%d Critical Mass CANCELLED" % p.i)


def coll_winner(st, inc, occ):
    a13 = inc.id == "CO13" and len(inc.augs) >= 2
    b13 = occ.id == "CO13" and len(occ.augs) >= 2
    if a13: return inc          # INTERP G14: both CO13 -> incoming wins; CO13 override beats stats
    if b13: return occ
    a, b = eff_stab(st, inc), eff_stab(st, occ)
    if a != b: return inc if a > b else occ
    a, b = eff_size(st, inc), eff_size(st, occ)
    if a != b: return inc if a > b else occ
    return inc


def win_triggers(st, co):
    """'When this CO wins a Collision' (CO30 and Augmentation AE10)."""
    p = co.owner
    if co.id == "CO30" and st.opps(p): dmg(st, p, pick_opp(st, p), 1)
    for a in list(co.augs):
        if a.id == "AE10" and st.opps(p): dmg(st, p, pick_opp(st, p), 1, "AE")


def enter(st, i, co, pos, cause=None):
    """Place CO object into orbit i at pos. Collision if occupied. Returns True if it stays."""
    p = st.P[i]; co.owner = i; co.pos = pos; p.entered += 1
    occ = p.orbit[pos]
    st.say("P%d: %s enters %s" % (i, co.id, PN[pos]))
    if occ is None:
        p.orbit[pos] = co
        on_enter(st, i, co); settle(st); return co.owner is not None
    st.stats["collisions"] += 1
    w = coll_winner(st, co, occ)
    if w is co:
        remove_co(st, occ, "ooo", cause)
        p.orbit[pos] = co; co.owner = i; co.pos = pos
        win_triggers(st, co)
        on_enter(st, i, co); settle(st); return co.owner is not None
    # incoming loses: trigger fires first, then it is knocked out (rules 5.4)
    co.owner = i
    on_enter(st, i, co, losing=True)
    st.ooo.append(co.card); co.owner = None; st.stats["knockouts"] += 1
    st.say("%s loses the collision, Out of Orbit" % co.id)
    win_triggers(st, occ)
    leave_triggers(st, i, "ooo", cause)
    settle(st); return False


def other_orbit_enter(st, i):
    """AE19: whenever any CO enters an opponent's orbit (opponent of the Augmentation's owner)."""
    for q in st.alive():
        if q.i == i: continue
        for c in q.orbit:
            if c:
                for a in c.augs:
                    if a.id == "AE19" and a.src == q.i: draw(st, q.i, 1)


def on_enter(st, i, co, losing=False):
    p = st.P[i]; b = st.bots[i]; cid = co.id
    other_orbit_enter(st, i)
    if cid == "CO06":
        opts = []
        for o in p.orbit:
            if o and o is not co:
                for e in range(4):
                    if p.orbit[e] is None: opts.append(((o, e), orbit_gain(st, i, o, e)))
        if opts:
            ch = b.pick(st, i, "move", opts, may=True)
            if ch: move_in_orbit(st, i, ch[0], ch[1])
    elif cid == "CO08":
        if p.hand:
            c8 = b.discard_pick(st, i, p.hand); p.hand.remove(c8); st.discard.append(c8)
    elif cid == "CO11":
        for q in st.opps(i): draw(st, q, 1)
    elif cid == "CO14":
        opts = []
        hosts = [c for c in p.orbit if c and c is not co] if losing else [c for c in p.orbit if c]
        for card in p.hand:
            if card["subtype"] == "Augmentation":
                for h in aug_hosts(st, i, card):
                    if h in hosts: opts.append(((card, h), aug_value(st, i, card, h)))
        if opts:
            ch = b.pick(st, i, "attach", opts, may=True)
            if ch:
                p.hand.remove(ch[0]); attach(st, i, ch[0], ch[1], paid=True)
    elif cid == "CO15": draw(st, i, 1)
    elif cid == "CO18":
        opts = [(q, rotation_harm(st, q)) for q in st.opps(i)]
        ch = b.pick(st, i, "rot_opp", opts, may=True) if opts else None
        if ch is not None: rotate_orbit(st, ch, actor=i)
    elif cid == "CO20":
        opts = [(c, card_value(c)) for c in st.discard if c["subtype"] == "Augmentation"]
        if opts:
            ch = b.pick(st, i, "take", dedupe(opts), may=True)
            if ch: st.discard.remove(ch); p.hand.append(ch)
    elif cid == "CO22": dmg(st, i, i, 1)
    elif cid == "CO26":
        opts = []
        for c in st.all_cos():
            if c is co and losing: continue
            for a in c.augs:
                if c is not co: opts.append(((a, c), aug_move_gain(st, i, a, co)))
        if opts and not losing:
            ch = b.pick(st, i, "augmove", opts, may=True)
            if ch:
                a = ch[0]; a.host.augs.remove(a); a.host = co; co.augs.append(a)
    elif cid == "CO33":
        top = [st.deck.pop() for _ in range(min(2, len(st.deck)))]
        if top:
            ch = b.pick(st, i, "keep", [(c, card_value(c)) for c in top], may=False)
            p.hand.append(ch); top.remove(ch)
            for c in top: st.deck.insert(0, c)
    elif cid == "CO34":
        opts = [(True, rotation_gain(st, i))]
        ch = b.pick(st, i, "rot_self", opts, may=True)
        if ch: rotate_orbit(st, i, actor=None)
    settle(st)


_last_discard = None


def dedupe(opts):
    seen, out = set(), []
    for c, v in opts:
        if c["id"] in seen: continue
        seen.add(c["id"]); out.append((c, v))
    return out


def discard_from_hand(st, i, n, exclude=None):
    p = st.P[i]
    for _ in range(n):
        pool = [c for c in p.hand if c is not exclude]
        if not pool: return
        c = st.bots[i].discard_pick(st, i, pool)
        p.hand.remove(c); st.discard.append(c)


def move_in_orbit(st, i, co, pos, cause=None):
    """Move a CO inside its orbit (not rotation, not entering). INTERP G11: no enters-orbit trigger, no cap use; the mover is the incoming CO."""
    p = st.P[co.owner]; old = co.pos; occ = p.orbit[pos]
    if occ is None:
        p.orbit[old] = None; p.orbit[pos] = co; co.pos = pos
    else:
        st.stats["collisions"] += 1
        co.pos = pos; w = coll_winner(st, co, occ); co.pos = old
        if w is co:
            p.orbit[old] = None
            remove_co(st, occ, "ooo", cause)
            p.orbit[pos] = co; co.pos = pos
            win_triggers(st, co)
        else:
            remove_co(st, co, "ooo", cause)
            win_triggers(st, occ)
    settle(st)


def attach(st, i, card, host, paid=False):
    host.augs.append(Aug(card, host, i))
    st.say("P%d attaches %s to %s (P%d)" % (i, card["id"], host.id, host.owner))
    settle(st)


def aug_hosts(st, i, card):
    """Legal hosts for an Augmentation. INTERP G21: the card text names its legal hosts; otherwise own COs only."""
    cid = card["id"]; mine = st.cos(i)
    opp = [c for q in st.opps(i) for c in st.cos(q)]
    anyc = mine + opp
    if cid in ("AE12", "AE13"): return [c for c in anyc if can_reduce(c, i)]
    if cid == "AE15": return anyc
    if cid in ("AE14", "AE11"): return opp
    if cid == "AE22": return [c for c in opp if can_reduce(c, i)]
    if cid == "AE03": return [c for c in mine if not c.augs]
    if cid == "AE06": return [c for c in mine if eff_size(st, c) <= 3]
    if cid == "AE09": return [c for c in mine if eff_stab(st, c) <= 2]
    return mine


def rotate_orbit(st, q, actor, dry=False):
    """Rotate orbit q one step clockwise. Simultaneous; collisions only where a stopped CO or a reverse CO is in the way.
    INTERP G12: contenders at one position are ordered stationary (incumbent), normal-direction mover, reverse mover; each later one is the 'incoming'.
    Swapping neighbours do not collide. INTERP G13: all moves are simultaneous, collisions are resolved after the whole rotation."""
    p = st.P[q]; plan = {}
    for c in p.orbit:
        if c is None: continue
        stat = c.id == "CO27" or has_aug(c, "AE16") or has_aug(c, "AE14")
        rev = c.id == "CO21" or has_aug(c, "AE15")
        d = 0 if stat else (-1 if rev else 1)
        plan[c] = ((c.pos + d) % 4, 0 if stat else (2 if rev else 1))
    groups = {}
    for c, (dst, order) in plan.items(): groups.setdefault(dst, []).append((order, c))
    losers, winners = [], {}
    saved = {c: c.pos for c in plan}
    for dst, g in groups.items():
        g.sort(key=lambda t: t[0])
        cur = g[0][1]
        for _, c in g[1:]:
            old = (cur.pos, c.pos); cur.pos = c.pos = dst
            w = coll_winner(st, c, cur)
            cur.pos, c.pos = saved[cur], saved[c]
            if w is c: losers.append(cur); cur = c
            else: losers.append(c)
        winners[dst] = cur
    if dry: return losers
    for c in plan: c.pos = saved[c]
    cause = actor if actor is not None and actor != q else None
    if losers: st.stats['rot_collisions'] = st.stats.get('rot_collisions', 0) + len(losers)
    newo = [None] * 4
    for dst, c in winners.items(): newo[dst] = c
    for dst, c in winners.items(): c.pos = dst
    p.orbit = newo
    st.say("P%d orbit rotates%s" % (q, " (collision: %s out)" % ",".join(c.id for c in losers) if losers else ""))
    for c in losers:
        for a in c.augs: st.discard.append(a.card)
        c.augs = []; c.temps = []
        st.ooo.append(c.card); c.owner = None; st.stats["knockouts"] += 1; st.stats["collisions"] += 1
        leave_triggers(st, q, "ooo", cause)
    for dst, c in winners.items():
        if len(groups[dst]) > 1: win_triggers(st, c)
    settle(st)
    return losers


# ================================================================== valuation helpers used by the engine for bots' option scores
def eval_orbit(st, i):
    return sum(eff_size(st, c) + 0.5 * min(eff_stab(st, c), 5) for c in st.P[i].orbit if c)


def orbit_gain(st, i, co, newpos):
    before = eval_orbit(st, i); old = co.pos; p = st.P[i]
    p.orbit[old] = None; p.orbit[newpos] = co; co.pos = newpos
    after = eval_orbit(st, i)
    p.orbit[newpos] = None; p.orbit[old] = co; co.pos = old
    return after - before


def rotation_gain(st, i):
    if rotation_harm(st, i) > 0: return -1
    p = st.P[i]; before = eval_orbit(st, i)
    old = list(p.orbit); olds = {c: c.pos for c in old if c}
    for c in old:
        if c: c.pos = (c.pos + 1) % 4
    p.orbit = [None] * 4
    for c in old:
        if c: p.orbit[c.pos] = c
    after = eval_orbit(st, i)
    for c, ps in olds.items(): c.pos = ps
    p.orbit = old
    return after - before


def rotation_harm(st, q):
    return sum(eff_size(st, c) for c in rotate_orbit(st, q, None, dry=True))


def card_value(c):
    if c["type"] == "CO": return c["size"] * 1.0 + (0.3 if c["stability"] >= 2 else 0)
    if c["damage_max"] > 0: return 2.5 + c["damage_max"]
    return 1.5


def aug_value(st, i, card, host):
    return 1.0


def aug_move_gain(st, i, a, to):
    return (1.0 if a.id not in ("AE12", "AE13", "AE22", "AE14", "AE15", "AE11") else -1.0) * (1 if a.src == i else 0.5)


# ================================================================== game flow
def setup(st, bots):
    cfg = st.cfg; n = cfg.n
    ids = list(cfg.deck_ids) if cfg.deck_ids else [c["id"] for c in DATA["cards"]]
    st.deck = [dict(CARDS[x]) if isinstance(x, str) else x for x in ids]
    st.rng.shuffle(st.deck); st.discard = []; st.ooo = []
    st.bots = bots
    sids = list(cfg.stars) if cfg.stars else None
    if sids is None:
        pool = list(STARS); st.rng.shuffle(pool)       # INTERP G3: random deal of 2, keep 1; bots pick by hp preference noise-free = first dealt
        sids = []
        for k in range(n): sids.append(pool[2 * k + st.rng.randrange(2)])
    st.P = [Player(i, STARS[sids[i]]) for i in range(n)]
    for p in st.P: p.hand = [st.deck.pop() for _ in range(5)]   # INTERP G3: hands dealt after Stars chosen
    st.cur = cfg.first if cfg.first is not None else st.rng.randrange(n)  # INTERP G2: random first player, clockwise seats
    st.actor = None; st.turn_over = False


def start_turn(st, i):
    p = st.P[i]; b = st.bots[i]
    p.entered = 0; p.used = set(); p.plays = 2; p.turns += 1
    for c in st.all_cos():
        c.temps = [t for t in c.temps if t["until"] != ("start", i)]
    # INTERP G5: start-of-turn triggers first, then the draw
    for c in list(st.all_cos()):
        for a in list(c.augs):
            if a.src != i or not p.alive or st.over: continue
            if a.id == "AE09" and st.opps(i): dmg(st, i, pick_opp(st, i), 1, "AE")
            elif a.id == "AE11" and st.P[c.owner].alive and c.owner != i: dmg(st, i, c.owner, 1, "AE")
    if st.over or not p.alive: return
    draw(st, i, st.cfg.first_draw if st.turn_no == 1 else 2)   # INTERP G4: first player also draws on turn 1, no compensation for later seats
    st.say("P%d (%s) starts with %d cards" % (i, p.sid, len(p.hand)))
    rotate_orbit(st, i, None)


def end_turn(st, i):
    p = st.P[i]
    for c in list(st.cos(i)):
        if st.over: return
        if c.id == "CO23" and c.augs and st.opps(i): dmg(st, i, pick_opp(st, i), 1)
        for a in c.augs:
            if a.id == "AE20" and a.src == i and c.pos == 0: draw(st, i, 1)
    for c in st.all_cos():
        c.temps = [t for t in c.temps if t["until"] != "eot"]
    settle(st)
    if st.over or not p.alive: return
    # INTERP G6/G7: order = triggers, Critical Mass (own total only, own end of turn), hand limit
    ts = total_size(st, i)
    if p.cm:
        if ts >= p.thr:
            st.winner, st.reason, st.over = i, "cm", True; st.win_turns = p.turns
            st.say("P%d wins by Critical Mass (%d)" % (i, ts)); return
        p.cm = False
    if ts >= p.thr:
        p.cm = True; st.stats["cm_announce"] += 1
        if i in st.cm_cancelled_players: st.stats["cm_retrigger"] += 1
        st.cm_ever.add(i); st.cm_starts.setdefault(i, p.turns)
        st.say("P%d announces Critical Mass (%d)" % (i, ts))
    while len(p.hand) > 7:
        c = st.bots[i].discard_pick(st, i, p.hand)   # INTERP G34: owner chooses
        p.hand.remove(c); st.discard.append(c)
    p.dmg_flag = False        # INTERP G28: 'since your last turn' flag is cleared at the end of your own turn; false on the first turn


def take_turn(st):
    i = st.cur; p = st.P[i]; st.turn_no += 1; st.turn_over = False; st.actor = None
    st.stats["turns"] += 1
    start_turn(st, i)
    if not st.over and p.alive:
        play_phase(st, i)
    if not st.over and p.alive:
        end_turn(st, i)
    track_lead(st)
    if st.over: return
    n = len(st.P)
    nxt = (i + 1) % n
    while not st.P[nxt].alive: nxt = (nxt + 1) % n
    if nxt <= i: st.round += 1
    st.cur = nxt


def track_lead(st):
    """Leader = highest (own total Size + 3*(HP)/... ) proxy: progress score for the strongest threat; lead change when the leader changes."""
    if len(st.alive()) < 2: return
    # progress = max(own CM progress, damage dealt to others) ; use HP lead + size lead
    def prog(p):
        others = [q for q in st.P if q.alive and q is not p]
        hp_lead = p.hp / p.maxhp - sum(q.hp / q.maxhp for q in others) / len(others)
        sz_lead = (total_size(st, p.i) - sum(total_size(st, q.i) for q in others) / len(others)) / 15.0
        return hp_lead + sz_lead
    vals = sorted(((prog(p), p.i) for p in st.alive()), reverse=True)
    if vals[0][0] - vals[1][0] < 0.05: ld = None
    else: ld = vals[0][1]
    st.history.append(ld)
    prev = [x for x in st.history[:-1] if x is not None]
    if ld is not None and prev and prev[-1] != ld: st.lead_changes += 1


def play_phase(st, i):
    p = st.P[i]; b = st.bots[i]
    if st.turn_no == 1:
        for c in p.hand:
            if not [a for a in gen_one(st, i, c)]: st.first_dead.append(c["id"])
    n = 0
    while not st.over and p.alive and not st.turn_over:
        acts = gen_actions(st, i)
        if not acts:
            if n == 0: st.stats["no_play_turns"] += 1
            break
        a = b.choose_action(st, i, acts)
        if a is None: break
        n += 1
        execute(st, i, a)
        settle(st)
    st.turn_plays.append((st.turn_no, 2 - p.plays))
    if n == 0: st.stats.setdefault("zero_action_turns", 0); st.stats["zero_action_turns"] += 1


def count_cards(st):
    n = len(st.deck) + len(st.discard) + len(st.ooo)
    for p in st.P:
        n += len(p.hand)
        for c in p.orbit:
            if c: n += 1 + len(c.augs)
    return n


def play(cfg, bots, seed, check=False):
    st = State(cfg, seed)
    setup(st, bots)
    total = count_cards(st)
    while not st.over and st.round < cfg.round_cap:
        take_turn(st)
        if check: assert count_cards(st) == total, ("card leak", count_cards(st), total, st.log[-6:])
    capped = not st.over
    return dict(st=st, winner=st.winner, reason=st.reason or ("cap" if capped else None), rounds=st.round + 1, turns=st.turn_no, capped=capped)


# ================================================================== action generation
def fxd(**k):
    d = dict(dmg=0, tgt=None, self_dmg=0, size=0, osize=0, knock=0, lose=0, draw=0, cost=0, heal=0, stab=0, tempo=0, kill=False, coll=None, fut=0, cm=0)
    d.update(k); return d


def act(kind, card, params, fx, play=True, name=None):
    return dict(kind=kind, card=card, params=params, fx=fx, play=play, name=name or (card["id"] if card else "?"))


def gen_actions(st, i):
    p = st.P[i]; out = []
    seen = set()
    if p.plays > 0:
        for c in p.hand:
            out.extend(gen_one(st, i, c))
    out.extend(gen_free(st, i))
    return out


def co_places(st, i, card):
    p = st.P[i]
    return [e for e in range(4) if e in RESTRICT.get(card["id"], range(4))]


def place_fx(st, i, card, pos, via_reclaim=False):
    p = st.P[i]; tmp = CO(card); tmp.owner = i; tmp.pos = pos
    occ = p.orbit[pos]; sz = eff_size(st, tmp)
    if occ is None:
        return fxd(size=sz, stab=eff_stab(st, tmp), coll="empty")
    w = coll_winner(st, tmp, occ)
    if w is tmp: return fxd(size=sz - eff_size(st, occ), lose=eff_size(st, occ), coll="win", stab=eff_stab(st, tmp), knock=0)
    return fxd(size=0, lose=sz, coll="lose", stab=0)


def gen_one(st, i, card):
    p = st.P[i]; out = []
    cid = card["id"]
    if card["type"] == "CO":
        if p.entered >= 1:
            return out        # INTERP G10: cap = 1 CO entering per turn, any source; loser of a collision also uses it
        for pos in co_places(st, i, card):
            out.append(act("co", card, dict(pos=pos), place_fx(st, i, card, pos)))
        return out
    sub = card["subtype"]; ops = st.opps(i); mine = st.cos(i)
    if sub == "Augmentation":
        if cid in ("AE21", "AE11") and len(p.hand) < 2: return out    # INTERP G26: a hard cost that cannot be paid makes the card illegal
        for h in aug_hosts(st, i, card):
            out.append(act("ae", card, dict(host=h), aug_fx(st, i, card, h)))
        return out
    # ---- Direct Effects
    def dm(k, **kw):   # damage action vs each opponent
        for q in ops:
            f = fxd(tgt=q, dmg=k, kill=(k >= st.P[q].hp), **kw)
            out.append(act("ae", card, dict(tgt=q), f))
    if cid == "AE23": dm(1)
    elif cid == "AE24":
        if len(mine) >= 2: dm(2)
    elif cid == "AE25":
        if len(p.hand) >= 1: dm(3, self_dmg=1)
    elif cid == "AE26":
        out.append(act("ae", card, {}, fxd(dmg=len(ops), tgt=min(ops, key=lambda q: st.P[q].hp), kill=any(st.P[q].hp <= 1 for q in ops))))
    elif cid == "AE27":
        k = min(3, sum(1 for c in mine if eff_size(st, c) >= 4))
        if k: dm(k)
    elif cid == "AE28":
        for c in mine:
            for q in ops:
                out.append(act("ae", card, dict(tgt=q, co=c), fxd(tgt=q, dmg=3, kill=3 >= st.P[q].hp, lose=eff_size(st, c))))
    elif cid == "AE29":
        for q in ops:
            for c in st.cos(q):
                if eff_size(st, c) >= 4 and choosable(st, i, c):
                    out.append(act("ae", card, dict(tgt=q, co=c), fxd(tgt=q, dmg=1, kill=1 >= st.P[q].hp, knock=int(eff_stab(st, c) <= 1))))
    elif cid == "AE30":
        for q in ops: dm_ = 2 if len(st.cos(q)) > len(mine) else 1; out.append(act("ae", card, dict(tgt=q), fxd(tgt=q, dmg=dm_, kill=dm_ >= st.P[q].hp)))
    elif cid == "AE31":
        if p.dmg_flag: dm(2)
    elif cid == "AE32":
        for q in ops:
            if total_size(st, q) >= 12: out.append(act("ae", card, dict(tgt=q), fxd(tgt=q, dmg=2, kill=2 >= st.P[q].hp)))
    elif cid == "AE33": dm(1, draw=1)
    elif cid == "AE34":
        k = min(3, len(st.ooo))
        if k: dm(k)
    elif cid == "AE35":
        for q in ops: d_ = 2 if p.hp < st.P[q].hp else 1; out.append(act("ae", card, dict(tgt=q), fxd(tgt=q, dmg=d_, kill=d_ >= st.P[q].hp)))
    elif cid == "AE36":
        k = min(3, sum(len(c.augs) for c in mine))
        if k: dm(k)
    elif cid == "AE37": dm(2)
    elif cid == "AE38":
        for q in ops:
            for c in st.cos(q):
                if not choosable(st, i, c): continue
                for pos in range(4):
                    if pos == c.pos: continue
                    out.append(act("ae", card, dict(tgt=q, co=c, pos=pos), move_opp_fx(st, i, q, c, pos)))
    elif cid == "AE39":
        for q in ops:
            for c in st.cos(q):
                if eff_stab(st, c) == 1 and choosable(st, i, c):
                    out.append(act("ae", card, dict(tgt=q, co=c), fxd(tgt=q, knock=1, osize=-eff_size(st, c))))
    elif cid == "AE40":
        if len(p.hand) >= 3:
            for c in st.all_cos():
                if c.owner == i or choosable(st, i, c):
                    out.append(act("ae", card, dict(co=c), fxd(cost=2, knock=1 if c.owner != i else 0, lose=eff_size(st, c) if c.owner == i else 0, osize=-eff_size(st, c) if c.owner != i else 0, tgt=c.owner)))
    elif cid == "AE41":
        mine_n = sum(1 for c in mine if c.pos == 0); opp_k = sum(1 for q in ops for c in st.cos(q) if c.pos == 0 and eff_stab(st, c) <= 1)
        out.append(act("ae", card, {}, fxd(knock=opp_k, lose=sum(eff_size(st, c) for c in mine if c.pos == 0 and eff_stab(st, c) <= 1))))
    elif cid == "AE42":
        for c in st.all_cos():
            for a in c.augs: out.append(act("ae", card, dict(aug=a), aug_removal_fx(st, i, a)))
    elif cid == "AE43":
        for c in st.all_cos():
            if len(c.augs) >= 2 and choosable(st, i, c): out.append(act("ae", card, dict(co=c), aug_removal_fx(st, i, c.augs[0], all_=True)))
    elif cid in ("AE44", "AE45", "AE46"):
        if cid == "AE46" and len(p.hand) < 2: return out
        if p.entered >= 1 and cid != "AE46": return out    # INTERP G10: reclaim counts against the cap
        pool = [c for c in st.ooo if cid != "AE45" or c["size"] <= 3]
        seenid = set()
        for c in pool:
            if c["id"] in seenid: continue
            seenid.add(c["id"])
            for pos in co_places(st, i, c):
                f = place_fx(st, i, c, pos); f["draw"] = 1 if cid == "AE45" else 0; f["cost"] = 1 if cid == "AE46" else 0
                out.append(act("ae", card, dict(co=c, pos=pos), f))
    elif cid == "AE47": out.append(act("ae", card, {}, fxd(draw=2)))
    elif cid == "AE48": out.append(act("ae", card, {}, fxd(draw=1)))
    elif cid == "AE49":
        seenid = set()
        for c in st.discard:
            if c["type"] == "CO" and c["id"] not in seenid:
                seenid.add(c["id"]); out.append(act("ae", card, dict(co=c), fxd(draw=1)))
    elif cid == "AE50":
        for c in [c for q in ops for c in st.cos(q)]:
            for a in c.augs:
                for m in mine: out.append(act("ae", card, dict(aug=a, host=m), aug_steal_fx(st, i, a, m)))
    elif cid == "AE51":
        if mine: out.append(act("ae", card, {}, fxd(stab=len(mine))))
    elif cid == "AE52":
        for q in ops:
            if st.P[q].cm:
                cs = [c for c in st.cos(q) if choosable(st, i, c)]
                if cs:
                    m = max(eff_size(st, c) for c in cs)
                    out.append(act("ae", card, dict(tgt=q), fxd(tgt=q, knock=1, osize=-m, cm=1)))
    elif cid == "AE53":
        for q in ops:
            for c in st.cos(q):
                if eff_size(st, c) >= 4 and choosable(st, i, c) and can_reduce(c, i):
                    out.append(act("ae", card, dict(tgt=q, co=c), fxd(tgt=q, knock=int(eff_stab(st, c) <= 2), osize=-eff_size(st, c) * int(eff_stab(st, c) <= 2))))
    elif cid == "AE54":
        if p.entered == 0:
            for c in p.hand:
                if c["type"] == "CO" and c is not card:
                    for pos in co_places(st, i, c):
                        f = place_fx(st, i, c, pos); out.append(act("ae", card, dict(co=c, pos=pos), f))
    elif cid == "AE55":
        for c in mine: out.append(act("ae", card, dict(co=c), fxd(lose=eff_size(st, c), cost=0, tempo=-1)))
    elif cid == "AE56":
        if p.hp < p.maxhp: out.append(act("ae", card, {}, fxd(heal=min(2, p.maxhp - p.hp))))
    elif cid == "AE57":
        for c in mine:
            for pos in range(4):
                if pos != c.pos:
                    out.append(act("ae", card, dict(co=c, pos=pos), self_move_fx(st, i, c, pos)))
    elif cid == "AE58":
        for q in ops: out.append(act("ae", card, dict(tgt=q), fxd(tgt=q, draw=1, knock=0, osize=-rotation_harm(st, q))))
    elif cid == "AE59":
        seenid = set()
        for c in st.ooo:
            if c["id"] not in seenid: seenid.add(c["id"]); out.append(act("ae", card, dict(co=c), fxd(draw=1)))
    elif cid == "AE60":
        h = sum(rotation_harm(st, q) for q in ops) - rotation_harm(st, i)
        out.append(act("ae", card, {}, fxd(osize=-h)))
    return out


def choosable(st, actor, co):
    if co.owner == actor: return True
    if has_aug(co, "AE17"): return False
    if co.id != "CO36" and any(o.id == "CO36" for o in st.cos(co.owner)): return False
    return True


def aug_fx(st, i, card, host):
    cid = card["id"]; own = host.owner == i
    sb, zb = eff_size(st, host), eff_stab(st, host)
    host.augs.append(Aug(card, host, i))
    sa, za = eff_size(st, host), eff_stab(st, host)
    host.augs.pop()
    f = fxd(size=(sa - sb) if own else 0, stab=(za - zb) if own else 0, cost=1 if cid in ("AE21", "AE11") else 0)
    if not own:
        f["osize"] = -(sb - sa) if sa < sb else 0
        f["tgt"] = host.owner
        if sa == 0 or za == 0: f["knock"] = 1; f["osize"] = -sb
    if cid in ("AE09",): f["fut"] = 2.0; f["tgt"] = None
    if cid == "AE11": f["fut"] = 2.0
    if cid == "AE10": f["fut"] = 0.5
    if cid in ("AE19", "AE20"): f["fut"] = 0.8
    if cid in ("AE12", "AE13", "AE22", "AE14", "AE15"): f["fut"] = 0.3 if not f["knock"] else 0
    if cid in ("AE04", "AE17", "AE16"): f["stab"] += 0.5
    if cid == "AE18": f["fut"] = 0.5
    return f


def aug_removal_fx(st, i, a, all_=False):
    host = a.host; own = host.owner == i
    n = len(host.augs) if all_ else 1
    saved = list(host.augs); sb, zb = eff_size(st, host), eff_stab(st, host)
    host.augs = [x for x in host.augs if (x is not a and not all_)]
    sa, za = eff_size(st, host), eff_stab(st, host)
    host.augs = saved
    d = (sa - sb)
    knock = int(za == 0 or sa == 0)
    if own: return fxd(size=d, stab=za - zb, lose=-d if d < 0 else 0)
    return fxd(osize=d if d < 0 else 0, knock=knock, tgt=host.owner, stab=0)


def aug_steal_fx(st, i, a, m):
    pos = a.id not in ("AE12", "AE13", "AE22", "AE14", "AE15", "AE11")
    return fxd(size=1 if pos else -1, fut=1 if pos else -2, tgt=a.host.owner)


def move_opp_fx(st, i, q, c, pos):
    p = st.P[q]; occ = p.orbit[pos]
    if occ is None: return fxd(tgt=q, tempo=0)
    old = c.pos; c.pos = pos
    w = coll_winner(st, c, occ); c.pos = old
    if w is c: return fxd(tgt=q, knock=1, osize=-eff_size(st, occ))
    return fxd(tgt=q, knock=1, osize=-eff_size(st, c))


def self_move_fx(st, i, c, pos):
    p = st.P[i]; occ = p.orbit[pos]
    if occ is None: return fxd(stab=orbit_gain(st, i, c, pos))
    old = c.pos; c.pos = pos
    w = coll_winner(st, c, occ); c.pos = old
    if w is c: return fxd(lose=eff_size(st, occ), coll="win")
    return fxd(lose=eff_size(st, c), coll="lose")


def gen_free(st, i):
    p = st.P[i]; out = []; sid = p.sid; ops = st.opps(i)
    if sid == "ST01" and "ST01" not in p.used and len(p.hand) >= 1 and st.deck + st.discard:
        out.append(act("free", None, dict(src="ST01"), fxd(draw=0, cost=0), play=False, name="ST01"))
    if sid == "ST02" and "ST02" not in p.used:
        for c in st.cos(i):
            for a in c.augs:
                for d in st.cos(i):
                    if d is not c: out.append(act("free", None, dict(src="ST02", aug=a, host=d), fxd(), play=False, name="ST02"))
    if sid == "ST05" and "ST05" not in p.used and len(st.cos(i)) >= 3 and ops:
        for q in ops: out.append(act("free", None, dict(src="ST05", tgt=q), fxd(dmg=1, tgt=q, kill=st.P[q].hp <= 1), play=False, name="ST05"))
    if sid == "ST07" and "ST07" not in p.used and p.dmg_flag and ops:
        for q in ops: out.append(act("free", None, dict(src="ST07", tgt=q), fxd(dmg=1, tgt=q, kill=st.P[q].hp <= 1), play=False, name="ST07"))
    if sid == "ST09" and "ST09" not in p.used and st.ooo:
        seenid = set()
        for c in st.ooo:
            if c["id"] in seenid: continue
            seenid.add(c["id"])
            for pos in co_places(st, i, c):
                out.append(act("free", None, dict(src="ST09", co=c, pos=pos), place_fx(st, i, c, pos), play=False, name="ST09"))
    for c in st.cos(i):
        for a in c.augs:
            if a.id == "AE18" and a.src == i and ("AE18", id(a)) not in p.used:
                for e in range(4):
                    if p.orbit[e] is None: out.append(act("free", None, dict(src="AE18", aug=a, co=c, pos=e), fxd(stab=orbit_gain(st, i, c, e)), play=False, name="AE18"))
    return out


# ================================================================== execution
def execute(st, i, a):
    p = st.P[i]; card = a["card"]; par = a["params"]; st.actor = i
    if a["kind"] == "free":
        src = par["src"]
        if src == "AE18": p.used.add(("AE18", id(par["aug"])))
        else: p.used.add(src)
        st.say("P%d uses %s" % (i, src))
        if par.get("tgt") is not None: st.interact += 1
        if src == "ST01":
            c = st.bots[i].discard_pick(st, i, p.hand); p.hand.remove(c); st.discard.append(c); draw(st, i, 1)
        elif src == "ST02":
            aug = par["aug"]; aug.host.augs.remove(aug); aug.host = par["host"]; par["host"].augs.append(aug)
        elif src in ("ST05", "ST07"): dmg(st, i, par["tgt"], 1)
        elif src == "ST09":
            reclaim(st, i, par["co"], par["pos"], via="ST09")
        elif src == "AE18":
            move_in_orbit(st, i, par["co"], par["pos"])
        st.actor = None; return
    st.stats["plays"] += 1; p.plays -= 1
    st.pc.setdefault(i, set()).add(card["id"])
    fxt = a["fx"].get("tgt")
    if (fxt is not None and fxt != i) or card["id"] in ("AE26", "AE41", "AE60"): st.interact += 1
    st.card_plays[card["id"]] = st.card_plays.get(card["id"], 0) + 1
    p.hand.remove(card)
    cid = card["id"]
    st.say("P%d plays %s %s" % (i, cid, {k: (v["id"] if isinstance(v, dict) else v.id if hasattr(v, "id") else v) for k, v in par.items() if k != "aug"}))
    if card["type"] == "CO":
        enter(st, i, CO(card), par["pos"]); st.actor = None; return
    if card["subtype"] == "Augmentation":
        if cid in ("AE21", "AE11"): discard_from_hand(st, i, 1)
        if cid == "AE18": pass
        attach(st, i, card, par["host"])
        st.actor = None; return
    # Direct Effect
    b = st.bots[i]; dx = extra_dmg(st, cid)
    def D(n, q): dmg(st, i, q, n + dx if n > 0 else n, "AE")
    if cid == "AE23": D(1, par["tgt"])
    elif cid == "AE24": D(2, par["tgt"])
    elif cid == "AE25": dmg(st, i, i, 1, "AE"); D(3, par["tgt"]) if not st.over and p.alive else None
    elif cid == "AE26":
        for q in list(st.opps(i)):
            if not st.over: D(1, q)
    elif cid == "AE27": D(min(3, sum(1 for c in st.cos(i) if eff_size(st, c) >= 4)), par["tgt"])
    elif cid == "AE28":
        c = par["co"]; remove_co(st, c, "ooo", None); D(3, par["tgt"])
    elif cid == "AE29":
        c = par["co"]; c.temps.append(dict(stab=-1, size=0, src=i, until="eot")); D(1, par["tgt"]);
    elif cid == "AE30": q = par["tgt"]; D(2 if len(st.cos(q)) > len(st.cos(i)) else 1, q)
    elif cid == "AE31": D(2, par["tgt"])
    elif cid == "AE32": D(2, par["tgt"])
    elif cid == "AE33": D(1, par["tgt"]); draw(st, i, 1)
    elif cid == "AE34": D(min(3, len(st.ooo)), par["tgt"])
    elif cid == "AE35": q = par["tgt"]; D(2 if p.hp < st.P[q].hp else 1, q)
    elif cid == "AE36": D(min(3, sum(len(c.augs) for c in st.cos(i))), par["tgt"])
    elif cid == "AE37": D(2, par["tgt"]); draw(st, par["tgt"], 2) if st.P[par["tgt"]].alive else None
    elif cid == "AE38": move_in_orbit(st, par["tgt"], par["co"], par["pos"], cause=i)
    elif cid == "AE39": remove_co(st, par["co"], "ooo", i)
    elif cid == "AE40":
        discard_from_hand(st, i, 2); remove_co(st, par["co"], "discard", i)
    elif cid == "AE41":
        for c in st.all_cos():
            if c.pos == 0: c.temps.append(dict(stab=-1, size=0, src=i, until="eot"))
    elif cid == "AE42":
        a_ = par["aug"]; a_.host.augs.remove(a_); st.discard.append(a_.card)
    elif cid == "AE43":
        c = par["co"]
        for a_ in c.augs: st.discard.append(a_.card)
        c.augs = []
    elif cid in ("AE44", "AE45", "AE46"):
        if cid == "AE46": discard_from_hand(st, i, 1)
        reclaim(st, i, par["co"], par["pos"], via=cid)
        if cid == "AE45": draw(st, i, 1)
    elif cid == "AE47": draw(st, i, 2)
    elif cid == "AE48":
        top = [st.deck.pop() for _ in range(min(3, len(st.deck)))]
        if top:
            ch = b.pick(st, i, "keep", [(c, card_value(c)) for c in top], may=False)
            p.hand.append(ch); top.remove(ch)
            for c in top: st.deck.insert(0, c)
    elif cid == "AE49": st.discard.remove(par["co"]); p.hand.append(par["co"])
    elif cid == "AE50":
        a_ = par["aug"]; a_.host.augs.remove(a_); a_.host = par["host"]; par["host"].augs.append(a_)  # INTERP G22: attach restrictions not re-checked on move
    elif cid == "AE51":
        for c in st.cos(i): c.temps.append(dict(stab=1, size=0, src=i, until=("start", i)))
    elif cid == "AE52":
        q = par["tgt"]; cs = [c for c in st.cos(q) if choosable(st, i, c)]   # INTERP: protected COs (CO36/AE17) are skipped
        if cs:
            m = max(eff_size(st, c) for c in cs)
            top = [c for c in cs if eff_size(st, c) == m]
            ch = top[0] if len(top) == 1 else b.pick(st, i, "knock", [(c, -eff_stab(st, c)) for c in top], may=False)
            remove_co(st, ch, "ooo", i)
    elif cid == "AE53": par["co"].temps.append(dict(stab=-2, size=0, src=i, until="eot"))
    elif cid == "AE54":
        c = par["co"]; p.hand.remove(c)
        ok = enter(st, i, CO(c), par["pos"])
        opts = []
        for ag in p.hand:
            if ag["subtype"] == "Augmentation":
                for h in aug_hosts(st, i, ag): opts.append(((ag, h), aug_value(st, i, ag, h) + aug_fx(st, i, ag, h)["size"] + aug_fx(st, i, ag, h)["stab"] * 0.3))
        if opts and not st.over:
            ch = b.pick(st, i, "attach", opts, may=True)
            if ch: p.hand.remove(ch[0]); attach(st, i, ch[0], ch[1], paid=True)
    elif cid == "AE55": remove_co(st, par["co"], "hand", None)
    elif cid == "AE56": p.hp = min(p.maxhp, p.hp + 2)     # INTERP G36: capped at starting HP (card text)
    elif cid == "AE57": move_in_orbit(st, i, par["co"], par["pos"])
    elif cid == "AE58": rotate_orbit(st, par["tgt"], actor=i); draw(st, i, 1)
    elif cid == "AE59": st.ooo.remove(par["co"]); st.discard.append(par["co"]); draw(st, i, 1)
    elif cid == "AE60":
        for q in [x.i for x in st.alive()]:
            if not st.over: rotate_orbit(st, q, actor=i)
    st.discard.append(card)
    st.actor = i; settle(st); st.actor = None


def extra_dmg(st, cid):
    if st.cfg.extra_dmg and CARDS[cid]["damage_max"] > 0 and CARDS[cid]["subtype"] == "Direct Effect": return st.cfg.extra_dmg
    return 0


def reclaim(st, i, card, pos, via):
    st.ooo.remove(card); st.stats["reclaims"] += 1
    co = CO(card)
    p = st.P[i]
    ok = enter(st, i, co, pos)   # INTERP G20: ownership transfers; reclaim counts toward the CO cap (ST09/AE46/AE54-type cards override by their text)
    if p.alive and p.sid == "ST11" and st.opps(i) and not st.over:
        dmg(st, i, pick_opp(st, i), 1)
    p.entered = p.entered   # no change
