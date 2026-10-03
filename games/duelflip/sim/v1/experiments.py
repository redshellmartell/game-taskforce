import sys
from game import Config, play
import bots as B
from run import match, mean
n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000

print("== Pusher target sweep vs strategic / greedy-12 (pusher win%)")
for t in [4, 8, 12, 16, 20, 25, 30]:
    B.ALL["p%d" % t] = (lambda t: (lambda seed=0: B.Pusher(seed, target=t)))(t)
    r1 = match(Config(), "p%d" % t, "strategic", 1000)
    r2 = match(Config(), "p%d" % t, "bank_early", 1000)
    print("target %2d: vs strategic %.1f  vs bank_early %.1f" % (t, 100*r1["a_wins"]/1000, 100*r2["a_wins"]/1000))

print("\n== Lifebuoy config sweep: first-seat win%% in mirror (strategic | greedy), ties%%, n=%d" % n)
for buoys in [(1,2),(1,1),(2,2),(0,0),(1,3),(2,3),(0,1),(0,2),(3,3)]:
    cfg = Config(buoys=buoys)
    rs = match(cfg, "strategic", "strategic", n, base=500000)
    rg = match(cfg, "greedy", "greedy", n, base=500000)
    print("buoys %s: strategic first %.1f (ties %.1f) | greedy first %.1f (ties %.1f) | strat buoys used/game %.2f" % (
        buoys, 100*rs["first_wins"]/n, 100*rs["ties"]/n, 100*rg["first_wins"]/n, 100*rg["ties"]/n, 0))

print("\n== Species bonus sweep (strategic mirror): first-seat win%, and %% games where bonus flips outcome")
for bonus in [0, 3, 5, 7]:
    cfg = Config(bonus=bonus)
    r = match(cfg, "strategic", "strategic", n, base=700000)
    flips = 0
    for i in range(n):
        res = play(cfg, (B.Strategic(i), B.Strategic(i+1)), 700000 + i)
        st = res["st"]
        raw = st.hauls_value(0) + 2*st.buoys[0] - st.hauls_value(1) - 2*st.buoys[1]
        rw = 0 if raw > 0 else 1
        flips += (rw != res["winner"])
    print("bonus %d: first %.1f ties %.1f  outcome decided by bonus (differs from raw-sum winner) %.1f%%" % (bonus, 100*r["first_wins"]/n, 100*r["ties"]/n, 100*flips/n))

print("\n== Unused-buoy value sweep (strategic vs greedy, strategic win%%; and strategic mirror first%%)")
for bv in [0, 1, 2, 3, 5]:
    cfg = Config(buoy_value=bv)
    r = match(cfg, "strategic", "greedy", n, base=900000)
    m = match(cfg, "strategic", "strategic", n, base=900000)
    print("buoy_value %d: strategic beats greedy %.1f%%, mirror first %.1f%%" % (bv, 100*r["a_wins"]/n, 100*m["first_wins"]/n))

print("\n== Unused-buoy hoarding vs spending: Strategic variants with buoy_thresh (vs strategic default)")
for th in [0, 6, 10, 16, 24, 99]:
    B.ALL["s_th%d" % th] = (lambda th: (lambda seed=0: B.Strategic(seed, buoy_thresh=th)))(th)
    r = match(Config(), "s_th%d" % th, "strategic", n, base=300000)
    print("buoy_thresh %2d (never spend if 99): win %.1f%%" % (th, 100*r["a_wins"]/n))

print("\n== Buoy hold-vs-use: share of winners' final unused buoys, strategic mirror")
tot=[0,0,0]; cnt=0
used=[0,0]
for i in range(n):
    res = play(Config(), (B.Strategic(i), B.Strategic(i+1)), 11000+i)
    st=res["st"]; w=res["winner"]
    tot[0]+=st.buoys[w]; tot[1]+=st.buoys[1-w]
    used[0]+=st.stats["buoys_used"][0]; used[1]+=st.stats["buoys_used"][1]
    # winners by seat holding unused buoy
print("avg unused buoys: winner %.2f loser %.2f; buoys used by seat0 %.2f seat1 %.2f per game" % (tot[0]/n, tot[1]/n, used[0]/n, used[1]/n))

print("\n== Bank-early dominance: bank_early vs each, plus 'bank-early w/ buoy hoard' share of 60 turns")
for o in ["random","greedy","pusher","collector","strategic","bank_early"]:
    r = match(Config(), "bank_early", o, n, base=40000)
    print("bank_early vs %-10s win %.1f%%" % (o, 100*r["a_wins"]/n))
# Variant: bank_early against pusher16 / s with 2 flips
class TwoFlip(B.BankEarly):
    name="two_flip"
    def keep_flipping(self, st, p): return len(st.pile) < 2
B.ALL["two_flip"]=TwoFlip
for o in ["strategic","greedy","bank_early"]:
    r = match(Config(), "two_flip", o, n, base=40000)
    print("two_flip vs %-10s win %.1f%%" % (o, 100*r["a_wins"]/n))

print("\n== Species-bonus swing: avg bonus-winning species per game and bonus margin (strategic mirror)")
b=[]
for i in range(500):
    res=play(Config(), (B.Strategic(i),B.Strategic(i+1)),i); st=res["st"]
    a=0;c=0
    for s in range(6):
        x=sum(1 for q,_ in st.haul[0] if q==s); y=sum(1 for q,_ in st.haul[1] if q==s)
        a+= x>y; c+= y>x
    b.append((a,c,6-a-c))
print("avg species won by p0 %.2f, p1 %.2f, tied %.2f" % tuple(mean([t[k] for t in b]) for k in range(3)))
