"""Bots for Last Bid Standing. bid(st,p) -> index into st.hands[p] or None (pass); pick(st,p,lots) -> lot index."""
import random
from game import CATS

ALL = None
def _all(st):
    return [(c, v) for c in range(CATS) for v in range(1, st.cfg.bid_max + 1)]

class Random:
    name = "random"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def bid(self, st, p):
        i = self.rng.randrange(len(st.hands[p]) + 1)
        return None if i == len(st.hands[p]) else i
    def pick(self, st, p, lots): return self.rng.randrange(len(lots))

class Greedy:
    """Always plays its highest bid card (best immediate chance at a lot); takes the highest printed value lot."""
    name = "greedy"
    def __init__(self, seed=0): pass
    def bid(self, st, p):
        h = st.hands[p]; return max(range(len(h)), key=lambda i: h[i][1])
    def pick(self, st, p, lots): return max(range(len(lots)), key=lambda i: lots[i][1])

class Strategic:
    """Rules v2 hint bot: Monte-Carlo estimate of standing first/second vs passing/burning, crash-aware.
    Flags (used for the ablation bots): memory (tracks shown income), hype (values Hype), crash (projects the crash),
    ties (models cancellation of equal bids)."""
    name = "strategic"
    cardval = 0.8; noise = 0.0; est_rate = 0.45; M = 16
    memory = True; hype = True; crash = True; ties = True; cap = True
    spec = 0.0; fav = None
    def __init__(self, seed=0, **kw):
        self.rng = random.Random(seed); self.__dict__.update(kw)
    # --- crash / worth -------------------------------------------------
    def est(self, st):
        rl = st.cfg.rounds - st.round
        e = [len(r) + rl * self.est_rate for r in st.hype]
        if not self.hype: return [0.0] * CATS, set()
        key = lambda c: (e[c], sum(v for _, v in st.hype[c]), -c)
        top = {max(range(CATS), key=key)} if self.crash else set()
        if self.cap: e = [min(x, 4.0) for x in e]
        return e, top
    def worth(self, st, p, lot, e, top):
        c, v = lot
        w = v + (0 if c in top else e[c])
        if self.fav is not None and c == self.fav: w += self.spec
        return w
    def mine(self, st, p, c): return sum(1 for l in st.won[p] if l[0] == c)
    def rivals(self, st, p, c): return sum(1 for q in range(st.n) if q != p for l in st.won[q] if l[0] == c) / max(1, st.n - 1)
    # --- rival model -----------------------------------------------------
    def sample_rivals(self, st, p):
        """Return list of value-lists per sample: values rivals bid this round."""
        rng = self.rng
        gone = {c for c in st.hands[p]}
        for row in st.hype: gone.update(row)
        gone.update(st.discard)
        rk = {}
        for q in range(st.n):
            if q == p: continue
            if self.memory: rk[q] = list(st.known[q]); gone.update(st.known[q])
            else: rk[q] = []
        pool = [c for c in _all(st) if c not in gone]
        need = {q: len(st.hands[q]) - len(rk[q]) for q in rk}
        tot = sum(need.values())
        out = []
        for _ in range(self.M):
            draw = rng.sample(pool, min(tot, len(pool))); k = 0; vals = []
            for q in rk:
                cards = rk[q] + draw[k:k + need[q]]; k += need[q]
                if not cards: continue
                if rng.random() < min(0.92, 0.35 + 0.15 * len(cards)):
                    ws = [c[1] ** 2 for c in cards]
                    vals.append(rng.choices(cards, ws)[0][1])
            out.append(vals)
        return out
    def odds(self, st, p, samples, v):
        a = b = 0
        for vals in samples:
            if self.ties:
                if v in vals: continue
                cnt = {}
                for x in vals: cnt[x] = cnt.get(x, 0) + 1
                higher = sum(1 for x in vals if x > v and cnt[x] == 1)
            else:
                higher = sum(1 for x in vals if x >= v)
            if higher == 0: a += 1
            elif higher == 1: b += 1
        n = len(samples); return a / n, b / n
    def passval(self, st):
        left = st.cfg.rounds - st.round
        return 2 * self.cardval * min(1.0, left / 5.0)
    def costof(self, st, v):
        left = st.cfg.rounds - st.round
        return self.cardval * (0.6 + 0.08 * v) * min(1.0, left / 5.0)
    def bid(self, st, p):
        h = st.hands[p]
        e, top = self.est(st)
        ws = sorted((self.worth(st, p, l, e, top) for l in st.block), reverse=True)
        ws += [0.0, 0.0]
        samples = self.sample_rivals(st, p)
        best, besti = self.passval(st), None
        for i, (c, v) in enumerate(h):
            p1, p2 = self.odds(st, p, samples, v)
            burn_val = 0.0
            if self.hype and c not in top:
                full = self.cap and (len(st.hype[c]) >= 4)
                if full: burn_val = 0.5 * (self.rivals(st, p, c) - self.mine(st, p, c))   # crash pressure only
                else: burn_val = self.mine(st, p, c) - 0.7 * self.rivals(st, p, c)
            val = p1 * ws[0] + p2 * ws[1] + (1 - p1 - p2) * burn_val - self.costof(st, v)
            if self.noise: val += self.rng.gauss(0, self.noise)
            if val > best: best, besti = val, i
        return besti
    def pick(self, st, p, lots):
        e, top = self.est(st)
        w = [self.worth(st, p, l, e, top) for l in lots]
        return max(range(len(lots)), key=lambda i: w[i])

