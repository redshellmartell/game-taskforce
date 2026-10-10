"""Bots for Heavenly Bodies v2. Interface: setup(st,p)->[(hand_idx,slot)x2]; draw(st,p)->'deck'|'deep';
turn(st,p,rebound)->(plan,(orbit,dir)); discard(st,p)->cards in discard order (last = new Deep Space top)."""
import random
import game
from game import (beats, crash, spin_orbit, apply_launches, patterns, legal_launches, CLOCK, CCW)

COLOURS = range(4)


def need(orbit, hand):
    """Estimated launches/draws to complete each pattern (lower is better). Returns list of T for crit, const, align."""
    sizes = [c[1] if c else 0 for c in orbit]; hs = sorted((c[1] for c in hand), reverse=True)
    TH = game.CFG["mass_eff"]
    arr = sorted(sizes); total = sum(arr); T = 0.0; k = 0
    while k < len(hs) and (total < TH or arr[0] == 0) and hs[k] > arr[0]:
        total += hs[k] - arr[0]; arr[0] = hs[k]; arr.sort(); k += 1; T += 1
    empties = sum(1 for x in arr if x == 0)
    if empties: T += 1.5 * empties; total += 3 * empties
    if total < TH: T += 1.5 * ((TH - total + 1) // 2)
    out = [T]
    ocol = [0] * 4; hcol = [0] * 4
    for c in orbit:
        if c: ocol[c[0]] += 1
    for c in hand: hcol[c[0]] += 1
    cn = min((4 - ocol[c]) + 1.5 * max(0, 4 - ocol[c] - hcol[c]) for c in COLOURS)
    if game.CFG["rainbow"]:
        u = sum(1 for c in COLOURS if ocol[c]); m = 4 - u; h = sum(1 for c in COLOURS if not ocol[c] and hcol[c])
        cn = min(cn, m + 1.5 * (m - h) + (0.0 if sum(ocol) == u else 1.0 * (sum(ocol) - u)))
    out.append(cn)
    osz = {c[1] for c in orbit if c}; hsz = {c[1] for c in hand}
    best = 99
    for S in ({1, 2, 3, 4}, {2, 3, 4, 5}):
        u = len(osz & S); h = len(hsz & (S - osz))
        best = min(best, (4 - u) + 1.5 * max(0, 4 - u - h))
    out.append(best)
    return out


_vcache = {}
def potential(orbit, hand):
    key = (tuple(orbit), tuple(sorted(hand)), game.CFG["mass_eff"], game.CFG["rainbow"])
    v = _vcache.get(key)
    if v is None:
        T = sorted(need(orbit, hand))
        v = 1.0 / (1 + T[0]) + 0.15 * (1.0 / (1 + T[1]) + 1.0 / (1 + T[2]))
        if len(_vcache) > 300000: _vcache.clear()
        _vcache[key] = v
    return v


def opp_potential(orbit):
    return potential(orbit, ())


def sim_turn(st, p, plan, spin, comet=True, shieldblind=False):
    """Return (orbits, hand_p, captured_by_p, lost_by_p, shielded_set_after). Hands of others are not tracked."""
    n = st.n
    orbits = [list(o) for o in st.orbits]
    orb, hand, _ = apply_launches(orbits[p], st.hands[p], plan)
    sh = set() if shieldblind else set(st.shielded)
    if game.CFG["shield"] and not shieldblind:
        for i, s_ in plan:
            if game.shield_ok(st.hands[p][i]): sh.add(st.hands[p][i])
    orbits[p] = orb; hand = list(hand)
    gain = []; lost = []
    if spin:
        q, d = spin
        orbits[q] = spin_orbit(orbits[q], d)
        for e in crash(orbits, q, n, comet, sh):
            if e[0] == "cap":
                if e[1] == p: gain.append(e[4])
                if e[2] == p: lost.append(e[4])
    return orbits, hand + gain, gain, lost, sh


class Heur:
    """Parametrised heuristic bot. w: dict of weights."""
    name = "heur"
    def __init__(self, seed, **kw):
        self.r = random.Random(seed)
        self.w = dict(threat=0.6, win_opp=3.0, win_me=2.0, expo=0.04, capt=0.0, noise=0.0, selfbias=0.0, deep_thr=0.04,
                      selfonly=False, cometblind=False, norecall=False, deckonly=False, topk=6, greedy=False, hold_expo=1.0, shieldblind=False, defence=0.0)
        self.w.update(kw)

    # ---- setup
    def setup(self, st, p):
        h = st.hands[p]
        if self.w["greedy"] or self.w.get("randsetup"):
            idx = sorted(range(5), key=lambda i: -h[i][1])[:2] if self.w["greedy"] else self.r.sample(range(5), 2)
            slots = [0, 2] if self.w["greedy"] else self.r.sample(range(4), 2)
            return list(zip(idx, slots))
        best = None
        for i in range(5):
            for j in range(i + 1, 5):
                orb = [None] * 4; orb[0] = h[i]; orb[2] = h[j]
                rest = [c for k, c in enumerate(h) if k not in (i, j)]
                v = potential(orb, rest) + self.r.random() * 0.01
                if best is None or v > best[0]: best = (v, i, j)
        return [(best[1], 0), (best[2], 2)]

    # ---- draw
    def draw(self, st, p):
        if self.w["deckonly"] or not st.deep: return "deck"
        if self.w["greedy"]: return "deep" if st.deep[-1][1] >= 4 else "deck"
        c = st.deep[-1]
        gain = potential(st.orbits[p], st.hands[p] + [c]) - potential(st.orbits[p], st.hands[p])
        return "deep" if gain > self.w["deep_thr"] else "deck"

    # ---- plans
    def _plans(self, st, p, rb):
        hand = st.hands[p]
        plans = legal_launches(st, p, False)
        if rb and len(hand) > 1:
            # prune rebound pairs to the 4 best-sized or best-potential cards
            order = sorted(range(len(hand)), key=lambda i: -potential(st.orbits[p], [hand[i]]))[:4]
            for i in order:
                for s in range(4):
                    for j in order:
                        if j == i: continue
                        for t in range(4):
                            if t != s: plans.append(((i, s), (j, t)))
        if self.w["norecall"]:
            occ = lambda s: st.orbits[p][s] is not None
            plans = [pl for pl in plans if not any(occ(s) for _, s in pl)] or [()]
        return plans

    def _spins(self, st, p):
        ne = [q for q in range(st.n) if any(st.orbits[q]) or q == p]
        return [(q, d) for q in ne for d in (CLOCK, CCW)]

    def _score(self, st, p, orbits, hand, gain, lost, expo=None):
        w = self.w; n = st.n
        if w["greedy"]:
            mine = sum(c[1] for c in orbits[p] if c)
            others = sum(sum(c[1] for c in orbits[o] if c) for o in range(n) if o != p) / (n - 1)
            return mine + 1.5 * len(hand) - 0.5 * others + 0.5 * sum(c[1] for c in gain) + self.r.random() * 0.01
        v = potential(orbits[p], hand)
        thr = max(opp_potential(orbits[o]) for o in range(n) if o != p)
        v -= w["threat"] * thr
        for o in range(n):
            if o != p and patterns(orbits[o]): v -= w["win_opp"] / (1 + ((o - p) % n) - 1 + 0.01) if False else w["win_opp"]
        if w["defence"]: v += w["defence"] * sum(orbits[p][k][1] for k in (1, 3) if orbits[p][k])
        if patterns(orbits[p]): v += w["win_me"]
        v += w["capt"] * len(gain)
        if expo is not None: v -= expo
        return v

    def _expo(self, st, p, orbits, sh=frozenset()):
        """Public-info risk: average size I lose over all single spins an opponent could make (launch ignored)."""
        n = st.n; tot = 0; cnt = 0
        for q in range(n):
            if not any(orbits[q]): continue
            for d in (CLOCK, CCW):
                o2 = [list(o) for o in orbits]; o2[q] = spin_orbit(o2[q], d)
                cnt += 1
                for e in crash(o2, q, n, True, sh):
                    if e[0] == "cap" and e[2] == p: tot += e[4][1]
        return self.w["expo"] * 10 * tot / max(1, cnt) * self.w["hold_expo"] if cnt else 0

    def turn(self, st, p, rb):
        w = self.w
        plans = self._plans(st, p, rb); spins = self._spins(st, p)
        if w["selfonly"]:
            mine = [(q, d) for q, d in spins if q == p]
            if mine and any(st.orbits[p]) or (mine and plans):
                spins = [s for s in mine]
        scored = []
        comet = not w["cometblind"]
        hand = st.hands[p]
        for pl in plans:
            for sp in spins:
                if not any(c for c in apply_launches(st.orbits[p], hand, pl)[0]) and sp[0] == p and not any(
                        any(st.orbits[q]) for q in range(st.n) if q != p):
                    continue
                orbits, h2, gain, lost, sh = sim_turn(st, p, pl, sp, comet, w["shieldblind"])
                scored.append((self._score(st, p, orbits, h2, gain, lost), pl, sp, orbits, h2, gain, sh))
        if not scored:
            return [], (p, CLOCK)
        scored.sort(key=lambda x: -x[0])
        if not w["greedy"] and w["expo"]:
            top = scored[: w["topk"]]
            rescored = []
            for sc, pl, sp, orbits, h2, gain, sh in top:
                e = self._expo(st, p, orbits, sh)
                if patterns(orbits[p]): e *= 2.5   # a winning orbit must survive
                rescored.append((sc - e, pl, sp))
            rescored.sort(key=lambda x: -x[0])
            cand = rescored
        else:
            cand = [(s[0], s[1], s[2]) for s in scored[: w["topk"]]]
        if w["noise"] and self.r.random() < w["noise"]:
            pick = self.r.choice(cand[: 4])
        else:
            pick = cand[0]
        # selfbias: cautious bots prefer spinning their own orbit when scores are close
        if w["selfbias"]:
            for c in cand:
                if c[2][0] == p and c[0] >= cand[0][0] - w["selfbias"]: pick = c; break
        return list(pick[1]), pick[2]

    def discard(self, st, p):
        hand = list(st.hands[p]); out = []
        while len(hand) > 5:
            if self.w["greedy"]:
                k = min(range(len(hand)), key=lambda i: hand[i][1])
            else:
                k = max(range(len(hand)), key=lambda i: potential(st.orbits[p], hand[:i] + hand[i + 1:]) + self.r.random() * 1e-6)
            out.append(hand.pop(k))
        st.hands[p] = hand
        return out


class Random:
    def __init__(self, seed): self.r = random.Random(seed)
    def setup(self, st, p): return list(zip(self.r.sample(range(5), 2), self.r.sample(range(4), 2)))
    def draw(self, st, p): return self.r.choice(["deck", "deep"])
    def turn(self, st, p, rb):
        hand = st.hands[p]; plan = []
        if hand and self.r.random() < 0.85:
            k = 2 if (rb and len(hand) > 1 and self.r.random() < 0.7) else 1
            idx = self.r.sample(range(len(hand)), k); slots = self.r.sample(range(4), k)
            plan = list(zip(idx, slots))
        ne = [q for q in range(st.n) if any(st.orbits[q])] or [p]
        # a launch might fill an empty orbit; engine falls back to first nonempty
        return plan, (self.r.choice(ne), self.r.choice((CLOCK, CCW)))
    def discard(self, st, p):
        out = []
        while len(st.hands[p]) > 5: out.append(st.hands[p].pop(self.r.randrange(len(st.hands[p]))))
        return out


def mk(cls, **kw): return lambda seed: cls(seed, **kw)

MAKERS = {"random": Random, "greedy": mk(Heur, greedy=True), "strategic": mk(Heur)}
ABLATED = {
    "shield-blind": mk(Heur, shieldblind=True),
    "threat-blind": mk(Heur, threat=0.0, win_opp=0.0),
    "defence-check": mk(Heur, defence=0.12, expo=0.08),
    "self-spin-only": mk(Heur, selfonly=True),
    "comet-blind": mk(Heur, cometblind=True),
    "no-recall": mk(Heur, norecall=True),
}
# persona bots (panel). planner: careful + exposure-aware; instinct: noisy; optimiser: strongest (high exposure, wide search);
# flavour: loves captures and spinning rivals; cautious: self-spinning and safety first.
PERSONA = {
    "strategist": mk(Heur, expo=0.06, topk=10, threat=0.8),
    "casual": mk(Heur, noise=0.3, expo=0.0, topk=4),
    "competitor": mk(Heur, expo=0.05, topk=12, threat=1.0, win_opp=4.0),
    "story": mk(Heur, capt=0.25, noise=0.15, expo=0.01, threat=0.3),
    "family": mk(Heur, selfbias=0.15, hold_expo=1.5, threat=0.2, noise=0.1),
    "barraiser": mk(Heur, expo=0.07, topk=14, threat=1.0, win_opp=4.0),
}
