"""Heavenly Bodies v2 (Gearbox) rules engine, cycle 1 rules with switches (see CFG_DEFAULT). Standard library only.
Slots: 0=North 1=East 2=South 3=West. Player p's left neighbour is (p+1)%n (play passes left).
Contacts: p's West (3) touches East (1) of (p+1)%n.  Cards are tuples (colour 0-3, size 1-5, copy).
Interpretations of ambiguous rules are listed in AMBIGUITIES at the bottom."""
import random

N_SLOTS = 4
CLOCK, CCW = 1, -1


CFG_DEFAULT = dict(win_at_end=True, rebound=False, shield=True, cm_by_count=True, rainbow=True, deepspace_draw=False,
                   deck40=False, capture_to_ds=False, opening_2p=2, mass=None, opening=None,
                   shield_mode='full', mass_plus=0, last_draw2=False)  # sweep switches: shield_mode full|big|spin, mass_plus, last_draw2  # opening: NEW test, bodies at setup for every count
CFG = dict(CFG_DEFAULT, n=2, mass_eff=16)   # active config of the game being played in this process (bots read it)
MASS_BY_COUNT = {2: 16, 3: 15, 4: 14}


def shield_ok(c):
    return bool(CFG['shield']) and (CFG['shield_mode'] != 'big' or c[1] in (1, 5))


def make_deck(deck40=False):
    d = []
    for c in range(4):
        for s in (1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5):
            d.append((c, s, sum(1 for x in d if x[0] == c and x[1] == s)))
    if deck40: d = [x for x in d if not (x[1] in (2, 3, 4) and x[2] == 2)]
    return d


def beats(a, b, comet=True):
    """1 if a wins the crash, -1 if b wins, 0 equal size."""
    if comet:
        if a[1] == 1 and b[1] == 5: return 1
        if a[1] == 5 and b[1] == 1: return -1
    return (a[1] > b[1]) - (a[1] < b[1])


def patterns(orbit):
    """Win patterns satisfied by an orbit (list of 4 slots), using the active CFG."""
    if any(c is None for c in orbit): return []
    sizes = sorted(c[1] for c in orbit); out = []
    if sum(sizes) >= CFG["mass_eff"]: out.append("mass")
    cols = {c[0] for c in orbit}
    if len(cols) == 1 or (CFG["rainbow"] and len(cols) == 4): out.append("const")
    if sizes in ([1, 2, 3, 4], [2, 3, 4, 5]): out.append("align")
    return out


def spin_orbit(orbit, d):
    new = [None] * 4
    for i in range(4): new[(i + d) % 4] = orbit[i]
    return new


def crash(orbits, q, n, comet=True, sh=frozenset()):
    """Resolve the contacts of orbit q (already spun): West contact first, then East. Sideways (sh) bodies never crash.
    Returns events ('cap', winner_owner, loser_owner, wcard, lcard) or ('tie', a_owner, b_owner, acard, bcard). Mutates orbits."""
    ev = []
    contacts = [((q, 3), ((q + 1) % n, 1)), (((q - 1) % n, 3), (q, 1))]
    for (pa, sa), (pb, sb) in contacts:
        a, b = orbits[pa][sa], orbits[pb][sb]
        if a is None or b is None or a in sh or b in sh: continue
        r = beats(a, b, comet)
        if r > 0: orbits[pb][sb] = None; ev.append(("cap", pa, pb, a, b))
        elif r < 0: orbits[pa][sa] = None; ev.append(("cap", pb, pa, b, a))
        else: orbits[pa][sa] = None; orbits[pb][sb] = None; ev.append(("tie", pa, pb, a, b))
    return ev


class State:
    def __init__(self, n, seed, log=False):
        self.n = n; self.rng = random.Random(seed)
        self.deck = make_deck(CFG["deck40"]); self.rng.shuffle(self.deck)
        self.hands = [[self.deck.pop() for _ in range(5)] for _ in range(n)]
        self.orbits = [[None] * 4 for _ in range(n)]
        self.deep = []; self.turn = 0; self.active = 0
        self.shielded = set()
        self.log = [] if log else None
        self.stats = dict(captures=0, ties=0, spins=0, crash_spins=0, self_spins=0, other_spins=0, other_crash=0, self_crash=0,
                          recalls=0, rebounds=0, formed=0, formed_survived=0, full_survived=0, full_formed=0, deep_takes=0,
                          draws=0, launches=0, cards_moved_turns=0, decisions=[0] * n, mover_caps=[0] * n,
                          armed=0, armed_attacked=0, armed_survived=0, armed_att_survived=0, armed_won=0, cap_by_size=[0] * 6)
        self.armed = {}; self.attacked = set()

    def totals(self): return [sum(c[1] for c in o if c) for o in self.orbits]
    def counts(self): return [sum(1 for c in o if c) for o in self.orbits]
    def L(self, s):
        if self.log is not None: self.log.append(s)


def cs(c): return "EFVS"[c[0]] + str(c[1])
def orb_str(o, sh=()): return "[" + " ".join((cs(c) + ("~" if c in sh else "")) if c else "--" for c in o) + "]"


