"""Fifty-Two Workshop rules engine (rules.md v2, revision 1). Standard library only.
Cards are ints 0..51: suit = c // 13 (0 Spade/Spring, 1 Club/Gear, 2 Diamond/Jewel, 3 Heart/Clock face), rank = c % 13 + 1.
Interpretations (ambiguities) are listed in notes.py."""
import random

S, C, D, H = 0, 1, 2, 3
def rk(c): return c % 13 + 1
def su(c): return c // 13
def name(c): return "A23456789TJQK"[rk(c) - 1].replace("T", "10") + "SCDH"[su(c)]

class Config:
    def __init__(self, n=4, hand_limit=7, spade=4, spade_pts=1, diamond=3, bench=5, target_adj=0, solo_win=31, rival_pile=24, retool=True,
                 gear_gather=False, rival_take=2, start=None, log=False, cap=600):
        self.n = n; self.hand_limit = hand_limit; self.spade = spade; self.spade_pts = spade_pts; self.diamond = diamond
        self.bench = bench; self.solo_win = solo_win; self.rival_pile = rival_pile; self.retool = retool; self.rival_take = rival_take; self.gear_gather = gear_gather
        self.log = log; self.cap = cap
        self.target = {1: 99, 2: 11, 3: 10, 4: 10}[n] + target_adj
        self.start = start or [3] * n

def train_of(shop, r):
    """ranks of the train containing rank r (r need not be in shop yet)."""
    lo = r
    while lo - 1 in shop: lo -= 1
    hi = r
    while hi + 1 in shop: hi += 1
    return range(lo, hi + 1)

def groups(shop):
    out, cur = [], []
    for r in sorted(shop):
        if cur and r != cur[-1] + 1: out.append(cur); cur = []
        cur.append(r)
    if cur: out.append(cur)
    return out

def score_shop(shop, cfg):
    """shop: dict rank -> suit."""
    tot = 0
    for g in groups(shop):
        k = len({shop[r] for r in g})
        for r in g:
            s = shop[r]
            tot += cfg.spade_pts if s == S else 1 if s == C else cfg.diamond if s == D else 1 + k
    return tot

def longest(shop):
    return max((len(g) for g in groups(shop)), default=0)

class State:
    pass

def cost_of(cfg, shop, card):
    r = rk(card); tr = train_of(shop, r)
    sp = sum(1 for x in tr if x != r and shop[x] == S) + (1 if su(card) == S else 0)
    return max(0, r - cfg.spade * sp)

def legal_builds(st, p):
    """list of (card, cost) the player may build now."""
    shop = st.shops[p]; hand = st.hands[p]; tot = sum(rk(c) for c in hand); out = []
    for c in set(hand):
        if rk(c) in shop and not st.cfg.retool: continue
        cost = cost_of(st.cfg, shop, c)
        if tot - rk(c) >= cost: out.append((c, cost))
    out.sort()
    return out

def bench_cards(st): return [c for c, _ in st.bench]

def take_bench(st, p, i):
    c, who = st.bench.pop(i)
    if who is not None and who != p: st.inter[p] += 1
    st.hands[p].append(c); return c

def take_deck(st, p):
    c = st.deck.pop(); st.hands[p].append(c); return c

def refill(st):
    while len(st.bench) < st.cfg.bench and st.deck: st.bench.append((st.deck.pop(), None))

def trim(st):
    """Bench > 5: leftmost card goes face down to the bottom of the deck (deck top = end of list, bottom = index 0)."""
    while len(st.bench) > st.cfg.bench: st.deck.insert(0, st.bench.pop(0)[0])

def lg(st, s):
    if st.cfg.log: st.log.append(s)

