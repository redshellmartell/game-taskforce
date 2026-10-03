import random

class Base:
    name = "base"
    def __init__(self, seed=0):
        self.rng = random.Random(seed)
    def keep_flipping(self, st, p): return False
    def use_buoy(self, st, p, card): return True
    def leave(self, st, p): return 0

def clash_p(st):
    rv = st.river_values()
    if not st.deck: return 0.0
    return sum(1 for _, v in st.deck if v in rv) / len(st.deck)

class Random(Base):
    name = "random"
    def keep_flipping(self, st, p): return self.rng.random() < 0.5
    def use_buoy(self, st, p, card): return self.rng.random() < 0.5
    def leave(self, st, p): return self.rng.randrange(len(st.river))

class Greedy(Base):
    """Best immediate gain: keep flipping while pile < 12; take everything but the lowest card;
    use buoy whenever pile is nonempty."""
    name = "greedy"
    def keep_flipping(self, st, p):
        return sum(v for _, v in st.pile) < 12
    def use_buoy(self, st, p, card):
        return sum(v for _, v in st.pile) > 0
    def leave(self, st, p):
        return min(range(len(st.river)), key=lambda i: st.river[i][1])

class BankEarly(Base):
    """Always flip exactly one card; buoy only if pile nonempty (never needed); leave lowest-value card."""
    name = "bank_early"
    def keep_flipping(self, st, p): return False
    def use_buoy(self, st, p, card): return False  # hoard buoys for end bonus
    def leave(self, st, p):
        return min(range(len(st.river)), key=lambda i: st.river[i][1])

class BankEarlyBait(BankEarly):
    """Bank early, leave the card whose value has most remaining copies in deck (max opp clash), tie lowest value."""
    name = "bank_early_bait"
    def leave(self, st, p):
        return max(range(len(st.river)),
                   key=lambda i: (st.deck_count(st.river[i][1]) * 3 - st.river[i][1]))

class Strategic(Base):
    """EV-based pusher: flip when gain EV > loss EV. Buoy if pile value >= buoy_thresh.
    Leave card by value-vs-bait tradeoff; species-aware."""
    name = "strategic"
    def __init__(self, seed=0, risk=1.0, buoy_thresh=10, bait_w=1.0):
        super().__init__(seed); self.risk = risk; self.buoy_thresh = buoy_thresh; self.bait_w = bait_w
    def keep_flipping(self, st, p):
        pv = sum(v for _, v in st.pile)
        pc = clash_p(st)
        if not st.deck: return False
        avg = sum(v for _, v in st.deck) / len(st.deck)
        buoy_save = 0.0
        if st.buoys[p] > 0:
            buoy_save = st.cfg.buoy_value  # cost of spending
            loss = min(pv, 0) + buoy_save + 0.0
            # with buoy a clash is cheap; but we may prefer to hold it
            loss = buoy_save + 0.3 * pv
        else:
            loss = pv * 2 * self.risk  # lose pile and opp gains it (swing 2x)
        return (1 - pc) * avg * 0.9 > pc * loss
    def use_buoy(self, st, p, card):
        pv = sum(v for _, v in st.pile)
        return pv * 2 >= self.buoy_thresh + st.cfg.buoy_value
    def species_need(self, st, p, s):
        a = sum(1 for x, _ in st.haul[p] if x == s)
        b = sum(1 for x, _ in st.haul[1 - p] if x == s)
        return a, b
    def leave(self, st, p):
        best, bi = -1e9, 0
        for i, (s, v) in enumerate(st.river):
            gain = 0.0
            for j, (s2, v2) in enumerate(st.river):
                if j == i: continue
                a, b = self.species_need(st, p, s2)
                gain += v2 + (st.cfg.bonus * 0.25 if a <= b + 1 else 0)
            # bait: leaving value v with many copies left raises opponent clash chance;
            # leaving a high card tempts them but costs us nothing extra (they must flip over it)
            n = len(st.deck) or 1
            oppclash = st.deck_count(v) / n
            sc = gain + self.bait_w * oppclash * 12 - 0.0 * v
            # card left is potentially taken by opponent
            sc -= 0.5 * v * (1 - oppclash)
            if sc > best: best, bi = sc, i
        return bi

class Pusher(Base):
    """Greedy pusher: flip until pile value >= target, uses buoy when pile >= 8."""
    name = "pusher"
    def __init__(self, seed=0, target=20):
        super().__init__(seed); self.target = target
    def keep_flipping(self, st, p):
        return sum(v for _, v in st.pile) < self.target
    def use_buoy(self, st, p, card):
        return sum(v for _, v in st.pile) >= 8
    def leave(self, st, p):
        return min(range(len(st.river)), key=lambda i: st.river[i][1])

class Collector(Base):
    """Species majority chaser: banks early-ish (2 flips), leaves cards of species it doesn't want."""
    name = "collector"
    def keep_flipping(self, st, p): return len(st.pile) < 2
    def use_buoy(self, st, p, card): return False
    def leave(self, st, p):
        def key(i):
            s, v = st.river[i]
            a = sum(1 for x, _ in st.haul[p] if x == s)
            b = sum(1 for x, _ in st.haul[1 - p] if x == s)
            return (a - b) * 3 + v  # leave cards least useful to me
        return min(range(len(st.river)), key=key)

ALL = {"random": Random, "greedy": Greedy, "bank_early": BankEarly, "bank_early_bait": BankEarlyBait,
       "strategic": Strategic, "pusher": Pusher, "collector": Collector}
