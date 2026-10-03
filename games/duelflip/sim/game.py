"""Duel Flip v2 rules engine. Interpretations are listed in playtest-report.md.
Bot interface (all get (st, p)):
  keep_flipping(st,p)        after 2nd flip and later flips: True = flip again
  on_clash(st,p,card,hit_bait) -> 'buoy' or 'bust'   (buoy only offered if ready)
  leave(st,p,cands)          cands = indices into st.river of own-pile cards; return one index
"""
import random

SPECIES = 6

class Config:
    def __init__(self, buoys=(1, 1), bonus=8, second_pts=3, refund_at=4, mandatory_second=True,
                 safe_first=True, take_leftovers=True, nvalues=10, cap=500, log=False):
        self.buoys = buoys; self.bonus = bonus; self.second_pts = second_pts
        self.refund_at = refund_at; self.mandatory_second = mandatory_second
        self.safe_first = safe_first; self.take_leftovers = take_leftovers
        self.nvalues = nvalues; self.cap = cap; self.log = log

class State:
    def __init__(self, cfg, rng):
        self.cfg = cfg
        self.deck = [(s, v) for s in range(SPECIES) for v in range(1, cfg.nvalues + 1)]
        rng.shuffle(self.deck)
        self.river = []; self.pile = []; self.discard = []
        self.haul = [[], []]
        self.buoys = list(cfg.buoys)
        self.turn = 0; self.player = 0
        self.first_pile_flips = 0
        self.stats = dict(busts=0, bust_bait=0, buoy_used=[0, 0], refunds=[0, 0], flips=0,
                          scout_discards=0, bust_pile=[], bank_pile=[], left_vals=[], left_taken_gain=0,
                          small_busts=0, turns_pile1=0, bait_clash_busts=0, bust_by_pile=[0]*12,
                          bait_left_n=0, forced_empty_end=0)
        self.history = []; self.log = []
    def river_values(self): return {v for _, v in self.river}
    def deck_count(self, v): return sum(1 for _, x in self.deck if x == v)
    def hauls_value(self, p): return sum(v for _, v in self.haul[p])
    def leftovers(self): return [c for c in self.river if c not in self.pile]
    def score(self, p):
        o = 1 - p; sc = self.hauls_value(p)
        for s in range(SPECIES):
            a = sum(1 for x, _ in self.haul[p] if x == s)
            b = sum(1 for x, _ in self.haul[o] if x == s)
            if a > b: sc += self.cfg.bonus
        if p == 1: sc += self.cfg.second_pts
        return sc
    def say(self, msg):
        if self.cfg.log: self.log.append(msg)

def fmt(c): return "%s%d" % ("CSUASK"[c[0]], c[1])  # C S U A S(nail) K  -> see NAMES
NAMES = "Cr St Ur An Sn Ke".split()
def fmt(c): return "%s%d" % (NAMES[c[0]], c[1])

def play(cfg, bots, seed):
    rng = random.Random(seed)
    st = State(cfg, rng)
    ended_early = False
    while True:
        p = st.player; bot = bots[p]; o = 1 - p
        st.pile = []
        busted = False
        left_before = list(st.river)
        # ---- first flip
        if not st.deck:
            ended_early = True; break
        got = False
        while st.deck:
            c = st.deck.pop(); st.stats["flips"] += 1
            if cfg.safe_first and c[1] in st.river_values():
                st.discard.append(c); st.stats["scout_discards"] += 1; continue
            if not cfg.safe_first and c[1] in st.river_values():
                st.deck.append(c); break  # (unused variant)
            st.river.append(c); st.pile.append(c); got = True; break
        if not got:
            ended_early = True; st.stats["forced_empty_end"] += 1; break
        st.say("T%d P%d first %s" % (st.turn, p, fmt(c)))
        # ---- further flips
        nflip = 1
        while True:
            if not st.deck: break
            if nflip >= 2 or not cfg.mandatory_second:
                if not bot.keep_flipping(st, p): break
            c = st.deck.pop(); st.stats["flips"] += 1; nflip += 1
            if c[1] in st.river_values():
                st.discard.append(c)
                hit_bait = any(x[1] == c[1] for x in st.river if x not in st.pile)
                choice = "bust"
                if st.buoys[p] > 0:
                    choice = bot.on_clash(st, p, c, hit_bait)
                if choice == "buoy" and st.buoys[p] > 0:
                    st.buoys[p] -= 1; st.stats["buoy_used"][p] += 1
                    st.say("T%d P%d flips %s CLASH -> buoy" % (st.turn, p, fmt(c)))
                    break
                busted = True
                st.stats["busts"] += 1
                pv = sum(v for _, v in st.pile)
                st.stats["bust_pile"].append(pv)
                st.stats["bust_by_pile"][min(len(st.pile), 11)] += 1
                if len(st.pile) == 1: st.stats["small_busts"] += 1
                give = list(st.pile)
                if hit_bait:
                    st.stats["bait_clash_busts"] += 1
                    for x in list(st.river):
                        if x not in st.pile and x[1] == c[1]:
                            give.append(x); st.river.remove(x)
                for x in st.pile: st.river.remove(x)
                st.haul[o].extend(give)
                st.say("T%d P%d flips %s CLASH%s -> BUST, opp gets %s" % (st.turn, p, fmt(c), "(bait)" if hit_bait else "", [fmt(x) for x in give]))
                break
            st.river.append(c); st.pile.append(c)
            st.say("T%d P%d flips %s" % (st.turn, p, fmt(c)))
        # ---- bank
        if not busted:
            if len(st.river) == 1:
                # ambiguity: cannot leave one and take others; we take it
                st.haul[p].append(st.river.pop())
            else:
                cands = [i for i, x in enumerate(st.river) if x in st.pile] if cfg.take_leftovers else list(range(len(st.river)))
                i = bot.leave(st, p, cands)
                assert i in cands
                keep = st.river[i]
                took = [x for j, x in enumerate(st.river) if j != i]
                st.haul[p].extend(took)
                st.stats["left_vals"].append(keep[1])
                st.stats["bank_pile"].append(len(st.pile))
                if len(st.pile) >= cfg.refund_at and st.buoys[p] == 0:
                    st.buoys[p] = 1; st.stats["refunds"][p] += 1
                st.river = [keep]
                st.say("T%d P%d banks %s leaves %s" % (st.turn, p, [fmt(x) for x in took], fmt(keep)))
        st.pile = []
        st.turn += 1
        st.history.append(st.hauls_value(0) - st.hauls_value(1))
        if not st.deck or st.turn >= cfg.cap: break
        st.player = o
    s0, s1 = st.score(0), st.score(1)
    if s0 > s1: w = 0
    elif s1 > s0: w = 1
    else:
        h0, h1 = len(st.haul[0]), len(st.haul[1])
        w = 0 if h0 > h1 else 1
    return {"winner": w, "scores": (s0, s1), "turns": st.turn, "st": st, "tie": s0 == s1,
            "capped": bool(st.deck) and st.turn >= cfg.cap}
