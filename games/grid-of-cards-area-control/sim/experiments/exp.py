import sys, os, statistics
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import game as G, bots as B
from run import run, by_bot, lead_stats, seat_rates, minutes
N = 2000
class Staller(B.Strategic):
    """Exploit probe: when ahead on known trophies, avoid every move that floods."""
    name = "staller"
    def act(self, st, p, acts):
        est = [st.tv[p] if q == p else st.tn[q] * 2.17 for q in range(st.n)]
        if st.tv[p] > 0 and st.tv[p] >= max(e for q, e in enumerate(est) if q != p):
            safe = [a for a in acts if all(not fl for _, _, fl in B.outcomes(st, p, a))]
            if safe: return Strategic_pick(self, st, p, safe)
        return B.Strategic.act(self, st, p, acts)
def Strategic_pick(bot, st, p, acts): return B.Strategic.act(bot, st, p, acts)
for n in (2, 3):
    r = run(n, [Staller] + [B.Strategic] * (n - 1), N, 800000 + n)
    print("E1 staller vs strategic %dp:" % n, {k: round(v, 3) for k, v in by_bot(r).items()}, "stall-end %.2f" % (sum(x["stall"] for x in r) / N), "turns %.1f" % statistics.mean(x["turns"] for x in r))
G.STALL_MULT = 6
r = run(2, [B.Strategic] * 2, N, 900001)
print("E2 2p stall limit 6n: stall-end %.2f turns %.1f sd %.1f floods %.1f min %.1f lead %.2f runaway %.3f" % (sum(x["stall"] for x in r) / N, statistics.mean(x["turns"] for x in r),
      statistics.pstdev(x["turns"] for x in r), statistics.mean(x["floods"] for x in r), minutes(statistics.mean(x["turns"] for x in r), statistics.mean(x["floods"] for x in r)), *lead_stats(r)[:2]))
G.STALL_MULT = 3
for n in (2, 3):
    r = run(n, [B.Planner, B.Strategic] if n == 2 else [B.Planner, B.Strategic, B.Greedy], 1000, 910000 + n)
    print("E3 planner vs strategic(+greedy) %dp:" % n, {k: round(v, 3) for k, v in by_bot(r).items()})
r = run(2, [B.Expert, B.Strategic], 1000, 920000)
print("E4 expert vs strategic 2p:", {k: round(v, 3) for k, v in by_bot(r).items()}, "stall-end %.2f" % (sum(x["stall"] for x in r) / 1000))