# --- ablation bots (designer's four) ---------------------------------------
class IgnoreHype(Strategic):  name = "ignore-hype"; hype = False
class IgnoreCrash(Strategic): name = "ignore-crash"; crash = False
class IgnoreTies(Strategic):  name = "ignore-ties"; ties = False
class IgnoreCap(Strategic):   name = "ignore-cap"; cap = False
class Lite(Strategic):         # weaker reference: few samples, cruder valuation
    name = "lite"; M = 5; cardval = 0.6; est_rate = 0.3; noise = 0.3
class NoMemory(Strategic):    name = "no-memory"; memory = False

# --- persona bots -----------------------------------------------------------
class Planner(Strategic):         # strategist: patient banker, tracks cards, plays the long game
    name = "planner"; cardval = 1.0; est_rate = 0.5; M = 24
class Instinct(Strategic):        # casual: gut feel, noisy, never counts cards
    name = "instinct"; noise = 0.8; cardval = 0.6; memory = False
    def bid(self, st, p):
        h = st.hands[p]
        if self.rng.random() < 0.25 and h:         # just throws a card because it looks fun
            return self.rng.randrange(len(h))
        return super().bid(st, p)
class Optimiser(Strategic):       # competitor: true-odds bot, more samples
    name = "optimiser"; M = 32; cardval = 0.8
class Expert(Optimiser):          # barraiser: same as optimiser
    name = "expert"
class Flavour(Strategic):         # story: picks a favourite category and goes big on it, even into a crash
    name = "flavour"; spec = 2.0; memory = False; crash = False
    def __init__(self, seed=0, **kw):
        super().__init__(seed, **kw); self.fav = self.rng.randrange(CATS); self.noise = 0.5
    def bid(self, st, p):
        h = st.hands[p]
        if not h: return None
        if self.rng.random() < 0.3:                    # dramatic: throw the biggest card of the favourite category
            fav = [i for i, (c, v) in enumerate(h) if c == self.fav]
            if fav: return max(fav, key=lambda i: h[i][1])
        return super().bid(st, p)
class Cautious(Strategic):        # family: safe, keeps a couple of cards, bids mid
    name = "cautious"; cardval = 0.8; noise = 0.4; memory = False
    def bid(self, st, p):
        h = st.hands[p]
        if len(h) <= 2: return None
        i = super().bid(st, p)
        if i is not None and h[i][1] >= 10:           # does not like risking the big cards on a tie
            mids = [j for j, (c, v) in enumerate(h) if 4 <= v <= 9]
            if mids: return self.rng.choice(mids)
        return i

class PIgnoreHype(Planner): name = "p-ignore-hype"; hype = False
class PIgnoreCrash(Planner): name = "p-ignore-crash"; crash = False
class PIgnoreTies(Planner): name = "p-ignore-ties"; ties = False
class PIgnoreCap(Planner): name = "p-ignore-cap"; cap = False
STANDARD = {"random": Random, "greedy": Greedy, "strategic": Strategic}
PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour,
           "family": Cautious, "barraiser": Expert}
