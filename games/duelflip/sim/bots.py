import random

def pv(st): return sum(v for _, v in st.pile)

def clash_p(st):
    if not st.deck: return 0.0
    rv = st.river_values()
    return sum(1 for _, v in st.deck if v in rv) / len(st.deck)

def species_counts(st, p, s):
    return (sum(1 for x, _ in st.haul[p] if x == s), sum(1 for x, _ in st.haul[1 - p] if x == s))

class Base:
    name = "base"
    leave_mode = "low"
    def __init__(self, seed=0, leave_mode=None):
        self.rng = random.Random(seed)
        if leave_mode: self.leave_mode = leave_mode
    def keep_flipping(self, st, p): return False
    def on_clash(self, st, p, card, hit_bait): return "buoy"
    def leave(self, st, p, cands):
        m = self.leave_mode; r = st.river
        if m == "low": return min(cands, key=lambda i: r[i][1])
        if m == "high": return max(cands, key=lambda i: r[i][1])
        if m == "rand": return self.rng.choice(cands)
        if m == "bait":   # most remaining copies in deck, tie lowest
            return max(cands, key=lambda i: (st.deck_count(r[i][1]), -r[i][1]))
        if m == "species":  # leave the card that helps the opponent's majority least
            def key(i):
                s, v = r[i]; a, b = species_counts(st, p, s)
                return (b + 1 > a) * 8 + v      # penalty if giving opp the card could swing species
            return min(cands, key=key)
        if m == "smart": return self.smart_leave(st, p, cands)
        raise ValueError(m)
    def smart_leave(self, st, p, cands):
        r = st.river; n = len(st.deck) or 1
        best, bi = -1e9, cands[0]
        for i in cands:
            s, v = r[i]
            a, b = species_counts(st, p, s)
            q = st.deck_count(v) / n
            # opp must flip 2+ cards: chance of hitting this value at least once ~ 1-(1-q)^2.  If so, I regain v + their pile.
            hit = 1 - (1 - q) ** 2
            cost = v
            if b + 1 > a >= b: cost += st.cfg.bonus * 0.6     # gifting opp a lead (or tie-break) in species
            elif b + 1 == a: cost += st.cfg.bonus * 0.3
            sc = -(1 - hit) * cost + hit * (v + 6)
            if sc > best: best, bi = sc, i
        return bi

class Random(Base):
    name = "random"; leave_mode = "rand"
    def keep_flipping(self, st, p): return self.rng.random() < 0.5
    def on_clash(self, st, p, card, hit_bait): return "buoy" if self.rng.random() < 0.5 else "bust"

class Greedy(Base):
    """Best immediate gain: flip until pile value >= 12, buoy whenever pile nonempty, leave lowest."""
    name = "greedy"
    def keep_flipping(self, st, p): return pv(st) < 12

class BankEarly(Base):
    """Timid: flip exactly the 2 mandatory cards, buoy on clash, leave lowest."""
    name = "bank_early"

class Pusher(Base):
    name = "pusher"
    def __init__(self, seed=0, target=20, leave_mode=None):
        super().__init__(seed, leave_mode); self.target = target
    def keep_flipping(self, st, p): return pv(st) < self.target
    def on_clash(self, st, p, card, hit_bait): return "buoy" if pv(st) >= 8 else "bust"

class RefundPusher(Base):
    """Aims to reach 4 cards in pile (refund), then banks."""
    name = "refund_pusher"
    def keep_flipping(self, st, p): return len(st.pile) < st.cfg.refund_at
    def on_clash(self, st, p, card, hit_bait): return "buoy" if pv(st) >= 6 else "bust"

class Hoarder(Base):
    """Never spends the Lifebuoy voluntarily (always busts) - tests whether holding matters."""
    name = "hoarder"
    def keep_flipping(self, st, p): return pv(st) < 12
    def on_clash(self, st, p, card, hit_bait): return "bust"

class Collector(Base):
    name = "collector"; leave_mode = "species"
    def keep_flipping(self, st, p): return len(st.pile) < 3
    def on_clash(self, st, p, card, hit_bait): return "buoy" if pv(st) >= 6 else "bust"

class Strategic(Base):
    """EV flip rule that accounts for buoy and refund; smart leave (bait + species)."""
    name = "strategic"; leave_mode = "smart"
    def __init__(self, seed=0, risk=1.0, buoy_min=9, leave_mode=None):
        super().__init__(seed, leave_mode); self.risk = risk; self.buoy_min = buoy_min
    def keep_flipping(self, st, p):
        if not st.deck: return False
        pc = clash_p(st); n = len(st.deck)
        avg = sum(v for _, v in st.deck) / n
        have = pv(st)
        if st.buoys[p] > 0:
            loss = 6 + 0.25 * have          # buoy cost, discounted by refund chance
            if len(st.pile) == st.cfg.refund_at - 1: loss -= 4
        else:
            loss = (2 * have + 3) * self.risk
        bonus_refund = 3 if (st.buoys[p] == 0 and len(st.pile) == st.cfg.refund_at - 1) else 0
        return (1 - pc) * (avg * 0.8 + bonus_refund) > pc * loss
    def on_clash(self, st, p, card, hit_bait):
        return "buoy" if pv(st) >= self.buoy_min else "bust"

ALL = {"random": Random, "greedy": Greedy, "bank_early": BankEarly, "pusher": Pusher,
       "refund_pusher": RefundPusher, "hoarder": Hoarder, "collector": Collector, "strategic": Strategic}
