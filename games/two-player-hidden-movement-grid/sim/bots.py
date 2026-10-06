import random
from functools import lru_cache
from game import FULL, HARB, plans, ev_params, step, score, S

@lru_cache(maxsize=None)
def _plans(hand): return plans(hand)

def plans_for(hand): return _plans(tuple(sorted(hand)))

def simulate(g, me, pm, po, noop_other=False):
    """Run one 3-step look-ahead with expected values. Returns (gain_me, gain_other, reveals_me, reveals_other, end state)."""
    st = g.s; s = st.copy()
    base = (score(st, 0), score(st, 1))
    for k in range(3):
        cards = (pm[k], po[k]) if me == 0 else (po[k], pm[k])
        step(s, cards)
    o = 1 - me
    return (score(s, me) + s.bonus[me] - base[me], score(s, o) + s.bonus[o] - base[o], s.rev[me], s.rev[o], s)

def adjacent(a, b): return max(abs(a % 5 - b % 5), abs(a // 5 - b // 5)) == 1

def nearest_face_up(s, pos):
    best = 0.0
    for i in range(25):
        if s.grid[i] in (1, 2, 3) and s.fup[i]:
            d = abs(i % 5 - pos % 5) + abs(i // 5 - pos // 5)
            best = max(best, s.grid[i] / (1 + d))
    return best

class Bot:
    name = "base"
    def __init__(self, seed=0, **kw):
        self.rng = random.Random(seed)
        for k, v in kw.items(): setattr(self, k, v)
    def want_ping(self, g, me): return False
    def plot(self, g, me, hand, known): raise NotImplementedError
    def rival_hand(self, g, me):
        return list(FULL) if getattr(self, "blind", False) else g.hands[1 - me]
    def rival_plans(self, g, me, known, k):
        rp = plans_for(self.rival_hand(g, me))
        if known: rp = [p for p in rp if p[:len(known)] == tuple(known)]
        noop = ("X", "X", "X"); sc = []
        for p in rp:
            gr, _, _, rv, _ = simulate(g, 1 - me, p, noop)
            sc.append((gr + 0.3 * rv + self.rng.random() * 1e-3, p))
        sc.sort(reverse=True)
        return [p for _, p in sc[:k]]

class Random(Bot):
    name = "random"
    def want_ping(self, g, me): return self.rng.random() < 0.5
    def plot(self, g, me, hand, known): return self.rng.choice(plans_for(hand))

class Greedy(Bot):
    name = "greedy"
    ping_p = 0.0
    def want_ping(self, g, me): return self.rng.random() < self.ping_p
    def extra(self, g, me, plan, s, rev): return 0.0
    def plot(self, g, me, hand, known):
        g.s.evp = ev_params(g.s); noop = ("X", "X", "X"); best = []
        for p in plans_for(hand):
            gm, go, rv, _, s = simulate(g, me, p, noop)
            best.append((gm + 0.3 * rv + self.extra(g, me, p, s, rv) + self.rng.random() * 1e-3, p))
        best.sort(reverse=True)
        return self.pick(best)
    def pick(self, best): return best[0][1]

class Strategic(Bot):
    name = "strategic"
    K = 6; ping = True; mix = 0.0; prox = 0.0
    def want_ping(self, g, me):
        if not self.ping: return False
        s = g.s; o = 1 - me
        for i in range(10, 15):
            if (s.grid[i] == 3 and s.fup[i]) or not s.fup[i]:
                dm = abs(i % 5 - s.pos[me] % 5) + abs(i // 5 - s.pos[me] // 5)
                do = abs(i % 5 - s.pos[o] % 5) + abs(i // 5 - s.pos[o] // 5)
                if dm <= 3 and do <= 3: return True
        d = abs(s.pos[0] % 5 - s.pos[1] % 5) + abs(s.pos[0] // 5 - s.pos[1] // 5)
        for i in range(25):
            if s.grid[i] == 3 and s.fup[i]:
                dm = abs(i % 5 - s.pos[me] % 5) + abs(i // 5 - s.pos[me] // 5)
                do = abs(i % 5 - s.pos[o] % 5) + abs(i // 5 - s.pos[o] // 5)
                if dm <= 3 and do <= 3: return True
        return d <= 3 and "T" in g.hands[me]
    def plot(self, g, me, hand, known):
        g.s.evp = ev_params(g.s); rps = self.rival_plans(g, me, known, self.K); o = 1 - me
        out = []
        for p in plans_for(hand):
            vals = []
            for rp in rps:
                gm, go, rv, _, s = simulate(g, me, p, rp)
                v = gm - go + 0.3 * rv
                if adjacent(s.pos[me], s.pos[o]) and "T" not in rp and s.pos[me] != HARB[me]: v -= 0.5
                if self.prox: v += self.prox * nearest_face_up(s, s.pos[me])
                vals.append(v)
            mean = sum(vals) / len(vals)
            val = mean if not self.mix else (1 - self.mix) * mean + self.mix * min(vals)
            out.append((val + self.rng.random() * 1e-3, p))
        return max(out)[1]

# ---- persona bots -----------------------------------------------------------
class Planner(Strategic):            # strategist: wider read of rival plans, values being near known salvage
    name = "planner"; K = 8; prox = 0.15
class Optimiser(Strategic):          # competitor: strong line, hedges against the worst case among likely plans
    name = "optimiser"; K = 6; mix = 0.4
class Expert(Strategic):             # bar raiser: strongest line, also wide read
    name = "expert"; K = 8; mix = 0.3; prox = 0.1
class Instinct(Greedy):              # casual: gut feel, noisy, pings on a whim
    name = "instinct"; ping_p = 0.4
    def pick(self, best):
        if self.rng.random() < 0.35: return self.rng.choice(best[:10])[1]
        return best[0][1]
class Flavour(Greedy):               # story: wants torpedoes and confrontation
    name = "flavour"
    def want_ping(self, g, me):
        s = g.s; return abs(s.pos[0] % 5 - s.pos[1] % 5) + abs(s.pos[0] // 5 - s.pos[1] // 5) <= 3
    def extra(self, g, me, plan, s, rev):
        v = 0.5 * rev
        if "T" in plan and adjacent(s.pos[me], s.pos[1 - me]): v += 1.2
        return v
class Cautious(Greedy):              # family: safe, avoids fog and torpedo range, goes home when ahead
    name = "cautious"
    def extra(self, g, me, plan, s, rev):
        o = 1 - me; v = -0.5 * rev
        if adjacent(s.pos[me], s.pos[o]) and "T" in g.hands[o] and s.pos[me] != HARB[me]: v -= 1.0
        if s.pos[me] == HARB[me] and score(g.s, me) > score(g.s, o): v += 0.8
        return v

# ---- exploit probes ---------------------------------------------------------
class Spammer(Strategic):            # torpedo spam: always plots T when it has one, hunts the rival
    name = "spammer"; K = 4
    def plot(self, g, me, hand, known):
        g.s.evp = ev_params(g.s)
        cand = [p for p in plans_for(hand) if "T" in p] or plans_for(hand)
        rps = self.rival_plans(g, me, known, self.K); o = 1 - me; out = []
        for p in cand:
            tot = 0
            for rp in rps:
                gm, go, rv, _, s = simulate(g, me, p, rp)
                tot += gm - go + 0.3 * rv
            out.append((tot / len(rps) + self.rng.random() * 1e-3, p))
        return max(out)[1]
class Camper(Strategic):             # harbour camping: prefers plans that end at home (once it holds any salvage)
    name = "camper"; K = 4
    def plot(self, g, me, hand, known):
        g.s.evp = ev_params(g.s); rps = self.rival_plans(g, me, known, self.K); out = []
        have = bool(g.s.piles[me])
        for p in plans_for(hand):
            tot = 0
            for rp in rps:
                gm, go, rv, _, s = simulate(g, me, p, rp)
                tot += gm - go + 0.3 * rv + (2.0 if have and s.pos[me] == HARB[me] else 0)
            out.append((tot / len(rps) + self.rng.random() * 1e-3, p))
        return max(out)[1]
class Mid(Strategic):                # mid-strength reference: reads only the 2 likeliest rival plans
    name = "mid"; K = 2
class NoTorp(Strategic):             # never plots T
    name = "notorp"
    def plot(self, g, me, hand, known):
        h = list(hand)
        if "T" in h and len(h) > 3: h.remove("T")
        return Strategic.plot(self, g, me, h, known)
class NoMiddle(Strategic):           # never enters row 3 (solo-path check)
    name = "nomiddle"
    def plot(self, g, me, hand, known):
        g.s.evp = ev_params(g.s); rps = self.rival_plans(g, me, known, self.K); o = 1 - me; out = []
        for p in plans_for(hand):
            pos = g.s.pos[me]; bad = False
            for c in p:
                if c in "NESW":
                    dx, dy = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}[c]
                    x, y = pos % 5 + dx, pos // 5 + dy
                    if 0 <= x < 5 and 0 <= y < 5: pos = y * 5 + x
                    if pos // 5 == 2: bad = True
            if bad: continue
            vals = []
            for rp in rps:
                gm, go, rv, _, s = simulate(g, me, p, rp); vals.append(gm - go + 0.3 * rv)
            out.append((sum(vals) / len(vals) + self.rng.random() * 1e-3, p))
        if not out: return Strategic.plot(self, g, me, hand, known)
        return max(out)[1]
class Blind(Strategic):              # strategic that ignores the cooling information (assumes rival holds all 9 cards)
    name = "blind"; blind = True
class NoPing(Strategic):
    name = "noping"; ping = False

STANDARD = {"random": Random, "greedy": Greedy, "strategic": Strategic}
PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}
