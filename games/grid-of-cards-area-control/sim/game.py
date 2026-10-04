"""Nine Fields rules v1. State, legal actions, flood resolution, scoring. Standard library only.
Interpretations are listed in AMBIGUITIES at the bottom."""
import random

# (id, value, capacity, axis) axis 0 = Row, 1 = Column (axis when entering the grid upright)
CARDS = []
_spec = [(1, 2, "RCRCRCRC"), (2, 2, "RCR"), (2, 3, "CRCRCRCR"), (3, 3, "CRC"), (3, 4, "RCRCRC"), (4, 4, "RC")]
_i = 0
for v, c, ax in _spec:
    for a in ax:
        _i += 1
        CARDS.append((_i, v, c, 0 if a == "R" else 1))
assert len(CARDS) == 30 and sum(c[1] for c in CARDS) == 65

STALL_MULT = 3   # rules: stall limit = 3 x players
ADJ = [[] for _ in range(9)]
for _c in range(9):
    r, k = divmod(_c, 3)
    if r > 0: ADJ[_c].append(_c - 3)
    if r < 2: ADJ[_c].append(_c + 3)
    if k > 0: ADJ[_c].append(_c - 1)
    if k < 2: ADJ[_c].append(_c + 1)

class State:
    __slots__ = ("n", "card", "axis", "pw", "supply", "tn", "tv", "deck", "dp", "since", "floods", "over",
                 "turn", "log", "tcards", "stall_end", "hist", "dec", "inter", "acts")
    def clone(self):
        s = State.__new__(State)
        s.n = self.n; s.card = self.card[:]; s.axis = self.axis[:]; s.pw = [l[:] for l in self.pw]
        s.supply = self.supply[:]; s.tn = self.tn[:]; s.tv = self.tv[:]; s.deck = self.deck; s.dp = self.dp
        s.since = self.since; s.floods = self.floods; s.over = self.over; s.turn = self.turn
        s.log = None; s.tcards = None; s.stall_end = self.stall_end; s.hist = None
        s.dec = None; s.inter = None; s.acts = None
        return s
    def nxt(self): return self.deck[self.dp] if self.dp < len(self.deck) else None
    def full(self, c): return sum(self.pw[c]) >= self.card[c][2]

def new_game(n, seed, log=False):
    rng = random.Random(seed)
    deck = CARDS[:]; rng.shuffle(deck)
    s = State(); s.n = n
    s.card = deck[:9]; s.axis = [c[3] for c in s.card]; s.pw = [[0] * n for _ in range(9)]
    s.supply = [4] * n; s.tn = [0] * n; s.tv = [0] * n; s.deck = deck; s.dp = 9
    s.since = 0; s.floods = 0; s.over = False; s.turn = 0; s.stall_end = False
    s.log = [] if log else None
    s.tcards = [[] for _ in range(n)]; s.hist = []; s.dec = [0] * n; s.inter = [0] * n
    s.acts = {"land": 0, "sail": 0}
    return s

def legal(st, p):
    out = []
    pw = st.pw; card = st.card
    if st.supply[p] > 0:
        for c in range(9):
            if sum(pw[c]) < card[c][2]: out.append(("L", c))
    for c in range(9):
        if pw[c][p] > 0:
            for d in ADJ[c]:
                if sum(pw[d]) < card[d][2]: out.append(("S", c, d))
    return out

def do_move(st, p, a):
    """Apply Land or Sail. Returns the flooded cell, or -1."""
    if a[0] == "L":
        c = a[1]; st.supply[p] -= 1; st.pw[c][p] += 1
    else:
        c = a[2]; st.pw[a[1]][p] -= 1; st.pw[c][p] += 1
    return c if sum(st.pw[c]) == st.card[c][2] else -1

def claim(st, c, trigger, final, p_log=None):
    cnt = st.pw[c]; mx = max(cnt)
    if mx == 0:
        w = None if final else trigger
    else:
        tied = [q for q in range(st.n) if cnt[q] == mx]
        if len(tied) > 1:
            m = min(st.tn[q] for q in tied)
            tied = [q for q in tied if st.tn[q] == m]
        w = tied[0] if len(tied) == 1 else None
    if w is not None:
        v = st.card[c][1]; st.tn[w] += 1; st.tv[w] += v
        if st.tcards is not None: st.tcards[w].append(st.card[c][0])
    return w

def resolve(st, p, c, d):
    """Flood of island at cell c, trigger p, direction choice d in {0,1}. Returns (winner, value, card_id)."""
    ax = st.axis[c]
    if ax == 0:
        r = c - c % 3; order = [r, r + 1, r + 2]
    else:
        k = c % 3; order = [k, k + 3, k + 6]
    if d: order.reverse()
    f = order[0]
    fell = st.card[f]
    w = claim(st, f, p, False)
    for q in range(st.n): st.supply[q] += st.pw[f][q]
    ncard, naxis, npw = st.card, st.axis, st.pw
    ncard[f], naxis[f], npw[f] = ncard[order[1]], naxis[order[1]], npw[order[1]]
    ncard[order[1]], naxis[order[1]], npw[order[1]] = ncard[order[2]], naxis[order[2]], npw[order[2]]
    nx = st.nxt()
    e = order[2]
    if nx is None:
        ncard[e], naxis[e], npw[e] = None, 0, [0] * st.n
        st.over = True
    else:
        ncard[e], naxis[e], npw[e] = nx, nx[3], [0] * st.n
        st.dp += 1
    return w, fell[1], fell[0], order

