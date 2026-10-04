import random

def pv(st): return sum(v for _, v in st.pile)

def bait_val(st): return st.bait[1] if st.bait else 0

def stop_value(st, total):
    """Swing for banking a pile worth `total` (one card is left behind at ~15% cost). Bait: claimed +b, else -b."""
    b = bait_val(st)
    return total * 0.85 + ((b if total > b + st.cfg.extra else -b) if st.bait else 0)

def clash_p(st):
    if not st.deck: return 0.0
    rv = st.river_values()
    return sum(1 for _, v in st.deck if v in rv) / len(st.deck)

def claim_prob(st, p, c, samples=30, rng=None):
    """Chance the opponent's next-turn pile beats a bait of value c (they flip 2, and push to 3 or 4 if short)."""
    rng = rng or random.Random(c * 7 + len(st.deck))
    cards = [v for _, v in st.deck if v != c]
    if len(cards) < 3: return 0.5
    ok = 0; bust = 0
    for _ in range(samples):
        pile = []; seen = {c}
        for _ in range(4):
            x = rng.choice(cards)
            if x in seen:
                if pile: bust += 1; pile = None
                break
            seen.add(x); pile.append(x)
            if len(pile) >= 2 and sum(pile) > c + st.cfg.extra: break
        if pile and sum(pile) > c + st.cfg.extra: ok += 1
    return ok / samples

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
        if m == "smart": return self.smart_leave(st, p, cands)
        raise ValueError(m)
    def smart_leave(self, st, p, cands):
        """Leave c to minimise expected swing: opponent claims with prob q (they gain c, I lose it), else c returns to me."""
        r = st.river; best, bi = -1e9, cands[0]
        tot = sum(x[1] for x in r)
        for i in cands:
            c = r[i][1]
            q = claim_prob(st, p, c, rng=self.rng)
            sc = (tot - c) + c * (1 - q) - c * q
            if sc > best: best, bi = sc, i
        return bi

class Random(Base):
    name = "random"; leave_mode = "rand"
    def keep_flipping(self, st, p): return self.rng.random() < 0.5
    def on_clash(self, st, p, card, hit_bait): return "buoy" if self.rng.random() < 0.5 else "bust"

class Greedy(Base):
    """Best immediate gain: flip until pile value >= 12, Lifebuoy on any clash, leave lowest."""
    name = "greedy"
    def keep_flipping(self, st, p): return pv(st) < 12

class BankEarly(Base):
    """Timid: the 2 mandatory flips, Lifebuoy on clash, leave lowest."""
    name = "bank_early"

class Pusher(Base):
    name = "pusher"
    def __init__(self, seed=0, target=20, leave_mode=None):
        super().__init__(seed, leave_mode); self.target = target
    def keep_flipping(self, st, p): return pv(st) < self.target
    def on_clash(self, st, p, card, hit_bait): return "buoy" if pv(st) >= 8 else "bust"

class Hoarder(Base):
    """Never spends the Lifebuoy voluntarily."""
    name = "hoarder"
    def keep_flipping(self, st, p): return pv(st) < 12
    def on_clash(self, st, p, card, hit_bait): return "bust"

class Strategic(Base):
    """One-step EV flip rule that knows the bait hurdle and the cost of busting (pile + bait); smart bait leave."""
    name = "strategic"; leave_mode = "smart"
    def __init__(self, seed=0, risk=1.0, buoy_min=9, leave_mode=None):
        super().__init__(seed, leave_mode); self.risk = risk; self.buoy_min = buoy_min
    def keep_flipping(self, st, p):
        if not st.deck: return False
        have = pv(st); b = bait_val(st); rv = st.river_values(); n = len(st.deck)
        stop = stop_value(st, have)
        ev = 0.0
        for _, v in st.deck:
            if v in rv: ev += (stop - 3) if st.buoys[p] > 0 else -(have + b) * self.risk
            else: ev += stop_value(st, have + v)
        return ev / n > stop
    def on_clash(self, st, p, card, hit_bait):
        return "buoy" if stop_value(st, pv(st)) + pv(st) + bait_val(st) >= self.buoy_min else "bust"

ALL = {"random": Random, "greedy": Greedy, "bank_early": BankEarly, "pusher": Pusher,
       "hoarder": Hoarder, "strategic": Strategic}


# ---- Persona bots (test panel, see panel/personas/*.md "How they play") ----
class Planner(Strategic):
    """Strategist: plays the long game. Careful flips, leaves the card with the lowest expected cost."""
    name = "planner"; leave_mode = "smart"
    def __init__(self, seed=0, leave_mode=None):
        super().__init__(seed, risk=1.2, buoy_min=9, leave_mode=leave_mode)

class Optimiser(Strategic):
    """Competitor: the strongest line the studio has found (EV flips, smart bait leave)."""
    name = "optimiser"

class Instinct(Greedy):
    """Casual: gut feel. A decent rule of thumb, but one choice in four is a coin flip."""
    name = "instinct"; leave_mode = "rand"
    def keep_flipping(self, st, p):
        return self.rng.random() < 0.5 if self.rng.random() < 0.25 else pv(st) < 12
    def on_clash(self, st, p, card, hit_bait):
        return ("buoy" if self.rng.random() < 0.5 else "bust") if self.rng.random() < 0.25 else "buoy"

class Flavour(Base):
    """Story lover: presses on for the dramatic big pile, spends the Lifebuoy only on a big pile, often leaves a high card."""
    name = "flavour"
    def keep_flipping(self, st, p): return pv(st) < 18
    def on_clash(self, st, p, card, hit_bait): return "buoy" if pv(st) >= 12 else "bust"
    def leave(self, st, p, cands):
        r = st.river
        return max(cands, key=lambda i: r[i][1]) if self.rng.random() < 0.5 else min(cands, key=lambda i: r[i][1])

class Cautious(Base):
    """Family: banks early, always takes the safe Lifebuoy, sometimes leaves a random card."""
    name = "cautious"
    def keep_flipping(self, st, p): return len(st.pile) < 2 and self.rng.random() < 0.2
    def leave(self, st, p, cands):
        r = st.river
        return self.rng.choice(cands) if self.rng.random() < 0.3 else min(cands, key=lambda i: r[i][1])

class Expert(Strategic):
    """Bar Raiser: the strongest line, but probes early: a slightly riskier EV rule and always the smart leave."""
    name = "expert"
    def __init__(self, seed=0, leave_mode=None):
        super().__init__(seed, risk=0.9, buoy_min=8, leave_mode=leave_mode)

PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}
