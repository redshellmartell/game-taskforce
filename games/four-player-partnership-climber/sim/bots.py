"""Ladder Pairs bots. Makers are callables seed -> bot. See game.py for the interface (bots use only public info + own hand;
Reader and persona bots have perfect memory of played cards, which a human would not: a ceiling caveat)."""
import random
from game import legal_leads, legal_follows


class Base:
    def __init__(self, seed): self.r = random.Random(seed)
    def setup(self, seat, bots): self.seat = seat
    def new_hand(self, g, me): self.me = me
    def observe(self, ev): pass


class Random(Base):
    def choose(self, g, me, legal, leading):
        opts = list(legal) + ([] if leading else [None])
        return self.r.choice(opts)


def _is_rope(pl): return pl[0] == "S" and pl[2] >= 14


class Greedy(Base):
    """Weak reference: lead = most cards then lowest top (Rope only if nothing else or <=3 cards left); follow = lowest beat;
    never beats a known partner; Rope only when it is the only beat or <=3 cards left (else pass)."""
    def choose(self, g, me, legal, leading):
        size = g.size[me]
        out = [pl for pl in legal if pl[1] == size]
        if out: return out[0]
        if leading:
            non = [pl for pl in legal if not _is_rope(pl)]
            pool = non if non and size > 3 else legal
            return sorted(pool, key=lambda pl: (-pl[1], pl[2]))[0]
        h = g.holder
        if g.known[h] is not None and g.known[h] == g.colour[me]: return None
        non = [pl for pl in legal if not _is_rope(pl)]
        if non: return min(non, key=lambda pl: pl[2])
        return legal[0]   # only Ropes beat it: play the lowest Rope


class Reader(Base):
    """Strong reference. Belief P[q] = chance q is my partner (exact from Rope reveals + soft update when someone beats me).
    Flags ablate exactly one rule-driven behaviour."""
    def __init__(self, seed, partner_blind=False, reveal_blind=False, uphill_blind=False, relay_blind=False,
                 noise=0.0, thr=0.6, rope_early=False, kind=False):
        super().__init__(seed)
        self.pb, self.rb, self.ub, self.xb = partner_blind, reveal_blind, uphill_blind, relay_blind
        self.noise, self.thr0, self.rope_early, self.kind = noise, thr, rope_early, kind

    def new_hand(self, g, me):
        self.me = me; self.w = [0.0 if q == me else 1.0 for q in range(4)]; self.tricks = 0

    def observe(self, ev):
        if ev[0] == "play" and ev[3] == self.me and ev[1] != self.me:
            self.w[ev[1]] *= 0.5   # someone beat my trick: less likely partner

    def P(self, g):
        me = self.me
        if self.pb: return [0.0] * 4
        if not self.rb:
            mine = g.colour[me]
            for q in range(4):
                if q != me and g.known[q] == mine:
                    return [1.0 if x == q else 0.0 for x in range(4)]
            c = [q for q in range(4) if q != me and g.known[q] is None]
        else:
            c = [q for q in range(4) if q != me]
        tot = sum(self.w[q] for q in c) or 1.0
        return [self.w[q] / tot if q in c else 0.0 for q in range(4)]

    # --- helpers
    def unseen(self, g, me):
        un = [0] * 16
        for r in range(1, 14): un[r] = 4 - g.played[r] - g.cnt[me][r]
        return un

    def beatable(self, g, me, pl, cnt):
        """could someone still hold a beat (using unseen cards; 12 set-aside cards make this conservative)?"""
        un = self.unseen(g, me); kind, n, top = pl
        ropes_left = 2 - sum(1 for r in (14, 15) if g.played[r]) - sum(1 for r in (14, 15) if cnt[r])
        if top >= 15: return False
        if kind == "S":
            if top < 14 and ropes_left > 0 + 0 and (top < 14): return True
            if top == 14: return (g.played[15] + cnt[15]) < 2
            return any(un[r] > 0 for r in range(top + 1, 14))
        if kind in "PT": return any(un[r] >= n for r in range(top + 1, 14))
        return any(all(un[x] > 0 for x in range(e - n + 1, e + 1)) for e in range(top + 1, 14))

    def lead(self, g, me, legal):
        size = g.size[me]; cnt = g.cnt[me]
        for pl in legal:
            if pl[1] == size: return pl
        best = None; bs = -99
        for pl in legal:
            kind, n, top = pl
            s = 1.0 * n - 0.35 * top
            if kind == "S" and top <= 13 and cnt[top] >= 2: s -= 0.5
            if kind == "S" and top <= 13 and cnt[top] == 1 and (cnt[top - 1] if top > 1 else 0) and (cnt[top + 1] if top < 13 else 0): s -= 0.3
            rest = size - n
            if _is_rope(pl):
                s -= 0.0 if (size <= 3 or self.rope_early) else 4.0
            if not self.xb and rest > 0:
                rem = list(cnt); from game import remove
                remove(rem, pl)
                comb = [x for x in legal_leads(rem) if x[1] == rest]
                if comb:   # hand after this play is one single combination
                    y = comb[0]
                    unb_y = not self.beatable(g, me, y, rem)
                    if unb_y: s += 2.0
                    elif not self.beatable(g, me, pl, cnt): s += 2.5
            if s > bs: bs, best = s, pl
        return best

    def choose(self, g, me, legal, leading):
        if self.noise and self.r.random() < self.noise:
            return self.r.choice(list(legal) + ([] if leading else [None]))
        if leading: return self.lead(g, me, legal)
        size = g.size[me]
        for pl in legal:
            if pl[1] == size: return pl
        h = g.holder; P = self.P(g); pH = P[h]
        thr = self.thr0
        if not self.ub:
            if g.uphill[me]: thr -= 0.1
            if g.uphill[h]: thr -= 0.05
            if g.scores[h] - g.scores[me] >= 4: thr += 0.1
        if pH >= thr: return None
        non = [pl for pl in legal if not _is_rope(pl)]
        hs = g.size[h]
        threat = hs <= 5 or size <= 5
        if non:
            best = min(non, key=lambda pl: pl[2])
            if best[2] >= 11 and not threat and pH > 0.2 and not self.kind and pH < thr and self.thr0 >= 0.6 and best[0] == "S": return None
            return best
        # only Ropes beat it
        if hs <= 4 or size <= 4 or self.rope_early or (pH < 0.2 and hs <= 7): return legal[0]
        return None


