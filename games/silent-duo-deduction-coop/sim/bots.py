"""Bots for Silent Duo. Every bot sees only an Obs (rules 5.1) plus its own memory of the public event log."""
import math, random


class RandomBot:
    name = "random"
    def keep(self, o, drawn): return self.rng.randrange(len(drawn))
    def __init__(self, seed=0, **kw): self.rng = random.Random(seed)
    def act(self, o, legal): return self.rng.choice(legal)


class Honest:
    """Interval tracking + card counting; lights when (near) certain, offers the pair that narrows most, else trims."""
    name = "honest"
    P = dict(light_p=0.97, risky_p=0.7, press=3.0, lam=0.6, min_gain=0.12, noise=0.0, count=True,
             beacon_w=0.2, conv=False, code=False, miss_code=False, hand_w=0.4, late_p=0.5, reef_p=0.9,
             pair_blind=False, trim_blind=False, beacon_wait=False)

    def __init__(self, seed=0, **kw):
        self.rng = random.Random(seed)
        self.p = {**Honest.P, **self.__class__.P, **kw}
        self.ptr = 0
        self.lastrev = {}      # own ship idx -> (shown, row) of the partner's latest offer
        self.hints = []        # code hints: (ship idx, decoded value, prior)
        self.missed = False

    # ---------------------------------------------------------- memory
    def sync(self, o):
        for e in o.events[self.ptr:]:
            if e[0] == "offer" and e[2] == o.me and e[1] != o.me:
                _, off, q, i, shown, row = e
                self.lastrev[i] = (shown, row)
                if self.p["code"] and o.n == 2:
                    js = [j for j, s in enumerate(o.ships[o.me]) if not s["lit"] and j != i]
                    if js: self.hints.append((js[0], ((shown + i) % 10) + 1, 0.4))
            elif e[0] == "miss" and e[1] != o.me and self.p["miss_code"] and o.n == 2:
                js = [j for j, s in enumerate(o.ships[o.me]) if not s["lit"]]
                if js: self.hints.append((js[0], e[3], 0.5))
        self.ptr = len(o.events)

    def cand(self, o, i):
        s = o.ships[o.me][i]
        vs = list(range(s["lo"] + 1, s["hi"]))
        if not vs: vs = [max(1, min(10, s["lo"] + 1))]
        if self.p["count"]: w = {v: float(o.remaining[v]) for v in vs}
        else: w = {v: 1.0 for v in vs}
        if sum(w.values()) <= 0: w = {v: 1.0 for v in vs}
        if self.p["conv"] and i in self.lastrev:
            r, row = self.lastrev[i]
            for v in vs:
                d = (v - r - 1) if row == "low" else (r - v - 1)
                w[v] *= math.exp(-max(d, 0) / 3.0)
        t = sum(w.values()) or 1.0
        w = {v: x / t for v, x in w.items()}
        for (j, d, q) in self.hints:
            if j == i and d in w and not o.ships[o.me][i]["lit"]:
                m = len(vs)
                pc = q / (q + (1 - q) * m / 10.0)
                w = {v: (1 - pc) * x for v, x in w.items()}
                w[d] += pc
        return w

    def need(self, o, c, ws):
        best = 0.0
        for w in ws.values():
            best = max(best, sum(x for v, x in w.items() if abs(v - c) <= 1))
        return best

    # ---------------------------------------------------------- decision
    def act(self, o, legal):
        self.sync(o)
        if self.p["noise"] and self.rng.random() < self.p["noise"]:
            return self.rng.choice(legal)
        me = o.me
        ws = {i: self.cand(o, i) for i, s in enumerate(o.ships[me]) if not s["lit"]}
        hand = o.hand
        unlit = sum(1 for q in o.ships for s in o.ships[q] if not s["lit"])
        lw = o.last_watch is not None
        left = o.last_watch if lw else o.deck_n + o.n
        # lights
        thr = self.p["light_p"]
        if lw: thr = 1e-9
        elif left < self.p["press"] * unlit: thr = self.p["risky_p"] if o.reefs_left > 1 else max(self.p["late_p"], self.p["reef_p"] - 0.2)
        elif o.reefs_left <= 1: thr = max(thr, self.p["reef_p"])
        best = None
        okl = {(a[1], a[2]) for a in legal if a[0] == "light"}
        for i, w in ws.items():
            for c in set(hand):
                if (i, c) not in okl: continue
                pr = sum(x for v, x in w.items() if abs(v - c) <= 1)
                if pr < thr: continue
                sc = pr + self.p["beacon_w"] * w.get(c, 0.0)
                others = {k: x for k, x in ws.items() if k != i}
                if others: sc -= 0.1 * self.need(o, c, others)
                if best is None or sc > best[0]: best = (sc, i, c)
        if best and self.p["beacon_wait"] and not lw and left >= self.p["press"] * unlit + 6:
            w = ws[best[1]]
            if w.get(best[2], 0.0) < 0.9 and len(w) > 1:       # safe light, but not an exact hit: wait for a Beacon if an Offer is worthwhile
                bo = self.best_offer(o, legal, ws)
                if bo and bo[0] >= self.p["min_gain"]: return bo[1]
        if best: return ("light", best[1], best[2])
        # deliberate-miss code (attack only)
        if self.p["miss_code"] and o.n == 2 and not self.missed and o.wrecked == 0 and not lw:
            oth = 1 - me
            js = [j for j, s in enumerate(o.ships[oth]) if not s["lit"]]
            if js:
                W = o.ships[oth][js[0]]["v"]
                if W in hand and (o.ships[oth][js[0]]["hi"] - o.ships[oth][js[0]]["lo"] - 1) > 3:
                    for i, w in ws.items():
                        if all(abs(W - v) >= 2 for v in w) and ("light", i, W) in legal:
                            self.missed = True
                            return ("light", i, W)
        # offers
        bo = self.best_offer(o, legal, ws)
        if lw:
            return bo[1] if bo else self.rng.choice(legal)
        if bo and bo[0] >= self.p["min_gain"]: return bo[1]
        trims = [a for a in legal if a[0] == "trim"]
        if trims: return self.pick_trim(o, trims, ws)
        return bo[1] if bo else self.rng.choice(legal)

    @staticmethod
    def u(m): return math.log(max(m, 3) / 3.0)

    def best_offer(self, o, legal, ws):
        me, best = o.me, None
        for a in legal:
            if a[0] != "offer": continue
            _, q, i, x, y = a
            s = o.ships[q][i]
            V, lo, hi = s["v"], s["lo"], s["hi"]
            if self.p["conv"] and not ((x < V and y < V) or (x > V and y > V)): continue
            m = hi - lo - 1
            g = 0.0
            for r in (x, y):
                l2, h2 = (max(lo, r), hi) if r < V else (lo, min(hi, r))
                g += (self.u(m) - self.u(h2 - l2 - 1)) / 2
            cost = 0.0
            for r in (x, y):
                c = self.need(o, r, ws) if ws else 0.0
                if o.hand.count(r) > 1: c *= 0.5
                cost += c / 2
            sc = g - self.p["lam"] * cost
            if self.p["code"] and o.n == 2:
                js = [j for j, t in enumerate(o.ships[q]) if not t["lit"] and j != i]
                if js:
                    W = o.ships[q][js[0]]["v"]
                    xx = ((W - 2 - i) % 10) + 1
                    if xx in (x, y) and (o.ships[q][js[0]]["hi"] - o.ships[q][js[0]]["lo"] - 1) > 3: sc += 0.5
            if best is None or sc > best[0]: best = (sc, a)
        if best is not None and self.p["pair_blind"]:
            q0, i0 = best[1][1], best[1][2]
            best = (best[0], self.rng.choice([a for a in legal if a[0] == "offer" and a[1] == q0 and a[2] == i0]))
        if best is None and self.p["conv"]:
            p2 = self.p; self.p = {**p2, "conv": False}
            try: return self.best_offer(o, legal, ws)
            finally: self.p = p2
        return best

    def keep(self, o, drawn):
        if self.p["trim_blind"]: return self.rng.randrange(len(drawn))
        ws = {i: self.cand(o, i) for i, s in enumerate(o.ships[o.me]) if not s["lit"]}
        oth = [s for q in o.ships if q != o.me for s in o.ships[q] if not s["lit"] and s["hi"] - s["lo"] - 1 > 3]
        def val(c):
            k = self.need(o, c, ws) if ws else 0.0
            k += self.p["hand_w"] * sum(1 for s in oth if s["lo"] < c < s["hi"] and c != s["v"]) / max(1, len(oth))
            if o.hand.count(c) > 0: k *= 0.8
            return k
        return 0 if val(drawn[0]) >= val(drawn[1]) else 1

    def pick_trim(self, o, trims, ws):
        oth = [s for q in o.ships if q != o.me for s in o.ships[q] if not s["lit"] and s["hi"] - s["lo"] - 1 > 3]
        best = None
        for a in trims:
            c = a[1]
            keep = self.need(o, c, ws) if ws else 0.0
            use = sum(1 for s in oth if s["lo"] < c < s["hi"] and c != s["v"]) / max(1, len(oth))
            keep += self.p["hand_w"] * use
            if o.hand.count(c) > 1: keep *= 0.6
            keep += self.rng.random() * 1e-3
            if best is None or keep < best[0]: best = (keep, a)
        return best[1]