def legal_launches(st, p, rebound_allowed):
    """Launch plans: tuples of (hand_index, slot)."""
    hand = st.hands[p]; plans = [()]
    plans += [((i, s),) for i in range(len(hand)) for s in range(4)]
    if rebound_allowed:
        for i in range(len(hand)):
            for s in range(4):
                for j in range(len(hand)):
                    if j == i: continue
                    for t in range(4):
                        if t != s: plans.append(((i, s), (j, t)))
    return plans


def apply_launches(orbit, hand, plan):
    """Returns (new_orbit, new_hand, recalled_count). Indices refer to the original hand."""
    orbit = list(orbit); hand = list(hand); played = set(); rec = 0
    for i, s in plan:
        c = hand[i]; played.add(i)
        if orbit[s] is not None: hand.append(orbit[s]); rec += 1
        orbit[s] = c
    return orbit, [c for k, c in enumerate(hand) if k not in played], rec


def rebound_ok(st, p):
    if not CFG["rebound"]: return False
    mine = sum(1 for c in st.orbits[p] if c)
    return all(mine < sum(1 for c in st.orbits[o] if c) for o in range(st.n) if o != p)


def is_armed(st, p):
    """Public-state test (engine view): p could finish a pattern with one launch from the current hand, or already has one."""
    o = st.orbits[p]
    if patterns(o): return True
    if sum(1 for c in o if c) < 3: return False
    for c in st.hands[p]:
        for s in range(4):
            t = list(o); t[s] = c
            if patterns(t): return True
    return False


def play(bots, seed, n=None, log=False, cap=200, **cfg):
    n = n or len(bots)
    CFG.clear(); CFG.update(CFG_DEFAULT); CFG.update(cfg); CFG["n"] = n
    CFG["mass_eff"] = (CFG["mass"] or (MASS_BY_COUNT[n] if CFG["cm_by_count"] else 15)) + CFG["mass_plus"]
    opening = CFG["opening"] if CFG["opening"] is not None else (CFG["opening_2p"] if n == 2 else 2)
    st = State(n, seed, log=log)
    for p in range(n):
        picks = bots[p].setup(st, p)[:opening]
        cards = [st.hands[p][ci] for ci, s in picks]
        for (ci, s), c in zip(picks, cards): st.orbits[p][s] = c
        st.hands[p] = [c for k, c in enumerate(st.hands[p]) if k not in {ci for ci, s in picks}]
    st.L("setup " + " | ".join(orb_str(o) for o in st.orbits))
    S = st.stats; leaders = []; winner = None; win_pat = None; long_night = False; first = True
    while st.turn < cap:
        p = st.turn % n; st.active = p
        # armed-position bookkeeping (positions armed at the end of an earlier turn, tested at the start of p's turn)
        if p in st.armed:
            S["armed"] += 1; att = p in st.attacked; still = is_armed(st, p)
            S["armed_attacked"] += att; S["armed_survived"] += still
            if att: S["armed_att_survived"] += still
            del st.armed[p]
        st.attacked.discard(p)
        # 0 win check at start (cycle-0 timing) when WIN_AT_END is off
        if not CFG["win_at_end"]:
            pats = patterns(st.orbits[p])
            if pats:
                winner = p; win_pat = pats; st.L("T%d P%d WINS(start) %s %s" % (st.turn, p, pats, orb_str(st.orbits[p]))); break
        # 1 wake
        for c in st.orbits[p]:
            if c: st.shielded.discard(c)
        # 2 draw
        if not (first and p == 0):
            if not st.deck:
                long_night = True; break
            dec_draw = 0
            src = "deck"
            if CFG["deepspace_draw"] and st.deep:
                dec_draw = 1; src = bots[p].draw(st, p)
            if src == "deep" and st.deep: st.hands[p].append(st.deep.pop()); S["deep_takes"] += 1
            else: st.hands[p].append(st.deck.pop())
            if CFG["last_draw2"] and st.turn == n - 1 and st.deck: st.hands[p].append(st.deck.pop())
            S["draws"] += 1
        first = False
        moved = 0; dec = 0
        # 3 launch
        rb = rebound_ok(st, p)
        if st.hands[p]: dec += 1
        plan, spin = bots[p].turn(st, p, rb)
        plan = [x for x in plan][: (2 if rb else 1)]
        if len(plan) == 2 and plan[0][1] == plan[1][1]: plan = plan[:1]
        if plan and st.hands[p]:
            if len(plan) == 2: S["rebounds"] += 1
            launched = [st.hands[p][i] for i, s in plan]
            neworb, newhand, rec = apply_launches(st.orbits[p], st.hands[p], plan)
            st.orbits[p] = neworb; st.hands[p] = newhand; S["recalls"] += rec; S["launches"] += len(plan)
            for c in launched:
                if shield_ok(c): st.shielded.add(c)
            st.L("T%d P%d launch %s -> %s" % (st.turn, p, " ".join(cs(c) for c in launched), orb_str(neworb, st.shielded)))
        if is_armed(st, p) or patterns(st.orbits[p]): pass
        pf = patterns(st.orbits[p])
        if all(c for c in st.orbits[p]): S["full_formed"] += 1
        if pf: S["formed"] += 1
        # 4 spin + 5 crash
        nonempty = [q for q in range(n) if any(st.orbits[q])]
        if nonempty:
            if len(nonempty) > 1: dec += 1
            q, d = spin
            if q not in nonempty: q = nonempty[0]
            st.orbits[q] = spin_orbit(st.orbits[q], d); S["spins"] += 1
            if q == p: S["self_spins"] += 1
            else: S["other_spins"] += 1; st.attacked.add(q)
            ev = crash(st.orbits, q, n, True, st.shielded)
            if CFG["shield_mode"] == "spin":
                for c in st.orbits[q]: st.shielded.discard(c)
            if ev:
                S["crash_spins"] += 1
                if q == p: S["self_crash"] += 1
                else: S["other_crash"] += 1
            for e in ev:
                if e[0] == "cap":
                    _, w, l, wc, lc = e
                    if CFG["capture_to_ds"]: st.deep.append(lc)
                    else: st.hands[w].append(lc)
                    S["captures"] += 1; moved += 1; S["cap_by_size"][lc[1]] += 1; st.attacked.add(l)
                    if w == p: S["mover_caps"][p] += 1
                    st.L("T%d P%d spin P%d %+d: P%d %s takes P%d %s" % (st.turn, p, q, d, w, cs(wc), l, cs(lc)))
                else:
                    _, a, b, ac, bc = e; S["ties"] += 1; moved += 1; st.attacked.add(a); st.attacked.add(b)
                    st.deep.append(ac); st.deep.append(bc)
                    st.L("T%d P%d spin P%d %+d: %s and %s collide, both lost" % (st.turn, p, q, d, cs(ac), cs(bc)))
        S["decisions"][p] += dec
        S["cards_moved_turns"] += 1 if moved else 0
        # 6 end: discard to 5, then win check
        if len(st.hands[p]) > 5:
            for c in bots[p].discard(st, p): st.deep.append(c)
        if CFG["win_at_end"]:
            pe = patterns(st.orbits[p])
            if pe:
                if pf: S["formed_survived"] += 1
                winner = p; win_pat = pe; st.turn += 1
                st.L("T%d P%d WINS %s %s" % (st.turn - 1, p, pe, orb_str(st.orbits[p]))); break
        st.turn += 1
        for o in range(n):
            if o != p and is_armed(st, o): st.armed[o] = 1
        t = st.totals(); mx = max(t)
        leaders.append(t.index(mx) if t.count(mx) == 1 else None)
    capped = winner is None and not long_night
    if winner is None and long_night:
        t = st.totals(); cnt = st.counts()
        big = [max((c[1] for c in o if c), default=0) for o in st.orbits]
        start = st.turn % n
        key = lambda i: (-t[i], -cnt[i], -big[i], (i - start) % n)
        winner = min(range(n), key=key); win_pat = ["longnight"]
        tie_level = sum(1 for i in range(n) if (t[i], cnt[i], big[i]) == (t[winner], cnt[winner], big[winner]))
        S["ln_tiebreak_order"] = int(tie_level > 1)
    return dict(winner=winner, turns=st.turn, capped=capped, leaders=leaders, pattern=win_pat, long_night=long_night, stats=S, st=st)