def play(cfg, bots, seed):
    rng = random.Random(seed); n = cfg.n
    st = State(); st.cfg = cfg; st.n = n; st.log = []; st.rng = rng
    deck = list(range(52)); rng.shuffle(deck); st.deck = deck
    st.hands = [[deck.pop() for _ in range(cfg.start[i])] for i in range(n)]
    st.bench = [(deck.pop(), None) for _ in range(cfg.bench)]
    st.shops = [dict() for _ in range(n)]
    st.inter = [0] * n; st.dec = [0] * n; st.builds = [[] for _ in range(n)]; st.retool_log = [[] for _ in range(n)]; st.turns = [0] * n
    st.gathers = [0] * n; st.nbuild = [0] * n; st.rival = []; st.retools = 0; st.scrap = 0; st.struck_deck = False; st.passes = 0; st.errors = 0
    st.hist = []; st.rounds_hist = []; st.struck_by = None; st.bot_ids = [type(b).__name__ for b in bots]
    p = 0; total = 0; struck = False; capped = False
    while True:
        total += 1
        if total > cfg.cap: capped = True; break
        bot = bots[p]; hand = st.hands[p]; shop = st.shops[p]
        builds = legal_builds(st, p); can_g = bool(st.bench or st.deck)
        if not builds and not can_g:
            st.passes += 1; lg(st, "P%d passes" % (p + 1))
        else:
            act = None
            if builds and can_g:
                st.dec[p] += 1; act = bot.action(st, p, builds)
                if act is not None and act not in [b[0] for b in builds]: act = None; st.errors += 1
            elif builds: act = bot.action(st, p, builds) if len(builds) > 1 else builds[0][0]
            if act is not None and not builds: act = None
            if act is None and not can_g: act = builds[0][0]
            if act is None: gather(st, p, bot)
            else: build(st, p, bot, act)
        st.turns[p] += 1
        # end of turn
        while len(hand) > cfg.hand_limit:
            k = len(hand) - cfg.hand_limit; st.dec[p] += 1
            ds = list(bot.discard(st, p, k))
            if len(ds) != k or any(ds.count(c) > hand.count(c) for c in set(ds)):
                st.errors += 1; ds = sorted(hand, key=rk)[:k]
            for c in ds: hand.remove(c); st.scrap += 1
            lg(st, "P%d hand limit -> scrap: %s" % (p + 1, " ".join(name(c) for c in ds)))
        if n == 1 and st.bench:
            idx = sorted(range(len(st.bench)), key=lambda j: (-rk(st.bench[j][0]), j))[:cfg.rival_take]
            top = [st.bench[j][0] for j in idx]
            for j in sorted(idx, reverse=True): st.bench.pop(j)
            st.rival.append(top[0]); lg(st, "Rival removes %s, %s under the deck" % (name(top[0]), name(top[1]) if len(top) > 1 else "-"))
            for x in top[1:]: st.deck.insert(0, x)
        trim(st); refill(st)
        if not struck and ((len(st.rival) >= cfg.rival_pile if n == 1 else len(shop) >= cfg.target) or not st.deck):
            struck = True; st.struck_by = p; st.struck_deck = not st.deck; lg(st, "THE CLOCK STRIKES (P%d, %d cards, deck %d)" % (p + 1, len(shop), len(st.deck)))
            if n == 1 or p == n - 1: break
        elif struck and p == n - 1: break
        p = (p + 1) % n
        if p == 0: st.rounds_hist.append([score_shop(s, cfg) for s in st.shops])
    scores = [score_shop(s, cfg) for s in st.shops]
    key = [(scores[i], len(st.shops[i]), longest(st.shops[i])) for i in range(n)]
    best = max(key); winners = [i for i in range(n) if key[i] == best]
    return dict(st=st, scores=scores, winners=winners, turns=total, capped=capped,
                tie=len(winners) > 1, scoretie=sum(1 for s in scores if s == max(scores)) > 1)

def gather(st, p, bot):
    k = 2
    if st.cfg.gear_gather:
        sh = st.shops[p]
        if any(sh[r] == C and len(train_of(sh, r)) >= 2 for r in sh): k = 3
    got = []
    for _ in range(k):
        opts = len(st.bench) + (1 if st.deck else 0)
        if opts == 0: break
        if opts > 1: st.dec[p] += 1
        i = bot.gather_pick(st, p)
        if i == -1 and st.deck: got.append(name(take_deck(st, p)) + "(deck)")
        elif 0 <= i < len(st.bench): got.append(name(take_bench(st, p, i)))
        else:
            st.errors += 1
            if st.bench: got.append(name(take_bench(st, p, 0)))
            else: got.append(name(take_deck(st, p)))
    st.gathers[p] += 1
    lg(st, "P%d gathers %s" % (p + 1, " ".join(got)))

def build(st, p, bot, card):
    cfg = st.cfg; shop = st.shops[p]; hand = st.hands[p]; r = rk(card)
    cost = cost_of(cfg, shop, card); hand.remove(card)
    retool = r in shop
    if retool: st.scrap += 1; st.retools += 1; st.retool_log[p].append((shop[r], su(card)))
    shop[r] = su(card)
    tr = train_of(shop, r); clubs = sum(1 for x in tr if shop[x] == C)
    took = []
    for _ in range(clubs):
        if st.bench:
            if len(st.bench) > 1: st.dec[p] += 1
            i = bot.gear_pick(st, p)
            if not 0 <= i < len(st.bench): st.errors += 1; i = 0
            took.append(name(take_bench(st, p, i)))
        elif st.deck: took.append(name(take_deck(st, p)) + "(deck)")
    paid = []
    if cost > 0:
        st.dec[p] += 1
        pay = list(bot.pay(st, p, cost))
        if sum(rk(c) for c in pay) < cost or any(pay.count(c) > hand.count(c) for c in set(pay)):
            st.errors += 1; pay = []; tot = 0
            for c in sorted(hand, key=lambda c: -rk(c)):
                if tot >= cost: break
                pay.append(c); tot += rk(c)
        for c in pay: hand.remove(c); st.bench.append((c, p))
        paid = pay
    st.builds[p].append(card); st.nbuild[p] += 1
    lg(st, "P%d %s %s (train %d-%d, cost %d)%s%s" % (p + 1, "retools" if retool else "builds", name(card), tr[0], tr[-1], cost,
       (" gears take " + " ".join(took)) if took else "", (" pays " + " ".join(name(c) for c in paid)) if paid else ""))
