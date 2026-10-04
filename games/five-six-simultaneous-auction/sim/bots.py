"""Bots for Last Bid Standing. bid(st,p) -> index into st.hands[p] or None (pass); pick(st,p,lots) -> lot index."""
import random
from game import CATS

# P(my value v is first / second standing) vs m rivals who each bid with prob q, value uniform 1..10 (precomputed by simulation)
_T = {}
def _table():
    if _T: return _T
    rng = random.Random(99)
    for m in (4, 5):
        for qi, q in enumerate((0.3, 0.5, 0.7, 0.9)):
            for v in range(1, 11):
                a = b = 0; N = 400
                for _ in range(N):
                    vals = [rng.randint(1, 10) for _ in range(m) if rng.random() < q]
                    if v in vals: continue
                    from collections import Counter
                    c = Counter(vals); un = sorted([x for x in vals if c[x] == 1], reverse=True)
                    higher = sum(1 for x in un if x > v)
                    if higher == 0: a += 1
                    elif higher == 1: b += 1
                _T[(m, qi, v)] = (a / N, b / N)
    return _T

def unseen_counts(st, p):
    cnt = [0] + [CATS * 0 + 4] * 10 if st.cfg.bid_max == 10 else None
    cnt = [0] + [CATS] * st.cfg.bid_max
    for row in st.hype:
        for c, v in row: cnt[v] -= 1
    for c, v in st.discard: cnt[v] -= 1
    for c, v in st.hands[p]: cnt[v] -= 1
    return cnt

class Random:
    name = "random"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def bid(self, st, p):
        i = self.rng.randrange(len(st.hands[p]) + 1)
        return None if i == len(st.hands[p]) else i
    def pick(self, st, p, lots): return self.rng.randrange(2)

class Greedy:
    """Always plays its highest bid card (best immediate chance at a lot); takes the higher printed value lot."""
    name = "greedy"
    def __init__(self, seed=0): pass
    def bid(self, st, p):
        h = st.hands[p]; return max(range(len(h)), key=lambda i: h[i][1])
    def pick(self, st, p, lots): return 0 if lots[0][1] >= lots[1][1] else 1

class Strategic:
    """Hint bot from rules.md: EV of each card vs passing, with projected-crash awareness."""
    name = "strategic"
    cardval = 0.5; noise = 0.0; est_rate = 0.4; saboteur = False; exact = False; spec = 0.0; fav = None
    def __init__(self, seed=0, **kw):
        self.rng = random.Random(seed); self.__dict__.update(kw)
    def est(self, st):
        rl = st.cfg.rounds - st.round
        e = [len(r) + rl * self.est_rate for r in st.hype]; m = max(e)
        return e, {c for c in range(CATS) if e[c] == m}
    def worth(self, st, p, lot, e, top, pref=True):
        c, v = lot
        w = v + (0 if c in top else e[c])
        if self.fav is not None and c == self.fav: w += self.spec
        return w
    def mine(self, st, p, c): return sum(1 for l in st.won[p] if l[0] == c)
    def rivals(self, st, p, c): return sum(1 for q in range(st.n) if q != p for l in st.won[q] if l[0] == c)
    def bid(self, st, p):
        h = st.hands[p]
        e, top = self.est(st)
        ws = sorted((self.worth(st, p, l, e, top) for l in st.block), reverse=True)
        T = _table(); m = st.n - 1
        avg = sum(len(st.hands[q]) for q in range(st.n) if q != p) / m
        qi = 0 if avg < 1 else 1 if avg < 2 else 2 if avg < 3.5 else 3
        pass_val = self.cardval
        best, besti = pass_val, None
        late = st.cfg.rounds - st.round
        for i, (c, v) in enumerate(h):
            p1, p2 = T[(m, qi, max(1, min(10, round(v * 10 / st.cfg.bid_max))))]
            if self.exact:   # use true unseen distribution for rivals' bids
                p1, p2 = self.exact_probs(st, p, v, qi)
            burn_val = 0.0 if c in top else self.mine(st, p, c) - 0.5 * self.rivals(st, p, c)
            if self.saboteur and late <= 2 and c in top and False: pass
            if self.saboteur and late <= 3:
                # push a rival leader's category over the top / or the crash target away from me
                burn_val += self.sab(st, p, c, e, top)
            val = p1 * ws[0] + p2 * ws[1] + (1 - p1 - p2) * burn_val - self.cardval * (0.6 + 0.08 * v)
            val += self.rng.gauss(0, self.noise) if self.noise else 0
            if val > best: best, besti = val, i
        return besti
    def sab(self, st, p, c, e, top):
        sc, _ = st.scores(); lead = max(range(st.n), key=lambda q: sc[q] if q != p else -1)
        return 0.5 * (self.mine(st, lead, c) * (1 if c in top else 0.2)) * 0.0 + (0.0)
    def exact_probs(self, st, p, v, qi):
        cnt = unseen_counts(st, p); tot = sum(cnt) or 1
        q = (0.3, 0.5, 0.7, 0.9)[qi]; m = st.n - 1; rng = self.rng
        a = b = 0; N = 20
        for _ in range(N):
            vals = []
            for _ in range(m):
                if rng.random() < q:
                    r = rng.random() * tot; acc = 0
                    for x in range(1, len(cnt)):
                        acc += cnt[x]
                        if r <= acc: vals.append(x); break
            if v in vals: continue
            from collections import Counter
            c = Counter(vals); un = [x for x in vals if c[x] == 1]
            higher = sum(1 for x in un if x > v)
            if higher == 0: a += 1
            elif higher == 1: b += 1
        return a / N, b / N
    def pick(self, st, p, lots):
        e, top = self.est(st)
        w = [self.worth(st, p, l, e, top) for l in lots]
        return 0 if w[0] >= w[1] else 1

