"""Silent Duo rules engine (rules.md v2). Standard library only.
Interpretations (ambiguities) are listed in AMBIGUITIES at the bottom."""
import random
from collections import Counter

FOG = {"calm": 4, "standard": 8, "storm": 12}


class Obs:
    """Everything a player may know (rules 5.1): own hand, others' ships, and the public table."""
    pass


class Game:
    def __init__(self, n=2, fog=8, seed=0, log=False, reefs=2):
        self.n, self.rng = n, random.Random(seed)
        self.logon, self.log = log, []
        cards = [v for v in range(1, 11) for _ in range(5)]
        self.rng.shuffle(cards)
        per_ship, hand_n = (3, 5) if n == 2 else (2, 4)
        self.ships = []
        for p in range(n):
            self.ships.append([dict(v=cards.pop(), lit=False, lo=0, hi=11, card=None) for _ in range(per_ship)])
        self.fog = [cards.pop() for _ in range(fog)]
        self.hands = [sorted(cards.pop() for _ in range(hand_n)) for _ in range(n)]
        self.deck = cards
        self.night = []
        self.night_own = [Counter() for _ in range(n)]   # cards a player sent to the Night pile (they saw them)
        self.reefs_left = reefs
        self.wrecked = 0
        self.seen = Counter()          # public card values: signal rows, lit ships and the cards lit with
        self.events = []               # public event log
        self.cur = self.rng.randrange(n)
        self.turns = 0
        self.last_watch = None         # turns left once the Last Watch begins
        self.over = False
        self.win = False
        self.stats = Counter()
        self.deck_at_end = len(self.deck)
        self.chooser = None            # callback(p, drawn) -> index of the Trim card to keep
        self.timeline = []             # per turn: (at_risk flag)

    # ------------------------------------------------------------ views
    def obs(self, p):
        o = Obs()
        o.me, o.n, o.hand = p, self.n, list(self.hands[p])
        o.deck_n, o.fog_n, o.night_n, o.wrecked = len(self.deck), len(self.fog), len(self.night), self.wrecked
        o.last_watch = self.last_watch
        o.reefs_left = self.reefs_left - self.wrecked
        o.ships = {}
        for q in range(self.n):
            o.ships[q] = [dict(lo=s["lo"], hi=s["hi"], lit=s["lit"], v=(s["v"] if (q != p or s["lit"]) else None)) for s in self.ships[q]]
        rem = [0] * 11
        vis = Counter(self.seen)
        for v in o.hand: vis[v] += 1
        vis.update(self.night_own[p])
        for q in range(self.n):
            if q != p:
                for s in self.ships[q]:
                    if not s["lit"]: vis[s["v"]] += 1
        for v in range(1, 11): rem[v] = max(0, 5 - vis[v])
        o.remaining = rem
        o.events = self.events          # shared public list; bots keep their own pointer
        return o

    # ------------------------------------------------------------ legality
    def legal(self, p):
        acts, hand = [], self.hands[p]
        vals = sorted(set(hand))
        for q in range(self.n):
            if q == p: continue
            for i, s in enumerate(self.ships[q]):
                if s["lit"]: continue
                ok = [c for c in vals if c != s["v"] and s["lo"] < c < s["hi"]]   # v2: both cards inside the open range
                for a in range(len(ok)):
                    for b in range(a + 1, len(ok)):
                        acts.append(("offer", q, i, ok[a], ok[b]))
        for i, s in enumerate(self.ships[p]):
            if not s["lit"]:
                for c in vals:
                    if s["lo"] <= c <= s["hi"]: acts.append(("light", i, c))    # v2: Light window L <= C <= H
        if self.deck:
            for c in vals: acts.append(("trim", c))
        return acts or [("pass",)]

    @staticmethod
    def decisions(acts, chosen):
        """Number of real choices in this turn: action type, target, card(s)."""
        if len(acts) == 1: return 0
        d = 1 if len({a[0] for a in acts}) > 1 else 0
        same = [a for a in acts if a[0] == chosen[0]]
        if chosen[0] == "offer":
            if len({(a[1], a[2]) for a in same}) > 1: d += 1
            if len([a for a in same if a[1:3] == chosen[1:3]]) > 1: d += 1
        elif chosen[0] == "light":
            if len({a[1] for a in same}) > 1: d += 1
            if len([a for a in same if a[1] == chosen[1]]) > 1: d += 1
        elif chosen[0] == "trim":
            d += 1 + (1 if len(same) > 1 else 0)   # which card to dump, which of the two drawn to keep
        return d

    def _ev(self, *e):
        self.events.append(e)
        if self.logon: self.log.append("T%d P%d %s" % (self.turns, self.cur, " ".join(map(str, e))))

    def _risk(self):
        unlit = sum(1 for q in self.ships for s in q if not s["lit"])
        left = len(self.deck) + self.n if self.last_watch is None else self.last_watch
        return self.wrecked >= 2 or left < 3 * unlit

    # ------------------------------------------------------------ one turn
    def step(self, action):
        p = self.cur
        hand = self.hands[p]
        self.turns += 1
        kind = action[0]
        drew = True
        if kind == "offer":
            _, q, i, a, b = action
            s = self.ships[q][i]
            hand.remove(a); hand.remove(b)
            shown, kept = (a, b) if self.rng.random() < 0.5 else (b, a)   # owner shuffles and flips one
            hand.append(kept); hand.sort()
            assert shown != s["v"]
            row = "low" if shown < s["v"] else "high"
            if row == "low": s["lo"] = max(s["lo"], shown)
            else: s["hi"] = min(s["hi"], shown)
            self.seen[shown] += 1
            self.stats["offers"] += 1
            self._ev("offer", p, q, i, shown, row)
        elif kind == "light":
            _, i, c = action
            s = self.ships[p][i]
            hand.remove(c)
            self.seen[c] += 1
            if abs(c - s["v"]) <= 1:
                s["lit"], s["card"] = True, c
                self.seen[s["v"]] += 1
                bea = c == s["v"]
                if bea:
                    self.stats["beacons"] += 1
                    if self.deck:
                        mv, self.fog = self.fog[:2], self.fog[2:]
                        self.deck.extend(mv)
                self.stats["lit"] += 1
                self._ev("light", p, i, c, s["v"], bea)
            else:
                row = "low" if c < s["v"] else "high"
                if row == "low": s["lo"] = max(s["lo"], c)
                else: s["hi"] = min(s["hi"], c)
                self.wrecked += 1
                self.stats["misses"] += 1
                self._ev("miss", p, i, c, row)
                if self.wrecked >= self.reefs_left:
                    return self._finish(False)
            if all(x["lit"] for q in self.ships for x in q):
                return self._finish(True)
        elif kind == "trim":
            hand.remove(action[1]); self.night.append(action[1]); self.night_own[p][action[1]] += 1
            self.stats["trims"] += 1
            self._ev("trim", p)
            drawn = [self.deck.pop(0) for _ in range(min(2, len(self.deck)))]
            if len(drawn) == 2:
                k = self.chooser(p, drawn) if self.chooser else 0
                keep, dump = drawn[k], drawn[1 - k]
                self.night.append(dump); self.night_own[p][dump] += 1
                hand.append(keep)
            else:
                hand.append(drawn[0])
            hand.sort()
            drew = False
            if not self.deck and self.last_watch is None:
                self.last_watch = self.n
                self.cur = (p + 1) % self.n
                self.timeline.append(self._risk())
                return None
        else:
            drew = False
            self.stats["passes"] += 1
            self._ev("pass", p)
        if drew and self.deck:
            hand.append(self.deck.pop(0)); hand.sort()
            if not self.deck and self.last_watch is None:
                self.last_watch = self.n          # each player, starting with the next, one more turn
                self.cur = (p + 1) % self.n
                self.timeline.append(self._risk())
                return None
        # advance
        if self.last_watch is not None:
            self.last_watch -= 1
            if self.last_watch <= 0:
                return self._finish(False)
        self.cur = (p + 1) % self.n
        self.timeline.append(self._risk())
        return None

    def _finish(self, win):
        self.over, self.win = True, win
        self.deck_at_end = len(self.deck)
        self.lit = sum(1 for q in self.ships for s in q if s["lit"])
        self.score = (10 + len(self.deck)) if win else self.lit
        return win


