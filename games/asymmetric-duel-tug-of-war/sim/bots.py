"""Bots for Tug of Crowns. Interface: choose(st, p, actions, retort=False) -> action; choose_lead(st, p) -> seat who leads."""
import random

def eff(st, p, a):
    """(immediate change in my margin, card inf played) for a play action."""
    c = st.hand[p][a[1]]; inf = c[1]
    if p == 0:
        return inf + 2 * (a[2] or 0)
    d = inf
    if a[2] is not None and "hush" in c[2]:
        t = st.row[0][a[2]]; d += t["card"][1] + t["bonus"]
    return d

def margin(st, p): return st.total(p) - st.total(1 - p)

def cost(st, p, a):
    """What the play costs me in future resources (lower = cheaper to spend)."""
    c = st.hand[p][a[1]]; v = c[1]
    if p == 0:
        v += 1.5 * (a[2] or 0)
        if "bank" in c[2] and st.treasury < 3: v -= 1.5     # banking is a gain
        if "steady" in c[2]: v += 0.3
    else:
        if "echo" in c[2]: v -= 1.0 if True else 0            # comes back unless I win
        if "hush" in c[2]: v += 1.0                           # hush is scarce
        if "retort" in c[2] and not st.passed[1]: v += 0.5
    return v

class Random:
    name = "random"
    def __init__(s, seed=0): s.r = random.Random(seed)
    def choose(s, st, p, acts, retort=False): return s.r.choice(acts)
    def choose_lead(s, st, p): return s.r.choice((0, 1))

class Greedy:
    """Plays the card with the biggest immediate margin gain until it leads by the needed margin, then passes."""
    name = "greedy"
    def __init__(s, seed=0): s.r = random.Random(seed)
    def choose(s, st, p, acts, retort=False):
        plays = [a for a in acts if a[0] == "play"]
        if retort:
            if plays and margin(st, p) < st.my_need(p): return max(plays, key=lambda a: eff(st, p, a))
            return ("decline",)
        if not plays: return ("pass",)
        if margin(st, p) >= st.my_need(p) and st.passed[1 - p]: return ("pass",)
        if margin(st, p) >= st.my_need(p) + 1: return ("pass",)
        return max(plays, key=lambda a: eff(st, p, a))
    def choose_lead(s, st, p): return p

