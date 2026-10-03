import random, itertools
from game import trick_winner

def strength(hand, trump, played):
    """Count of likely winners: master/near-master cards. Trumps with <=3 higher unseen, off-suit with <=1."""
    hs = set(hand); n = 0.0
    for (s, r) in hand:
        u = sum(1 for rr in range(r + 1, 10) if (s, rr) not in hs and (s, rr) not in played)
        if trump is not None and s == trump:
            n += 1 if u <= 1 else (0.6 if u <= 3 else 0)
        else:
            n += 1 if u == 0 else (0.5 if u == 1 else 0)
    return n

def cur_winner(trick, trump):
    return trick_winner(trick, trump) if trick else None

def beats(c, trick, trump):
    """Would card c currently win the trick if played now?"""
    return trick_winner(trick + [(9, c)], trump) == 9

def lowest(cs): return min(cs, key=lambda c: c[1])
def highest(cs): return max(cs, key=lambda c: c[1])

class Base:
    name = "base"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def plan(self, R, seat, hand): raise NotImplementedError
    def swap(self, R, seat, h9): raise NotImplementedError
    def play(self, R, seat, legal, trick): raise NotImplementedError

class Random(Base):
    name = "random"
    def plan(self, R, seat, hand): return self.rng.choice([None, 0, 1, 2, 3]), self.rng.randint(3, 7)
    def swap(self, R, seat, h9): return self.rng.sample(h9, 2)
    def play(self, R, seat, legal, trick): return self.rng.choice(legal)

def longest_trump(hand):
    return max([0, 1, 2, 3], key=lambda s: (sum(1 for c in hand if c[0] == s), sum(c[1] for c in hand if c[0] == s)))

def drop_lowest(h9, trump):
    order = sorted(h9, key=lambda c: (c[0] == trump, c[1]))
    return order[:2]

def win_cheap(legal, trick, trump):
    w = [c for c in legal if beats(c, trick, trump)]
    return lowest(w) if w else None

class Greedy(Base):
    """Best immediate gain: grab every trick it cheaply can; fixed simple plan."""
    name = "greedy"
    def plan(self, R, seat, hand):
        hi = sum(1 for c in hand if c[1] >= 7)
        return longest_trump(hand), max(3, min(7, 2 + hi))
    def swap(self, R, seat, h9): return drop_lowest(h9, R.trump)
    def play(self, R, seat, legal, trick):
        if not trick: return highest(legal)
        return win_cheap(legal, trick, R.trump) or lowest(legal)

class Strategic(Base):
    """Heuristic from design notes: winner-count planning, role-aware trick play that aims at the exact crew total."""
    name = "strategic"
    offset = 0; noise = 0.0; plan_noise = 0
    def plan(self, R, seat, hand):
        best = max([None, 0, 1, 2, 3], key=lambda t: (strength(hand, t, set()), sum(1 for c in hand if c[0] == t) if t is not None else 0))
        s = strength(hand, best, set())
        tg = int(round(2 * s)) + self.offset
        if self.plan_noise: tg += self.rng.choice([-1, 0, 1]) if self.rng.random() < self.plan_noise else 0
        return best, max(3, min(7, tg))
    def swap(self, R, seat, h9):
        want = R.target / 2.0
        best = None
        for pair in itertools.combinations(range(9), 2):
            keep = [h9[i] for i in range(9) if i not in pair]
            sc = (abs(strength(keep, R.trump, set()) - want), -sum(c[1] for c in keep if c[0] == R.trump))
            if best is None or sc < best[0]: best = (sc, pair)
        return [h9[i] for i in best[1]]
    def want_win(self, R, seat, legal, trick):
        hand = R.hands[seat]
        if R.role(seat) == "D":
            X = 7 - R.target; dt = R.tricks[seat]
            proj = dt + min(R.remaining, strength(hand, R.trump, R.played))
            return dt > X or proj >= X
        need = R.target - R.crew
        if need <= 0: return False
        if need >= R.remaining: return True
        if trick:
            partner = R.safe if seat == R.planner else R.planner
            if cur_winner(trick, R.trump) == partner: return False
        return True
    def play(self, R, seat, legal, trick):
        if self.noise and self.rng.random() < self.noise: return self.rng.choice(legal)
        win = self.want_win(R, seat, legal, trick)
        if not trick:
            if win:
                m = [c for c in legal if strength([c], R.trump, R.played | (set((s, r) for s in range(4) for r in range(1, 10)) - set(R.hands[seat]) - R.played) ) ] if False else None
                masters = [c for c in legal if self.master(R, seat, c)]
                return highest(masters) if masters else (lowest(legal) if R.role(seat) != "D" else highest(legal))
            return lowest(legal)
        if win:
            return win_cheap(legal, trick, R.trump) or lowest(legal)
        losers = [c for c in legal if not beats(c, trick, R.trump)]
        return lowest(losers) if losers else lowest(legal)
    def master(self, R, seat, c):
        hs = set(R.hands[seat]); s, r = c
        if R.trump is not None and s != R.trump:
            # a trump could still cut; ignore if trumps all gone (approximate: master within suit only)
            pass
        return all((s, rr) in hs or (s, rr) in R.played for rr in range(r + 1, 10))

class Planner(Strategic):      # strategist: full counting, long game
    name = "planner"

class Optimiser(Strategic):    # competitor: strategic + exploit (tuned target offset found by experiment)
    name = "optimiser"
    offset = 0
    def swap(self, R, seat, h9):
        return super().swap(R, seat, h9)

class Instinct(Strategic):     # casual: gut feel, noisy, no counting of target math
    name = "instinct"
    noise = 0.25; plan_noise = 0.5

class Flavour(Strategic):      # story: dramatic - big targets, lead aces, go for the double-cross
    name = "flavour"
    noise = 0.10
    def plan(self, R, seat, hand):
        tr = max([0, 1, 2, 3], key=lambda s: (max([c[1] for c in hand if c[0] == s] or [0]), sum(1 for c in hand if c[0] == s)))
        nines = sum(1 for c in hand if c[1] >= 8)
        if nines >= 3: tr = None
        s = strength(hand, tr, set())
        return tr, max(4, min(7, int(round(2 * s)) + 1))
    def want_win(self, R, seat, legal, trick):
        if R.role(seat) == "D": return True
        return super().want_win(R, seat, legal, trick)

class Cautious(Strategic):     # family: simple and safe, plays like greedy, modest target
    name = "cautious"
    def plan(self, R, seat, hand):
        tr, tg = super().plan(R, seat, hand)
        return tr, max(4, min(5, tg))
    def swap(self, R, seat, h9): return drop_lowest(h9, R.trump)
    def play(self, R, seat, legal, trick):
        if not trick: return highest(legal) if R.crew < R.target or R.role(seat) == "D" else lowest(legal)
        return win_cheap(legal, trick, R.trump) or lowest(legal)

STD = {"random": Random, "greedy": Greedy, "strategic": Strategic}
PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious}
