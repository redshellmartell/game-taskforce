"""Whiskerdark: full rules (rules.md v2). Standard library only.
A run is fully determined by the deal permutation, the Ghost set and the bot's choices."""
NAMES = ["", "Moth", "Mouse", "Spider", "Rat", "Crow", "Owl", "Snake", "Fox", "Hound"]
NB = [[q for q in (p - 3, p + 3, p - 1 if p % 3 else -1, p + 1 if p % 3 < 2 else -1) if 0 <= q < 9] for p in range(9)]
TRICKS = {1: "Glow", 2: "Dart", 3: "Silk", 4: "Scavenge", 5: "Carry", 7: "Hypnotise", 8: "Feint"}
READY, SPENT = 1, 2

class Config:
    def __init__(self, base_claws=2, anger=2, hunt="soft", hypno_cap=4, dart=3, ghost_hound=7,
                 hound_swap=True, escapes=2, cap=20, ghost_drop=2, carry_cut=2, thief=False, glow_free=True):
        self.base_claws, self.anger, self.hunt, self.hypno_cap = base_claws, anger, hunt, hypno_cap
        self.dart, self.ghost_hound, self.hound_swap, self.escapes, self.cap = dart, ghost_hound, hound_swap, escapes, cap
        self.ghost_drop, self.carry_cut = ghost_drop, carry_cut
DEFAULT = Config()

