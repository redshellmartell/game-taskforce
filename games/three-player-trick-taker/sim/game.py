"""Split the Take - full rules (rules.md v1). Standard library only.
Interpretation notes are in AMBIGUITIES at the bottom."""
import random

NT = None  # No Trump
SUITNAMES = ["Co", "Ge", "Ke", "Ma"]

def deck():
    return [(s, r) for s in range(4) for r in range(1, 10)]

def legal_cards(hand, led):
    if led is None: return list(hand)
    f = [c for c in hand if c[0] == led]
    return f or list(hand)

def trick_winner(trick, trump):
    """trick: list of (seat, card). Returns seat."""
    led = trick[0][1][0]
    pool = [x for x in trick if trump is not None and x[1][0] == trump] or [x for x in trick if x[1][0] == led]
    return max(pool, key=lambda x: x[1][1])[0]

class Round:
    """Public/private info a bot may consult. Bots should only read their own hand."""
    def __init__(s, planner):
        s.planner = planner; s.safe = (planner + 1) % 3; s.dc = (planner + 2) % 3
        s.trump = NT; s.target = 0
        s.hands = [None] * 3
        s.tricks = [0, 0, 0]
        s.played = set()     # public cards played this round
        s.trick_no = 0
        s.heat = None
    def role(s, seat): return "P" if seat == s.planner else ("S" if seat == s.safe else "D")
    @property
    def remaining(s): return 7 - s.trick_no
    @property
    def crew(s): return s.tricks[s.planner] + s.tricks[s.safe]