class Greedy(Honest):
    name = "greedy"
    P = dict(light_p=0.5, risky_p=0.4, lam=0.0, min_gain=0.0, count=False)

class PairBlind(Honest):
    name = "pair_blind"; P = dict(pair_blind=True)
class TrimBlind(Honest):
    name = "trim_blind"; P = dict(trim_blind=True)
class BeaconBlind(Honest):
    name = "beacon_blind"; P = dict(beacon_w=0.0)
class BeaconHunter(Honest):
    name = "beacon_hunter"; P = dict(beacon_wait=True, beacon_w=0.5)

class Convention(Honest):
    name = "convention"
    P = dict(conv=True)

class CodeAttack(Honest):
    name = "code"
    P = dict(code=True, miss_code=True)

# ---------------------------------------------------------------- persona bots
class Strategist(Honest):      # planner: careful counting, trades later for sure lights, protects needed cards
    P = dict(light_p=0.98, lam=0.9, press=3.4, min_gain=0.1, hand_w=0.5)

class Casual(Honest):          # instinct: no card counting, lights on a hunch, noisy
    P = dict(light_p=0.6, risky_p=0.5, lam=0.2, count=False, noise=0.2, min_gain=0.05)

class Competitor(Honest):      # optimiser: strongest line, hunts Beacons
    P = dict(light_p=0.96, lam=0.7, beacon_w=0.5, press=3.2, min_gain=0.1, hand_w=0.5, risky_p=0.75)

class Story(Honest):           # flavour: dramatic gambles, big reveals, likes the Beacon, a bit noisy
    P = dict(light_p=0.7, risky_p=0.55, lam=0.3, beacon_w=0.8, noise=0.1, min_gain=0.05)

class Family(Honest):          # cautious: only certain lights, simple offers, often trims, a bit noisy
    P = dict(light_p=0.995, risky_p=0.85, lam=0.5, noise=0.1, min_gain=0.3, count=False, reef_p=0.99, late_p=0.8)

class Expert(Honest):          # barraiser: strongest line and probes the code/convention exploits (soft convention prior)
    P = dict(light_p=0.96, lam=0.7, beacon_w=0.5, press=3.2, min_gain=0.1, hand_w=0.5, risky_p=0.75)

PERSONA = {"strategist": Strategist, "casual": Casual, "competitor": Competitor,
           "story": Story, "family": Family, "barraiser": Expert}
TIERS = {"random": RandomBot, "greedy": Greedy, "honest": Honest, "convention": Convention, "code": CodeAttack}
