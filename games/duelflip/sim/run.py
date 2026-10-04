"""Duel Flip revision 2 simulation. Usage: python3 run.py [N=2000] [--exp] [--json ../playtest.json]
Prints a compact summary; details go to sim/results.json."""
import sys, json, math, collections, os
from game import Config, play
import bots as B
import notes as N

HERE = os.path.dirname(os.path.abspath(__file__))
def mk(spec, seed):
    if ":" in spec:
        n, m = spec.split(":"); return B.ALL[n](seed, leave_mode=m)
    return B.ALL[spec](seed)
def mean(x): return sum(x) / len(x) if x else 0.0

def match(cfg, a, b, n, base=0):
    R = dict(a=0.0, first=0.0, ties=0, scoreties=0, caps=0, turns=[], lc=[], el=0, eln=0, el3=0, el3n=0, games=0,
             S=collections.defaultdict(float), left=[], claim_by_val=[0]*11, bait_by_val=[0]*11, bust_pile=[], bank_pile=[])
    for i in range(n):
        seed = base + i; a_first = (i % 2 == 0)
        bs = (mk(a, seed), mk(b, seed + 1)) if a_first else (mk(b, seed + 1), mk(a, seed))
        r = play(cfg, bs, seed); st = r["st"]; a_seat = 0 if a_first else 1; w = r["winner"]
        R["a"] += 0.5 if w is None else (w == a_seat); R["first"] += 0.5 if w is None else (w == 0)
        R["ties"] += r["tie"]; R["scoreties"] += r["scoretie"]; R["caps"] += r["capped"]; R["turns"].append(r["turns"])
        h = st.history; sg = [(d > 0) - (d < 0) for d in h]; nz = [x for x in sg if x]
        R["lc"].append(sum(1 for x, y in zip(nz, nz[1:]) if x != y))
        k = len(h) // 2
        if k and h[k] and w is not None: R["eln"] += 1; R["el"] += ((h[k] > 0) == (w == 0))
        k = len(h) // 3
        if k and h[k] and w is not None: R["el3n"] += 1; R["el3"] += ((h[k] > 0) == (w == 0))
        s = st.stats
        for key in ("busts", "bait_busts", "flips", "scout_discards", "claims", "claim_tries", "bait_turns", "forced_empty_end"): R["S"][key] += s[key]
        R["S"]["buoys"] += sum(s["buoy_used"]); R["S"]["buoys_left"] += sum(st.buoys)
        R["left"] += s["left_vals"]; R["bust_pile"] += s["bust_pile"]; R["bank_pile"] += s["bank_pile"]
        for v in range(11): R["claim_by_val"][v] += s["claim_by_val"][v]; R["bait_by_val"][v] += s["bait_by_val"][v]
        R["games"] += 1
    return R

def sd(x):
    m = mean(x); return math.sqrt(sum((v - m) ** 2 for v in x) / len(x))

def headline(n, cfg):
    names = list(B.ALL); avg = {}; total = 0; caps = 0; pair = {}
    for a in names:
        w = []
        for b in names:
            if a == b: continue
            R = match(cfg, a, b, n); total += n; caps += R["caps"]; w.append(R["a"] / n); pair[a + " v " + b] = round(R["a"] / n, 3)
        avg[a] = mean(w)
    mir = {}
    for nm in names:
        mir[nm] = match(cfg, nm, nm, n, base=100000); total += n; caps += mir[nm]["caps"]
    return names, avg, mir, total, caps, pair

def leave_exps(n, cfg):
    out = {}
    for a, b in [("strategic:low", "strategic:smart"), ("strategic:high", "strategic:smart"),
                 ("strategic:low", "strategic:high"), ("strategic:rand", "strategic:smart")]:
        R = match(cfg, a, b, n, base=500000); out[a + " v " + b] = round(R["a"] / n, 3)
    return out

