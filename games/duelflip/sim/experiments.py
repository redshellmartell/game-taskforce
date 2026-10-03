import sys
from game import Config, play
from run import match, mk, mean, mirror_line
n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
cfg = Config()

print("== A. Leave-mode test (same bot, different leave rule), win%% of row vs 'greedy:low', n=%d" % n)
for base in ["greedy", "strategic", "bank_early"]:
    ref = base + ":low"
    for m in ["low", "high", "rand", "bait", "species", "smart"]:
        if m == "low":
            continue
        r = match(cfg, base + ":" + m, ref, n)
        print("%-12s leave=%-8s vs leave=low: %.1f%%" % (base, m, 100 * r["a_wins"] / n))

print("\n== B. Seat balance: first-seat win%% by second_pts and buoys (mirrors), n=%d" % n)
for bots_ in ["random", "greedy", "bank_early", "pusher", "strategic"]:
    row = []
    for sp in [0, 2, 3, 4]:
        c = Config(second_pts=sp)
        r = match(c, bots_, bots_, n, base=300000)
        row.append("+%d: %.1f" % (sp, 100 * r["first_wins"] / n))
    print("%-12s %s" % (bots_, "   ".join(row)))

print("\n== C. Mixed-skill seat check: strategic first vs strategic second only etc. (rules as written)")
r = match(cfg, "strategic", "greedy", n, base=400000)
print("strategic vs greedy: strategic wins %.1f%%, first seat wins %.1f%%" % (100 * r["a_wins"] / n, 100 * r["first_wins"] / n))

print("\n== D. Pusher target sweep vs strategic (win%% of pusher)")
for t in [4, 8, 12, 16, 20, 30]:
    import bots as B
    B.ALL["pt"] = lambda seed, leave_mode=None, t=t: B.Pusher(seed, target=t, leave_mode=leave_mode)
    r = match(cfg, "pt", "strategic", n)
    print("target %2d: %.1f%%" % (t, 100 * r["a_wins"] / n))

print("\n== E. Species bonus: share of games where bonus flips outcome")
import random
flip = 0; tot = 0; ws = []
for i in range(n):
    r = play(cfg, (mk("strategic", i), mk("strategic", i + 1)), 500000 + i); st = r["st"]
    s0, s1 = r["scores"]
    b0 = b1 = 0
    for s in range(6):
        a = sum(1 for x, _ in st.haul[0] if x == s); b = sum(1 for x, _ in st.haul[1] if x == s)
        b0 += a > b; b1 += b > a
    raw0 = s0 - 8 * b0; raw1 = s1 - 8 * b1 - 3
    w_raw = 0 if raw0 > raw1 else 1
    flip += (w_raw != r["winner"]); tot += 1; ws.append((b0, b1))
print("bonus flips winner in %.1f%% of games; avg species won p1 %.2f p2 %.2f" % (100 * flip / tot, mean([a for a, _ in ws]), mean([b for _, b in ws])))

print("\n== F. Refund threshold sweep, strategic mirror, first-seat win%% / avg turns / busts per game")
for ra in [3, 4, 5, 99]:
    c = Config(refund_at=ra); r = match(c, "strategic", "strategic", n, base=600000)
    print("refund_at %s: first %.1f%% turns %.1f busts/g %.2f" % (ra, 100 * r["first_wins"] / n, mean(r["turns"]), r["busts"] / n))
print("\n== G. Hoarder vs greedy (never uses buoy) - does holding matter? win%% of hoarder")
r = match(cfg, "hoarder", "greedy", n); print("%.1f%%" % (100 * r["a_wins"] / n))
print("\n== H. Rule toggles, strategic vs random win%% and bank_early mirror ties/turns")
for lab, c in [("as written", Config()), ("optional 2nd flip", Config(mandatory_second=False)), ("no scout", None)]:
    if c is None: continue
    r = match(c, "strategic", "random", n, base=700000)
    m = match(c, "bank_early", "bank_early", n, base=710000)
    print("%-18s strat v rand %.1f%% | bank_early mirror busts/g %.2f ties %.1f%% turns %.1f" % (lab, 100 * r["a_wins"] / n, m["busts"] / n, 100 * m["ties"] / n, mean(m["turns"])))
print("\n== I. Leaving-allowed-leftover variant (take_leftovers=False): leave-low strategic vs greedy")
c = Config(take_leftovers=False)
r = match(c, "greedy:low", "greedy:high", n); print("low vs high (leftover may stay): %.1f%%" % (100 * r["a_wins"] / n))