class Run:
    def __init__(self, perm, ghosts=(), cfg=DEFAULT, log=False):
        self.cfg = cfg
        self.g = list(perm)                       # card at each grid position, 0 = empty
        self.st = [0] * 10                        # 0 not in pack, 1 ready, 2 spent
        self.angry = [False] * 10
        self.ghost = [False] * 10
        for c in ghosts: self.ghost[c] = True
        self.known = [None] * 9                   # what the player knows about each position
        self.over = False; self.won = False; self.killer = None
        self.turns = 0; self.decisions = 0; self.log = [] if log else None
        self.stats = dict(tricks=[], beaten=[], shoved=[], thief=0, hunt=0, silk=0, carry_swap=0, drift=0, first=None, wise=0, fights=0, ever_ready=set(),
                          wise_ready_fights=0, ready_traj=[], feint_win=False, hypno_win=False, tricks_win=None)
        if cfg.hound_swap:
            i = self.g.index(9)
            if i < 3:
                self.g[i], self.g[i + 6] = self.g[i + 6], self.g[i]
                self.known[i + 6] = 9
        self.islit = [False] * 10
        self.relight()
        self.flags = {}
    def clone(self):
        n = Run.__new__(Run); n.__dict__.update(self.__dict__)
        n.g = list(self.g); n.st = list(self.st); n.angry = list(self.angry); n.known = list(self.known); n.islit = list(self.islit)
        n.flags = dict(self.flags); n.log = None
        s = dict(self.stats); s["tricks"] = list(s["tricks"]); s["beaten"] = list(s["beaten"]); s["shoved"] = list(s["shoved"])
        s["ever_ready"] = set(s["ever_ready"]); s["ready_traj"] = list(s["ready_traj"]); n.stats = s
        return n
    # ---- helpers
    def lit_pos(self, p): return self.g[p] != 0 and (p < 3 or any(self.g[q] == 0 for q in NB[p]))
    def relight(self):
        """Recompute Lit state from positions; returns the cards that just turned face up."""
        new = []
        for p in range(9):
            c = self.g[p]
            if not c: continue
            lit = self.lit_pos(p)
            if lit:
                self.known[p] = c
                if not self.islit[c]: new.append(c)
            self.islit[c] = lit
        return new
    def L(self, s):
        if self.log is not None: self.log.append("T%d %s" % (self.turns, s))
    def ready(self): return sum(1 for c in range(1, 10) if self.st[c] == READY)
    def claws(self): return self.cfg.base_claws + self.ready() + (2 if self.st[6] == READY else 0)
    def danger(self, c, dart=False, hypno=False, carry=False):
        d = max(c - self.cfg.ghost_drop, 0) if self.ghost[c] else c
        if self.angry[c]: d += self.cfg.anger
        if dart: d -= self.cfg.dart
        if carry: d -= self.cfg.carry_cut
        d = max(d, 0)
        if hypno: d = min(d, self.cfg.hypno_cap)
        return d
    def lit_cards(self): return [p for p in range(9) if self.g[p] and self.lit_pos(p)]
    def dark_cards(self): return [p for p in range(9) if self.g[p] and not self.lit_pos(p)]
    def pos_of(self, c): return self.g.index(c) if c in self.g else -1
    def spent_others(self, excl=4): return [c for c in range(1, 10) if self.st[c] == SPENT and c != excl]
    def deduce(self):
        """pos -> card for every position the player knows or can deduce by elimination."""
        k = {p: self.known[p] for p in range(9) if self.g[p] and self.known[p]}
        unk = [p for p in range(9) if self.g[p] and p not in k]
        rest = [c for c in self.g if c and c not in k.values()]
        if len(unk) == 1 and len(rest) == 1: k[unk[0]] = rest[0]
        return k
    def hound_pos(self):
        for p, c in self.deduce().items():
            if c == 9: return p
        return -1
    def spend(self, c):
        assert self.st[c] == READY; self.st[c] = SPENT
    # ---- tricks (phase 1)
    def can_trick(self, c):
        if self.st[c] != READY or c not in TRICKS or self.flags.get(c): return False
        if c == 1: return bool(self.dark_cards())
        if c == 4: return bool(self.spent_others())
        if c == 3: return bool(self.shovable()) and bool(self.dark_cards())
        return True
    def shovable(self): return [p for p in self.lit_cards() if not self.angry[self.g[p]]]
    def _use(self, c, spend=True):
        if spend: self.spend(c)
        self.flags[c] = True; self.stats["tricks"].append(c); self.decisions += 1
    def glow(self, p):
        self._use(1, spend=False)
        self.known[p] = self.g[p]; self.L("Glow sees %s at %d" % (NAMES[self.g[p]], p))
    def dart(self): self._use(2); self.flags["dart"] = True
    def hypno(self): self._use(7); self.flags["hypno"] = True
    def feint(self): self._use(8); self.flags["feint"] = True
    def scavenge(self, cards):
        self._use(4)
        for c in cards[:2]: self.st[c] = READY
        self.L("Scavenge readies %s" % [NAMES[c] for c in cards[:2]])
    def silk(self, px, py):
        """Free extra Shove (no Anger); Phase 2 action is still to come."""
        self._use(3); self.stats["silk"] += 1
        self._swap(px, py, anger=False); self.L("Silk shove %s into %d" % (NAMES[self.g[py]], py))
    def carry(self, p=None, q=None):
        """Spend the Crow; optional swap of two grid cards; then -2 on this turn's Fight."""
        self._use(5); self.flags["carry"] = True
        if p is not None:
            self.stats["carry_swap"] += 1
            self.g[p], self.g[q] = self.g[q], self.g[p]; self.known[p], self.known[q] = self.known[q], self.known[p]
            self.relight(); self.L("Carry swaps %d,%d" % (p, q))
    def drift(self, c):
        p = self.pos_of(c); self.g[p] = 0; self.known[p] = None; self.st[c] = READY
        self.stats["ever_ready"].add(c); self.stats["drift"] += 1; self.decisions += 1
        self.relight(); self.L("Drift %s" % NAMES[c])
    def driftable(self):
        return [c for c in (1, 2, 3) if self.ghost[c] and self.st[c] == 0 and c in self.g and self.lit_pos(self.pos_of(c))]
    # ---- actions
    def pay(self, n, bot):
        for _ in range(n):
            self.spend(bot.pick_spend(self))
    def thief(self, bot):
        if self.ready():
            self.pay(1, bot); self.stats["thief"] += 1; self.L("Thief spends a trophy")
    def fight(self, p, bot):
        c = self.g[p]; f = self.flags
        d = self.danger(c, f.get("dart"), f.get("hypno"), f.get("carry")); cl = self.claws()
        w = 0 if f.get("feint") else max(0, d - cl)
        self.stats["fights"] += 1
        if self.stats["first"] is None: self.stats["first"] = "fight"
        if self.st[6] == READY:
            self.stats["wise_ready_fights"] += 1
            if 0 if f.get("feint") else max(0, d - cl + 2) != w: self.stats["wise"] += 1
        self.L("Fight %s (danger %d, claws %d, wounds %d, ready %d)" % (NAMES[c], d, cl, w, self.ready()))
        self.decisions += 1
        if w > self.ready():
            self.over = True; self.killer = c; self.L("DEAD, killed by %s" % NAMES[c]); return
        self.pay(w, bot)
        if c == 9:
            self.over = self.won = True; self.stats["beaten"].append(9)
            self.stats["feint_win"] = bool(f.get("feint")); self.stats["hypno_win"] = bool(f.get("hypno")); self.L("ESCAPE"); return
        self.g[p] = 0; self.known[p] = None; self.angry[c] = False; self.st[c] = READY; self.stats["ever_ready"].add(c)
        self.stats["beaten"].append(c)
        self.relight()
    def _swap(self, px, py, anger):
        x, y = self.g[px], self.g[py]
        self.g[px], self.g[py] = y, x; self.known[px] = y; self.known[py] = x
        if anger: self.angry[x] = True
        self.stats["shoved"].append(x)
        self.relight()
    def shove(self, px, py, bot):
        if self.stats["first"] is None: self.stats["first"] = "shove"
        self.decisions += 1
        self._swap(px, py, True); self.L("Shove into %d, %s comes up" % (py, NAMES[self.g[px]]))
    # ---- turn
    def turn(self, bot):
        self.turns += 1; self.flags = {}
        for c in range(1, 10):
            if self.st[c] == READY: self.stats["ever_ready"].add(c)
        self.stats["ready_traj"].append(self.ready())
        bot.act(self)
        if self.over: return
        h = self.pos_of(9)
        if h >= 0 and not self.ghost[9] and self.lit_pos(h):
            if self.cfg.hunt == "lethal" and not self.ready():
                self.over = True; self.killer = 9; return
            if self.ready():
                self.pay(1, bot); self.stats["hunt"] += 1; self.L("Hunt spends a trophy")
    # ---- legal actions (used by random/greedy bots)
    def legal_actions(self):
        acts = [("fight", p) for p in self.lit_cards()]
        dk = self.dark_cards()
        if dk:
            acts += [("shove", p, q) for p in self.lit_cards() if not self.angry[self.g[p]] for q in dk]
        return acts

def play(perm, ghosts, bot, cfg=DEFAULT, log=False):
    r = Run(perm, ghosts, cfg, log)
    while not r.over and r.turns < cfg.cap:
        r.turn(bot)
    r.capped = not r.over
    return r
