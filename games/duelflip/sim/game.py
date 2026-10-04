"""Duel Flip rules engine, revision 2 rules (bait hurdle, bust gives whole river, no species, no refund).
Bot interface (all get (st, p)):
  keep_flipping(st,p)        after 2nd flip and later flips: True = flip again
  on_clash(st,p,card,hit_bait) -> 'buoy' or 'bust'   (only asked if Lifebuoy ready)
  leave(st,p,cands)          cands = indices into st.river (pile cards only; bait already resolved); return one index
st.bait = the bait card at turn start (or None); st.pile = this turn's cards; st.river = bait + pile during the turn.
"""
import random

class Config:
    def __init__(self, second_pts=3, claim_ge=False, extra=0, cap=500, log=False):
        self.second_pts = second_pts; self.claim_ge = claim_ge; self.extra = extra; self.cap = cap; self.log = log

class State:
    def __init__(self, cfg, rng):
        self.cfg = cfg
        self.deck = [(s, v) for s in range(6) for v in range(1, 11)]
        rng.shuffle(self.deck)
        self.river = []; self.pile = []; self.discard = []; self.bait = None
        self.haul = [[], []]; self.buoys = [1, 1]
        self.turn = 0; self.player = 0
        self.stats = dict(busts=0, bait_busts=0, buoy_used=[0, 0], flips=0, scout_discards=0,
                          bust_pile=[], bank_pile=[], left_vals=[], claims=0, claim_tries=0, bait_turns=0,
                          forced_empty_end=0, claim_by_val=[0]*11, bait_by_val=[0]*11)
        self.history = []; self.log = []
    def river_values(self): return {v for _, v in self.river}
    def deck_count(self, v): return sum(1 for _, x in self.deck if x == v)
    def hauls_value(self, p): return sum(v for _, v in self.haul[p])
    def score(self, p): return self.hauls_value(p) + (self.cfg.second_pts if p == 1 else 0)
    def say(self, msg):
        if self.cfg.log: self.log.append(msg)

NAMES = "Cr St Ur An Sn Ke".split()
def fmt(c): return "%s%d" % (NAMES[c[0]], c[1])

def play(cfg, bots, seed):
    rng = random.Random(seed); st = State(cfg, rng)
    bait_owner = None; S = st.stats
    while True:
        p = st.player; bot = bots[p]; o = 1 - p
        st.pile = []; busted = False
        st.bait = st.river[0] if st.river else None
        if st.bait: S["bait_turns"] += 1
        # first flip (safe scout)
        got = False
        while st.deck:
            c = st.deck.pop(); S["flips"] += 1
            if c[1] in st.river_values():
                st.discard.append(c); S["scout_discards"] += 1; continue
            st.river.append(c); st.pile.append(c); got = True; break
        if not got:
            S["forced_empty_end"] += 1
            if st.bait: st.haul[bait_owner].append(st.river.pop())
            break
        st.say("T%d P%d first %s%s" % (st.turn, p, fmt(c), (" (bait %s)" % fmt(st.bait)) if st.bait else ""))
        nflip = 1
        while st.deck:
            if nflip >= 2 and not bot.keep_flipping(st, p): break
            c = st.deck.pop(); S["flips"] += 1; nflip += 1
            if c[1] in st.river_values():
                st.discard.append(c)
                hit_bait = bool(st.bait) and st.bait[1] == c[1]
                choice = bot.on_clash(st, p, c, hit_bait) if st.buoys[p] > 0 else "bust"
                if choice == "buoy" and st.buoys[p] > 0:
                    st.buoys[p] -= 1; S["buoy_used"][p] += 1
                    st.say("T%d P%d flips %s CLASH -> Lifebuoy" % (st.turn, p, fmt(c))); break
                busted = True; S["busts"] += 1; S["bust_pile"].append(sum(v for _, v in st.pile))
                if hit_bait: S["bait_busts"] += 1
                st.haul[o].extend(st.river); st.say("T%d P%d flips %s CLASH -> BUST, opp takes %s" % (st.turn, p, fmt(c), [fmt(x) for x in st.river]))
                st.river = []; break
            st.river.append(c); st.pile.append(c); st.say("T%d P%d flips %s" % (st.turn, p, fmt(c)))
        if not busted:
            total = sum(v for _, v in st.pile)
            if st.bait:
                S["claim_tries"] += 1; S["bait_by_val"][st.bait[1]] += 1
                ok = total >= st.bait[1] if cfg.claim_ge else total > st.bait[1] + cfg.extra
                st.river.remove(st.bait)
                if ok:
                    st.haul[p].append(st.bait); S["claims"] += 1; S["claim_by_val"][st.bait[1]] += 1
                else: st.haul[o].append(st.bait)
                st.say("T%d P%d pile %d vs bait %s: %s" % (st.turn, p, total, fmt(st.bait), "claims" if ok else "fails, bait returns"))
            if len(st.pile) == 1:
                st.haul[p].append(st.river.pop()); st.say("T%d P%d banks single card" % (st.turn, p))
            else:
                i = bot.leave(st, p, list(range(len(st.river))))
                keep = st.river[i]
                st.haul[p].extend(x for j, x in enumerate(st.river) if j != i)
                S["left_vals"].append(keep[1]); S["bank_pile"].append(len(st.pile))
                st.river = [keep]; bait_owner = p
                st.say("T%d P%d banks, leaves %s" % (st.turn, p, fmt(keep)))
        st.pile = []; st.bait = None
        st.turn += 1
        st.history.append(st.hauls_value(0) - st.hauls_value(1) - cfg.second_pts)
        if not st.deck or st.turn >= cfg.cap: break
        st.player = o
    if st.river and bait_owner is not None: st.haul[bait_owner].append(st.river.pop())  # bait at end goes to owner
    s0, s1 = st.score(0), st.score(1)
    if s0 != s1: w = 0 if s0 > s1 else 1
    else:
        h0, h1 = len(st.haul[0]), len(st.haul[1])
        w = 0 if h0 > h1 else 1 if h1 > h0 else None
    return {"winner": w, "scores": (s0, s1), "turns": st.turn, "st": st, "tie": w is None,
            "scoretie": s0 == s1, "capped": bool(st.deck) and st.turn >= cfg.cap}