class ReaderBest(Reader):
    """Second strategic bot (found in experiments/e1.py): greedy-style leads, passes for a partner only when the partner is KNOWN.
    Best of 9 Reader variants tried against Greedy (about +1 to +2 points per bot, inside noise)."""
    def __init__(self, seed, **k):
        super().__init__(seed, kind=True, thr=0.99, **k); self.g_ = Greedy(seed)
    def lead(self, g, me, legal): return self.g_.choose(g, me, legal, True)


class CodeBot(Reader):
    """Code attack: the two CodeBots agree 'my first single of the hand is odd if Sun, even if Moon' and read each other's."""
    def setup(self, seat, bots):
        self.seat = seat; self.ally = next((i for i, b in enumerate(bots) if i != seat and isinstance(b, CodeBot)), None)

    def new_hand(self, g, me):
        super().new_hand(g, me); self.sent = False; self.sig = {}

    def observe(self, ev):
        super().observe(ev)
        if ev[0] == "play" and ev[2][0] == "S" and ev[2][2] <= 13:
            q = ev[1]
            if q == self.ally and q not in self.sig: self.sig[q] = "Sun" if ev[2][2] % 2 else "Moon"

    def P(self, g):
        p = super().P(g); a = self.ally
        if a is not None and a in self.sig and not self.pb:
            same = (self.sig[a] == g.colour[self.me])
            return [1.0 if q == a and same else 0.0 for q in range(4)] if same else [0.0 if q == a else p[q] for q in range(4)]
        return p

    def choose(self, g, me, legal, leading):
        act = super().choose(g, me, legal, leading)
        if act is not None and not self.sent and act[0] == "S" and act[2] <= 13:
            want = 1 if g.colour[me] == "Sun" else 0
            alts = [pl for pl in legal if pl[0] == "S" and pl[2] <= 13 and pl[2] % 2 == want]
            if act[2] % 2 != want and alts:
                alt = min(alts, key=lambda pl: abs(pl[2] - act[2]))
                if abs(alt[2] - act[2]) <= 2: act = alt
            self.sent = True
        return act


class Noisy(Greedy):
    """instinct / casual: greedy with gut-feel random moves."""
    def __init__(self, seed, eps=0.25): super().__init__(seed); self.eps = eps
    def choose(self, g, me, legal, leading):
        if self.r.random() < self.eps: return self.r.choice(list(legal) + ([] if leading else [None]))
        return super().choose(g, me, legal, leading)


class Flavour(Greedy):
    """story / flavour: dramatic - plays Ropes as soon as it can (reveal!), likes runs, 20% impulsive."""
    def choose(self, g, me, legal, leading):
        if self.r.random() < 0.2: return self.r.choice(list(legal) + ([] if leading else [None]))
        ropes = [pl for pl in legal if _is_rope(pl)]
        if ropes and g.trick_no >= 2 and g.known[me] is None: return ropes[0]
        if leading:
            runs = [pl for pl in legal if pl[0] == "R"]
            if runs: return max(runs, key=lambda pl: (pl[1], -pl[2]))
        return super().choose(g, me, legal, leading)


MAKERS = {"random": Random, "greedy": Greedy, "strategic": Reader}
ABL = {
    "A1_partner_blind": lambda s: Reader(s, partner_blind=True),
    "A2_reveal_blind": lambda s: Reader(s, reveal_blind=True),
    "A3_uphill_blind": lambda s: Reader(s, uphill_blind=True),
    "A4_relay_blind": lambda s: Reader(s, relay_blind=True),
}
CODE = CodeBot

PERSONA = {
    "strategist": lambda s: Reader(s, thr=0.6),                          # planner
    "competitor": lambda s: Reader(s, thr=0.6, noise=0.0, rope_early=False),   # optimiser (same strong line)
    "barraiser": lambda s: Reader(s, thr=0.6),                           # expert
    "casual": lambda s: Noisy(s, 0.25),                                  # instinct
    "story": lambda s: Flavour(s),                                       # flavour
    "family": lambda s: Reader(s, thr=0.4, noise=0.1, kind=True),        # cautious: helps likely partners, gentle
}