if __name__ == "__main__":
    args = sys.argv[1:]; nums = [a for a in args if a.isdigit()]; n = int(nums[0]) if nums else 2000
    cfg = Config()
    names, avg, mir, total, caps, pair = headline(n, cfg)
    S = mir["strategic"]; t = S["turns"]; mu = mean(t)
    gap = max(abs(100 * m["first"] / n - 50) for m in mir.values())
    seat1 = {k: round(m["first"] / n, 3) for k, m in mir.items()}
    el = S["el"] / max(1, S["eln"]); el3 = S["el3"] / max(1, S["el3n"])
    exps = leave_exps(n, cfg) if "--exp" in args else {}
    ss = S["S"]
    res = dict(n=n, avg=avg, pair=pair, seat1_mirror=seat1, gap=gap, turns_mean=mu, turns_sd=sd(t), ties=S["ties"] / n,
               scoreties=S["scoreties"] / n, caps=caps, lc=mean(S["lc"]), el_half=el, el_third=el3, exps=exps,
               claim_rate=ss["claims"] / max(1, ss["claim_tries"]), bait_turn_rate=ss["bait_turns"] / sum(t),
               busts_per_game=ss["busts"] / n, bait_busts_per_game=ss["bait_busts"] / n, buoys_per_game=ss["buoys"] / n,
               left_hist=dict(collections.Counter(S["left"])), scout_per_game=ss["scout_discards"] / n,
               claim_by_val=[round(S["claim_by_val"][v] / S["bait_by_val"][v], 3) if S["bait_by_val"][v] else None for v in range(11)],
               bait_by_val=S["bait_by_val"], avg_bust_pile=mean(S["bust_pile"]), forced_end=ss["forced_empty_end"] / n,
               hist=sorted(collections.Counter(t).items()), total=total)
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1)
    print("n=%d/pairing, %d games total" % (n, total))
    print("bot avg win%%: " + ", ".join("%s %.1f" % (k, 100 * v) for k, v in avg.items()))
    print("strategic - random gap: %.1f pts" % (100 * (avg["strategic"] - avg["random"])))
    print("seat1 win%% mirrors: " + ", ".join("%s %.1f" % (k, 100 * v) for k, v in seat1.items()) + "  worst gap %.1f" % gap)
    print("length (strategic mirror): mean %.1f turns sd %.1f range %d-%d; ties %.2f%% (full ties %.2f%%) caps %d" % (mu, sd(t), min(t), max(t), 100 * S["ties"] / n, 100 * S["scoreties"] / n, caps))
    print("lead changes %.2f; halfway leader wins %.1f%%; one-third leader wins %.1f%%" % (mean(S["lc"]), 100 * el, 100 * el3))
    print("bait: present on %.0f%% of turns, claimed %.0f%% of tries; busts/g %.2f (bait busts %.2f); buoys/g %.2f; avg bust pile %.1f"
          % (100 * res["bait_turn_rate"], 100 * res["claim_rate"], res["busts_per_game"], res["bait_busts_per_game"], res["buoys_per_game"], res["avg_bust_pile"]))
    print("claim rate by bait value 1-10: " + " ".join("%s" % ("-" if x is None else "%.2f" % x) for x in res["claim_by_val"][1:]))
    for k, v in exps.items(): print("leave exp  %-34s first wins %.1f%%" % (k, 100 * v))
    if "--json" in args:
        path = args[args.index("--json") + 1]
        cards = N.cards(res)
        out = {"verdict": N.VERDICT, "revision": N.REVISION, "games_simulated": total,
               "seat_win_rates": {"1": round(seat1["strategic"], 3), "2": round(1 - seat1["strategic"], 3)}, "seat_balance_gap": round(gap, 1),
               "bot_win_rates": {k: round(v, 3) for k, v in avg.items()}, "skill_expression": round(100 * (avg["strategic"] - avg["random"]), 1),
               "length": {"mean_turns": round(mu, 1), "stdev": round(sd(t), 1), "estimated_minutes": N.ESTIMATED_MINUTES, "target_minutes": N.TARGET_MINUTES},
               "length_histogram": [{"turns": k, "games": v} for k, v in res["hist"]],
               "ties": round(res["scoreties"], 4), "turn_cap_hits": caps, "lead_changes_mean": round(res["lc"], 2),
               "runaway_leader_rate": round(el, 3), "cards": cards, "ambiguities": N.AMBIGUITIES, "problems": N.PROBLEMS}
        json.dump(out, open(path, "w"), indent=2); open(path, "a").write("\n"); print("wrote", path)
