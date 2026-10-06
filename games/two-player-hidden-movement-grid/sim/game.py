"""Dead Reckoning rules engine. Grid idx = y*5+x (x 0-4 = A-E, y 0-4 = rows 1-5).
Cells: 0 open, 1-3 salvage value, 4 mine, 5 reef, 6 sonar. Harbours are at idx 2 (Blue, seat 0) and 22 (Red, seat 1), cell value 0.
Cards: N E S W T (X = no-op, used only inside bot models)."""
import random, itertools

HARB = (2, 22)
FULL = tuple("NNEESSWWT")
DELTA = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
COMP = [1]*6 + [2]*6 + [3]*3 + [4]*3 + [5]*3 + [6]*2      # 23 sea cards (rules v2)
ZB = [1]*3 + [2]*3 + [4, 5, 6]; ZM = [3]*3 + [4, 5]       # blue/red waters (9 each), middle (5)
# zone of each square: 0 = Blue waters (rows 1-2), 1 = Middle (row 3), 2 = Red waters (rows 4-5)
ZONE = [0 if i // 5 < 2 else 1 if i // 5 == 2 else 2 for i in range(25)]

class Config:
    def __init__(self, torp8=True, max_rounds=12, log=False, harbour_safe=True, zoned=True, ping_steps=2):
        self.zoned = zoned; self.ping_steps = ping_steps; self.torp8 = torp8; self.max_rounds = max_rounds; self.log = log; self.harbour_safe = harbour_safe

class S:
    """Light state used for both real play and bot look-ahead copies."""
    __slots__ = ("pos", "piles", "grid", "fup", "canc", "bonus", "rev", "sonar", "unrev", "zoned", "stats", "cfg", "ev", "evp", "log")
    def copy(self):
        c = S.__new__(S)
        c.pos = self.pos[:]; c.piles = [self.piles[0][:], self.piles[1][:]]; c.grid = self.grid[:]; c.fup = self.fup[:]
        c.canc = [False, False]; c.bonus = [0.0, 0.0]; c.rev = [0, 0]; c.sonar = self.sonar[:]
        c.unrev = self.unrev; c.zoned = self.zoned; c.stats = None; c.cfg = self.cfg; c.ev = True; c.evp = self.evp; c.log = None
        return c

def ev_params(s):
    """Public-information expectation for a face-down card: (expected salvage, P(mine), P(sonar))."""
    out = {}
    for z in (0, 1, 2):
        u = s.unrev[z] if s.zoned else s.unrev[0]
        n = sum(u.values())
        out[z] = (0.0, 0.0, 0.0) if n == 0 else (sum(v * c for v, c in u.items() if v in (1, 2, 3)) / n, u.get(4, 0) / n, u.get(6, 0) / n)
    return out

def score(s, p): return sum(s.piles[p])

def _enter(s, p, t, start):
    """Apply the effect of sub p entering square t. Returns True if it bounced."""
    k = s.grid[t]
    if s.ev and not s.fup[t] and t not in HARB:           # face-down card in look-ahead: use expected value
        esal, pm, ps = s.evp[ZONE[t]]
        s.bonus[p] += esal + ps * 0.3
        if pm and s.piles[p]: s.bonus[p] -= pm * min(s.piles[p])
        s.rev[p] += 1; s.grid[t] = 0; s.fup[t] = True
        return False
    if not s.fup[t] and t not in HARB:
        s.fup[t] = True; (s.unrev[ZONE[t]] if s.zoned else s.unrev[0])[k] -= 1
    if k in (1, 2, 3):
        s.piles[p].append(k); s.grid[t] = 0
        if s.stats is not None: s.stats["taken%d" % k][p] += 1
    elif k == 4:
        s.grid[t] = 0; s.canc[p] = True
        if s.piles[p]: s.piles[p].remove(min(s.piles[p]))
        if s.stats is not None: s.stats["mines"][p] += 1
    elif k == 5:
        s.fup[t] = True
        if s.stats is not None: s.stats["reef_found"][p] += 1
        return True
    elif k == 6:
        s.sonar[p] += 1; s.grid[t] = 0
        if s.stats is not None: s.stats["taken6"][p] += 1
        if s.ev: s.bonus[p] += 0.0
    return False

def step(s, cards):
    pos = s.pos; tgt = [0, 0]
    for p in (0, 1):
        c = cards[p]; cur = pos[p]
        if s.canc[p] or c in ("T", "X"): tgt[p] = cur; continue
        dx, dy = DELTA[c]; x, y = cur % 5 + dx, cur // 5 + dy
        if not (0 <= x < 5 and 0 <= y < 5) or (s.grid[y*5+x] == 5 and s.fup[y*5+x]):
            tgt[p] = cur
            if s.stats is not None: s.stats["blocked"][p] += 1
        else: tgt[p] = y*5+x
    if tgt[0] == tgt[1] or (tgt[0] == pos[1] and tgt[1] == pos[0]):
        if s.stats is not None and (tgt[0] != pos[0] or tgt[1] != pos[1]): s.stats["collisions"] += 1
        tgt = [pos[0], pos[1]]
    start = pos[:]; bounced = [False, False]
    for p in (0, 1):
        if tgt[p] != start[p]:
            pos[p] = tgt[p]
            bounced[p] = _enter(s, p, tgt[p], start[p])
            if bounced[p]: pos[p] = start[p]
    for p in (0, 1):                                            # reef bounce clash
        if bounced[p] and not bounced[1-p] and pos[1-p] == start[p] and start[1-p] != start[p]:
            pos[1-p] = start[1-p]
    # torpedoes
    steal = [None, None]
    for p in (0, 1):
        if cards[p] == "T" and not s.canc[p]:
            r = 1 - p; a, b = pos[p], pos[r]
            dx, dy = abs(a % 5 - b % 5), abs(a // 5 - b // 5)
            near = max(dx, dy) == 1 if s.cfg.torp8 else dx + dy == 1
            if s.stats is not None: s.stats["fired"][p] += 1
            if near and not (s.cfg.harbour_safe and b == HARB[r]):
                if s.stats is not None: s.stats["hits"][p] += 1
                steal[p] = max(s.piles[r]) if s.piles[r] else 0
    for p in (0, 1):
        if steal[p]:
            s.piles[1-p].remove(steal[p]) if steal[p] in s.piles[1-p] else None
    for p in (0, 1):
        if steal[p]: s.piles[p].append(steal[p])
    # after a Mine the step above set canc; the Mine step itself was already resolved

def plans(hand):
    return sorted(set(itertools.permutations(hand, 3)))

def salvage_left(s):
    return sum(1 for i in range(25) if s.grid[i] in (1, 2, 3))

class Game:
    def __init__(self, cfg, bots, seed):
        self.cfg = cfg; self.bots = bots; rng = random.Random(seed); self.rng = rng
        s = S.__new__(S); s.cfg = cfg; s.zoned = cfg.zoned
        s.grid = [0] * 25; s.fup = [False] * 25
        sq_ = lambda ys: [y*5+x for y in ys for x in range(5) if y*5+x not in HARB]
        if cfg.zoned:
            pk = [(ZB[:], sq_((0, 1))), (ZM[:], sq_((2,))), (ZB[:], sq_((3, 4)))]
            for cards, sqs in pk:
                rng.shuffle(cards)
                for i, c in zip(sqs, cards): s.grid[i] = c
        else:
            deck = COMP[:]; rng.shuffle(deck)
            for i, c in zip(sq_((4, 3, 2, 1, 0)), deck): s.grid[i] = c
        for h in HARB: s.fup[h] = True
        s.pos = [HARB[0], HARB[1]]; s.piles = [[], []]; s.canc = [False, False]; s.bonus = [0.0, 0.0]
        s.rev = [0, 0]; s.sonar = [0, 0]; s.ev = False; s.evp = None
        def cnt(l):
            d = {}
            for c in l: d[c] = d.get(c, 0) + 1
            return d
        s.unrev = {0: cnt(ZB), 1: cnt(ZM), 2: cnt(ZB)} if cfg.zoned else {0: cnt(COMP)}
        keys = ["fired", "hits", "mines", "taken1", "taken2", "taken3", "taken6", "reef_found", "blocked"]
        s.stats = {k: [0, 0] for k in keys}; s.stats.update(collisions=0, pings=[0, 0], harbour_rounds=[0, 0], Tplays=[0, 0], rounds=0)
        s.log = [] if cfg.log else None
        self.s = s; self.hand = [list(FULL), list(FULL)]; self.cool = [[], []]
        self.history = []; self.round_scores = []

    def note(self, m):
        if self.s.log is not None: self.s.log.append(m)

    def run(self):
        s = self.s; cfg = self.cfg
        for rnd in range(1, cfg.max_rounds + 1):
            s.stats["rounds"] = rnd
            hands = [list(self.hand[p]) for p in (0, 1)]
            for p in (0, 1):                                   # hand = full minus cooling row
                h = list(FULL)
                for c in self.cool[p]: h.remove(c)
                hands[p] = h
            self.hands = hands
            # phase 1 ping
            sc = [score(s, 0), score(s, 1)]
            pinger = None
            for p in (0, 1):
                if sc[p] < sc[1 - p] and s.sonar[p] > 0 and self.bots[p].want_ping(self, p):
                    pinger = p; s.sonar[p] -= 1; s.stats["pings"][p] += 1
            plots = [None, None]
            if pinger is not None:
                r = 1 - pinger; n = self.cfg.ping_steps
                plots[r] = self.bots[r].plot(self, r, hands[r], None)
                plots[pinger] = self.bots[pinger].plot(self, pinger, hands[pinger], plots[r][:n])
                self.note("R%d: P%d pings; P%d's first %d cards %s are revealed" % (rnd, pinger + 1, r + 1, n, "".join(plots[r][:n])))
            else:
                for p in (0, 1): plots[p] = self.bots[p].plot(self, p, hands[p], None)
            for p in (0, 1):
                assert sorted(plots[p] + tuple(c for c in hands[p])) is not None
                hh = list(hands[p])
                for c in plots[p]: hh.remove(c)                   # raises if illegal
                s.stats["Tplays"][p] += plots[p].count("T")
            self.note("R%d plots: P1 %s  P2 %s  (pos %s %s, score %d-%d)" % (rnd, "".join(plots[0]), "".join(plots[1]), sq(s.pos[0]), sq(s.pos[1]), score(s, 0), score(s, 1)))
            s.canc = [False, False]
            for k in range(3):
                step(s, (plots[0][k], plots[1][k]))
                for p in (0, 1):
                    if s.pos[p] == HARB[p]: s.stats["harbour_rounds"][p] += 0
                self.history.append(score(s, 0) - score(s, 1))
                self.note("  step%d %s/%s -> P1 %s P2 %s score %d-%d" % (k + 1, plots[0][k], plots[1][k], sq(s.pos[0]), sq(s.pos[1]), score(s, 0), score(s, 1)))
            for p in (0, 1):
                if s.pos[p] == HARB[p]: s.stats["harbour_rounds"][p] += 1
            if rnd == 1: s.stats['coll_r1'] = s.stats['collisions']; self.r1 = score(s, 0) - score(s, 1)
            self.cool = [list(plots[0]), list(plots[1])]
            self.round_scores.append(score(s, 0) - score(s, 1))
            if salvage_left(s) == 0: break
        a, b = score(s, 0), score(s, 1)
        key = lambda p: (score(s, p), len(s.piles[p]), s.piles[p].count(3))
        winner = 0 if key(0) > key(1) else 1 if key(1) > key(0) else None
        return dict(winner=winner, rounds=s.stats["rounds"], scores=(a, b), capped=salvage_left(s) > 0, game=self)

def sq(i): return "ABCDE"[i % 5] + str(i // 5 + 1)

def play(cfg, bots, seed):
    g = Game(cfg, bots, seed); r = g.run(); return r
