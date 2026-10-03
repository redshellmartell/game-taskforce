"""Duel Flip rules engine. Interpretations are listed in playtest-report.md."""
import random

SPECIES = 6
VALUES = 10

class Config:
    def __init__(self, buoys=(1, 2), bonus=5, buoy_value=2, nvalues=10, cap=500, second_pts=0):
        self.second_pts = second_pts
        self.buoys = buoys          # (first player, second player)
        self.bonus = bonus
        self.buoy_value = buoy_value
        self.nvalues = nvalues
        self.cap = cap

class State:
    def __init__(self, cfg, rng):
        self.cfg = cfg
        self.deck = [(s, v) for s in range(SPECIES) for v in range(1, cfg.nvalues + 1)]
        rng.shuffle(self.deck)
        self.river = []              # list of (species, value)
        self.pile = []               # cards flipped this turn (subset of river)
        self.discard = []
        self.haul = [[], []]
        self.buoys = list(cfg.buoys)
        self.turn = 0
        self.player = 0
        self.stats = {"busts": 0, "buoys_used": [0, 0], "pushes": 0, "flips": 0}
        self.history = []            # score diff (p0-p1) on hauls after each turn

    def river_values(self):
        return {v for _, v in self.river}

    def deck_count(self, v):
        return sum(1 for _, x in self.deck if x == v)

    def hauls_value(self, p):
        return sum(v for _, v in self.haul[p])

    def score(self, p):
        o = 1 - p
        sc = self.hauls_value(p)
        for s in range(SPECIES):
            a = sum(1 for x, _ in self.haul[p] if x == s)
            b = sum(1 for x, _ in self.haul[o] if x == s)
            if a > b:
                sc += self.cfg.bonus
        sc += self.cfg.buoy_value * self.buoys[p]
        if p == 1: sc += self.cfg.second_pts
        return sc

def play(cfg, bots, seed):
    """bots = (bot_for_first, bot_for_second). Returns result dict."""
    rng = random.Random(seed)
    st = State(cfg, rng)
    while True:
        p = st.player
        bot = bots[p]
        if not st.deck:
            break
        st.pile = []
        busted = False
        first = True
        while True:
            if not st.deck:
                break
            if not first and not bot.keep_flipping(st, p):
                break
            card = st.deck.pop()
            first = False
            st.stats["flips"] += 1
            if card[1] in st.river_values():
                st.discard.append(card)
                if st.buoys[p] > 0 and bot.use_buoy(st, p, card):
                    st.buoys[p] -= 1
                    st.stats["buoys_used"][p] += 1
                    break
                busted = True
                st.stats["busts"] += 1
                if not st.pile: st.stats["dead"] = st.stats.get("dead", 0) + 1
                for c in st.pile:
                    st.river.remove(c)
                    st.haul[1 - p].append(c)
                break
            st.river.append(card)
            st.pile.append(card)
        if not busted:
            if len(st.river) == 1:
                st.haul[p].append(st.river.pop())
            elif len(st.river) >= 2:
                i = bot.leave(st, p)
                keep = st.river[i]
                st.haul[p].extend(c for j, c in enumerate(st.river) if j != i)
                st.river = [keep]
        st.pile = []
        st.turn += 1
        st.history.append(st.hauls_value(0) - st.hauls_value(1))
        if not st.deck or st.turn >= cfg.cap:
            break
        st.player = 1 - p
    s0, s1 = st.score(0), st.score(1)
    if s0 > s1: w = 0
    elif s1 > s0: w = 1
    else:
        h0, h1 = len(st.haul[0]), len(st.haul[1])
        w = 0 if h0 > h1 else 1 if h1 > h0 else 1
    return {"winner": w, "scores": (s0, s1), "turns": st.turn, "st": st,
            "tie": s0 == s1, "capped": st.turn >= cfg.cap and st.deck}
