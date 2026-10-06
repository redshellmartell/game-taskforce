"""Ladder Pairs (rules.md v1) engine. 4 players, 6 hands. Standard library only.
A play is a tuple (kind, n, top): kind 'S' single, 'P' pair, 'T' triple, 'R' run (n>=3); top = rank (Ropes are 14/15 singles).
Bot interface: bot.choose(g, me, legal, leading) -> a play from `legal`, or None to pass (only when following).
Bots may read only public state plus their own hand: g.cnt[me], g.size, g.known, g.scores, g.uphill, g.holder, g.played,
g.hand_no, g.trick_no, g.colour[me] (own Rope colour). Hooks: bot.setup(seat, bots), bot.new_hand(g, me), bot.observe(ev).

Interpretations chosen where rules.md is silent are listed in AMBIGUITIES (also copied to playtest.json)."""
import random
import simkit

HANDS = 6; TURN_CAP = 200; UPHILL_GAP = 4


class Cfg:
    def __init__(self, uphill=True, relay=True, first_pts=3, second_pts=1, uphill_gap=UPHILL_GAP, log=False):
        self.uphill = uphill; self.relay = relay; self.first_pts = first_pts; self.second_pts = second_pts
        self.uphill_gap = uphill_gap; self.log = log


AMBIGUITIES = [
    "Hand-ending tie for the Ropes: which Rope shows when the Relay partner 'shows their Rope (if still in hand)' - Relay only matters for knowledge if the partner's Rope was unplayed; chosen: leader's colour becomes public (equal to the out player's, who had to play a Rope to go out).",
    "'Players ranked by fewest cards left' for the turn cap is unreachable (max ~176 turns); implemented but never hit.",
    "Four of a kind is not a type: a pair+pair split is the only way to play it (as stated in the playbook, not in the rules text sections 1-6).",
    "Who counts as 'first player out' when the second player out ends the hand mid-trick: first = earlier out; no points for non-going-out players beyond team share (as stated).",
    "Uphill threshold uses scores at the START of the hand ('4 or more below the highest score'); a player exactly 4 below is Uphill (>=4).",
    "Final tie-break step 3 'better finish in hand 6' is applied to tied players; players still tied after it share the win. Sim resolves a shared win by a random pick and reports the shared-win rate as ties.",
    "'You cannot go out without playing your Rope' is a consequence, not a restriction: the Rope is a card in hand and the hand empties only when it is played. Needs no extra rule text.",
    "Is passing allowed for the leader after a Relay (lead goes to partner): not allowed (must lead), as for any leader.",
    "Passed player may play again in the same trick: trick ends only after every other in-hand player passes consecutively since the last play (a pass-then-play is possible once someone else plays).",
]


class G:
    pass


def legal_leads(cnt):
    out = []
    for r in range(1, 16):
        if cnt[r] > 0: out.append(("S", 1, r))
    for r in range(1, 14):
        if cnt[r] >= 2: out.append(("P", 2, r))
        if cnt[r] >= 3: out.append(("T", 3, r))
    for s in range(1, 12):
        if cnt[s] and cnt[s + 1]:
            e = s + 1
            while e < 13 and cnt[e + 1]:
                e += 1
                out.append(("R", e - s + 1, e))
    return out


def legal_follows(cnt, cur):
    kind, n, top = cur; out = []
    if kind == "S":
        for r in range(top + 1, 16):
            if cnt[r] > 0: out.append(("S", 1, r))
    elif kind in "PT":
        need = n
        for r in range(top + 1, 14):
            if cnt[r] >= need: out.append((kind, n, r))
    else:
        for e in range(max(top + 1, n), 14):
            if all(cnt[r] > 0 for r in range(e - n + 1, e + 1)): out.append(("R", n, e))
    return out


def remove(cnt, play):
    kind, n, top = play
    if kind == "S": cnt[top] -= 1
    elif kind in "PT":
        cnt[top] -= n
    else:
        for r in range(top - n + 1, top + 1): cnt[r] -= 1