# ---- persona bots -----------------------------------------------------------
class Planner(Strategic):         # strategist: patient banker, cares about the long game
    name = "planner"; cardval = 1.15; est_rate = 0.5
class Instinct(Strategic):        # casual: gut feel, noisy, never counts cards
    name = "instinct"; noise = 1.2; cardval = 0.8
    def bid(self, st, p):
        h = st.hands[p]
        if self.rng.random() < 0.25 and h:         # just throws a card because it looks fun
            return self.rng.randrange(len(h))
        return super().bid(st, p)
class Optimiser(Strategic):       # competitor: true-odds bot
    name = "optimiser"; exact = True; cardval = 1.0; est_rate = 0.45
class Expert(Optimiser):          # barraiser: probes exploits; leans on low cards cheaply (no extra tricks beyond optimiser)
    name = "expert"; cardval = 1.0
class Flavour(Strategic):         # story: picks a favourite category and goes big on it, even into a crash
    name = "flavour"; spec = 2.0
    def __init__(self, seed=0, **kw):
        super().__init__(seed, **kw); self.fav = self.rng.randrange(CATS); self.noise = 0.6
    def est(self, st):
        e, top = super().est(st); return e, set()      # romantically ignores the crash
    def bid(self, st, p):
        h = st.hands[p]
        if not h: return None
        if self.rng.random() < 0.3:                    # dramatic: throw the biggest card of the favourite category
            fav = [i for i, (c, v) in enumerate(h) if c == self.fav]
            if fav: return max(fav, key=lambda i: h[i][1])
        return super().bid(st, p)
class Cautious(Strategic):        # family: safe, keeps a couple of cards, bids mid
    name = "cautious"; cardval = 1.4; noise = 0.5
    def bid(self, st, p):
        h = st.hands[p]
        if len(h) <= 2: return None
        i = super().bid(st, p)
        if i is not None and h[i][1] >= 9:            # does not like risking the big cards on a tie
            mids = [j for j, (c, v) in enumerate(h) if 4 <= v <= 8]
            if mids: return self.rng.choice(mids)
        return i

STANDARD = {"random": Random, "greedy": Greedy, "strategic": Strategic}
PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour,
           "family": Cautious, "barraiser": Expert}