def final_tide(st):
    for c in range(9):
        if st.card[c] is not None: claim(st, c, None, True)

def play(n, bots, seed, log=False, cap=600):
    """bots: list of n bot objects (seat 0 moves first). Returns dict of results."""
    st = new_game(n, seed, log)
    rng = random.Random(seed ^ 0x5bd1e995)
    # opening pawns: last seat first, counter-clockwise
    for p in range(n - 1, -1, -1):
        empty = [c for c in range(9) if sum(st.pw[c]) == 0]
        c = bots[p].opening(st, p, empty)
        st.pw[c][p] += 1; st.supply[p] -= 1
        if log: st.log.append("open: seat %d lands on cell %d" % (p + 1, c))
    p = 0; turns = 0; lead_hist = []; mid = None; hit_cap = False
    while not st.over and turns < cap:
        turns += 1; st.turn = turns
        acts = legal(st, p)
        if not acts:
            st.since += 1
            if log: st.log.append("t%d seat %d passes" % (turns, p + 1))
        else:
            if len(acts) > 1: st.dec[p] += 1
            a, d = bots[p].act(st, p, acts)
            st.acts["land" if a[0] == "L" else "sail"] += 1
            tgt = a[1] if a[0] == "L" else a[2]
            if any(st.pw[tgt][q] for q in range(n) if q != p): st.inter[p] += 1
            fid = st.card[tgt][0] if sum(st.pw[tgt]) + 1 == st.card[tgt][2] else None
            fc = do_move(st, p, a)
            if fc < 0:
                st.since += 1
                if log: st.log.append("t%d seat %d %s" % (turns, p + 1, _fmt(st, a)))
            else:
                st.dec[p] += 1
                cid = st.card[fc][0]
                w, val, fellid, order = resolve(st, p, fc, d)
                st.floods += 1; st.since = 0
                if w is not None and w != p: st.inter[p] += 1
                # turn the flooded island if it is still in the grid
                for pos in order:
                    if st.card[pos] is not None and st.card[pos][0] == cid:
                        st.axis[pos] ^= 1
                if log:
                    st.log.append("t%d seat %d %s floods card %d (axis %s, dir %d): card %d value %d falls to %s. scores %s"
                                  % (turns, p + 1, _fmt(st, a), cid, "?", d,
                                     fellid, val, "nobody" if w is None else "seat %d" % (w + 1), st.tv))
                lead_hist.append(_leader(st))
                if st.floods == 11: mid = _leader(st)
            if st.since >= STALL_MULT * n and not st.over:
                st.over = True; st.stall_end = True
        p = (p + 1) % n
    hit_cap = (turns >= cap and not st.over)
    final_tide(st)
    sc = st.tv[:]
    order = sorted(range(n), key=lambda q: (sc[q], st.tn[q], q), reverse=True)
    top = sc[order[0]]
    tie = sum(1 for q in range(n) if sc[q] == top) > 1
    return {"st": st, "winner": order[0], "scores": sc, "turns": turns, "tie": tie, "cap": hit_cap,
            "stall": st.stall_end, "floods": st.floods, "leads": lead_hist, "mid": mid}

def _leader(st):
    m = max(st.tv)
    ls = [q for q in range(st.n) if st.tv[q] == m]
    return ls[0] if len(ls) == 1 and m > 0 else -1

def _fmt(st, a):
    return "lands on cell %d" % a[1] if a[0] == "L" else "sails cell %d -> %d" % (a[1], a[2])

AMBIGUITIES = [
 "'Floods' triggers when count BECOMES equal to capacity. Opening pawns can never fill an island (capacity >= 2, one pawn each). I treat 'full' as count >= capacity.",
 "The flooded island is turned only if it did not fall off; I find it by card identity after the slide.",
 "Stall limit counts passes and non-flood turns; opening placements do not count. It ends the game on the turn the counter hits 3 x players.",
 "Final tide is scored in reading order, pile sizes updated as each island is claimed (used for the fewest-trophies tiebreak).",
 "Rules do not say whether a flooded island that is also the last in line (falls off) still counts as 'flooded island still in grid' - it does not; no turn.",
 "'Fewest trophy cards' tiebreak: if tied players have equal pile sizes nobody claims; island is removed (no refill difference).",
 "First player is random; I always make seat 1 the first player and the result is the same as random assignment.",
 "Pawns on the falling island return to supply even for players with no majority (stated), so supply can exceed 4 never; pawns are conserved.",
 "Not stated: whether Land is allowed onto an island that is already flooded-full - no (not full is required).",
]