def new_game(rng, cfg):
    g = G(); g.cfg = cfg; g.scores = [0] * 4; g.firsts = [0] * 4; g.rng = rng
    g.dealer = rng.randrange(4); g.hand_no = 0; g.hist = []
    return g


def play_hand(g, bots, rng):
    cfg = g.cfg
    g.hand_no += 1
    ropes = [("Sun", 14), ("Sun", 15), ("Moon", 14), ("Moon", 15)]; rng.shuffle(ropes)
    g.colour = [ropes[p][0] for p in range(4)]; rope_rank = [ropes[p][1] for p in range(4)]
    partner = [next(q for q in range(4) if q != p and g.colour[q] == g.colour[p]) for p in range(4)]
    g.partner_truth = partner
    nums = [r for r in range(1, 14) for _ in range(4)]; rng.shuffle(nums)
    g.cnt = [[0] * 16 for _ in range(4)]
    for p in range(4):
        for r in nums[10 * p:10 * p + 10]: g.cnt[p][r] += 1
        g.cnt[p][rope_rank[p]] += 1
    g.size = [11] * 4; g.known = [None] * 4; g.played = [0] * 16; g.holder = None
    top_score = max(g.scores)
    g.uphill = [bool(cfg.uphill and top_score - g.scores[p] >= cfg.uphill_gap) for p in range(4)]
    lo = min(g.scores); tied = [p for p in range(4) if g.scores[p] == lo]
    start = (g.dealer + 1) % 4
    lead = next((start + k) % 4 for k in range(4) if (start + k) % 4 in tied)
    first_lead = lead
    for p in range(4):
        b = bots[p]
        if hasattr(b, "new_hand"): b.new_hand(g, p)
    out = []; turns = 0; g.trick_no = 0
    st = dict(first_lead=first_lead, forced=0, follow=0, runs3=0, rope_trick=None, ropes=0, relays=0, kinds=[set() for _ in range(4)],
              uphill=list(g.uphill), forced_streak=[0] * 4, decisions=[0] * 4, turns_by=[0] * 4, beats=[0] * 4, log=[])
    log = st["log"] if cfg.log else None
    ended = False
    while not ended:
        g.trick_no += 1; p = lead; cur = None; g.holder = None; streak = 0; g.cur = None
        while True:
            if p in out: p = (p + 1) % 4; continue
            cnt = g.cnt[p]
            if cur is None:
                legal = legal_leads(cnt); leading = True
            else:
                legal = legal_follows(cnt, cur); leading = False
            turns += 1; st["turns_by"][p] += 1
            if not legal:
                action = None; st["forced"] += 1; st["follow"] += 1; st["forced_streak"][p] += 1
                if st["forced_streak"][p] == 3: st["runs3"] += 1
            else:
                if not leading:
                    st["follow"] += 1; st["forced_streak"][p] = 0
                if len(legal) + (0 if leading else 1) > 1: st["decisions"][p] += 1
                action = bots[p].choose(g, p, legal, leading)
                if action is not None and action not in legal: raise ValueError("illegal play %r by %d" % (action, p))
                if leading and action is None: raise ValueError("leader passed")
            if action is None:
                streak += 1
                for b in bots:
                    if hasattr(b, "observe"): b.observe(("pass", p))
                if log is not None: log.append("t%d seat%d passes" % (g.trick_no, p))
            else:
                kind, n, top = action
                remove(cnt, action); g.size[p] -= n; st["kinds"][p].add(kind if kind != "S" or top < 14 else "Rope")
                if kind == "S" and top >= 14:
                    g.known[p] = g.colour[p]; st["ropes"] += 1
                    if st["rope_trick"] is None: st["rope_trick"] = g.trick_no
                    g.played[top] += 1
                else:
                    for r in range(top - n + 1, top + 1) if kind == "R" else [top]:
                        g.played[r] += 1 if kind in "SR" else n
                if cur is not None and g.holder is not None: st["beats"][p] += 1
                prev = g.holder; g.holder = p; cur = action; g.cur = cur; streak = 0
                for b in bots:
                    if hasattr(b, "observe"): b.observe(("play", p, action, prev))
                if log is not None: log.append("t%d seat%d %s %s%s" % (g.trick_no, p, "leads" if leading else "plays", kind + str(n) + "@" + str(top), " (Rope %s)" % g.colour[p] if top >= 14 else ""))
                if g.size[p] == 0:
                    out.append(p)
                    if log is not None: log.append("  seat%d is OUT (#%d)" % (p, len(out)))
                    if len(out) == 2: ended = True; break
            if turns >= TURN_CAP: ended = True; break
            holder_in = g.holder not in out
            need = (4 - len(out)) - (1 if holder_in else 0)
            if streak >= need: break
            p = (p + 1) % 4
        if ended: break
        w = g.holder
        if w in out:
            if cfg.relay:
                lead = partner[w]; g.known[lead] = g.colour[lead]; st["relays"] += 1
                for b in bots:
                    if hasattr(b, "observe"): b.observe(("relay", w, lead))
                if log is not None: log.append("  RELAY: seat%d's partner seat%d leads" % (w, lead))
            else:
                lead = (w + 1) % 4
                while lead in out: lead = (lead + 1) % 4
        else:
            lead = w
        for b in bots:
            if hasattr(b, "observe"): b.observe(("trick_end", w))
    capped = turns >= TURN_CAP and len(out) < 2
    if len(out) < 2:   # cap fallback: fewest cards left ranks next
        rest = sorted((q for q in range(4) if q not in out), key=lambda q: (g.size[q], rng.random()))
        out += rest[:2 - len(out)]
    a, b2 = out[0], out[1]
    pts = [0] * 4
    team_a = {a, partner[a]}
    for q in range(4):
        base = 0
        if q in team_a: base += cfg.first_pts
        if b2 in team_a:
            if q in team_a: base += cfg.second_pts
        elif q not in team_a: base += cfg.second_pts
        pts[q] = base * (2 if g.uphill[q] else 1)
    for q in range(4): g.scores[q] += pts[q]
    g.firsts[a] += 1
    st.update(out=out, pts=pts, turns=turns, capped=capped, partner=partner, sweep=(b2 in team_a), lead_team_3=(first_lead in team_a),
              lead_partner_pos=(partner[first_lead] - first_lead) % 4, last_finish=list(out))
    if log is not None: log.append("HAND %d end: out order %s, pts %s, scores %s" % (g.hand_no, out, pts, g.scores))
    g.dealer = (g.dealer + 1) % 4
    g.hist.append(st)
    return st


def play(bots, seed, cfg=None):
    cfg = cfg or Cfg()
    rng = random.Random(seed); g = new_game(rng, cfg)
    for p, b in enumerate(bots):
        if hasattr(b, "setup"): b.setup(p, bots)
    leaders = []; turns = 0; capped = False
    for _ in range(HANDS):
        st = play_hand(g, bots, rng); turns += st["turns"]; capped = capped or st["capped"]
        m = max(g.scores); ls = [q for q in range(4) if g.scores[q] == m]
        leaders.append(ls[0] if len(ls) == 1 else None)
    m = max(g.scores); cands = [q for q in range(4) if g.scores[q] == m]
    shared = False
    if len(cands) > 1:
        m2 = max(g.firsts[q] for q in cands); cands = [q for q in cands if g.firsts[q] == m2]
    if len(cands) > 1:
        def fin(q):
            o = g.hist[-1]["out"]
            return o.index(q) if q in o else 2 + g.size[q]
        m3 = min(fin(q) for q in cands); cands = [q for q in cands if fin(q) == m3]
    if len(cands) > 1: shared = True
    winner = rng.choice(cands)
    return dict(winner=winner, turns=turns, capped=capped, leaders=leaders, shared=shared, scores=list(g.scores), hands=g.hist)