class Game:
    def __init__(s, bots, seed, rounds=6, heat=True, log=False):
        s.bots = bots; s.rng = random.Random(seed); s.nrounds = rounds; s.heat_on = heat
        s.scores = [0, 0, 0]; s.dc_wins = [0, 0, 0]; s.tricks_total = [0, 0, 0]
        s.log = [] if log else None
        s.decisions = [0, 0, 0]; s.turns = [0, 0, 0]
        s.rec = []        # per-round records
        s.lead_seq = []   # sole leader (or None) after each round
        s.ruffs = 0; s.tricks_played = 0

    def say(s, t):
        if s.log is not None: s.log.append(t)

    def run(s):
        planner = s.rng.randrange(3)
        for rd in range(s.nrounds):
            s.one_round(rd, planner)
            planner = (planner - 1) % 3     # role cards pass left: P->S seat, S->D seat, D->P seat
        return s.finish()

    def one_round(s, rd, planner):
        R = Round(planner)
        mx = max(s.scores); who = [i for i in range(3) if s.scores[i] == mx]
        R.heat = who[0] if (s.heat_on and len(who) == 1 and rd > 0) else None
        d = deck(); s.rng.shuffle(d)
        R.hands = [d[0:7], d[7:14], d[14:21]]; stash = d[21:]  # 15-card stash
        p, sf, dc = R.planner, R.safe, R.dc
        tr, tg = s.bots[p].plan(R, p, list(R.hands[p]))
        assert tr in (0, 1, 2, 3) and 3 <= tg <= 7
        R.trump, R.target = tr, tg; s.decisions[p] += 1
        h9 = R.hands[sf] + stash[:3]
        disc = s.bots[sf].swap(R, sf, list(h9)); s.decisions[sf] += 1
        assert len(disc) == 3 and disc[0] != disc[1] and all(c in h9 for c in disc)
        R.hands[sf] = [c for c in h9 if c not in disc]
        s.say("R%d P=%d S=%d D=%d trump=%s target=%d heat=%s scores=%s" % (rd + 1, p, sf, dc, "NT" if tr is None else SUITNAMES[tr], tg, R.heat, s.scores))
        s.say("  P hand: %s | S hand after swap: %s" % (fmt(R.hands[p]), fmt(R.hands[sf])))
        leader = dc
        for t in range(7):
            trick = []; led = None
            for k in range(3):
                seat = (leader + k) % 3
                lg = legal_cards(R.hands[seat], led)
                if len(lg) > 1: s.decisions[seat] += 1
                s.turns[seat] += 1
                c = s.bots[seat].play(R, seat, lg, list(trick))
                assert c in lg
                R.hands[seat].remove(c); R.played.add(c); trick.append((seat, c))
                if led is None: led = c[0]
            w = trick_winner(trick, R.trump)
            wc = [c for a_, c in trick if a_ == w][0]
            if R.trump is not None and led != R.trump and wc[0] == R.trump: s.ruffs += 1
            R.tricks[w] += 1; R.trick_no += 1; s.tricks_played += 1; leader = w
            s.say("  T%d %s -> %d" % (t + 1, " ".join("%d:%s" % (a, fmt([c])) for a, c in trick), w))
        crew = R.crew; dev = abs(crew - R.target); ok = dev <= 1; clean = dev == 0; blown = dev >= 2
        pts = [R.tricks[i] for i in range(3)]
        bonus = [0, 0, 0]
        if clean: bonus[p], bonus[sf] = 3, 4
        elif ok: bonus[p], bonus[sf], bonus[dc] = 1, 2, 1
        else: bonus[dc] = 5; s.dc_wins[dc] += 1
        if R.heat is not None: bonus[R.heat] = max(0, bonus[R.heat] - 2)
        for i in range(3):
            s.scores[i] += pts[i] + bonus[i]; s.tricks_total[i] += pts[i]
        mx = max(s.scores); who = [i for i in range(3) if s.scores[i] == mx]
        s.lead_seq.append(who[0] if len(who) == 1 else None)
        s.say("  crew=%d target=%d %s; tricks=%s bonus=%s -> scores %s" % (crew, tg, "CLEAN" if clean else ("MESSY" if ok else "BLOWN"), R.tricks, bonus, s.scores))
        s.rec.append(dict(target=tg, trump=tr, ok=ok, clean=clean, crew=crew, planner=p, safe=sf, dc=dc, heat=R.heat,
                          pts=[pts[i] + bonus[i] for i in range(3)], bonus=bonus, tricks=list(R.tricks)))

    def finish(s):
        mx = max(s.scores); tied = [i for i in range(3) if s.scores[i] == mx]
        if len(tied) > 1:
            m2 = max(s.dc_wins[i] for i in tied); tied = [i for i in tied if s.dc_wins[i] == m2]
        if len(tied) > 1:
            m3 = max(s.tricks_total[i] for i in tied); tied = [i for i in tied if s.tricks_total[i] == m3]
        s.winners = tied
        return s

def fmt(cards):
    return " ".join("%s%d" % (SUITNAMES[c[0]], c[1]) for c in sorted(cards))

AMBIGUITIES = [
 "Heat when the leader is the Double-Crosser who also failed to score a bonus: Heat just does nothing (reduces a 0 bonus by 0). Simulated as no effect; rules say 'reduces your bonus by 1' which is unclear when no bonus is earned.",
 "Rules say the Planner 'starts' by random draw but also that the DC deals starting with the Planner; dealing order has no effect in the sim.",
 "Heat in round 1 and on ties is never held (as written); a 3-way tie at the top gives no Heat.",
 "Revoke rule text ('trick count taken as played' vs 'scored as 0 tricks') is internally contradictory; revokes are impossible in the sim.",
 "Role passing direction: 'pass each card one seat left' was implemented as the planner seat moving one seat to the right each round (P card goes left to become S). Because rotation is cyclic the choice is symmetric.",
 "Tiebreaker 1 counts double-crosses only when the crew missed; Heat-reduced successes still count.",
 "Rules.md section 4 phase 6: 'more or less than Target' - a Target the crew cannot reach (e.g. 7 with 0 tricks possible) is legal; no minimum-hand check.",
 "Safecracker swap draws before the Planner's Plan is known to the DC? No: Plan announced first. Safecracker's hand is therefore adapted to a public Target and trump, giving the crew a 2-player information edge over the DC (a design property, not an ambiguity).",
]