AMBIGUITIES = [
    "Sideways bodies and the spin: the sim keeps the sideways mark on the card, so it moves with the spin (rules say so). Clear, but 'turn upright at Wake' must also cover a body that was spun into another slot meanwhile.",
    "REBOUND on with SHIELD on: sim shields both launched bodies (rules say 'at most one sideways'; only an issue if Rebound returns).",
    "Win check order at End: discard to 5 first, then pattern check; a discard never touches the orbit, so the order does not matter. Clear.",
    "A body Recalled by a Launch was upright (Wake already stood it up), so a Recall never returns a sideways card. Clear.",
    "Shielded body in a contact: the other body is also safe (contact does nothing). Also holds if the shielded body is the one that would have been captured by the opponent's winner of the other contact. Clear.",
    "Long Night tie-break step 4 ('tied player who would take the next turn soonest, counting from the player whose Draw found the Deck empty'): sim counts the empty-Deck player as 0, so that player wins a full tie. Needs one word in the rules: 'including that player'.",
    "'Equal Size: both go to Deep Space' - with a shielded body there is no crash, so two equal bodies can sit in contact; the sim allows it, no rule needed.",
    "A player with no hand cards and an empty orbit slot can still spin; with every orbit empty the spin is skipped (unreachable after setup).",
    "OPENING_2P=1: the first player's skipped Draw means 4 cards in hand, not 3 plus a draw; sim keeps the other 4 cards.",
    "Spin of an orbit holding a single shielded body: legal, no effect. Strategic bots use this as a 'pass'. Not a rules problem, but 'must spin' is soft.",
    "Hand limit 5 is checked in End only: a player may hold 8+ cards through opponents' turns. Clear.",
]
