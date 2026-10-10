"""Bots for Heavenly Bodies: random, greedy, strategic, plus one bot per test-panel persona (PERSONA)."""
import random
from game import total_size, card_value, rot_value, eval_orbit, gen_one


def keepv(c):
    """How much a card in hand is worth keeping (higher = keep)."""
    if c["type"] == "CO": return 1.5 + 0.5 * c["size"]
    if c["damage_max"] > 0: return 3.0 + c["damage_max"]
    return 2.0


class Random:
    name = "random"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def choose_action(self, st, i, acts):
        k = self.rng.randrange(len(acts) + 1)
        return acts[k] if k < len(acts) else None
    def pick(self, st, i, kind, opts, may=False):
        if not opts: return None
        k = self.rng.randrange(len(opts) + (1 if may else 0))
        return opts[k][0] if k < len(opts) else None
    def pick_opp(self, st, i, ops, why): return self.rng.choice(ops)
    def discard_pick(self, st, i, pool): return self.rng.choice(pool)
    def rot_dir(self, st, i, q=None): return self.rng.choice((1, -1))      # q None = own Rotation Phase; else a card rotation of orbit q


def dead_cards(st, i):
    return [c for c in st.P[i].hand if c["type"] == "AE" and not gen_one(st, i, c)]


class Greedy(Random):
    name = "greedy"
    w_north = 0.0
    def rot_dir(self, st, i, q=None):
        own = q is None or q == i
        qq = i if q is None else q
        vp, vm = rot_value(st, qq, 1, q is not None, self.w_north if own else 0.0), rot_value(st, qq, -1, q is not None, self.w_north if own else 0.0)
        if not own: vp, vm = -vp, -vm
        if abs(vp - vm) < 1e-9: return self.rng.choice((1, -1))
        return 1 if vp > vm else -1
    def score(self, st, i, a):
        f = a["fx"]
        if a["kind"] == "recycle": return 0.6 if dead_cards(st, i) else 0.0
        if f["kill"]: return 1000
        v = 3 * f["dmg"] + f["size"] + 1.5 * f["knock"] - 3 * f["self_dmg"] - f["lose"] + 0.5 * f["draw"] - 0.5 * f["cost"] + 0.2 * f["stab"] + f["fut"] + 1.0 * f["heal"]
        return v
    def choose_action(self, st, i, acts):
        best = max(acts, key=lambda a: self.score(st, i, a) + self.rng.random() * 0.01)
        return best if self.score(st, i, best) > 0 else None
    def pick(self, st, i, kind, opts, may=False):
        if not opts: return None
        o = max(opts, key=lambda t: t[1])
        if may and o[1] <= 0: return None
        return o[0]
    def pick_opp(self, st, i, ops, why): return min(ops, key=lambda q: st.P[q].hp)
    def discard_pick(self, st, i, pool): return min(pool, key=keepv)


