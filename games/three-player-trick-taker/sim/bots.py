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
    def plan(self, R, seat, hand): return self.rng.choice([0, 1, 2, 3]), self.rng.randint(3, 7)
    def swap(self, R, seat, h9): return self.rng.sample(h9, 3)
    def play(self, R, seat, legal, trick): return self.rng.choice(legal)

def longest_trump(hand):
    return max([0, 1, 2, 3], key=lambda s: (sum(1 for c in hand if c[0] == s), sum(c[1] for c in hand if c[0] == s)))

def drop_lowest(h9, trump):
    order = sorted(h9, key=lambda c: (c[0] == trump, c[1]))
    return order[:3]

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

class Basic(Base):
    """Heuristic from design notes: winner-count planning, role-aware trick play that aims at the exact crew total."""
    name = "basic"
    offset = 0; noise = 0.0; plan_noise = 0
    def plan(self, R, seat, hand):
        best = max([0, 1, 2, 3], key=lambda t: (strength(hand, t, set()), sum(1 for c in hand if c[0] == t)))
        s = strength(hand, best, set())
        tg = int(round(2 * s)) + self.offset
        if self.plan_noise: tg += self.rng.choice([-1, 0, 1]) if self.rng.random() < self.plan_noise else 0
        return best, max(3, min(7, tg))
    def swap(self, R, seat, h9):
        want = R.target / 2.0
        best = None
        for pair in itertools.combinations(range(10), 3):
            keep = [h9[i] for i in range(10) if i not in pair]
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

ALL = set((s, r) for s in range(4) for r in range(1, 10))

class Counter(Basic):
    """Card-counting strategic bot (rules v3 bot hints). Tracks played cards; treats a card as a sure winner if no unseen
    card can beat it given follow-suit and trumps. Crew steer the count to the Target; DC steers it 2+ away."""
    name = "strategic"
    def unseen(self, R, seat):
        return ALL - R.played - set(R.hands[seat])
    def higher(self, c, un): return sum(1 for (s, r) in un if s == c[0] and r > c[1])
    def sure_lead(self, R, c, un, hand):
        """Leading c: certain to win?"""
        if self.higher(c, un): return False
        if c[0] == R.trump: return True
        return not any(s == R.trump for s, r in un)
    def sure_count(self, R, seat):
        un = self.unseen(R, seat); hand = R.hands[seat]
        sure = 0.0
        for c in hand:
            h = self.higher(c, un)
            if c[0] == R.trump: sure += 1 if h == 0 else (0.5 if h == 1 else 0)
            elif not any(s == R.trump for s, r in un): sure += 1 if h == 0 else (0.4 if h == 1 else 0)
            else: sure += 0.5 if h == 0 else 0     # could be ruffed
        return sure
    def play(self, R, seat, legal, trick):
        if self.noise and self.rng.random() < self.noise: return self.rng.choice(legal)
        role = R.role(seat); un = self.unseen(R, seat); hand = R.hands[seat]
        if role == "D": return self.dc_play(R, seat, legal, trick, un)
        need = R.target - R.crew
        partner = R.safe if seat == R.planner else R.planner
        if need > 0:
            if need >= R.remaining:   # must win everything
                if trick: return win_cheap(legal, trick, R.trump) or lowest(legal)
                sl = [c for c in legal if self.sure_lead(R, c, un, hand)]
                return highest(sl) if sl else highest(legal)
            if trick:
                if cur_winner(trick, R.trump) == partner and not (len(trick) == 1 and False): return lowest(legal) if not beats(lowest(legal), trick, R.trump) else lowest(legal)
                return win_cheap(legal, trick, R.trump) or lowest(legal)
            sl = [c for c in legal if self.sure_lead(R, c, un, hand)]
            if sl: return lowest(sl)
            # lead a high card of a non-trump suit where we are strongest, else lowest
            return lowest(legal) if R.role(seat) == "S" else highest([c for c in legal if c[0] != R.trump] or legal)
        # need <= 0: play to lose
        if trick:
            losers = [c for c in legal if not beats(c, trick, R.trump)]
            if losers:
                # shed the highest losing card, but never waste trumps if a non-trump loser exists
                nt = [c for c in losers if c[0] != R.trump]
                return highest(nt) if nt else highest(losers)
            return lowest(legal)   # forced to win: win as cheaply as possible
        # leading: lowest-risk card, i.e. one most likely to lose
        def risk(c):
            h = self.higher(c, un)
            return (c[0] == R.trump, -h, c[1])
        return min(legal, key=risk)
    def dc_play(self, R, seat, legal, trick, un):
        r = R.remaining; T = R.target; crew = R.crew
        sure = min(r, self.sure_count(R, seat))
        grab_k = crew + r - T + 2      # DC needs this many of the remaining tricks to push crew to T-2 or lower
        duck_k = crew + r - T - 2      # DC may win at most this many to push crew to T+2 or higher
        if duck_k >= 0 and (sure < grab_k or duck_k <= sure and False):
            mode = "duck"
        elif grab_k <= r and sure >= grab_k - 0.5: mode = "grab"
        elif duck_k >= 0: mode = "duck"
        else: mode = "grab"
        if duck_k >= 0 and grab_k > r: mode = "duck"
        if mode == "grab":
            if trick: return win_cheap(legal, trick, R.trump) or lowest(legal)
            sl = [c for c in legal if self.sure_lead(R, c, un, R.hands[seat])]
            return lowest(sl) if sl else highest(legal)
        if trick:
            losers = [c for c in legal if not beats(c, trick, R.trump)]
            if losers:
                nt = [c for c in losers if c[0] != R.trump]
                return highest(nt) if nt else highest(losers)
            return lowest(legal)
        return min(legal, key=lambda c: (c[0] == R.trump, -self.higher(c, un), c[1]))

class Strategic(Counter):
    name = "strategic"

class Planner(Counter):      # strategist: full counting, long game
    name = "planner"

class Optimiser(Counter):    # competitor: strategic + exploit (tuned target offset found by experiment)
    name = "optimiser"
    offset = 0
    def swap(self, R, seat, h9):
        return super().swap(R, seat, h9)

class Instinct(Basic):     # casual: gut feel, noisy, no counting of target math
    name = "instinct"
    noise = 0.25; plan_noise = 0.5

class Flavour(Basic):      # story: dramatic - big targets, lead aces, go for the double-cross
    name = "flavour"
    noise = 0.10
    def plan(self, R, seat, hand):
        tr = max([0, 1, 2, 3], key=lambda s: (max([c[1] for c in hand if c[0] == s] or [0]), sum(1 for c in hand if c[0] == s)))
        nines = sum(1 for c in hand if c[1] >= 8)
        s = strength(hand, tr, set())
        return tr, max(4, min(7, int(round(2 * s)) + 1))
    def want_win(self, R, seat, legal, trick):
        if R.role(seat) == "D": return True
        return super().want_win(R, seat, legal, trick)

class Cautious(Basic):     # family: simple and safe, plays like greedy, modest target
    name = "cautious"
    def plan(self, R, seat, hand):
        tr, tg = super().plan(R, seat, hand)
        return tr, max(4, min(5, tg))
    def swap(self, R, seat, h9): return drop_lowest(h9, R.trump)
    def play(self, R, seat, legal, trick):
        if not trick: return highest(legal) if R.crew < R.target or R.role(seat) == "D" else lowest(legal)
        return win_cheap(legal, trick, R.trump) or lowest(legal)

class Expert(Counter):         # barraiser: strongest line = card-counting engine
    name = "expert"

STD = {"random": Random, "greedy": Greedy, "strategic": Strategic, "basic": Basic}
PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}
