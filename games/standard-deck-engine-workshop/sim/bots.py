"""Bots for Fifty-Two Workshop. Interface: action(st,p,builds) -> card|None(gather); gather_pick(st,p)-> bench idx or -1 (deck);
gear_pick(st,p) -> bench idx; pay(st,p,cost) -> list of cards; discard(st,p,k) -> list of cards."""
import random, itertools
from game import *

def subsets_cover(hand, cost):
    """all (cards,total) subsets of hand with total >= cost, minimal-ish (cards <= len)."""
    out = []; idx = range(len(hand))
    for k in range(1, len(hand) + 1):
        for comb in itertools.combinations(idx, k):
            t = sum(rk(hand[i]) for i in comb)
            if t >= cost: out.append(([hand[i] for i in comb], t))
        if out: break          # fewest cards first
    return out

class Random:
    def __init__(self, seed, **kw): self.rng = random.Random(seed * 7919 + 13)
    def action(self, st, p, builds):
        k = self.rng.randrange(len(builds) + 1)
        return None if k == len(builds) else builds[k][0]
    def gather_pick(self, st, p):
        i = self.rng.randrange(len(st.bench) + (1 if st.deck else 0))
        return -1 if i == len(st.bench) else i
    def gear_pick(self, st, p): return self.rng.randrange(len(st.bench))
    def pay(self, st, p, cost):
        hand = st.hands[p][:]; self.rng.shuffle(hand); out = []; t = 0
        for c in hand:
            if t >= cost: break
            out.append(c); t += rk(c)
        return out
    def discard(self, st, p, k): return self.rng.sample(st.hands[p], k)

class Greedy:
    """Best immediate points. Builds if any build adds points; gather takes best immediate-gain cards, else highest rank."""
    def __init__(self, seed, **kw): self.rng = random.Random(seed * 31 + 5)
    def gain(self, st, p, c):
        shop = st.shops[p]
        if rk(c) in shop: return -1
        s2 = dict(shop); s2[rk(c)] = su(c)
        return score_shop(s2, st.cfg.diamond) - score_shop(shop, st.cfg.diamond)
    def action(self, st, p, builds):
        best = max(builds, key=lambda b: (self.gain(st, p, b[0]), -b[1]))
        return best[0] if self.gain(st, p, best[0]) > 0 else None
    def worth(self, st, p, c): return (self.gain(st, p, c), rk(c))
    def gather_pick(self, st, p):
        opts = [(self.worth(st, p, c), i) for i, (c, _) in enumerate(st.bench)]
        if not opts: return -1
        w, i = max(opts); return i if w[0] > 0 or not st.deck else (i if w[1] >= 7 else -1)
    def gear_pick(self, st, p): return max(range(len(st.bench)), key=lambda i: self.worth(st, p, st.bench[i][0]))
    def pay(self, st, p, cost):
        subs = subsets_cover(st.hands[p], cost)
        return min(subs, key=lambda s: (s[1], sum(self.gain(st, p, c) for c in s[0])))[0]
    def discard(self, st, p, k): return sorted(st.hands[p], key=lambda c: self.worth(st, p, c))[:k]

