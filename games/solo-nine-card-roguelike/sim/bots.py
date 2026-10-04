"""Bots for Nine Lives Dungeon: random, greedy, strategic, and one bot per panel persona (PERSONA)."""
import random
from game import NB, NAMES, READY, SPENT

SPEND_ORDER = [1, 3, 5, 2, 4, 7, 6, 8]

def dist(p, q): return abs(p // 3 - q // 3) + abs(p % 3 - q % 3)

class Random:
    name = "random"
    def __init__(self, seed=0): self.rng = random.Random(seed)
    def pick_spend(self, r): return self.rng.choice([c for c in range(1, 10) if r.st[c] == READY])
    def act(self, r):
        for c in (1, 2, 3, 4, 5, 7, 8):
            if r.can_trick(c) and self.rng.random() < 0.5:
                if c == 1:
                    d = r.dark_cards(); self.rng.shuffle(d)
                    for i, p in enumerate(d[:2]): r.glow(p)
                elif c == 2: r.dart()
                elif c == 3: r.silk()
                elif c == 4:
                    so = r.spent_others(); self.rng.shuffle(so); r.scavenge(so[:2])
                elif c == 5:
                    p, q = self.rng.sample([x for x in range(9) if r.g[x]], 2); r.carry(p, q)
                elif c == 7: r.hypno()
                elif c == 8: r.feint()
        a = self.rng.choice(r.legal_actions())
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
    """The designer's outline (rules.md section 7), deterministic. Variant switches are for experiments."""
    name = "strategic"
    def __init__(self, seed=0, hide=True, look=True, push=True, use_strike=True, noise=0.0):
        self.hide, self.look, self.push, self.use_strike, self.noise = hide, look, push, use_strike, noise
        self.rng = random.Random(seed)
    def pick_spend(self, r):
        rd = [c for c in range(1, 10) if r.st[c] == READY]
        so = len(r.spent_others())
        for c in SPEND_ORDER:
            if r.st[c] == READY and not (c == 4 and so >= 2): return c
        return rd[0]
    # --- evaluation
    def fight_eval(self, r, p, dart=False, hypno=False, feint=False, scav=None):
        """(survives, wounds, ready_after_pay) for fighting position p with the given tricks, tricks spent first."""
        rd = r.ready(); owl = r.st[6] == READY
        if scav:   # scavenge spends the Rat and readies `scav` spent cards (Owl may be one of them)
            rd += len(scav) - 1
            if 6 in scav: owl = True
        for t, used in ((2, dart), (7, hypno), (8, feint)):
            if used:
                rd -= 1
                if t == 6: owl = False
        c = r.g[p]; d = r.danger(c, dart, hypno)
        cl = r.cfg.base_claws + rd + (2 if owl else 0)
        w = 0 if feint else max(0, d - cl)
        return (w <= rd, w, rd - w)
    def strike_plan(self, r, p):
        """Cheapest trick set making the Hound fight survivable, or None."""
        so = [c for c in r.spent_others() if c != 4][:]
        opts = []
        tr = [t for t in (7, 8, 2) if r.st[t] == READY]
        sc_opts = [None]
        if r.st[4] == READY and so:
            # readying the cards that help most: Snake, Fox, Owl, Mouse, then any
            pr = sorted(so, key=lambda c: [8, 7, 6, 2].index(c) if c in (8, 7, 6, 2) else 9)
            sc_opts.append(pr[:2])
        best = None
        for sc in sc_opts:
            avail = list(tr) + [c for c in (sc or []) if c in (7, 8, 2)]
            for mask in range(1 << len(avail)):
                use = [avail[i] for i in range(len(avail)) if mask >> i & 1]
                # tricks readied by scavenge must come after it; fine since scavenge first
                if any(t in (sc or []) for t in use) and not sc: continue
                ok, w, left = self.fight_eval(r, p, 2 in use, 7 in use, 8 in use, sc)
                if ok:
                    cost = len(use) + (1 if sc else 0)
                    if best is None or cost < best[0]: best = (cost, sc, use)
        return best
    fix = False   # v2 fix: never shove into the space holding the known Hound (the outline loops on this), prefer a known clean card
    def far_dark(self, r, hide=True):
        empt = [p for p in range(9) if r.g[p] == 0]
        best = None; dd = r.deduce(); dk = r.dark_cards()
        if self.fix:
            if not hide:
                good = [p for p in dk if p in dd and dd[p] != 9 and r.danger(dd[p]) <= r.claws() and not r.angry[dd[p]]]
                if good: return min(good, key=lambda p: (r.danger(dd[p]), p))
            dk = [p for p in dk if dd.get(p) != 9] or dk
        for p in dk:
            m = min([dist(p, e) for e in empt] + [p // 3 + 0])     # doorway distance = row index
            if best is None or (m, p) > best[0]: best = ((m, p), p)
        return best[1] if best else None
    def act(self, r):
        if self.noise and self.rng.random() < self.noise:
            return Random.act(self, r)
        for _ in range(4):                                  # allow tricks to change the picture, then act
            if self.step(r): return
    def step(self, r):
        lit = r.lit_cards(); hp = r.pos_of(9); hlit = hp >= 0 and hp in lit
        # Scavenge when 2 spent others
        if r.st[4] == READY and len(r.spent_others()) >= 2 and not r.flags.get(4):
            so = sorted(r.spent_others(), key=lambda c: [8, 7, 6, 2, 3, 5, 1].index(c) if c in (8, 7, 6, 2, 3, 5, 1) else 9)
            r.scavenge(so[:2])
        # 2. Strike
        if hlit and self.use_strike:
            plan = self.strike_plan(r, hp)
            if plan:
                cost, sc, use = plan
                if sc: r.scavenge(sc)
                for t in use: {2: r.dart, 7: r.hypno, 8: r.feint}[t]()
                r.fight(hp, self); return True
        # 3. Hide
        if hlit and self.hide and r.ready() < 3:
            tgt = self.far_dark(r)
            if tgt is not None:
                if not r.angry[9] and r.dark_cards():
                    if r.can_trick(3): r.silk()
                    r.shove(hp, tgt, self); return True
                if r.angry[9] and r.can_trick(5):
                    r.carry(hp, tgt); lit = r.lit_cards(); hp = r.pos_of(9); hlit = hp in lit
        # 4. Look
        dd = r.deduce()
        if self.look and r.can_trick(1) and r.hound_pos() < 0 and r.ready() >= 2:
            unk = [p for p in r.dark_cards() if p not in dd]
            if len(unk) >= 3:
                plan = self.grow_choice(r, lit)
                tg = []
                if plan is not None: tg = [q for q in NB[plan] if q in unk]
                for q in sorted(unk): 
                    if q not in tg: tg.append(q)
                r.glow(tg[0]); 
                dd = r.deduce()
                if len(tg) > 1 and tg[1] not in dd: r.glow(tg[1])
        # 5. Grow
        g = self.grow_choice(r, lit)
        if g is not None:
            r.fight(g, self); return True
        # 6. Push
        if self.push:
            best = None
            for p in lit:
                c = r.g[p]
                if c == 9: continue
                for dart in ((False, True) if r.st[2] == READY and not r.flags.get(2) else (False,)):
                    ok, w, left = self.fight_eval(r, p, dart=dart)
                    if ok and left >= 1:
                        net = (2 if c in (7, 8) else 1) - w - (1 if dart else 0)
                        key = (net, -p, not dart)
                        if best is None or key > best[0]: best = (key, p, dart)
            if best:
                if best[2]: r.dart()
                r.fight(best[1], self); return True
        # 7. Shove
        sh = [p for p in lit if not r.angry[r.g[p]]]
        tgt = self.far_dark(r, hide=False)
        if sh and tgt is not None:
            x = max(sh, key=lambda p: (r.danger(r.g[p]), -p))
            if r.can_trick(3): r.silk()
            r.shove(x, tgt, self); return True
        # 8. Forced
        best = None
        for p in lit:
            for dart in ((False, True) if r.st[2] == READY and not r.flags.get(2) else (False,)):
                ok, w, left = self.fight_eval(r, p, dart=dart)
                if ok:
                    key = (1, (2 if r.g[p] in (7, 8) else 1) - w - (1 if dart else 0), -p)
                    if best is None or key > best[0]: best = (key, p, dart)
        if best:
            if best[2]: r.dart()
            r.fight(best[1], self); return True
        if hlit: r.fight(hp, self)
        else: r.fight(max(lit, key=lambda p: r.g[p]), self)
        return True
    def grow_choice(self, r, lit):
        cands = []; dd = r.deduce(); cl = r.claws(); rd = r.ready()
        for p in lit:
            c = r.g[p]
            if c == 9 or r.danger(c) > cl: continue
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
        big = [p for p in lit if r.g[p] in (7, 8) and r.fight_eval(r, p)[0]] if False else \
              [p for p in lit if r.g[p] in (7, 8) and self.fight_eval(r, p)[0] and self.fight_eval(r, p)[2] >= 1]
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
    """Applies a given first option, then plays on with the strategic outline."""
    def __init__(self, opt): super().__init__(0); self.opt = opt
    def act(self, r):
        if self.opt is not None:
            o, self.opt = self.opt, None
            for t in o["tricks"]:
                if t == "scav": r.scavenge(o["scav"])
                elif t == "dart": r.dart()
                elif t == "hypno": r.hypno()
                elif t == "feint": r.feint()
                elif t == "silk": r.silk()
            if o["kind"] == "fight": r.fight(o["p"], self)
            else: r.shove(o["p"], o["q"], self)
        else:
            super().act(r)

class Lookahead(Strategic):
    """Determinised Monte Carlo: samples the hidden cards consistent with what the player knows, tries each candidate
    first move (with its tricks) followed by the strategic outline, and plays the option that wins most often.
    Used to measure how winnable the game is by a much stronger player than the outline."""
    name = "lookahead"
    K = 12
    def __init__(self, seed=0, K=None):
        super().__init__(seed); self.rng = random.Random(seed)
        if K: self.K = K
    def options(self, r):
        lit = r.lit_cards(); dk = r.dark_cards(); dd = r.deduce(); opts = []
        scav = []
        if r.st[4] == READY and r.spent_others():
            so = sorted(r.spent_others(), key=lambda c: [8, 7, 6, 2, 3, 5, 1].index(c) if c in (8, 7, 6, 2, 3, 5, 1) else 9)[:2]
            scav = [None, so]
        else: scav = [None]
        unk = [q for q in dk if q not in dd]; far = self.far_dark(r)
        ys = [q for q in dk if q in dd] + ([q for q in unk if q == far] + [q for q in unk if q != far][:2])
        for sc in scav:
            pre = [] if not sc else ["scav"]
            for p in lit:
                base = list(pre)
                opts.append(dict(kind="fight", p=p, tricks=base, scav=sc))
                for t, nm in ((2, "dart"), (7, "hypno"), (8, "feint")):
                    if r.st[t] == READY or (sc and t in sc):
                        opts.append(dict(kind="fight", p=p, tricks=base + [nm], scav=sc))
            for p in lit:
                if r.angry[r.g[p]]: continue
                for q in ys:
                    opts.append(dict(kind="shove", p=p, q=q, tricks=list(pre), scav=sc))
                    if r.st[3] == READY: opts.append(dict(kind="shove", p=p, q=q, tricks=list(pre) + ["silk"], scav=sc))
        return opts
    def sample(self, r):
        c = r.clone(); dd = r.deduce()
        up = [p for p in range(9) if r.g[p] and p not in dd]
        cards = [r.g[p] for p in up]; self.rng.shuffle(cards)
        for p, x in zip(up, cards): c.g[p] = x
        return c
    def act(self, r):
        # keep the outline's Look step (Glow) because information is not valued by rollouts
        if r.can_trick(1) and r.hound_pos() < 0 and r.ready() >= 2:
            dd = r.deduce(); unk = [p for p in r.dark_cards() if p not in dd]
            if len(unk) >= 3:
                r.glow(unk[0]); dd = r.deduce()
                if unk[1] not in dd: r.glow(unk[1])
        opts = self.options(r)
        if len(opts) == 1: best = opts[0]
        else:
            worlds = [self.sample(r) for _ in range(self.K)]
            score = [0.0] * len(opts)
            for w in worlds:
                for i, o in enumerate(opts):
                    c = w.clone(); c.flags = {}
                    # a trick's validity is checked on the real state; apply to the sampled world
                    c.turns = 0
                    b = _Scripted(o)
                    try:
                        while not c.over and c.turns < 30: c.turn(b)
                    except AssertionError: score[i] -= 1; continue
                    score[i] += c.won - 0.001 * c.turns
            best = opts[max(range(len(opts)), key=lambda i: score[i])]
        for t in best["tricks"]:
            if t == "scav": r.scavenge(best["scav"])
            elif t == "dart": r.dart()
            elif t == "hypno": r.hypno()
            elif t == "feint": r.feint()
            elif t == "silk": r.silk()
        if best["kind"] == "fight": r.fight(best["p"], self)
        else: r.shove(best["p"], best["q"], self)

class Strategic2(Strategic):
    """Outline plus the shove-target fix."""
    name = "strategic2"
    fix = True
