"""Heavenly Bodies v2 (Gearbox) rules engine. Standard library only.
Slots: 0=North 1=East 2=South 3=West. Player p's left neighbour is (p+1)%n (play passes left).
Contacts: p's West (3) touches East (1) of (p+1)%n.  Cards are tuples (colour 0-3, size 1-5, copy).
Interpretations of ambiguous rules are listed in AMBIGUITIES at the bottom."""
import random

N_SLOTS = 4
CLOCK, CCW = 1, -1


def make_deck():
    d = []
    for c in range(4):
        for s in (1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5):
            d.append((c, s, sum(1 for x in d if x[0] == c and x[1] == s)))
    return d


def beats(a, b, comet=True):
    """1 if a wins the crash, -1 if b wins, 0 equal size."""
    if comet:
        if a[1] == 1 and b[1] == 5: return 1
        if a[1] == 5 and b[1] == 1: return -1
    return (a[1] > b[1]) - (a[1] < b[1])


def patterns(orbit):
    """Win patterns satisfied by an orbit (list of 4 slots)."""
    if any(c is None for c in orbit): return []
    sizes = sorted(c[1] for c in orbit); out = []
    if sum(sizes) >= 15: out.append("mass")
    if len({c[0] for c in orbit}) == 1: out.append("const")
    if sizes in ([1, 2, 3, 4], [2, 3, 4, 5]): out.append("align")
    return out


def spin_orbit(orbit, d):
    new = [None] * 4
    for i in range(4): new[(i + d) % 4] = orbit[i]
    return new


def crash(orbits, q, n, comet=True, one=None):
    """Resolve the contacts of orbit q (already spun): West contact first, then East.
    Returns list of events ('cap', winner_owner, loser_owner, wcard, lcard, slotref) or ('tie', a_owner, b_owner, acard, bcard, ...).
    Mutates orbits (removes losers)."""
    ev = []
    contacts = [((q, 3), ((q + 1) % n, 1)), (((q - 1) % n, 3), (q, 1))]
    if one is not None: contacts = [contacts[0 if one > 0 else 1]]
    for (pa, sa), (pb, sb) in contacts:
        a, b = orbits[pa][sa], orbits[pb][sb]
        if a is None or b is None: continue
        r = beats(a, b, comet)
        if r > 0: orbits[pb][sb] = None; ev.append(("cap", pa, pb, a, b))
        elif r < 0: orbits[pa][sa] = None; ev.append(("cap", pb, pa, b, a))
        else: orbits[pa][sa] = None; orbits[pb][sb] = None; ev.append(("tie", pa, pb, a, b))
    return ev


class State:
    def __init__(self, n, seed, rebound=True, opening=2, mass=15, log=False):
        self.n = n; self.rng = random.Random(seed); self.rebound = rebound; self.mass = mass
        self.deck = make_deck(); self.rng.shuffle(self.deck)
        self.hands = [[self.deck.pop() for _ in range(5)] for _ in range(n)]
        self.orbits = [[None] * 4 for _ in range(n)]
        self.deep = []; self.turn = 0; self.active = 0
        self.log = [] if log else None
        self.stats = dict(captures=0, ties=0, spins=0, crash_spins=0, self_spins=0, other_spins=0, other_crash=0, self_crash=0,
                          recalls=0, rebounds=0, formed=0, formed_survived=0, full_survived=0, full_formed=0, deep_takes=0,
                          draws=0, launches=0, cards_moved_turns=0, decisions=[0] * n, mover_caps=[0] * n)
        self.pending = {}   # player -> pattern list formed on own launch, to test survival
        self.fullpending = {}
        self.history_totals = []

    def totals(self): return [sum(c[1] for c in o if c) for o in self.orbits]
    def counts(self): return [sum(1 for c in o if c) for o in self.orbits]
    def L(self, s):
        if self.log is not None: self.log.append(s)


def cs(c): return "EFVS"[c[0]] + str(c[1])
def orb_str(o): return "[" + " ".join(cs(c) if c else "--" for c in o) + "]"


def legal_launches(st, p, rebound_allowed):
    """Return list of launch plans: tuples of (card_index, slot). Plans use distinct slots; indices into the hand as it is at plan time."""
    hand = st.hands[p]; plans = [()]
    singles = [((i, s),) for i in range(len(hand)) for s in range(4)]
    plans += singles
    if rebound_allowed:
        for i in range(len(hand)):
            for s in range(4):
                for j in range(len(hand)):
                    if j == i: continue
                    for t in range(4):
                        if t != s: plans.append(((i, s), (j, t)))
    return plans


