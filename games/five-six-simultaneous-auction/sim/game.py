"""Last Bid Standing simulation (rules v3, revision 2: face-down income, Hype ceiling +4). Standard library only.
Interpretations (see report): lots are taken from a fixed shuffled deck two per round; the first bidder picks a lot;
passers draw after resolution; the discard pile is reshuffled into the deck only when a draw is needed and the deck is empty.
"""
import random
from dataclasses import dataclass, field

CATS = 4
@dataclass
class Config:
    players: int = 6
    rounds: int = 14
    start_hand: int = 4
    income: int = 2
    bid_max: int = 11            # bid values 1..bid_max per category
    lot_bonus: int = 0           # added to every printed lot value (tuning knob)
    bubble: str = "crash"        # "crash" or "halve"
    hype_cap: int = 4            # v3: max Hype bonus per lot (0 = no cap)
    log: bool = False

LOT_VALUES = [2, 2, 3, 3, 4, 4, 5]

class State:
    def __init__(self, cfg, rng):
        self.cfg, self.rng, self.n = cfg, rng, cfg.players
        lots = [(c, v + cfg.lot_bonus) for c in range(CATS) for v in LOT_VALUES]
        rng.shuffle(lots)
        self.lotdeck = lots
        bids = [(c, v) for c in range(CATS) for v in range(1, cfg.bid_max + 1)]
        rng.shuffle(bids)
        self.hands = [[bids.pop() for _ in range(cfg.start_hand)] for _ in range(self.n)]
        self.biddeck, self.discard = bids, []
        self.hype = [[] for _ in range(CATS)]
        self.won = [[] for _ in range(self.n)]
        self.unsold = []
        self.known = [[] for _ in range(self.n)]   # public: income cards drawn and still in hand
        self.round = 0
        self.block = []
        self.log = []
        self.leaders = []            # provisional unique leader (or -1) after each round
        self.stats = dict(cancelled=0, unsold=0, nodraw=0, reshuffles=0, forced_pass=0, passes=0, bids=0,
                          burned=[0] * CATS, nostand_rounds=0, hand_sum=0, hand_obs=0, sec=0.0, block_sum=0)
        self.plays = [dict(pass_=0, bid=[0] * (cfg.bid_max + 1)) for _ in range(self.n)]
        self.lotwins_by_bid = [0] * (cfg.bid_max + 1)
        self.score_hist = []
        self.cancelled_by = [0] * self.n
        self.crash_before_last = None
        self.leader_before_last = None

    def hype_counts(self):
        return [len(r) for r in self.hype]

    def crashed(self):
        """Exactly one category crashes (rules 6.2): most Hype, then bid-value total, then highest cards, then fixed order."""
        h = self.hype_counts()
        if max(h) == 0: return set()
        key = lambda c: (h[c], sum(v for _, v in self.hype[c]), sorted((v for _, v in self.hype[c]), reverse=True), -c)
        return {max(range(CATS), key=key)}

    def scores(self):
        h = self.hype_counts(); cr = self.crashed()
        eff = [(0 if c in cr and self.cfg.bubble == "crash" else (h[c] // 2 if c in cr else h[c])) for c in range(CATS)]
        if self.cfg.hype_cap: eff = [min(x, self.cfg.hype_cap) for x in eff]
        return [sum(v + eff[c] for c, v in w) for w in self.won], eff

    def provisional_leader(self):
        s, _ = self.scores(); m = max(s)
        top = [i for i in range(self.n) if s[i] == m]
        return top[0] if len(top) == 1 else -1

    def income(self, passers):
        """Rules 5 'Income procedure'. Returns (reshuffled, K). Drawn cards become public (st.known)."""
        P = len(passers)
        if P == 0: return False, 0
        resh = False
        if len(self.biddeck) < 2 * P:
            self.biddeck = self.biddeck + self.discard; self.discard = []; self.rng.shuffle(self.biddeck)
            self.stats["reshuffles"] += 1; resh = True
        K = min(2, len(self.biddeck) // P)
        if K == 0: self.stats["nodraw"] += 1
        for _ in range(K):
            for p in passers:
                c = self.biddeck.pop(); self.hands[p].append(c)  # v3: face down, not public
        return resh, K

def play(cfg, bots, seed):
    rng = random.Random(seed); st = State(cfg, rng); n = st.n
    for r in range(cfg.rounds):
        st.round = r + 1
        if r == cfg.rounds - 1:
            st.leader_before_last = st.provisional_leader(); st.crash_before_last = st.crashed()
        st.block = st.block + [st.lotdeck.pop(), st.lotdeck.pop()]; st.stats['block_sum'] += len(st.block)
        choice = []
        for p in range(n):
            st.stats["hand_sum"] += len(st.hands[p]); st.stats["hand_obs"] += 1
            if not st.hands[p]:
                st.stats["forced_pass"] += 1; choice.append(None); continue
            i = bots[p].bid(st, p)
            choice.append(None if i is None or i < 0 else i)
        played = {}
        for p in range(n):
            if choice[p] is None:
                st.plays[p]["pass_"] += 1; st.stats["passes"] += 1
            else:
                card = st.hands[p][choice[p]]; played[p] = card
                st.plays[p]["bid"][card[1]] += 1; st.stats["bids"] += 1
        for p in sorted(played, reverse=True):      # remove from hands
            st.hands[p].pop(choice[p])
            if played[p] in st.known[p]: st.known[p].remove(played[p])
        cnt = {}
        for p, (c, v) in played.items(): cnt[v] = cnt.get(v, 0) + 1
        stand = sorted([p for p, (c, v) in played.items() if cnt[v] == 1], key=lambda p: -played[p][1])
        st.stats["cancelled"] += sum(1 for p, (c, v) in played.items() if cnt[v] > 1)
        for p, (c, v) in played.items():
            if cnt[v] > 1: st.cancelled_by[p] += 1
        winners = stand[:2]
        lots = list(st.block)
        if len(winners) == 0: st.stats["nostand_rounds"] += 1
        for p in winners:                                   # first picks any lot, then second picks any remaining
            k = bots[p].pick(st, p, lots)
            st.won[p].append(lots.pop(k)); st.lotwins_by_bid[played[p][1]] += 1
        st.block = lots
        burned = 0
        for p, card in played.items():
            if p in winners: st.discard.append(card)
            else:
                st.hype[card[0]].append(card); st.stats["burned"][card[0]] += 1; burned += 1
        passers = [p for p in range(n) if choice[p] is None]
        st.income(passers)
        st.stats["sec"] += 25 + 15 + 4 * burned + 6 * len(winners) + 3 * 2 * len(passers)
        st.leaders.append(st.provisional_leader()); st.score_hist.append(st.scores()[0])
        if cfg.log:
            st.log.append("R%d lots %s bids %s -> winners %s, unsold %d, hype %s" % (
                r + 1, st.block, {p + 1: played[p] for p in played}, [w + 1 for w in winners], len(st.block), st.hype_counts()))
    st.stats["unsold"] = len(st.block)
    sc, eff = st.scores()
    # tiebreakers: cards in hand, then total value in hand
    key = [(sc[p], len(st.hands[p]), sum(v for _, v in st.hands[p])) for p in range(n)]
    best = max(key); win = [p for p in range(n) if key[p] == best]
    return dict(st=st, scores=sc, winners=win, eff=eff)