class Strategic:
    """Heuristic from the design notes' bot hints, parameterised so persona bots can reuse it."""
    def __init__(self, seed, thr=2.5, wS=1.5, wC=1.2, wT=0.5, wP=0.3, denial=0.3, clock=True, eps=0.0, heart=0.0, safe=False, money=0.15, **kw):
        self.rng = random.Random(seed * 101 + 7)
        self.thr, self.wS, self.wC, self.wT, self.wP, self.denial, self.clock, self.eps, self.heart, self.safe, self.money = thr, wS, wC, wT, wP, denial, clock, eps, heart, safe, money
    def bval(self, st, p, c, shop=None):
        """value of building card c into shop of player p (ignores payment)."""
        shop = st.shops[p] if shop is None else shop; r = rk(c)
        if r in shop: return None
        s2 = dict(shop); s2[r] = su(c); dia = st.cfg.diamond
        gain = score_shop(s2, dia) - score_shop(shop, dia)
        tl = len(train_of(shop, r)); v = gain + self.wT * (tl - 1)
        if tl >= 2:
            if su(c) == S: v += self.wS
            elif su(c) == C: v += self.wC
        if su(c) == H and tl >= 2: v += self.heart
        return v
    def hold(self, st, p, c, check_rivals=True):
        b = self.bval(st, p, c); v = self.money * rk(c)
        if b is not None:
            v += max(0.0, b) * 0.6 - (0.4 if rk(c) > 9 else 0)
            if c in st.hands[p] or any(rk(x) == rk(c) for x in st.hands[p]): v -= 1.0
        if check_rivals and self.denial and st.n > 1:
            for q in range(st.n):
                if q != p:
                    bq = self.bval(st, q, c)
                    if bq is not None and bq > 3: v += self.denial * (bq - 3)
        return v
    def pcards(self, st, p, c, cost):
        h = sorted((rk(x) for x in st.hands[p] if x != c), reverse=True); t = n = 0
        for x in h:
            if t >= cost: break
            t += x; n += 1
        return n
    def action(self, st, p, builds):
        if self.eps and self.rng.random() < self.eps:
            k = self.rng.randrange(len(builds) + 1); return None if k == len(builds) else builds[k][0]
        scored = []
        for c, cost in builds:
            v = self.bval(st, p, c) - self.wP * self.pcards(st, p, c, cost)
            if self.safe: v -= 0.25 * cost
            if self.clock and len(st.shops[p]) + 1 >= st.cfg.target and st.n > 1:
                mine = score_shop({**st.shops[p], rk(c): su(c)}, st.cfg.diamond)
                opp = max(score_shop(st.shops[q], st.cfg.diamond) for q in range(st.n) if q != p)
                if mine < opp - 2: v -= 3
            scored.append((v, c))
        v, c = max(scored)
        thr = self.thr if len(st.hands[p]) < st.cfg.hand_limit - 1 else -9   # a full hand makes Gathering pointless: build the best card
        return c if v > thr else None
    def gather_pick(self, st, p):
        opts = [(self.hold(st, p, c), i) for i, (c, _) in enumerate(st.bench)]
        if self.eps and self.rng.random() < self.eps:
            return self.rng.randrange(len(opts) + 1) - 1 if st.deck else self.rng.randrange(len(opts))
        if not opts: return -1
        v, i = max(opts)
        return i if v > 1.0 or not st.deck else -1
    def gear_pick(self, st, p):
        return max(range(len(st.bench)), key=lambda i: self.hold(st, p, st.bench[i][0]))
    def pay(self, st, p, cost):
        hand = st.hands[p]; subs = subsets_cover(hand, cost)
        return min(subs, key=lambda s: (len(s[0]), s[1], sum(self.hold(st, p, c, False) for c in s[0])))[0]
    def discard(self, st, p, k): return sorted(st.hands[p], key=lambda c: self.hold(st, p, c, False))[:k]

class Rush(Strategic):
    """Clock rusher: always builds the cheapest legal build, gathers cheap unbuilt ranks (prefers Spades)."""
    def action(self, st, p, builds):
        return min(builds, key=lambda b: (b[1], su(b[0]) not in (S, D), rk(b[0])))[0]
    def hold(self, st, p, c, check_rivals=True):
        r = rk(c)
        if r in st.shops[p] or any(rk(x) == r for x in st.hands[p]): return 0.1 * r
        return 6 - 0.3 * r + (0.8 if su(c) == S else 0.3 if su(c) == D else 0)
    def gather_pick(self, st, p):
        opts = [(self.hold(st, p, c), i) for i, (c, _) in enumerate(st.bench)]
        if not opts: return -1
        v, i = max(opts); return i if v > 2.5 or not st.deck else -1
    def pay(self, st, p, cost):
        subs = subsets_cover(st.hands[p], cost)
        return min(subs, key=lambda s: (len(s[0]), s[1]))[0]

# Persona bots (panel/personas/*.md, "How they play")
class Planner(Strategic):      # strategist: engine first, long game, denies rivals
    def __init__(self, seed, **kw): super().__init__(seed, thr=2.0, wS=2.2, wC=1.8, wT=0.8, denial=0.5, heart=0.8)
class Instinct(Strategic):     # casual: decent gut feel, noisy
    def __init__(self, seed, **kw): super().__init__(seed, thr=2.3, denial=0.0, clock=False, eps=0.25)
class Optimiser(Strategic):    # competitor: strongest line, denial and clock timing
    def __init__(self, seed, **kw): super().__init__(seed, thr=2.3, wS=1.8, wC=1.4, wT=0.6, denial=0.8, heart=0.5)
class Flavour(Strategic):      # story: long mixed trains, hearts and gears for drama, even if a little worse
    def __init__(self, seed, **kw): super().__init__(seed, thr=1.8, wS=0.8, wC=2.0, wT=1.6, wP=0.1, denial=0.0, heart=2.0, clock=False)
class Cautious(Strategic):     # family: cheap safe builds, simple, never fancy
    def __init__(self, seed, **kw): super().__init__(seed, thr=1.5, wS=0.5, wC=0.5, wT=0.2, denial=0.0, clock=False, eps=0.1, safe=True, money=0.1)
class Expert(Optimiser):       # barraiser: optimiser that also takes the rush line when it is ahead on tempo
    def __init__(self, seed, **kw): super().__init__(seed)
    def action(self, st, p, builds):
        mine = len(st.shops[p]); opp = max(len(st.shops[q]) for q in range(st.n) if q != p) if st.n > 1 else 0
        if mine >= opp + 2: return Rush.action(self, st, p, builds)
        return super().action(st, p, builds)

ALL = {"random": Random, "greedy": Greedy, "strategic": Strategic}
EXTRA = {"rush": Rush}
PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}