def apply_launches(orbit, hand, plan):
    """Pure helper: returns (new_orbit, new_hand, recalled_count). Plan lists (hand_index, slot) in order; indices refer to the original hand."""
    orbit = list(orbit); hand = list(hand); played = set(); rec = 0
    for i, s in plan:
        c = hand[i]; played.add(i)
        if orbit[s] is not None: hand.append(orbit[s]); rec += 1
        orbit[s] = c
    return orbit, [c for k, c in enumerate(hand) if k not in played], rec


def rebound_ok(st, p):
    if not st.rebound: return False
    mine = sum(1 for c in st.orbits[p] if c)
    return all(mine < sum(1 for c in st.orbits[o] if c) for o in range(st.n) if o != p)


def play(bots, seed, n=None, rebound=True, mass=15, log=False, cap=200, opening=2, win_at_end=False, one_contact=False):
    n = n or len(bots)
    st = State(n, seed, rebound=rebound, mass=mass, log=log); st.one = one_contact
    # setup: each bot picks `opening` of 5 cards for distinct slots
    for p in range(n):
        picks = bots[p].setup(st, p)
        cards = [st.hands[p][ci] for ci, s in picks]
        for (ci, s), c in zip(picks, cards): st.orbits[p][s] = c
        st.hands[p] = [c for k, c in enumerate(st.hands[p]) if k not in {ci for ci, s in picks}]
    st.L("setup " + " | ".join(orb_str(o) for o in st.orbits))
    S = st.stats; leaders = []; winner = None; win_pat = None; long_night = False; first = True
    cap_turns = cap
    while st.turn < cap_turns:
        p = st.turn % n; st.active = p
        # 0 win check
        pats = patterns(st.orbits[p])
        if mass != 15 and not any(c is None for c in st.orbits[p]):
            pats = [x for x in pats if x != "mass"] + (["mass"] if sum(c[1] for c in st.orbits[p]) >= mass else [])
        if p in st.pending:
            if pats: S["formed_survived"] += 1
            del st.pending[p]
        if p in st.fullpending:
            if all(c for c in st.orbits[p]): S["full_survived"] += 1
            del st.fullpending[p]
        if pats:
            winner = p; win_pat = pats; st.L("T%d P%d WINS %s %s" % (st.turn, p, pats, orb_str(st.orbits[p]))); break
        # 1 draw
        if not st.deck:
            long_night = True; break
        moved = 0
        dec = 0
        if not (first and p == 0):
            if st.deep:
                dec += 1
                src = bots[p].draw(st, p)
            else: src = "deck"
            if src == "deep" and st.deep: st.hands[p].append(st.deep.pop()); S["deep_takes"] += 1
            else: st.hands[p].append(st.deck.pop())
            S["draws"] += 1
        first = False
        # 2 launch
        rb = rebound_ok(st, p)
        if st.hands[p]: dec += 1
        plan, spin = bots[p].turn(st, p, rb)
        plan = [x for x in plan][: (2 if rb else 1)]
        if len(plan) == 2 and plan[0][1] == plan[1][1]: plan = plan[:1]
        if plan and st.hands[p]:
            if len(plan) == 2: S["rebounds"] += 1
            neworb, newhand, rec = apply_launches(st.orbits[p], st.hands[p], plan)
            st.orbits[p] = neworb; st.hands[p] = newhand; S["recalls"] += rec; S["launches"] += len(plan)
            st.L("T%d P%d launch %s -> %s" % (st.turn, p, " ".join(cs(st.hands[p][i] if False else c) for c in [] ) or len(plan), orb_str(neworb)))
        pf = patterns(st.orbits[p])
        if all(c for c in st.orbits[p]): st.fullpending[p] = 1; S["full_formed"] += 1
        if pf: st.pending[p] = pf; S["formed"] += 1
        # 3 spin
        nonempty = [q for q in range(n) if any(st.orbits[q])]
        if nonempty:
            if len(nonempty) > 1: dec += 1
            q, d = spin
            if q not in nonempty: q = nonempty[0]
            st.orbits[q] = spin_orbit(st.orbits[q], d); S["spins"] += 1
            if q == p: S["self_spins"] += 1
            else: S["other_spins"] += 1
            ev = crash(st.orbits, q, n, True, d if one_contact else None)
            if ev:
                S["crash_spins"] += 1
                if q == p: S["self_crash"] += 1
                else: S["other_crash"] += 1
            for e in ev:
                if e[0] == "cap":
                    _, w, l, wc, lc = e; st.hands[w].append(lc); S["captures"] += 1; moved += 1
                    if w == p: S["mover_caps"][p] += 1
                    st.L("T%d P%d spin P%d %+d: P%d %s takes P%d %s" % (st.turn, p, q, d, w, cs(wc), l, cs(lc)))
                else:
                    _, a, b, ac, bc = e; S["ties"] += 1; moved += 1
                    first_c, second_c = (ac, bc)
                    mine = [c for c in st.hands[p] + st.orbits[p] if c]
                    cnt = lambda c: sum(1 for x in mine if x[0] == c[0])
                    top, bottom = (ac, bc) if cnt(ac) <= cnt(bc) else (bc, ac)
                    st.deep.append(bottom); st.deep.append(top)
                    st.L("T%d P%d spin P%d %+d: %s and %s collide, knocked out" % (st.turn, p, q, d, cs(ac), cs(bc)))
        S["decisions"][p] += dec + (1 if False else 0)
        S["cards_moved_turns"] += 1 if moved else 0
        # 5 cool down
        if len(st.hands[p]) > 5:
            order = bots[p].discard(st, p)
            for c in order: st.deep.append(c)
        if win_at_end:
            pe = patterns(st.orbits[p])
            if pe:
                winner = p; win_pat = pe; st.turn += 1; break
        st.turn += 1
        t = st.totals(); mx = max(t)
        leaders.append(t.index(mx) if t.count(mx) == 1 else None)
    capped = st.turn >= cap_turns
    if winner is None and long_night:
        t = st.totals(); cnt = st.counts()
        best = max(t); c1 = [i for i in range(n) if t[i] == best]
        bc = max(cnt[i] for i in c1); c2 = [i for i in c1 if cnt[i] == bc]
        winner = c2[0] if len(c2) == 1 else None; win_pat = ["longnight"] if winner is not None else ["longnight_tie"]
        S["ln_shared"] = len(c2)
    return dict(winner=winner, turns=st.turn, capped=capped, leaders=leaders, pattern=win_pat, long_night=long_night, stats=S, st=st)


