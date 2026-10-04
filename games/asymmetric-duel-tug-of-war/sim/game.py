"""Tug of Crowns rules v1. Seat 0 = Treasurer, seat 1 = Whisperer. Crown pos: -4 (T throne) .. +4 (W throne).
Interpretations (ambiguities) are listed in AMBIGUITIES."""
import random

# name: (copies, inf, keywords)
T_DECK = {"Tax Collector": (4, 2, "bank"), "Granary": (2, 3, "bank"), "Ledger": (3, 3, "steady"),
          "Gold Purse": (3, 4, ""), "Mint Master": (2, 5, ""), "Royal Loan": (2, 1, "spend2"),
          "Patron": (2, 2, "spend1 steady"), "Treasury Vault": (1, 1, "spend3 steady"),
          "Chancellor's Seal": (1, 6, "steady")}
W_DECK = {"Gossip": (4, 1, "echo"), "Shadow Envoy": (1, 2, "echo retort"), "Courtier": (3, 3, ""),
          "Spymaster": (2, 4, ""), "Silencer": (3, 1, "hush"), "The Whisper": (1, 5, "hush"),
          "False Witness": (2, 1, "hush retort"), "Eavesdropper": (2, 2, "retort"), "Veiled Threat": (2, 3, "retort")}

AMBIGUITIES = [
    "Hushing a card with Spend: bonus is lost, but the coins were already discarded (rules say so implicitly; assumed).",
    "Retort: Whisperer who has passed but whose opponent then passes: contest ends. If T has passed and W has not, W keeps playing alone; assumed W may still pass afterwards.",
    "Does a Retort card played after pass count as a decision when the Treasurer then passes? Assumed no Retort after T's pass (as written).",
    "Court-rule margin applies to the leader at start of Phase 4; a leader who wins by 1 at pos 2/3 ties - the rules never say whether this counts as 'lost' for choosing the next lead chooser (assumed: tie -> same chooser).",
    "Position 0 after round 7: 'most recent round that moved the crown' - assumed per rules; Echo 'tied' counts as not won (as written).",
    "Lead change count and 'leader' at pos 0 for trailer draws: no extra draws at 0 (as written).",
    "Draw pile exhaustion is routine (deck of 20, 6 start + 2/round + extras): rules do not say what happens to Whisperer's Echo-return cards when the game is already effectively out of cards (nothing; fine).",
    "A player who passed with cards in hand may not re-enter (T), but W may via Retort only after T plays a card; T playing a card after W passed with no Retort in hand just continues.",
]

def card_list(deck):
    out = []
    for name, (n, inf, kw) in deck.items():
        for _ in range(n): out.append((name, inf, kw))
    return out

class State:
    def __init__(self, seed, log=False):
        self.rng = random.Random(seed)
        self.pos = 0
        self.draw = [card_list(T_DECK), card_list(W_DECK)]
        for d in self.draw: self.rng.shuffle(d)
        self.hand = [[self.draw[p].pop() for _ in range(6)] for p in (0, 1)]
        self.discard = [[], []]
        self.treasury = 0
        self.row = [[], []]          # entries: dict(card, bonus, hushed)
        self.passed = [False, False]
        self.rnd = 1
        self.chooser = 0
        self.history = []            # crown pos after each round
        self.round_winners = []
        self.last_mover = None
        self.logon = log; self.log = []
        self.stats = dict(plays=[{}, {}], won_with=[{}, {}], hush=0, hush_blank=0, retort=0, spend_used=0, spend_coins=0,
                          hushed_spend=0, actions=0, passes=0, bank_lost=0, echo_returned=0, throne_win=0, round_end_win=0,
                          pos0_end=0, tiebreak_noround=0, ties_rounds=0, double_moves=0, hush_targets_avail=[], rounds=0)
    def L(self, s):
        if self.logon: self.log.append("R%d %s" % (self.rnd, s))
    def total(self, p):
        return sum(0 if e["hushed"] else e["card"][1] + e["bonus"] for e in self.row[p])
    def leader(self):
        return 0 if self.pos < 0 else (1 if self.pos > 0 else None)
    def need(self):
        """(leader, margin leader needs)"""
        a = abs(self.pos); ld = self.leader()
        return ld, (3 if a == 3 else 2 if a == 2 else 1)
    def my_need(self, p):
        ld, m = self.need()
        return m if ld == p else 1
    def hush_targets(self):
        return [i for i, e in enumerate(self.row[0]) if not e["hushed"] and "steady" not in e["card"][2]]
    def spend_max(self, card):
        for k in card[2].split():
            if k.startswith("spend"): return min(int(k[5:]), self.treasury)
        return 0
    def actions(self, p, retort=False):
        acts = []
        if retort:
            acts.append(("decline",))
        elif not self.passed[p] or False:
            acts.append(("pass",))
        for i, c in enumerate(self.hand[p]):
            if retort and "retort" not in c[2]: continue
            if p == 0:
                for n in range(self.spend_max(c) + 1): acts.append(("play", i, n))
            else:
                if "hush" in c[2] and self.hush_targets():
                    for t in self.hush_targets(): acts.append(("play", i, t))
                else:
                    acts.append(("play", i, None))
        return acts
    def apply_play(self, p, i, param):
        c = self.hand[p].pop(i); e = dict(card=c, bonus=0, hushed=False)
        self.row[p].append(e)
        d = self.stats["plays"][p]; d[c[0]] = d.get(c[0], 0) + 1
        self.stats["actions"] += 1
        if p == 0 and param:
            self.treasury -= param; self.discard[0] += [("coin", 0, "")] * param
            e["bonus"] = 2 * param; self.stats["spend_used"] += 1; self.stats["spend_coins"] += param
        if p == 1 and "hush" in c[2]:
            self.stats["hush"] += 1
            if param is not None and param < len(self.row[0]):
                t = self.row[0][param]; t["hushed"] = True
                if t["bonus"]: self.stats["hushed_spend"] += 1
            else: self.stats["hush_blank"] += 1
        self.L("%s plays %s%s" % ("TW"[p], c[0], (" spend %d" % param) if (p == 0 and param) else (" hush #%s" % param if p == 1 and "hush" in c[2] else "")))
    def draw_n(self, p, n):
        for _ in range(n):
            if self.draw[p]: self.hand[p].append(self.draw[p].pop())

