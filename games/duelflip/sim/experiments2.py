import sys
from game import Config, play
from run import match, mk, mean
import bots as B
n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
cfg = Config()
print("== Strategic decomposition (win%% of row vs greedy:low, n=%d)" % n)
for s in ["strategic", "strategic:low", "greedy:smart", "greedy:low", "bank_early:smart", "bank_early:low"]:
    print("%-18s %.1f" % (s, 100 * match(cfg, s, "greedy:low", n, base=800000)["a_wins"] / n))
print("\n== Buoy spend threshold sweep (strategic buoy_min) vs default strategic")
for bm in [0, 5, 9, 14, 20, 999]:
    B.ALL["sb"] = lambda seed, leave_mode=None, bm=bm: B.Strategic(seed, buoy_min=bm, leave_mode=leave_mode)
    print("buoy_min %3d: %.1f%%" % (bm, 100 * match(cfg, "sb", "strategic", n, base=810000)["a_wins"] / n))
print("\n== Risk sweep vs default strategic")
for rk in [0.3, 0.6, 1.0, 1.5, 2.5]:
    B.ALL["sr"] = lambda seed, leave_mode=None, rk=rk: B.Strategic(seed, risk=rk, leave_mode=leave_mode)
    print("risk %.1f: %.1f%%" % (rk, 100 * match(cfg, "sr", "strategic", n, base=820000)["a_wins"] / n))
print("\n== Bust size and refund frequency, strategic mirror")
import collections
bp = []; ref = 0; use = [0, 0]; g = 0; unused_end = 0; small = 0; turns = 0; bust1 = 0
for i in range(n):
    r = play(cfg, (mk("strategic", i), mk("strategic", i + 1)), 900000 + i); s = r["st"].stats
    bp += s["bust_pile"]; ref += sum(s["refunds"]); use[0] += s["buoy_used"][0]; use[1] += s["buoy_used"][1]
    turns += r["turns"]; g += 1
    unused_end += sum(r["st"].buoys)
print("busts with pile value<=5: %.0f%% ; <=9: %.0f%% ; >=15: %.0f%%" % tuple(100 * sum(1 for x in bp if f(x)) / len(bp) for f in (lambda x: x <= 5, lambda x: x <= 9, lambda x: x >= 15)))
print("avg bust pile value %.1f; refunds/game %.2f; buoys used/game %.2f; ready buoys left at end/game %.2f" % (mean(bp), ref / g, sum(use) / g, unused_end / g))
print("\n== How often does the leave choice have 2+ candidates, and how often does smart pick non-lowest?")
class Spy(B.Strategic):
    stats = [0, 0, 0]
    def leave(self, st, p, cands):
        i = super().leave(st, p, cands)
        Spy.stats[0] += 1
        if len(cands) > 1:
            Spy.stats[1] += 1
            if st.river[i][1] != min(st.river[j][1] for j in cands): Spy.stats[2] += 1
        return i
B.ALL["spy"] = Spy
for i in range(n // 4): play(cfg, (mk("spy", i), mk("spy", i + 1)), 950000 + i)
print("banks %d, with choice %.0f%%, non-lowest picked in %.0f%% of choices" % (Spy.stats[0], 100 * Spy.stats[1] / Spy.stats[0], 100 * Spy.stats[2] / Spy.stats[1]))
print("\n== Dead-turn rate (turn where swing <=3 pts or banks <=3 pts) strategic mirror")
dead = tot = 0; zero = 0
for i in range(n // 2):
    c = Config(); r = play(c, (mk("strategic", i), mk("strategic", i + 1)), 960000 + i); h = [0] + r["st"].history
    for a, b in zip(h, h[1:]):
        tot += 1; dead += abs(b - a) <= 3; zero += (b == a)
print("turns with |haul swing| <=3: %.1f%% ; exactly zero: %.1f%% (v1: ~9-12%% were no-effect busts)" % (100 * dead / tot, 100 * zero / tot))