AMBIGUITIES = [
    "Can a card recalled by the first Rebound Launch be launched again by the second? Sim: yes, into a different slot (recalled card is in hand at once).",
    "Rebound: second Launch may Recall as well; may both Launches target slots in any order? Sim: any two different slots.",
    "Must the Rebound check use bodies after the first Launch? Rules say start of step: sim follows that.",
    "Equal-size crash in 2p when both contacts tie: the 'active chooses which goes on top' is per collision; order of two collisions undefined. Sim: West first.",
    "Which card goes on top is the active player's choice but no guidance on intent (deny/keep). Sim: the colour the active player holds least goes on top.",
    "Spinning an orbit where the crash removes a body that is the winner of the other contact: contacts use different slots so independent, but with 2 players West-contact capture may empty a slot that is later compared? (not the case: slots differ). No effect.",
    "'Draw' when Deck empty ends the game even if Deep Space has cards: sim follows the text. The first player's skipped Draw on turn 1 means the deck cannot be empty then.",
    "Long Night tie: 'share the win' - sim counts as a tie (no single winner).",
    "A win pattern with Critical Mass: does a 4-body orbit of total 15 counting bodies only, yes. Constellation with duplicate sizes allowed.",
    "Can a player spin an orbit that has bodies only in non-contact slots (N,S)? Legal but crashes nothing; sim allows ('must spin non-empty orbit') -> pure rotation.",
    "Hand limit applies at Cool down only; captured cards can bring a hand to 8+. Discard order choice: sim discards the least useful first, last discard becomes top.",
    "Setup: players with a 5-card hand keep 3. Opening Launch order for first player (skipping Draw): hand 3 -> may Launch. Rebound in first turn: all have 2 bodies so no Rebound for P1.",
    "Spin when every orbit is empty: skipped. Sim cannot reach it in normal play (opening bodies).",
    "A Launch onto an occupied slot returns the old body: is that a 'Recall' even if the player wants the old card back later in the same turn? Allowed in sim.",
    "Does the slot rule 'North/South never touch anything' hold after a spin? Slots rotate with the bodies; contacts are slot positions. Sim: yes, contacts are fixed positions.",
]
