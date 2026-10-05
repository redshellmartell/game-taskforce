import sys, os, statistics
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.argv = ["x", "2000"]
import run as R, bots as B
def summ(name, rs, n):
    lc, ew, k = R.lead_stats(rs)
    print(name, "seat", [round(x,3) for x in R.seat_rates(rs,n)], "bots", {a:round(b,3) for a,b in R.by_bot(rs).items()}, "lc %.2f early %.3f turns %.1f storms %.2f shared %.3f" % (lc, ew, statistics.mean(r["turns"] for r in rs), statistics.mean(r["storms"] for r in rs), sum(r["shared"] for r in rs)/len(rs)))
which = sys.argv[1] if False else None
import sys as _s
mode = os.environ.get("EXP")
if mode == "big2":
    rs = R.run(2, [B.Strategic]*2, 10000, 100000*2); summ("2p mirror 10000", rs, 2)
if mode == "sand":
    summ("2p sandbag v strategic", R.run(2, [B.Sandbag, B.Strategic], 2000, 810000), 2)
    summ("3p sandbag + 2 strategic", R.run(3, [B.Sandbag, B.Strategic, B.Strategic], 2000, 820000), 3)
    summ("4p sandbag + 3 strategic", R.run(4, [B.Sandbag, B.Strategic, B.Strategic, B.Strategic], 2000, 830000), 4)
if mode == "tp":
    summ("2p twoply v strategic", R.run(2, [B.TwoPly, B.Strategic], 1000, 840000), 2)
    summ("3p twoply+2strategic", R.run(3, [B.TwoPly, B.Strategic, B.Strategic], 1000, 850000), 3)
if mode == "rem2":
    import game as G
    G.REMOVE[2] = 3
    summ("2p remove 3 mirror 5000", R.run(2, [B.Strategic]*2, 5000, 200000), 2)
    G.REMOVE[2] = 6
    summ("2p remove 6 mirror 3000", R.run(2, [B.Strategic]*2, 3000, 200000), 2)