class Strategic:
    """Cheapest-winning-play heuristic with stake-based budget. Parameters tune the persona variants."""
    name = "strategic"
    def __init__(s, seed=0, noise=0.0, last_word=True, stake_bias=0.0, drama=0.0, caution=0.0, push=True):
        s.r = random.Random(seed); s.noise = noise; s.last_word = last_word
        s.stake_bias = stake_bias; s.drama = drama; s.caution = caution; s.push = push
    def stake(s, st, p):
        """How many 'cost points' this round is worth to me."""
        mine = st.pos * (1 if p == 1 else -1)        # positive = crown toward my throne
        base = 4.0 + s.stake_bias
        if mine >= 2: base += 3              # a push can end the game
        if mine <= -3: base += 4             # I must stop the opponent's push
        if mine <= -2: base += 1.5
        if st.rnd >= 6: base += 2.5
        if st.rnd == 7: base += 3
        # shortage of cards: spend freely if the draw piles are gone
        if len(st.hand[p]) > 7: base += 1.5
        return base
    def choose_lead(s, st, p):
        if s.r.random() < s.noise: return s.r.choice((0, 1))
        if p == 1:   # whisperer likes last word only with retorts in hand
            return 1 - p if s.last_word and not any("retort" in c[2] for c in st.hand[p]) else p
        return 1 - p if s.last_word else p
    def choose(s, st, p, acts, retort=False):
        plays = [a for a in acts if a[0] == "play"]
        passa = ("decline",) if retort else ("pass",)
        if not plays: return passa
        if s.noise and s.r.random() < s.noise * 0.5:
            return s.r.choice(acts)
        m = margin(st, p); need = st.my_need(p)
        mine = st.pos * (1 if p == 1 else -1)
        want = need
        if s.push and mine >= 2 and not retort: want = max(need, 5)   # a 2-step push wins the game
        if s.push and mine >= -1 and mine < 2: want = max(need, 5) if s.r.random() < 0.0 else need
        opp_passed = st.passed[1 - p]
        stake = s.stake(s, st, p) if False else s.stake(st, p)
        ok = [a for a in plays if m + eff(st, p, a) >= want]
        if m >= want:
            if opp_passed: return passa
            # winning, opponent still to act: hold if the lead is comfortable
            if m >= want + 1 or s.r.random() < 0.5 + s.caution: return passa
            return passa
        if ok:
            best = min(ok, key=lambda a: cost(st, p, a) + s.r.random() * 0.01)
            if cost(st, p, best) <= stake + s.drama: return best
        # cannot win with one card (or too expensive)
        if opp_passed and not ok:
            # try two-card catch-up: only if my best two cards beat deficit and stake high
            effs = sorted((eff(st, p, a) for a in plays), reverse=True)
            if sum(effs[:2]) + m >= want and stake >= 7 + s.drama:
                return max(plays, key=lambda a: eff(st, p, a))
            return passa
        if not opp_passed:
            # build: play an efficient card (Echo / Bank / cheap) if it's nearly free
            cheap = [a for a in plays if cost(st, p, a) <= 1.5 + s.drama]
            if cheap and stake >= 5 and m < want:
                return min(cheap, key=lambda a: cost(st, p, a) - 0.1 * eff(st, p, a))
            if ok: return min(ok, key=lambda a: cost(st, p, a))
            return passa if m >= 0 or stake < 6 else max(plays, key=lambda a: eff(st, p, a)) if stake >= 8 else passa
        return passa

# ----- persona bots (follow panel/personas/*.md "How they play")
class Planner(Strategic):      # strategist: plans ahead, banks coins, careful stakes
    name = "planner"
    def __init__(s, seed=0): super().__init__(seed, noise=0.0, last_word=True, stake_bias=-0.5)
class Instinct(Strategic):     # casual: gut feel, noisy, no counting
    name = "instinct"
    def __init__(s, seed=0): super().__init__(seed, noise=0.30, last_word=False, stake_bias=1.0)
class Optimiser(Strategic):    # competitor: strongest line
    name = "optimiser"
    def __init__(s, seed=0): super().__init__(seed, noise=0.0, last_word=True, stake_bias=0.0)
class Flavour(Strategic):      # story: dramatic plays, big spends, hushes, leads for flair
    name = "flavour"
    def __init__(s, seed=0): super().__init__(seed, noise=0.15, last_word=False, stake_bias=2.0, drama=2.0)
    def choose(s, st, p, acts, retort=False):
        plays = [a for a in acts if a[0] == "play"]
        # drama: always take a Hush with a big target, or spend coins
        dram = [a for a in plays if (p == 1 and a[2] is not None and "hush" in st.hand[p][a[1]][2] and eff(st, p, a) >= 5)
                or (p == 0 and (a[2] or 0) >= 2)]
        if dram and s.r.random() < 0.7 and margin(st, p) < 6: return max(dram, key=lambda a: eff(st, p, a))
        return super().choose(st, p, acts, retort)
class Cautious(Strategic):     # family: simple/safe, passes when ahead, doesn't read the opponent
    name = "cautious"
    def __init__(s, seed=0): super().__init__(seed, noise=0.20, last_word=False, stake_bias=-1.5, caution=0.3, push=False)
class Expert(Strategic):       # barraiser: strongest line, tests exploits; slightly more aggressive stake use
    name = "expert"
    def __init__(s, seed=0): super().__init__(seed, noise=0.0, last_word=True, stake_bias=0.5)

PERSONA = {"strategist": Planner, "casual": Instinct, "competitor": Optimiser, "story": Flavour, "family": Cautious, "barraiser": Expert}
ALL = {"random": Random, "greedy": Greedy, "strategic": Strategic}