class Strategic(Greedy):
    name = "strategic"
    w_dmg = 1.0; w_cm = 1.0; w_def = 1.0; w_self = 1.0; eps = 0.0; w_card = 1.0; thresh = 0.3; w_flair = 0.0; w_cost = 1.0
    soften = False; w_north = 0.35; recycle_ok = True
    def __init__(self, seed=0, **kw):
        super().__init__(seed)
        for k, v in kw.items(): setattr(self, k, v)

    def threat(self, st, q):
        p = st.P[q]; ts = total_size(st, q)
        return 100 if p.cm else max(0, ts - (p.thr - 4)) * 3

    def score(self, st, i, a):
        f = a["fx"]; p = st.P[i]; v = 0.0
        t = f["tgt"]
        if a["kind"] == "recycle":
            if not self.recycle_ok: return -1.0
            return 1.0 if dead_cards(st, i) else (0.45 if len(p.hand) >= 6 else 0.0)
        pos = a["params"].get("pos") if a["params"] else None
        if pos == 0 and self.w_north and a["kind"] in ("co", "ae"):       # placing into the exposed North position
            cc = a["card"] if a["card"] and a["card"]["type"] == "CO" else a["params"].get("co")
            if isinstance(cc, dict) and cc.get("type") == "CO": v -= self.w_north * cc["size"] * (1.0 if cc["stability"] <= 2 else 0.4)
        if f["kill"] and not self.soften: return 1000
        if f["dmg"] and t is not None:
            hp = st.P[t].hp
            v += self.w_dmg * f["dmg"] * (1 + 3.0 / max(hp, 1)) * 1.6
            v += self.w_def * 0.0
        if f["self_dmg"]: v -= f["self_dmg"] * 2.5 * (1 + 3.0 / max(p.hp, 1)) * (2 if self.soften else 1)
        my = total_size(st, i); thr = p.thr
        prog = 1 + my / thr
        v += self.w_cm * f["size"] * 1.3 * prog
        if my + f["size"] >= thr > my: v += 8 * self.w_cm
        if p.cm and my + f["size"] < thr: v -= 100
        if p.cm and f["size"] + my >= thr and f["lose"] == 0: v += 4
        v -= f["lose"] * 1.3 * self.w_cm * prog
        v += 0.35 * f["stab"] * self.w_def
        if t is not None and (f["knock"] or f["osize"]):
            th = self.threat(st, t)
            k = f["knock"] * 2.2 + (-f["osize"]) * 0.5
            v += k * (1 + th / 10.0) * self.w_def
            q = st.P[t]
            if q.cm and total_size(st, t) + f["osize"] < q.thr: v += 60 * self.w_def
        v += self.w_card * 1.0 * f["draw"] - self.w_cost * 1.2 * f["cost"]
        v += 1.1 * f["fut"] + 1.4 * f["heal"] * (1 + 2.0 / max(p.hp, 1))
        if a["kind"] == "free" and a["name"] == "ST01":
            pool = p.hand
            return 1.0 if pool and min(keepv(c) for c in pool) < 2.5 else 0.0
        if a["kind"] == "free" and a["name"] == "ST02": return 0.0
        if self.w_flair:
            if f["coll"] in ("win", "lose"): v += self.w_flair * 2
            if a["name"] in ("AE28", "AE25", "AE40", "AE60", "AE38"): v += self.w_flair * 3
            if a["kind"] == "ae" and a["card"] and a["card"]["id"] in ("AE44", "AE45", "AE46") : v += self.w_flair * 3
        return v

    def choose_action(self, st, i, acts):
        if self.eps and self.rng.random() < self.eps:
            k = self.rng.randrange(len(acts) + 1)
            return acts[k] if k < len(acts) else None
        best = max(acts, key=lambda a: self.score(st, i, a) + self.rng.random() * 0.01)
        return best if self.score(st, i, best) > self.thresh else None

    def pick_opp(self, st, i, ops, why):
        if self.soften: return max(ops, key=lambda q: st.P[q].hp)
        return max(ops, key=lambda q: self.threat(st, q) - st.P[q].hp * 0.8 + self.rng.random() * 0.01)

    def pick(self, st, i, kind, opts, may=False):
        if self.eps and self.rng.random() < self.eps: return Random.pick(self, st, i, kind, opts, may)
        return Greedy.pick(self, st, i, kind, opts, may)


class Planner(Strategic):       # strategist: long game, builds size and defence, keeps a card engine
    name = "planner"; w_cm = 1.25; w_def = 1.2; w_card = 1.4


class Instinct(Strategic):      # casual: gut feel, noisy
    name = "instinct"; eps = 0.22; w_flair = 0.4


class Optimiser(Strategic):     # competitor: strongest line, takes every kill, shuts down CM
    name = "optimiser"; w_dmg = 1.2; w_def = 1.3


class Flavour(Strategic):       # story: dramatic plays (collisions, sacrifices, reclaims)
    name = "flavour"; eps = 0.1; w_flair = 1.5; w_cost = 0.5


class Cautious(Strategic):      # family: avoids self-harm, soft blows, builds safely
    name = "cautious"; eps = 0.12; w_dmg = 0.7; soften = True; w_cost = 1.8


class Expert(Strategic):        # bar raiser: strongest line, probes for degenerate/cheap lines (here: balanced attack + defence)
    name = "expert"; w_dmg = 1.15; w_cm = 1.15; w_def = 1.4; w_card = 1.2


class AlwaysCW(Strategic):      # ablation: always rotates clockwise (rotation direction is never a decision)
    name = "always_cw"
    def rot_dir(self, st, i, q=None): return 1


class IgnoreNorth(Strategic):   # ablation: ignores North exposure (direction and placement)
    name = "ignore_north"; w_north = 0.0


class NoRecycle(Strategic):     # ablation: never uses Recycle
    name = "no_recycle"; recycle_ok = False


class NoMull(Strategic):        # ablation: never takes the free mulligan
    name = "no_mull"; mull = False


class NoBurst(Strategic):       # ablation: never plays AE25 / AE28 (tests whether their winning link is causal)
    name = "no_burst"
    def choose_action(self, st, i, acts):
        acts = [a for a in acts if not (a["card"] and a["card"]["id"] in ("AE25", "AE28"))]
        return Strategic.choose_action(self, st, i, acts) if acts else None


class CMFirst(Strategic):       # sensitivity: builds Critical Mass first
    name = "cm_first"; w_cm = 1.7; w_dmg = 0.6


class DmgFirst(Strategic):      # sensitivity: damage first
    name = "dmg_first"; w_cm = 0.6; w_dmg = 1.7


PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}
STANDARD = {"random": Random, "greedy": Greedy, "strategic": Strategic}
ABL = {"always_cw": AlwaysCW, "ignore_north": IgnoreNorth, "no_recycle": NoRecycle, "no_mull": NoMull, "no_burst": NoBurst, "cm_first": CMFirst, "dmg_first": DmgFirst}
