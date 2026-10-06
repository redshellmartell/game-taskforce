"""Tug of Crowns rules v3 (fixed lead: round loser leads, cap 2, double at 6). Seat 0 = Treasurer, seat 1 = Whisperer. Crown pos: -3 (T throne) .. -1, start 0, +1 .. +3 (W throne); 0 never re-entered.
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

AMBIGUITIES = []   # revision 1: all 8 earlier ambiguities resolved in rules v2. New interpretations are listed in NOTES.
NOTES = [
    "Lead draws its bonus card after the chooser decides (after Phase 1 extras); modelled that way.",
    "Lead wins equal totals except 0-0 (a tie); a lead with an empty row and an empty opposing row ties.",
    "Step counting from T1 toward the Whisperer: W1 (1 step), W2 (2 steps); the start card is never counted.",
]
KNOB = {"cap": 2, "court": 1, "double_at": 6, "lead_draw": 0, "lead_ties": True, "gates_draw": 2, "murmur_draw": 1, "second_draw": 0, "tie_to_second": False, "draw_if_fewer": False}

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
        self.tcards = []
        self.lead = 0
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
                          pos0_end=0, tiebreak_noround=0, ties_rounds=0, double_moves=0, hush_targets_avail=[], rounds=0, card_round=[{}, {}], round_w=[0, 0], reshuf=[0, 0], lead_rounds=0, lead_won=0, lead_self=[0, 0], lead_self_n=[0, 0], dead_hand=0)
    def L(self, s):
        if self.logon: self.log.append("R%d %s" % (self.rnd, s))
    @property
    def treasury(self): return len(self.tcards)
    def total(self, p):
        return sum(0 if e["hushed"] else e["card"][1] + e["bonus"] for e in self.row[p])
    def leader(self):
        return 0 if self.pos < 0 else (1 if self.pos > 0 else None)
    def my_need(self, p):
        """margin I need to win the round now: lead wins ties (needs 0, unless both rows are empty)."""
        if (self.lead == p) != KNOB["tie_to_second"] and KNOB["lead_ties"]: return 0 if self.total(p) > 0 else 1
        return 1
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
            self.discard[0] += [self.tcards.pop() for _ in range(param)]
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
            if not self.draw[p]:
                if self.discard[p]:
                    self.draw[p] = self.discard[p]; self.discard[p] = []; self.rng.shuffle(self.draw[p]); self.stats["reshuf"][p] += 1
                else: return
            self.hand[p].append(self.draw[p].pop())

def play(bots, seed, log=False, max_rounds=7):
    st = State(seed, log)
    turns = 0; stats = st.stats
    for r in range(1, 8):
        st.rnd = r; stats["rounds"] = r
        if r > 1:
            for p in (0, 1): st.draw_n(p, 2)
            tr = st.leader()
            if tr is not None and abs(st.pos) in (1, 2) and KNOB["court"]:
                st.draw_n(1 - tr, KNOB["gates_draw"] if abs(st.pos) == 2 else KNOB["murmur_draw"])
        ch = st.chooser
        lead = ch
        st.lead = lead
        if not KNOB["draw_if_fewer"] or len(st.hand[lead]) <= len(st.hand[1 - lead]): st.draw_n(lead, KNOB["lead_draw"])
        st.draw_n(1 - lead, KNOB["second_draw"])
        stats["lead_self"][ch] += lead == ch; stats["lead_self_n"][ch] += 1
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
        winner = None
        if t0 != t1: winner = 0 if t0 > t1 else 1
        elif t0 > 0 and KNOB["lead_ties"]: winner = (1 - lead) if KNOB["tie_to_second"] else lead
        moved = 0
        if winner is None:
            stats["ties_rounds"] += 1; st.round_winners.append(None)
        else:
            m = abs(t0 - t1); moved = 2 if m >= KNOB["double_at"] else 1
            if moved == 2: stats["double_moves"] += 1
            tgt = -1 if winner == 0 else 1
            seq = [-3, -2, -1, 1, 2, 3]
            if st.pos == 0:
                st.pos = tgt * moved
            else:
                i = seq.index(st.pos) + tgt * moved
                st.pos = seq[max(0, min(5, i))]
            st.last_mover = winner
            st.round_winners.append(winner)
        stats["lead_rounds"] += 1; stats["lead_won"] += winner == lead
        for p_ in (0, 1):
            for nm in set(e["card"][0] for e in st.row[p_]):
                d = stats["card_round"][p_].setdefault(nm, [0, 0]); d[0] += 1; d[1] += (winner == p_)
        stats["round_w"][0] += winner == 0; stats["round_w"][1] += winner == 1
        st.history.append(st.pos)
        st.L("totals T%d W%d winner %s pos %d" % (t0, t1, winner, st.pos))
        # cleanup
        for e in st.row[0]:
            if "bank" in e["card"][2]:
                if st.treasury < KNOB["cap"]: st.tcards.append(e["card"])
                else: st.discard[0].append(e["card"]); stats["bank_lost"] += 1
            else: st.discard[0].append(e["card"])
        for e in st.row[1]:
            if "echo" in e["card"][2] and winner != 1:
                st.hand[1].append(e["card"]); stats["echo_returned"] += 1
            else: st.discard[1].append(e["card"])
        if abs(st.pos) == 3:
            stats["throne_win"] = 1
            return dict(st=st, winner=0 if st.pos < 0 else 1, turns=turns, rounds=r, capped=False, end="throne")
        st.chooser = st.chooser if winner is None else (1 - winner)   # loser leads next round
    # round 7 end
    if st.pos != 0:
        stats["round_end_win"] = 1
        return dict(st=st, winner=0 if st.pos < 0 else 1, turns=turns, rounds=7, capped=False, end="leader")
    stats["pos0_end"] = 1; stats["tiebreak_noround"] = 1; w = 1
    return dict(st=st, winner=w, turns=turns, rounds=7, capped=False, end="tiebreak")
