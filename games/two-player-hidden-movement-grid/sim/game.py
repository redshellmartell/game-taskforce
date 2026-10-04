"""Dead Reckoning rules engine. Grid idx = y*5+x (x 0-4 = A-E, y 0-4 = rows 1-5).
Cells: 0 open, 1-3 salvage value, 4 mine, 5 reef, 6 sonar. Harbours are at idx 2 (Blue, seat 0) and 22 (Red, seat 1), cell value 0.
Cards: N E S W T (X = no-op, used only inside bot models)."""
import random, itertools

HARB = (2, 22)
FULL = tuple("NNEESSWWT")
DELTA = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
COMP = [1]*5 + [2]*5 + [3]*3 + [4]*4 + [5]*3 + [6]*3      # 23 sea cards

class Config:
    def __init__(self, torp8=True, max_rounds=10, log=False, harbour_safe=True):
        self.torp8 = torp8; self.max_rounds = max_rounds; self.log = log; self.harbour_safe = harbour_safe

class S:
    """Light state used for both real play and bot look-ahead copies."""
    __slots__ = ("pos", "piles", "grid", "fup", "canc", "bonus", "rev", "sonar", "unrev", "stats", "cfg", "ev", "evp", "log")
    def copy(self):
        c = S.__new__(S)
        c.pos = self.pos[:]; c.piles = [self.piles[0][:], self.piles[1][:]]; c.grid = self.grid[:]; c.fup = self.fup[:]
        c.canc = [False, False]; c.bonus = [0.0, 0.0]; c.rev = [0, 0]; c.sonar = self.sonar[:]
        c.unrev = self.unrev; c.stats = None; c.cfg = self.cfg; c.ev = True; c.evp = self.evp; c.log = None
        return c

def ev_params(s):
    """Public-information expectation for a face-down card: (expected salvage, P(mine), P(sonar))."""
    n = sum(s.unrev.values())
    if n == 0: return (0.0, 0.0, 0.0)
    sal = sum(v * c for v, c in s.unrev.items() if v in (1, 2, 3))
    return (sal / n, s.unrev.get(4, 0) / n, s.unrev.get(6, 0) / n)

def score(s, p): return sum(s.piles[p]) + s.sonar[p]

def _enter(s, p, t, start):
    """Apply the effect of sub p entering square t. Returns True if it bounced."""
    k = s.grid[t]
    if s.ev and not s.fup[t] and t not in HARB:           # face-down card in look-ahead: use expected value
        esal, pm, ps = s.evp
        s.bonus[p] += esal + ps * 1.0
        if pm and s.piles[p]: s.bonus[p] -= pm * min(s.piles[p])
        s.rev[p] += 1; s.grid[t] = 0; s.fup[t] = True
        return False
    if not s.fup[t] and t not in HARB:
        s.fup[t] = True; s.unrev[k] -= 1
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
        deck = COMP[:]; rng.shuffle(deck)
        s = S.__new__(S); s.cfg = cfg
        s.grid = [0] * 25; s.fup = [False] * 25
        order = [y*5+x for y in (4, 3, 2, 1, 0) for x in range(5) if y*5+x not in HARB]
        for i, c in zip(order, deck): s.grid[i] = c
        for h in HARB: s.fup[h] = True
        s.pos = [HARB[0], HARB[1]]; s.piles = [[], []]; s.canc = [False, False]; s.bonus = [0.0, 0.0]
        s.rev = [0, 0]; s.sonar = [0, 0]; s.ev = False; s.evp = None
        s.unrev = {}
        for c in COMP: s.unrev[c] = s.unrev.get(c, 0) + 1
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
            first = 0 if sc[0] < sc[1] else 1 if sc[1] < sc[0] else (0 if rnd % 2 == 1 else 1)
            pinger = None
            for p in (first, 1 - first):
                if s.sonar[p] > 0 and self.bots[p].want_ping(self, p):
                    pinger = p; s.sonar[p] -= 1; s.stats["pings"][p] += 1; break
            plots = [None, None]
            if pinger is not None:
                r = 1 - pinger
                plots[r] = self.bots[r].plot(self, r, hands[r], None)
                plots[pinger] = self.bots[pinger].plot(self, pinger, hands[pinger], plots[r][0])
                self.note("R%d: P%d pings; P%d's step-1 card %s is revealed" % (rnd, pinger + 1, r + 1, plots[r][0]))
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
