"""Last Bid Standing simulation (rules v1). Standard library only.
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
    income: int = 1
    bid_max: int = 10            # bid values 1..bid_max per category
    lot_bonus: int = 0           # added to every printed lot value (tuning knob)
    bubble: str = "crash"        # "crash" or "halve"
    log: bool = False

LOT_VALUES = [1, 1, 2, 2, 3, 3, 4]

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
        self.round = 0
        self.block = []
        self.log = []
        self.leaders = []            # provisional unique leader (or -1) after each round
        self.stats = dict(cancelled=0, unsold=0, nodraw=0, reshuffles=0, forced_pass=0, passes=0, bids=0,
                          burned=[0] * CATS, nostand_rounds=0, hand_sum=0, hand_obs=0, sec=0.0)
        self.plays = [dict(pass_=0, bid=[0] * (cfg.bid_max + 1)) for _ in range(self.n)]
        self.lotwins_by_bid = [0] * (cfg.bid_max + 1)
        self.crash_before_last = None
        self.leader_before_last = None

    def hype_counts(self):
        return [len(r) for r in self.hype]

    def crashed(self):
        h = self.hype_counts(); m = max(h)
        return {c for c in range(CATS) if h[c] == m and m > 0}

    def scores(self):
        h = self.hype_counts(); cr = self.crashed()
        eff = [(0 if c in cr and self.cfg.bubble == "crash" else (h[c] // 2 if c in cr else h[c])) for c in range(CATS)]
        return [sum(v + eff[c] for c, v in w) for w in self.won], eff

    def provisional_leader(self):
        s, _ = self.scores(); m = max(s)
        top = [i for i in range(self.n) if s[i] == m]
        return top[0] if len(top) == 1 else -1

    def draw(self, p):
        if not self.biddeck:
            self.rng.shuffle(self.discard); self.biddeck, self.discard = self.discard, []
            self.stats["reshuffles"] += 1
        self.hands[p].append(self.biddeck.pop())

def play(cfg, bots, seed):
    rng = random.Random(seed); st = State(cfg, rng); n = st.n
    for r in range(cfg.rounds):
        st.round = r + 1
        if r == cfg.rounds - 1:
            st.leader_before_last = st.provisional_leader(); st.crash_before_last = st.crashed()
        st.block = [st.lotdeck.pop(), st.lotdeck.pop()]
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
        cnt = {}
        for p, (c, v) in played.items(): cnt[v] = cnt.get(v, 0) + 1
        stand = sorted([p for p, (c, v) in played.items() if cnt[v] == 1], key=lambda p: -played[p][1])
        st.stats["cancelled"] += sum(1 for p, (c, v) in played.items() if cnt[v] > 1)
        winners = stand[:2]
        lots = list(st.block)
        if len(winners) >= 1:
            p1 = winners[0]; k = bots[p1].pick(st, p1, lots)
            st.won[p1].append(lots[k]); st.lotwins_by_bid[played[p1][1]] += 1; other = lots[1 - k]; lots = [other]
            if len(winners) == 2:
                p2 = winners[1]; st.won[p2].append(other); st.lotwins_by_bid[played[p2][1]] += 1; lots = []
        else:
            st.stats["nostand_rounds"] += 1
        for l in lots: st.unsold.append(l); st.stats["unsold"] += 1
        burned = 0
        for p, card in played.items():
            if p in winners: st.discard.append(card)
            else:
                st.hype[card[0]].append(card); st.stats["burned"][card[0]] += 1; burned += 1
        passers = [p for p in range(n) if choice[p] is None]
        for _ in range(cfg.income):
            if passers and len(st.biddeck) + len(st.discard) < len(passers):
                st.stats["nodraw"] += 1; break
            for p in passers: st.draw(p)
        st.stats["sec"] += 25 + 15 + 4 * burned + 6 * (2 - len(lots))
        st.leaders.append(st.provisional_leader())
        if cfg.log:
            st.log.append("R%d lots %s bids %s -> winners %s, unsold %d, hype %s" % (
                r + 1, st.block, {p + 1: played[p] for p in played}, [w + 1 for w in winners], len(lots), st.hype_counts()))
    sc, eff = st.scores()
    # tiebreakers: cards in hand, then total value in hand
    key = [(sc[p], len(st.hands[p]), sum(v for _, v in st.hands[p])) for p in range(n)]
    best = max(key); win = [p for p in range(n) if key[p] == best]
    return dict(st=st, scores=sc, winners=win, eff=eff)
