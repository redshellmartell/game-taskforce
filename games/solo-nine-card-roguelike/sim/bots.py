"""Bots for Whiskerdark (rules v2): random, greedy, strategic (outline), lookahead, and one bot per panel persona (PERSONA)."""
import random
from game import NB, NAMES, READY, SPENT

SPEND_ORDER = [2, 5, 3, 4, 7, 1, 6, 8]          # rules v2 outline: Mouse, Crow, Spider, Rat, Snake, Moth, Owl, Fox
SMALL = (1, 2, 3)

def dist(p, q): return abs(p // 3 - q // 3) + abs(p % 3 - q % 3)

class Random:
    """Rules v2: each Ready trick / Drift in card order is used with probability 1/2; then a uniform legal action."""
    name = "random"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def pick_spend(self, r): return self.rng.choice([c for c in range(1, 10) if r.st[c] == READY])
    def act(self, r):
        rg = self.rng
        for c in range(1, 10):
            if c in r.driftable() and rg.random() < 0.5: r.drift(c)
            if r.can_trick(c) and rg.random() < 0.5:
                if c == 1: r.glow(rg.choice(r.dark_cards()))
                elif c == 2: r.dart()
                elif c == 3: r.silk(rg.choice(r.shovable()), rg.choice(r.dark_cards()))
                elif c == 4:
                    so = r.spent_others(); rg.shuffle(so); r.scavenge(so[:2])
                elif c == 5:
                    if rg.random() < 0.5:
                        p, q = rg.sample([x for x in range(9) if r.g[x]], 2); r.carry(p, q)
                    else: r.carry()
                elif c == 7: r.hypno()
                elif c == 8: r.feint()
        a = rg.choice(r.legal_actions())
        if a[0] == "fight": r.fight(a[1], self)
        else: r.shove(a[1], a[2], self)

class Greedy:
    name = "greedy"
    def __init__(self, seed=0): pass
    def pick_spend(self, r): return [c for c in range(1, 10) if r.st[c] == READY][0]
    def act(self, r):
        lit = r.lit_cards(); cl = r.claws(); rd = r.ready()
        ok = [p for p in lit if max(0, r.danger(r.g[p]) - cl) <= rd]
        if ok:
            r.fight(min(ok, key=lambda p: (r.danger(r.g[p]), p)), self); return
        sh = [p for p in lit if not r.angry[r.g[p]]]; dk = r.dark_cards()
        if sh and dk:
            r.shove(max(sh, key=lambda p: (r.danger(r.g[p]), -p)), min(dk), self); return
        r.fight(max(lit, key=lambda p: r.g[p]), self)

class Strategic:
    """The designer's v2 outline (rules.md section 7), deterministic. `off` = set of ablated features:
    glow dart silk scav carry swap hypno feint drift shove owlfirst hide."""
    name = "strategic"
    def __init__(self, seed=0, off=(), hide=True, look=True, push=True, use_strike=True, noise=0.0):
        self.off = set(off); self.hide, self.look, self.push, self.use_strike, self.noise = hide, look, push, use_strike, noise
        self.rng = random.Random(seed)
    def ok(self, k): return k not in self.off
    def pick_spend(self, r):
        order = ([6] + SPEND_ORDER) if "owlfirst" in self.off else SPEND_ORDER
        so = len(r.spent_others())
        for c in order:
            if r.st[c] == READY and not (c == 4 and so >= 2): return c
        return [c for c in range(1, 10) if r.st[c] == READY][0]
    # --- evaluation
    def fight_eval(self, r, p, dart=False, hypno=False, feint=False, scav=None, carry=False):
        """(survives, wounds, ready_after_pay) fighting position p; newly used tricks cost a trophy, flags already set are free."""
        f = r.flags; rd = r.ready(); owl = r.st[6] == READY
        if scav:
            rd += len(scav) - 1
            if 6 in scav: owl = True
        for t, used, key in ((2, dart, "dart"), (7, hypno, "hypno"), (8, feint, "feint"), (5, carry, "carry")):
            if used and not f.get(key):
                rd -= 1
                if t == 6: owl = False
        dart, hypno, feint, carry = (dart or f.get("dart"), hypno or f.get("hypno"), feint or f.get("feint"), carry or f.get("carry"))
        c = r.g[p]; d = r.danger(c, dart, hypno, carry)
        cl = r.cfg.base_claws + rd + (2 if owl else 0)
        w = 0 if feint else max(0, d - cl)
        return (w <= rd, w, rd - w)
    def strike_plan(self, r, p):
        """Cheapest trick set making the Hound fight survivable, or None."""
        so = [c for c in r.spent_others() if c != 4 and not r.flags.get(c)]
        tr = [t for t in (7, 8, 2, 5) if r.st[t] == READY and self.ok({7: "hypno", 8: "feint", 2: "dart", 5: "carry"}[t]) and not r.flags.get(t)]
        sc_opts = [None]
        if r.st[4] == READY and so and self.ok("scav") and not r.flags.get(4):
            pr = sorted(so, key=lambda c: [8, 7, 6, 2, 5].index(c) if c in (8, 7, 6, 2, 5) else 9)
            sc_opts.append(pr[:2])
        best = None
        for sc in sc_opts:
            avail = list(tr) + [c for c in (sc or []) if c in (7, 8, 2, 5) and self.ok({7: "hypno", 8: "feint", 2: "dart", 5: "carry"}[c])]
            for mask in range(1 << len(avail)):
                use = [avail[i] for i in range(len(avail)) if mask >> i & 1]
                ok, w, left = self.fight_eval(r, p, 2 in use, 7 in use, 8 in use, sc, 5 in use)
                if ok:
                    cost = len(use) + (1 if sc else 0)
                    if best is None or cost < best[0]: best = (cost, sc, use)
        return best
    def use_tricks(self, r, use):
        for t in use: {2: r.dart, 7: r.hypno, 8: r.feint, 5: r.carry}[t]()
    # --- targets
    def hide_target(self, r):
        empt = [p for p in range(9) if r.g[p] == 0]; best = None
        for p in r.dark_cards():
            m = min([dist(p, e) for e in empt] + [p // 3])
            if best is None or (m, p) > best[0]: best = ((m, p), p)
        return best[1] if best else None
    def shove_target(self, r):
        dd = r.deduce(); dk = [p for p in r.dark_cards() if dd.get(p) != 9]
        if not dk: return None
        good = [p for p in dk if p in dd and r.danger(dd[p]) <= r.claws()]
        if good: return min(good, key=lambda p: (r.danger(dd[p]), p))
        unk = [p for p in dk if p not in dd]
        return min(unk) if unk else min(dk)
    # --- phase 1 helpers
    def drift_step(self, r):
        if not self.ok("drift"): return
        for c in r.driftable():
            p = r.pos_of(c); hp = r.hound_pos()
            if hp >= 0 and r.g[hp] and not r.lit_pos(hp) and hp in NB[p] and r.ready() < 3: continue
            r.drift(c)
    def glow_step(self, r):
        if not (self.look and self.ok("glow") and r.can_trick(1)): return
        dd = r.deduce(); unk = [p for p in r.dark_cards() if p not in dd]
        if not unk: return
        plan = self.grow_choice(r, r.lit_cards()); tg = [q for q in NB[plan] if q in unk] if plan is not None else []
        r.glow(min(tg) if tg else min(unk))
    def act(self, r):
        if self.noise and self.rng.random() < self.noise:
            return Random.act(self, r)
        for _ in range(8):
            self.drift_step(r)
            if r.over or self.step(r): return
        if not r.acted:
            lit = r.lit_cards(); hp = r.pos_of(9)
            r.fight(hp if hp in lit else max(lit, key=lambda p: r.g[p]), self)
    def step(self, r):
        """One pass of outline steps 3-9; returns True once the Phase 2 action is taken."""
        self.drift_step(r); self.glow_step(r)
        lit = r.lit_cards(); hp = r.pos_of(9); hlit = hp >= 0 and hp in lit
        if r.st[4] == READY and self.ok("scav") and not r.flags.get(4) and len([c for c in r.spent_others() if not r.flags.get(c)]) >= 2:
            so = sorted([c for c in r.spent_others() if not r.flags.get(c)], key=lambda c: [8, 7, 6, 2, 3, 5, 1].index(c) if c in (8, 7, 6, 2, 3, 5, 1) else 9)
            r.scavenge(so[:2])
        # Strike
        if hlit and self.use_strike:
            plan = self.strike_plan(r, hp)
            if plan:
                cost, sc, use = plan
                if sc: r.scavenge(sc)
                self.use_tricks(r, use); r.fight(hp, self); return True
        # Hide
        if hlit and self.hide and self.ok("hide") and r.ready() < 3:
            tgt = self.hide_target(r)
            if tgt is not None:
                if not r.angry[9] and r.dark_cards() and self.ok("shove"):
                    if self.ok("silk") and r.can_trick(3):
                        r.silk(hp, tgt); return False
                    r.shove(hp, tgt, self); return True
                if r.angry[9] and r.can_trick(5) and self.ok("carry") and self.ok("swap"):
                    r.carry(hp, tgt); return False
        # Grow
        g = self.grow_choice(r, lit)
        if g is not None:
            r.fight(g, self); return True
        # Push
        if self.push:
            best = None
            for p in lit:
                c = r.g[p]
                if c == 9: continue
                for dart in ((False, True) if r.can_trick(2) and self.ok("dart") else (False,)):
                    for carry in ((False, True) if r.can_trick(5) and self.ok("carry") else (False,)):
                        ok, w, left = self.fight_eval(r, p, dart=dart, carry=carry)
                        if ok and left >= 1:
                            net = (2 if c in (7, 8) else 1) - w - dart - carry
                            key = (net, -p, not dart, not carry)
                            if best is None or key > best[0]: best = (key, p, dart, carry)
            if best:
                if best[2]: r.dart()
                if best[3]: r.carry()
                r.fight(best[1], self); return True
        # Shove
        sh = r.shovable(); tgt = self.shove_target(r)
        if sh and tgt is not None and self.ok("shove"):
            x = max(sh, key=lambda p: (r.danger(r.g[p]), -p))
            if self.ok("silk") and r.can_trick(3):
                r.silk(x, tgt); return False
            r.shove(x, tgt, self); return True
        # Forced
        best = None
        for p in lit:
            for dart in ((False, True) if r.can_trick(2) and self.ok("dart") else (False,)):
                ok, w, left = self.fight_eval(r, p, dart=dart)
                if ok:
                    key = (1, (2 if r.g[p] in (7, 8) else 1) - w - dart, -p)
                    if best is None or key > best[0]: best = (key, p, dart)
        if best:
            if best[2]: r.dart()
            r.fight(best[1], self); return True
        if hlit: r.fight(hp, self)
        else: r.fight(max(lit, key=lambda p: r.g[p]), self)
        return True
    def grow_choice(self, r, lit):
        cands = []; dd = r.deduce(); cl = r.claws(); rd = r.ready(); f = r.flags
        for p in lit:
            c = r.g[p]
            if c == 9 or r.danger(c, f.get("dart"), f.get("hypno"), f.get("carry")) > cl: continue
            dark_n = [q for q in NB[p] if r.g[q] and not r.lit_pos(q)]
            hits_hound = any(dd.get(q) == 9 for q in dark_n)
            if hits_hound and rd + 1 < 4: continue
            unk = sum(1 for q in dark_n if q not in dd)
            hound_unknown = r.hound_pos() < 0
            cands.append(((unk if hound_unknown else 0), -r.danger(c), p))
        if not cands: return None
        return min(cands)[2]

# ---------------------------------------------------------------- persona bots
class Planner(Strategic):
    """strategist: strategic outline, plus Glow whenever the Hound is unknown (looks ahead, gathers information)."""
    name = "planner"
class Instinct(Strategic):
    """casual: gut feel. Mostly sensible, but acts on a random legal move 25% of the time and never counts cards."""
    name = "instinct"
    def __init__(self, seed=0): super().__init__(seed, hide=False, look=False, noise=0.25)
class Optimiser(Strategic):
    """competitor: strongest line, tries the Hound strike as early as any plan allows; same engine as the outline."""
    name = "optimiser"
class Flavour(Strategic):
    """story: dramatic moves. Always charges the Hound when lit, even if it is fatal; takes big fights (Snake/Fox) for the tale."""
    name = "flavour"
    def __init__(self, seed=0): super().__init__(seed, hide=False, look=False)
    def step(self, r):
        lit = r.lit_cards(); hp = r.pos_of(9)
        if hp in lit and r.ready() >= 2:
            for t in (8, 7):
                if r.st[t] == READY: (r.feint if t == 8 else r.hypno)()
            r.fight(hp, self); return True
        big = [p for p in lit if r.g[p] in (7, 8) and self.fight_eval(r, p)[0] and self.fight_eval(r, p)[2] >= 1]
        if big:
            r.fight(max(big, key=lambda p: r.g[p]), self); return True
        return super().step(r)
class Cautious(Strategic):
    """family: safe and simple. Only takes clean fights, shoves otherwise, never uses tricks except Silk; never gambles."""
    name = "cautious"
    def __init__(self, seed=0): super().__init__(seed, hide=False, look=False, push=False, use_strike=False)
    def step(self, r):
        lit = r.lit_cards(); hp = r.pos_of(9)
        if hp in lit and self.fight_eval(r, hp)[0] and r.ready() >= 3:
            r.fight(hp, self); return True
        ok = [p for p in lit if r.g[p] != 9 and r.danger(r.g[p]) <= r.claws()]
        if ok:
            r.fight(max(ok, key=lambda p: (-r.danger(r.g[p]) , -p)), self); return True   # smallest fight first
        sh = [p for p in lit if not r.angry[r.g[p]]]; dk = r.dark_cards()
        if sh and dk:
            r.shove(max(sh, key=lambda p: (r.danger(r.g[p]), -p)), min(dk), self); return True
        return Strategic.step(self, r)
class Expert(Strategic):
    """barraiser: strongest line (the outline) with Glow and push enabled; probes the same engine."""
    name = "expert"

PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}


class _Scripted(Strategic):
    """Applies a scripted first turn (pre-actions, then a Phase 2 action or 'auto'), then plays on with the outline."""
    def __init__(self, opt, off=()): super().__init__(0, off=off); self.opt = opt
    def act(self, r):
        if self.opt is None: return super().act(r)
        o, self.opt = self.opt, None
        for a in o["pre"]:
            k = a[0]
            if k == "scav": r.scavenge(a[1])
            elif k == "dart": r.dart()
            elif k == "hypno": r.hypno()
            elif k == "feint": r.feint()
            elif k == "carry": r.carry(*a[1:])
            elif k == "silk": r.silk(a[1], a[2])
        if o["kind"] == "fight": r.fight(o["p"], self)
        elif o["kind"] == "shove": r.shove(o["p"], o["q"], self)
        else: super().act(r)

class Lookahead(Strategic):
    """Determinised Monte Carlo: samples the hidden cards consistent with what the player knows, tries each candidate
    first move (with its tricks, Silk shoves, Carry with or without a swap) followed by the outline, and plays the option
    that wins most often. `off` removes trick options (ablations). Carry's swap options: pull a known Hound away."""
    name = "lookahead"
    K = 12
    def __init__(self, seed=0, K=None, off=()):
        super().__init__(seed, off=off); self.rng = random.Random(seed)
        if K: self.K = K
    def options(self, r):
        lit = r.lit_cards(); dk = r.dark_cards(); dd = r.deduce(); opts = []
        scav = [None]
        if r.can_trick(4) and self.ok("scav"):
            so = sorted([c for c in r.spent_others() if not r.flags.get(c)], key=lambda c: [8, 7, 6, 2, 3, 5, 1].index(c) if c in (8, 7, 6, 2, 3, 5, 1) else 9)[:2]
            if so: scav.append(so)
        unk = [q for q in dk if q not in dd]; far = self.hide_target(r)
        ys = [q for q in dk if q in dd and dd[q] != 9] + ([q for q in unk if q == far] + [q for q in unk if q != far][:2])
        hp = r.pos_of(9)
        for sc in scav:
            pre = [] if not sc else [("scav", sc)]
            def has(t, nm): return self.ok(nm) and (r.st[t] == READY or (sc and t in sc)) and not r.flags.get(t)
            sets = [[]]
            for t, nm, a in ((2, "dart", ("dart",)), (7, "hypno", ("hypno",)), (8, "feint", ("feint",)), (5, "carry", ("carry",))):
                if has(t, nm): sets.append([a])
            if has(2, "dart") and has(5, "carry"): sets.append([("dart",), ("carry",)])
            for p in lit:
                for ts in sets: opts.append(dict(kind="fight", p=p, pre=pre + ts))
            if not sc:
                if self.ok("shove"):
                    for p in [x for x in lit if not r.angry[r.g[x]]]:
                        for q in ys:
                            opts.append(dict(kind="shove", p=p, q=q, pre=[]))
                            if r.can_trick(3) and self.ok("silk"):
                                opts.append(dict(kind="auto", pre=[("silk", p, q)]))
                if has(5, "carry") and self.ok("swap") and hp >= 0 and hp in lit and far is not None:
                    opts.append(dict(kind="auto", pre=[("carry", hp, far)]))
        return opts
    def sample(self, r):
        c = r.clone(); dd = r.deduce()
        up = [p for p in range(9) if r.g[p] and p not in dd]
        cards = [r.g[p] for p in up]; self.rng.shuffle(cards)
        for p, x in zip(up, cards): c.g[p] = x
        return c
    def act(self, r):
        self.drift_step(r); self.glow_step(r)
        opts = self.options(r)
        if len(opts) == 1: best = opts[0]
        else:
            worlds = [self.sample(r) for _ in range(self.K)]
            score = [0.0] * len(opts)
            for w in worlds:
                for i, o in enumerate(opts):
                    c = w.clone(); c.flags = dict(r.flags); c.turns = 0
                    b = _Scripted(o, self.off)
                    try:
                        while not c.over and c.turns < 30:
                            if c.turns == 0: c.turns = 1; c.stats["ready_traj"].append(c.ready()); b.act(c); (c.over or c.finish_turn(b))
                            else: c.turn(b)
                    except (AssertionError, ValueError, IndexError): score[i] -= 1; continue
                    score[i] += c.won - 0.001 * c.turns
            best = opts[max(range(len(opts)), key=lambda i: score[i])]
        for a in best["pre"]:
            k = a[0]
            if k == "scav": r.scavenge(a[1])
            elif k == "dart": r.dart()
            elif k == "hypno": r.hypno()
            elif k == "feint": r.feint()
            elif k == "carry": r.carry(*a[1:])
            elif k == "silk": r.silk(a[1], a[2])
        if best["kind"] == "fight": r.fight(best["p"], self)
        elif best["kind"] == "shove": r.shove(best["p"], best["q"], self)
        else: Strategic.act(self, r)