def play(bots, seed, log=False, max_rounds=7):
    st = State(seed, log)
    turns = 0; stats = st.stats
    for r in range(1, 8):
        st.rnd = r; stats["rounds"] = r
        if r > 1:
            ex = 0 if st.pos == 0 else (2 if abs(st.pos) == 3 else 1 if abs(st.pos) in (1, 2) else 0)
            for p in (0, 1):
                st.draw_n(p, 2)
            tr = st.leader()
            if tr is not None: st.draw_n(1 - tr, ex)
        # lead choice
        ch = st.chooser
        lead = bots[ch].choose_lead(st, ch)
        st.row = [[], []]; st.passed = [False, False]
        stats["hush_targets_avail"].append(0)
        cur = lead; first_actor_done = False
        while not (st.passed[0] and st.passed[1]):
            p = cur
            if st.passed[p]:
                cur = 1 - p; continue
            if not st.hand[p]:
                st.passed[p] = True; st.L("%s has no cards, passes" % "TW"[p]); cur = 1 - p; continue
            acts = st.actions(p)
            a = bots[p].choose(st, p, acts)
            turns += 1
            if a[0] == "pass":
                st.passed[p] = True; stats["passes"] += 1; stats["actions"] += 1; st.L("%s passes" % "TW"[p])
            else:
                st.apply_play(p, a[1], a[2])
                if p == 0 and st.passed[1]:
                    ra = st.actions(1, retort=True)
                    if len(ra) > 1:
                        b = bots[1].choose(st, 1, ra, retort=True)
                        if b[0] == "play":
                            stats["retort"] += 1; st.apply_play(1, b[1], b[2]); turns += 1
            cur = 1 - p
        # resolve
        t0, t1 = st.total(0), st.total(1)
        ld, need = st.need()
        winner = None
        if t0 != t1:
            hi = 0 if t0 > t1 else 1; m = abs(t0 - t1)
            if hi == ld and m < need: winner = None
            else: winner = hi
        else: m = 0
        moved = 0
        if winner is None:
            stats["ties_rounds"] += 1; st.round_winners.append(None)
        else:
            m = abs(t0 - t1); moved = 2 if m >= 5 else 1
            if moved == 2: stats["double_moves"] += 1
            old = st.pos
            st.pos += -moved if winner == 0 else moved
            st.pos = max(-4, min(4, st.pos)); st.last_mover = winner
            st.round_winners.append(winner)
            for e in st.row[winner]:
                n = e["card"][0]; stats["won_with"][winner][n] = stats["won_with"][winner].get(n, 0) + 1
        st.history.append(st.pos)
        st.L("totals T%d W%d winner %s pos %d" % (t0, t1, winner, st.pos))
        # cleanup
        for e in st.row[0]:
            if "bank" in e["card"][2]:
                if st.treasury < 3: st.treasury += 1
                else: st.discard[0].append(e["card"]); stats["bank_lost"] += 1
            else: st.discard[0].append(e["card"])
        for e in st.row[1]:
            if "echo" in e["card"][2] and winner != 1:
                st.hand[1].append(e["card"]); stats["echo_returned"] += 1
            else: st.discard[1].append(e["card"])
        if abs(st.pos) == 4:
            stats["throne_win"] = 1
            return dict(st=st, winner=0 if st.pos < 0 else 1, turns=turns, rounds=r, capped=False, end="throne")
        st.chooser = st.chooser if winner is None else (1 - winner)
    # round 7 end
    if st.pos != 0:
        stats["round_end_win"] = 1
        return dict(st=st, winner=0 if st.pos < 0 else 1, turns=turns, rounds=7, capped=False, end="leader")
    stats["pos0_end"] = 1
    if st.last_mover is None:
        stats["tiebreak_noround"] = 1; w = 0
    else: w = st.last_mover
    return dict(st=st, winner=w, turns=turns, rounds=7, capped=False, end="tiebreak")
