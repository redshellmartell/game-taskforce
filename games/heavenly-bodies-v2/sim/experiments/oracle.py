"""Oracle safety test: with perfect information of the next opponent's hand, how often can the active player complete a
winning pattern AND leave it unbreakable for one opponent turn? (structural check on the 'orbit must survive a round' rule)"""
import sys; sys.path.insert(0,'..')
from multiprocessing import Pool
import game as G
import bots as B
from game import play, patterns, crash, spin_orbit, apply_launches, rebound_ok, CLOCK, CCW

def safe_vs(st, orbits, p, n, rb_flags):
    """orbits: orbits after my turn. Return True if every opponent (sequentially next one only, then others by ignoring) cannot capture my body."""
    o = (p + 1) % n  # next opponent only (lower bound on danger; others add more)
    hand = st.hands[o]
    mine = sum(1 for c in orbits[o] if c)
    rb = st.rebound and all(mine < sum(1 for c in orbits[x] if c) for x in range(n) if x != o)
    plans = [()] + [((i, s),) for i in range(len(hand)) for s in range(4)]
    if rb:
        plans += [((i, s), (j, t)) for i in range(len(hand)) for s in range(4) for j in range(len(hand)) if j != i for t in range(4) if t != s]
    base_ct = sum(1 for c in orbits[p] if c)
    for pl in plans:
        orb_o, _, _ = apply_launches(orbits[o], hand, pl)
        for q in range(n):
            ob = [list(x) for x in orbits]; ob[o] = orb_o
            if not any(ob[q]): continue
            for d in (CLOCK, CCW):
                o2 = [list(x) for x in ob]; o2[q] = spin_orbit(o2[q], d)
                for e in crash(o2, q, n):
                    if e[2] == p: return False
    return True

def probe(args):
    n, seed = args
    bots = [B.MAKERS['strategic'](seed*3+i) for i in range(n)]
    res = dict(pos=0, form=0, safe=0)
    # replay a game via play but intercept: wrap bots' turn to probe
    class P:
        def __init__(s, b): s.b = b
        def __getattr__(s, k): return getattr(s.b, k)
        def turn(s, st, p, rb):
            res['pos'] += 1
            hand = st.hands[p]
            plans = G.legal_launches(st, p, rb)
            if rb: plans = [pl for pl in plans] 
            found = False; safe = False
            for pl in plans[:]:
                for q in range(n):
                    for d in (CLOCK, CCW):
                        orbits = [list(x) for x in st.orbits]
                        orbits[p], _, _ = apply_launches(orbits[p], hand, pl)
                        if not any(orbits[q]): continue
                        orbits[q] = spin_orbit(orbits[q], d)
                        ev = crash(orbits, q, n)
                        if any(e[0]=="cap" and e[2]==p for e in ev): continue
                        if patterns(orbits[p]):
                            found = True
                            if safe_vs(st, orbits, p, n, None): safe = True; break
                    if safe: break
                if safe: break
            res['form'] += found; res['safe'] += safe
            return s.b.turn(st, p, rb)
    play([P(b) for b in bots], seed, n)
    return res

if __name__ == "__main__":
    with Pool(4) as pool:
        for n in (2, 3, 4):
            rs = pool.map(probe, [(n, s) for s in range(12)])
            pos = sum(r['pos'] for r in rs); f = sum(r['form'] for r in rs); s = sum(r['safe'] for r in rs)
            print(n, "positions", pos, "can form pattern", f, "can form AND safe vs next opp", s)
