import sys, itertools
from collections import defaultdict
from game import Config, play
import bots as B

def match(cfg, a, b, n, base=0):
    """a plays first in half... seats randomised via seed parity: a is first in even games."""
    res = {"a_wins": 0, "a_first_wins": 0, "a_first_games": 0, "first_wins": 0, "ties": 0, "caps": 0,
           "turns": [], "lead_changes": [], "early_leader_wins": 0, "early_n": 0, "buoys_unused_win": [0,0], "busts": 0}
    for i in range(n):
        seed = base + i
        a_first = (i % 2 == 0)
        bots = (B.ALL[a](seed), B.ALL[b](seed + 1)) if a_first else (B.ALL[b](seed + 1), B.ALL[a](seed))
        r = play(cfg, bots, seed)
        a_seat = 0 if a_first else 1
        w = r["winner"]
        res["a_wins"] += (w == a_seat)
        res["first_wins"] += (w == 0)
        if a_first:
            res["a_first_games"] += 1; res["a_first_wins"] += (w == 0)
        res["ties"] += r["tie"]; res["caps"] += bool(r["capped"])
        res["turns"].append(r["turns"])
        h = r["st"].history
        signs = [1 if d > 0 else -1 if d < 0 else 0 for d in h]
        nz = [s for s in signs if s]
        res["lead_changes"].append(sum(1 for x, y in zip(nz, nz[1:]) if x != y))
        k = len(h) // 3
        if k and h[k] != 0:
            res["early_n"] += 1
            res["early_leader_wins"] += ((h[k] > 0) == (w == 0))
        res["busts"] += r["st"].stats["busts"]
        # leftover buoys of winner
        res["buoys_unused_win"][0] += r["st"].buoys[w]
    return res

def mean(x): return sum(x) / len(x)

def summary(cfg, n):
    names = ["random", "greedy", "bank_early", "bank_early_bait", "pusher", "collector", "strategic"]
    out = []
    print("== Round robin (win%% of ROW vs COL, seats alternate), n=%d per pair" % n)
    print("%-16s" % "" + "".join("%-16s" % c for c in names) + "avg")
    tot = {}
    for a in names:
        row = []
        for b in names:
            if a == b: row.append(None); continue
            r = match(cfg, a, b, n)
            row.append(100 * r["a_wins"] / n)
        tot[a] = mean([x for x in row if x is not None])
        print("%-16s" % a + "".join("%-16s" % ("-" if x is None else "%.1f" % x) for x in row) + "%.1f" % tot[a])
    return tot

def mirror(cfg, n, name):
    r = match(cfg, name, name, n, base=100000)
    return r

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    cfg = Config()
    summary(cfg, n)
    print("\n== Mirror matches (seat bias, length, ties, leader)")
    for nm in ["random", "greedy", "bank_early", "bank_early_bait", "pusher", "collector", "strategic"]:
        r = mirror(cfg, n, nm)
        print("%-16s first-seat win %.1f%%  ties %.2f%%  caps %d  turns avg %.1f (min %d max %d)  lead changes %.1f  early-leader wins %.1f%%  busts/game %.2f"
              % (nm, 100*r["first_wins"]/n, 100*r["ties"]/n, r["caps"], mean(r["turns"]), min(r["turns"]), max(r["turns"]),
                 mean(r["lead_changes"]), 100*r["early_leader_wins"]/max(1,r["early_n"]), r["busts"]/n))
