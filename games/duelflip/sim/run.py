import sys
from game import Config, play
import bots as B

def mk(spec, seed):
    """spec: name or name:leave_mode"""
    if ":" in spec:
        n, m = spec.split(":"); return B.ALL[n](seed, leave_mode=m)
    return B.ALL[spec](seed)

def match(cfg, a, b, n, base=0):
    R = dict(a_wins=0, first_wins=0, ties=0, caps=0, turns=[], lc=[], el=0, eln=0, busts=0, games=0,
             small_busts=0, bait_busts=0, scout=0, flips=0, bust_pile=[], bank_pile=[], left=[], refunds=0, forced=0, scores=[])
    for i in range(n):
        seed = base + i; a_first = (i % 2 == 0)
        bs = (mk(a, seed), mk(b, seed + 1)) if a_first else (mk(b, seed + 1), mk(a, seed))
        r = play(cfg, bs, seed); st = r["st"]
        a_seat = 0 if a_first else 1; w = r["winner"]
        R["a_wins"] += (w == a_seat); R["first_wins"] += (w == 0)
        R["ties"] += r["tie"]; R["caps"] += r["capped"]; R["turns"].append(r["turns"])
        h = st.history; sg = [x for x in ((d > 0) - (d < 0) for d in h) if x]
        R["lc"].append(sum(1 for x, y in zip(sg, sg[1:]) if x != y))
        k = len(h) // 3
        if k and h[k]: R["eln"] += 1; R["el"] += ((h[k] > 0) == (w == 0))
        s = st.stats
        R["busts"] += s["busts"]; R["small_busts"] += s["small_busts"]; R["bait_busts"] += s["bait_clash_busts"]
        R["scout"] += s["scout_discards"]; R["flips"] += s["flips"]; R["bust_pile"] += s["bust_pile"]
        R["bank_pile"] += s["bank_pile"]; R["left"] += s["left_vals"]; R["refunds"] += sum(s["refunds"]); R["forced"] += s["forced_empty_end"]
        R["scores"].append(sum(r["scores"]))
        R["games"] += 1
    return R

def mean(x): return sum(x) / len(x) if x else 0.0

def mirror_line(nm, R, n):
    t = R["turns"]
    return ("%-22s seat1 %.1f%%  ties %.2f%%  caps %d  turns %.1f (%d-%d)  LC %.1f  earlyLeadWin %.0f%%  busts/g %.2f  bust/turn %.1f%%  1-card-busts/g %.2f  bait-busts/g %.2f  avgbustpile %.1f  avgbankpile %.1f"
            % (nm, 100 * R["first_wins"] / n, 100 * R["ties"] / n, R["caps"], mean(t), min(t), max(t), mean(R["lc"]),
               100 * R["el"] / max(1, R["eln"]), R["busts"] / n, 100 * R["busts"] / sum(t), R["small_busts"] / n, R["bait_busts"] / n,
               mean(R["bust_pile"]), mean(R["bank_pile"])))

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    cfg = Config()
    names = list(B.ALL)
    print("== Round robin, win%% of ROW vs COL, n=%d/pair, seats alternate" % n)
    print("%-14s" % "" + "".join("%-14s" % c[:13] for c in names) + "avg")
    for a in names:
        row = []
        for b in names:
            row.append(None if a == b else 100 * match(cfg, a, b, n)["a_wins"] / n)
        v = [x for x in row if x is not None]
        print("%-14s" % a + "".join("%-14s" % ("-" if x is None else "%.1f" % x) for x in row) + "%.1f" % mean(v))
    print("\n== Mirror matches")
    for nm in names:
        print(mirror_line(nm, match(cfg, nm, nm, n, base=100000), n))