def play(game, bots, cap=200):
    """bots: list of bot objects with act(obs, legal) -> action. Returns the game. Counts decisions per player."""
    dec = [0] * game.n
    game.chooser = lambda p, drawn: bots[p].keep(game.obs(p), drawn)
    while not game.over and game.turns < cap:
        p = game.cur
        acts = game.legal(p)
        a = bots[p].act(game.obs(p), acts) if len(acts) > 1 else acts[0]
        assert a in acts, (a, acts[:5])
        dec[p] += Game.decisions(acts, a)
        game.step(a)
    game.dec = dec
    game.capped = not game.over
    if game.capped: game._finish(False)
    return game


AMBIGUITIES = [
    "Rules 4 A says an Offer needs an open range of at least 3 values, 5.2 says 2 or more legal values that are not V. Coded as: both cards strictly inside (L,H), different, neither equal to V (so the range holds at least 3 values by construction).",
    "Reveal token flip: 'Low' shows the lower card. Coded as a 50/50 pick; the rules do not say what happens when both offered cards are on the same side of V (the shown card then narrows only one side, the other may be useless). Legal and allowed.",
    "Trim with exactly 1 card in the deck: draw it and keep it (stated). Trim that empties the deck starts the Last Watch (stated by Phase 3 'by any draw').",
    "Trim cards are Night-piled face-down but the trimmer saw them: coded as private knowledge for card counting; the rules list this under 'each player additionally knows' only for cards sent to the Night pile, and it is unclear whether the kept/dumped Trim cards in 3-player games are visible to the third player (coded: no).",
    "Beacon: 'top 2 cards of the Fog pile to the bottom of the draw deck'; a Beacon lit on the turn that empties the deck is impossible (Light draws after), coded as stated. Beacon during Light that is the last ship is irrelevant.",
    "Last Watch: 'every player takes exactly one more turn, starting with the player to the left of the one who emptied the deck'. Coded as n turns, each Offer/Light/skip; a Trim is illegal (deck empty). Cannot tell if a win on the last turn needs the turn to finish: wins are immediate.",
    "Light legality L <= C <= H allows C equal to L or H, i.e. a card equal to a value already ruled out by a signal. Allowed; it is a safe-looking but sometimes hopeless play (coded legal).",
    "Rules 6 turn cap formula (26 + 8 + 2 = 36) assumes deck 26 at Standard; with Trim burning 2 per turn it is an upper bound. Not an issue in sim.",
    "Offer legality when only one of the cards is inside the range: not legal; a player who has two in-range cards of different values may have none, so Offers are often unavailable late and Trim becomes the default (see findings).",
    "3 players: the Light resolver (player on the left) is the only one who learns nothing extra; the third player sees the ship but the rules do not say whether they may stop a mis-resolve. Not coded.",
]
