"""Silent Duo rules engine (rules.md v1). Standard library only.
Interpretations (ambiguities) are listed in AMBIGUITIES at the bottom."""
import random
from collections import Counter

FOG = {"calm": 4, "standard": 8, "storm": 12}


class Obs:
    """Everything a player may know (rules 5.1): own hand, others' ships, and the public table."""
    pass


class Game:
    def __init__(self, n=2, fog=8, seed=0, log=False, reefs=3):
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
        self.timeline = []             # per turn: (at_risk flag)

    # ------------------------------------------------------------ views
    def obs(self, p):
        o = Obs()
        o.me, o.n, o.hand = p, self.n, list(self.hands[p])
        o.deck_n, o.fog_n, o.night_n, o.wrecked = len(self.deck), len(self.fog), len(self.night), self.wrecked
        o.last_watch = self.last_watch
        o.ships = {}
        for q in range(self.n):
            o.ships[q] = [dict(lo=s["lo"], hi=s["hi"], lit=s["lit"], v=(s["v"] if (q != p or s["lit"]) else None)) for s in self.ships[q]]
        rem = [0] * 11
        vis = Counter(self.seen)
        for v in o.hand: vis[v] += 1
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
                ok = [c for c in vals if c != s["v"]]
                for a in range(len(ok)):
                    for b in range(a + 1, len(ok)):
                        acts.append(("offer", q, i, ok[a], ok[b]))
        for i, s in enumerate(self.ships[p]):
            if not s["lit"]:
                for c in vals: acts.append(("light", i, c))
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
            if len(same) > 1: d += 1
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
            hand.remove(action[1]); self.night.append(action[1])
            self.stats["trims"] += 1
            self._ev("trim", p)
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
    "Last Watch: rules say the player who drew the last card takes the final turn; read as 'n turns starting with the next player'. A Beacon during it adds nothing (deck empty), as written.",
    "Beacon when the draw deck is non-empty but Fog is smaller than 2: moves what is left. Beacon timing is before the draw (Phase 1), so the added cards are at the bottom behind the draw.",
    "Light is 'legal' with a card whose success is already impossible (e.g. a card that cannot be within 1 of any value in the ship's signal range). Nothing forbids it, so bots may waste Reefs deliberately; the resolver cannot refuse.",
    "Pass is only legal when nothing else is; in the Last Watch a player with an empty hand and no legal offer/light passes. A player with a full hand but only Offers that tell nothing must still take an action (forced bad moves).",
    "Offer needs the two cards to differ from each other and from V, but nothing stops an Offer that tells the owner nothing new (e.g. a card already outside the known range). That is legal and wastes a card.",
    "The 3-player 'resolver' for a Light is the player on the lighter's left; Offers are resolved by the owner. The third player gets no role beyond watching.",
    "Whether a Light that is a miss still draws a card: read as yes (Phase 2 follows Phase 1) unless the third Reef ended the game.",
    "Trim when the draw deck has exactly 1 card is legal and draws that last card, starting the Last Watch (rules do not say).",
    "Beacon text says 'lit and also Beacon' but does not say whether the played card of a lit-by-1 stays; read as it stays on the ship, both out of play.",
]
