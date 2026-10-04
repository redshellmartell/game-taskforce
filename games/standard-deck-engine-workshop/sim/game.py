"""Fifty-Two Workshop rules engine (rules.md v1). Standard library only.
Cards are ints 0..51: suit = c // 13 (0 Spade/Spring, 1 Club/Gear, 2 Diamond/Jewel, 3 Heart/Clock face), rank = c % 13 + 1.
Interpretations (ambiguities) are listed in notes.py."""
import random

S, C, D, H = 0, 1, 2, 3
def rk(c): return c % 13 + 1
def su(c): return c // 13
def name(c): return "A23456789TJQK"[rk(c) - 1].replace("T", "10") + "SCDH"[su(c)]

class Config:
    def __init__(self, n=4, hand_limit=7, spade=3, diamond=3, bench=5, target_adj=0, solo_win=22, start=None, log=False, cap=600):
        self.n = n; self.hand_limit = hand_limit; self.spade = spade; self.diamond = diamond
        self.bench = bench; self.solo_win = solo_win; self.log = log; self.cap = cap
        self.target = {1: 11, 2: 11, 3: 10, 4: 9}[n] + target_adj
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

def score_shop(shop, dia=3):
    """shop: dict rank -> suit."""
    tot = 0
    for g in groups(shop):
        k = len({shop[r] for r in g})
        for r in g:
            s = shop[r]
            tot += 1 if s in (S, C) else dia if s == D else 1 + k
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
        if rk(c) in shop: continue
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

def lg(st, s):
    if st.cfg.log: st.log.append(s)

def play(cfg, bots, seed):
    rng = random.Random(seed); n = cfg.n
    st = State(); st.cfg = cfg; st.n = n; st.log = []; st.rng = rng
    deck = list(range(52)); rng.shuffle(deck); st.deck = deck
    st.hands = [[deck.pop() for _ in range(cfg.start[i])] for i in range(n)]
    st.bench = [(deck.pop(), None) for _ in range(cfg.bench)]
    st.shops = [dict() for _ in range(n)]
    st.inter = [0] * n; st.dec = [0] * n; st.builds = [[] for _ in range(n)]; st.turns = [0] * n
    st.gathers = [0] * n; st.nbuild = [0] * n; st.rival = []; st.apprentice = 0; st.passes = 0; st.errors = 0
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
            ds = bot.discard(st, p, k)
            ds = list(ds)
            if len(ds) != k or any(ds.count(c) > hand.count(c) for c in set(ds)):
                st.errors += 1; ds = sorted(hand, key=rk)[:k]
            for c in ds: hand.remove(c); st.bench.append((c, p))
            lg(st, "P%d hand limit -> Bench: %s" % (p + 1, " ".join(name(c) for c in ds)))
        if n == 1 and st.bench:
            i = max(range(len(st.bench)), key=lambda j: (rk(st.bench[j][0]), -j))
            st.rival.append(st.bench.pop(i)[0]); lg(st, "Rival removes %s" % name(st.rival[-1]))
        refill(st)
        if not struck and (len(shop) >= cfg.target or not st.deck):
            struck = True; st.struck_by = p; lg(st, "THE CLOCK STRIKES (P%d, %d cards, deck %d)" % (p + 1, len(shop), len(st.deck)))
            if n == 1 or p == n - 1: break
        elif struck and p == n - 1: break
        p = (p + 1) % n
        if p == 0: st.rounds_hist.append([score_shop(s, cfg.diamond) for s in st.shops])
    scores = [score_shop(s, cfg.diamond) for s in st.shops]
    key = [(scores[i], len(st.shops[i]), longest(st.shops[i])) for i in range(n)]
    best = max(key); winners = [i for i in range(n) if key[i] == best]
    return dict(st=st, scores=scores, winners=winners, turns=total, capped=capped,
                tie=len(winners) > 1, scoretie=sum(1 for s in scores if s == max(scores)) > 1)

def gather(st, p, bot):
    k = 2
    if st.n > 1 and len(st.shops[p]) < min(len(st.shops[q]) for q in range(st.n) if q != p): k = 3; st.apprentice += 1
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
    cost = cost_of(cfg, shop, card); hand.remove(card); shop[r] = su(card)
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
    lg(st, "P%d builds %s (train %d-%d, cost %d)%s%s" % (p + 1, name(card), tr[0], tr[-1], cost,
       (" gears take " + " ".join(took)) if took else "", (" pays " + " ".join(name(c) for c in paid)) if paid else ""))
