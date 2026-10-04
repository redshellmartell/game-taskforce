"""Bots for Nine Fields. Interface: opening(st,p,empty)->cell ; act(st,p,acts)->(action, direction 0/1)."""
import random
from game import legal, do_move, resolve, claim, ADJ

AVG = 2.17

def totals(st, p, wpot):
    """Estimated total per player: known own trophies, estimated others (pile size x average), plus board potential."""
    n = st.n
    tot = [st.tv[q] if q == p else st.tn[q] * AVG for q in range(n)]
    if wpot:
        for c in range(9):
            card = st.card[c]
            if card is None: continue
            cnt = st.pw[c]; m = max(cnt)
            if m == 0: continue
            lead = [q for q in range(n) if cnt[q] == m]
            share = (0.5 + 0.5 * sum(cnt) / card[2]) * card[1] * wpot / len(lead)
            for q in lead: tot[q] += share
    return tot

def evalv(st, p, wpot, opp_max=0.0):
    t = totals(st, p, wpot)
    others = [t[q] for q in range(st.n) if q != p]
    ref = opp_max * max(others) + (1 - opp_max) * sum(others) / len(others)
    return t[p] - ref

def outcomes(st, p, a):
    """Yield (state_after, direction) for each way to play action a (2 directions if it floods)."""
    s2 = st.clone(); fc = do_move(s2, p, a)
    if fc < 0:
        yield s2, 0, False
        return
    cid = s2.card[fc][0]
    for d in (0, 1):
        s3 = s2.clone(); resolve(s3, p, fc, d)
        for q in range(9):   # turn the flooded island if still there
            if s3.card[q] is not None and s3.card[q][0] == cid: s3.axis[q] ^= 1
        yield s3, d, True

class Base:
    name = "base"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def opening(self, st, p, empty): return self.rng.choice(empty)
    def act(self, st, p, acts):
        a = self.rng.choice(acts); return a, self.rng.randint(0, 1)

class Random(Base): name = "random"

class Greedy(Base):
    """Best immediate trophy gain; otherwise prefers Landing next to nothing special (random)."""
    name = "greedy"
    def act(self, st, p, acts):
        best, pick = None, []
        for a in acts:
            for s2, d, fl in outcomes(st, p, a):
                v = s2.tv[p] - st.tv[p] + self.rng.random() * 0.01
                if fl and s2.tv[p] == st.tv[p]: v -= 0.0
                if best is None or v > best: best, pick = v, [(a, d)]
                elif v == best: pick.append((a, d))
        return self.rng.choice(pick)
    def opening(self, st, p, empty): return max(empty, key=lambda c: (st.card[c][1], self.rng.random()))

class Strategic(Base):
    """One-ply lookahead on a heuristic: trophies plus majority potential on the board."""
    name = "strategic"
    wpot = 0.7; opp_max = 0.3; noise = 0.0; top_k = 0
    def score(self, s2, p): return evalv(s2, p, self.wpot, self.opp_max)
    def act(self, st, p, acts):
        scored = []
        for a in acts:
            bd, bv = 0, None
            for s2, d, fl in outcomes(st, p, a):
                v = self.score(s2, p)
                if bv is None or v > bv: bv, bd = v, d
            scored.append((bv + self.rng.random() * 0.02 + (self.rng.gauss(0, self.noise) if self.noise else 0), a, bd))
        scored.sort(key=lambda x: -x[0])
        if self.top_k:
            return self.deepen(st, p, scored[:self.top_k])
        return scored[0][1], scored[0][2]
    def deepen(self, st, p, cands):
        return cands[0][1], cands[0][2]
    def opening(self, st, p, empty):
        return max(empty, key=lambda c: (st.card[c][1] * 1.0 + 0.3 * st.card[c][2] - 0.4 * sum(1 for d in ADJ[c] if st.card[d] and sum(st.pw[d])), self.rng.random()))

class TwoPly(Strategic):
    """Looks at the next player's best reply (by the same heuristic from their view) for the top candidates."""
    name = "twoply"; top_k = 6
    def deepen(self, st, p, cands):
        best, pick = None, cands[0]
        q = (p + 1) % st.n
        for v0, a, d in cands:
            s2 = [s3 for s3, dd, fl in outcomes(st, p, a) if dd == d][0]
            if s2.over: val = v0
            else:
                reply = None
                for b in legal(s2, q):
                    for s4, d2, fl in outcomes(s2, q, b):
                        ev = evalv(s4, q, self.wpot, self.opp_max)
                        if reply is None or ev > reply: reply = ev
                val = v0 if reply is None else 0.5 * v0 - 0.5 * reply
            if best is None or val > best: best, pick = val, (v0, a, d)
        return pick[1], pick[2]

# ---- persona bots
class Planner(TwoPly):          # strategist: plans ahead
    name = "planner"; top_k = 6; wpot = 0.8; opp_max = 0.2
class Optimiser(TwoPly):        # competitor: strongest line, plays against the leader
    name = "optimiser"; top_k = 4; wpot = 0.7; opp_max = 0.8
class Expert(TwoPly):           # barraiser: strongest, also stalls when ahead (exploit probe)
    name = "expert"; top_k = 8; wpot = 0.75; opp_max = 0.6
class Instinct(Strategic):      # casual: by feel, noisy
    name = "instinct"; noise = 1.2; wpot = 0.5
    def act(self, st, p, acts):
        if self.rng.random() < 0.25: return Base.act(self, st, p, acts)
        return Strategic.act(self, st, p, acts)
class Cautious(Strategic):      # family: safe and simple; avoids handing opponents trophies, noisy
    name = "cautious"; noise = 0.8; wpot = 0.4; opp_max = 0.0
    def act(self, st, p, acts):
        if self.rng.random() < 0.15: return Base.act(self, st, p, acts)
        return Strategic.act(self, st, p, acts)
class Flavour(Base):            # story: loves a big flood and a big island falling
    name = "flavour"
    def act(self, st, p, acts):
        if self.rng.random() < 0.8:
            best, pick = None, []
            for a in acts:
                for s2, d, fl in outcomes(st, p, a):
                    big = 0
                    if fl: big = 5 + max(s2.tv) - max(st.tv) + (s2.tv[p] - st.tv[p]) * 0.5
                    v = big + self.rng.random()
                    if best is None or v > best: best, pick = v, [(a, d)]
            return pick[0]
        return Base.act(self, st, p, acts)

PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour,
           "family": Cautious, "barraiser": Expert}
STANDARD = {"random": Random, "greedy": Greedy, "strategic": Strategic}
