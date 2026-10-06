"""Headline run + experiments for Last Bid Standing. Usage: python3 run.py [games=2000] [--no-exp]
Writes ../playtest.json (verdict fields filled by hand-reviewed constants below) and sim/results.json."""
import json, math, os, sys, statistics as stt
from dataclasses import replace
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import Config, play, CATS
import bots as B
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SLUG = "five-six-simultaneous-auction"
TARGET_MIN = 20

CLS = {"S": B.Strategic, "R": B.Random, "G": B.Greedy, "N": B.NoMemory, "H": B.IgnoreHype, "C": B.IgnoreCrash,
       "T": B.IgnoreTies, "P": B.Planner, "I": B.Instinct, "A": B.IgnoreCap, "L": B.Lite}
KINDS = {"mixed": "SRGSRG", "mixedP": "PRGPRG", "SvR": "SRSRSR", "PvR": "PRPRPR", "LvR": "LRLRLR", "oneS": "SRRRRR", "oneP": "PRRRRR",
         "oneL": "LRRRRR", "oneG": "GRRRRR", "allS": "SSSSSS", "allR": "RRRRRR", "allG": "GGGGGG", "PvS": "PSPSPS",
         "abl-H": "SHSHSH", "abl-C": "SCSCSC", "abl-T": "STSTST", "abl-A": "SASASA", "ablP-H": "PHPHPH", "ablP-C": "PCPCPC",
         "ablP-T": "PTPTPT", "ablP-A": "PAPAPA"}
def table(kind, n, g):
    """bot class list for a table; rotated by game index g so every bot meets every seat equally."""
    base = [CLS[ch] for ch in KINDS[kind]][:n]
    k = g % n
    return base[k:] + base[:k]

def pearson(x, y):
    n = len(x); mx, my = sum(x) / n, sum(y) / n
    sx = math.sqrt(sum((a - mx) ** 2 for a in x)); sy = math.sqrt(sum((b - my) ** 2 for b in y))
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy) if sx and sy else 0.0

def evaluate(cfg, kind, N, seed0=0, detail=False):
    n = cfg.players; seat = [0.0] * n; byb = {}; cnt = {}; ties = 0
    leadch = []; early = []; early10 = []; cap = 0
    unsold = canc = nodraw = resh = forced = 0; hype_pts = tot_pts = 0; lastflip = crashflip = 0
    blk = []; handavg = []; leftover = []; sec = []; crashed = [0] * CATS; crash_none = 0; margin = []
    X = {"pass": [], "bid": [[] for _ in range(cfg.bid_max + 1)], "lotcat": [[] for _ in range(CATS)], "lotval": [[] for _ in range(8)],
         "win": [], "plays": [[0, 0] for _ in range(cfg.bid_max + 1)]}
    for g in range(N):
        classes = table(kind, n, g)
        bots = [c(seed0 + g * 7 + i) for i, c in enumerate(classes)]
        r = play(cfg, bots, seed0 + g); st = r["st"]; w = r["winners"]
        for x in w:
            seat[x] += 1 / len(w); byb.setdefault(classes[x].name, [0.0, 0]); byb[classes[x].name][0] += 1 / len(w)
        for c in classes: byb.setdefault(c.name, [0.0, 0]); byb[c.name][1] += 1
        ties += len(w) > 1
        lc = 0; last = -1
        for l in st.leaders:
            if l >= 0:
                if last >= 0 and l != last: lc += 1
                last = l
        leadch.append(lc)
        for arr, idx in ((early, cfg.rounds // 2), (early10, cfg.rounds - 3)):
            l = st.leaders[idx - 1]
            if l >= 0: arr.append(1 if l in w else 0)
        blk.append(st.stats["block_sum"] / cfg.rounds); unsold += st.stats["unsold"]; canc += st.stats["cancelled"]; nodraw += st.stats["nodraw"]; resh += st.stats["reshuffles"]
        forced += st.stats["forced_pass"]; handavg.append(st.stats["hand_sum"] / st.stats["hand_obs"])
        leftover.append(sum(len(h) for h in st.hands) / n); sec.append(st.stats["sec"])
        sc, eff = r["scores"], r["eff"]
        hp = sum(eff[c] for p in range(n) for c, v in st.won[p]); hype_pts += hp; tot_pts += sum(sc)
        for c in st.crashed(): crashed[c] += 1
        if st.leader_before_last is not None and st.leader_before_last >= 0 and st.leader_before_last not in w: lastflip += 1
        if st.crash_before_last != st.crashed(): crashflip += 1
        ss = sorted(sc, reverse=True); margin.append(ss[0] - ss[1])
        if detail:
            for p in range(n):
                win = 1 if p in w else 0; X["win"].append(win)
                X["pass"].append(st.plays[p]["pass_"])
                for v in range(1, cfg.bid_max + 1): X["bid"][v].append(st.plays[p]["bid"][v])
                for c in range(CATS): X["lotcat"][c].append(sum(1 for l in st.won[p] if l[0] == c))
                for v in range(1, 8): X["lotval"][v].append(sum(1 for l in st.won[p] if l[1] - cfg.lot_bonus == v))
            for v in range(1, cfg.bid_max + 1):
                X["plays"][v][0] += sum(pl["bid"][v] for pl in st.plays); X["plays"][v][1] += st.lotwins_by_bid[v]
    res = dict(block_mean=sum(blk) / N, n=n, N=N, seat={i + 1: seat[i] / N for i in range(n)}, bot={k: v[0] / v[1] for k, v in byb.items()},
               ties=ties / N, lead_changes=sum(leadch) / N, runaway_half=sum(early) / max(1, len(early)),
               runaway_late=sum(early10) / max(1, len(early10)), unsold_per_game=unsold / N, cancelled_bids_per_game=canc / N,
               nodraw_per_game=nodraw / N, reshuffles=resh / N, forced_pass_rate=forced / (N * n * cfg.rounds),
               hype_share_of_points=hype_pts / max(1, tot_pts), mean_hand=sum(handavg) / N, leftover_cards=sum(leftover) / N,
               minutes=2 + 1 + sum(sec) / N / 60, minutes_sd=stt.pstdev(sec) / 60, last_round_winner_flip=lastflip / N,
               last_round_crash_flip=crashflip / N, crash_rate_by_cat=[c / N for c in crashed], mean_margin=sum(margin) / N,
               leadchange_hist=[leadch.count(k) for k in range(max(leadch) + 1)])
    if detail: res["X"] = X
    return res

def spread(res):  # max deviation of a seat from fair, in points
    return max(abs(v - 1 / res["n"]) for v in res["seat"].values()) * 100

def _job(a):
    key, n, kind, kw, N, seed0, detail = a
    return key, evaluate(replace(Config(players=n), **kw), kind, N, seed0=seed0, detail=detail)

def pct(x): return round(x * 100, 1)
def gapof(r, a="strategic", b="random"): return (r["bot"][a] - r["bot"][b]) * 100

# Configurations tried beyond the headline (max 5; the first pass is the headline itself). Edit EXP to change.
EXP = {"E1 lots 3-6": dict(lot_bonus=1), "E2 hand5": dict(start_hand=5), "E3 bids1-11": dict(bid_max=11),
       "E4 lots 4-7": dict(lot_bonus=2), "E5 income1": dict(income=1)}

def main():
    if '--rewrite' in sys.argv:
        out = json.load(open(os.path.join(HERE, 'results.json'))); write_playtest(out, 2000); return
    from multiprocessing import Pool
    N = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 2000
    jobs = []
    for n in (5, 6):
        for kind in KINDS:
            jobs.append(("%dp-%s" % (n, kind), n, kind, {}, N, n * 100000, kind == "mixed"))
    if "--no-exp" not in sys.argv:
        for name, kw in EXP.items():
            for kind in ("oneS", "allS", "abl-N"):
                jobs.append(("%s 6p-%s" % (name, kind), 6, kind, kw, N // 2, 777000, False))
    with Pool(4) as p: res = dict(p.map(_job, jobs))
    out = {"headline": {k: v for k, v in res.items() if k[:3] in ("5p-", "6p-")}, "experiments": {k: v for k, v in res.items() if k[:3] not in ("5p-", "6p-")}}
    with open(os.path.join(HERE, "results.json"), "w") as f: json.dump(out, f, default=lambda o: o, indent=1)
    write_playtest(out, N)
    h = out["headline"]
    print("Headline %d games per table kind (2 player counts x %d kinds)" % (N, len(KINDS)))
    for n in (5, 6):
        g = lambda k: h["%dp-%s" % (n, k)]
        print("%dp seatgap(allS) %.1f | lone S %.1f vs R %.1f (gap %.1f) | lone NoMem gap %.1f | lone G gap %.1f | mixed S/R/G %s" % (
            n, spread(g("allS")), pct(g("oneS")["bot"]["strategic"]), pct(g("oneS")["bot"]["random"]), gapof(g("oneS")), gapof(g("oneN"), "no-memory"),
            gapof(g("oneG"), "greedy"), [pct(g("mixed")["bot"][k]) for k in ("strategic", "random", "greedy")]))
        print("   3S+3R: S-R %.1f | 3N+3R: N-R %.1f | planner v instinct %s | S v instinct %s | planner v S %s" % (
            gapof(g("SvR")), gapof(g("NvR"), "no-memory"), (pct(g("PvI")["bot"]["planner"]), pct(g("PvI")["bot"]["instinct"])),
            (pct(g("SvI")["bot"]["strategic"]), pct(g("SvI")["bot"]["instinct"])), (pct(g("PvS")["bot"]["planner"]), pct(g("PvS")["bot"]["strategic"]))))
        print("   ablation (full S minus ablated, points): " + ", ".join("%s %.1f" % (k[4:], gapof(g(k), "strategic", {"N": "no-memory", "H": "ignore-hype", "C": "ignore-crash", "T": "ignore-ties"}[k[4]])) for k in ("abl-N", "abl-H", "abl-C", "abl-T")))
        a = g("allS")
        print("   allS: hype%% %.0f forced%% %.1f unsold %.1f block %.1f cancelled %.1f LC %.2f runaway %.2f/%.2f flip %.2f min %.1f tie %.3f" % (
            a["hype_share_of_points"] * 100, a["forced_pass_rate"] * 100, a["unsold_per_game"], a["block_mean"], a["cancelled_bids_per_game"],
            a["lead_changes"], a["runaway_half"], a["runaway_late"], a["last_round_winner_flip"], a["minutes"], a["ties"]))
    print("--- experiments (6p, %d games)" % (N // 2))
    for name in EXP:
        e = lambda k: out["experiments"]["%s 6p-%s" % (name, k)]
        a = e("allS")
        print("%s: loneS gap %.1f | N-abl S-N %.1f | allS hype%% %.0f forced%% %.1f unsold %.1f LC %.2f run %.2f flip %.2f seatgap %.1f" % (
            name, gapof(e("oneS")), gapof(e("abl-N"), "strategic", "no-memory"), a["hype_share_of_points"] * 100, a["forced_pass_rate"] * 100,
            a["unsold_per_game"], a["lead_changes"], a["runaway_half"], a["last_round_winner_flip"], spread(a)))

def write_playtest(out, N):
    h = out["headline"]; ps = json.load(open(os.path.join(HERE, "previous.json")))
    m5, m6 = h["5p-mixed"], h["6p-mixed"]
    avg = lambda f: (f(h["5p-" ]) if False else 0)
    both = lambda k, f: (f(h["5p-" + k]) + f(h["6p-" + k])) / 2
    bw = {k: round((m5["bot"][k] + m6["bot"][k]) / 2, 3) for k in ("random", "greedy", "strategic")}
    skill = round(both("oneS", gapof), 1)
    skill_mem = round(both("oneN", lambda r: gapof(r, "no-memory")), 1)
    skill_g = round(both("oneG", lambda r: gapof(r, "greedy")), 1)
    mixed_gap = round(both("SvR", gapof), 1)
    abl = {nm: round(both("abl-" + k, lambda r: gapof(r, "strategic", nm)), 1) for k, nm in (("N", "no-memory"), ("H", "ignore-hype"), ("C", "ignore-crash"), ("T", "ignore-ties"))}
    pvi = round(both("PvI", lambda r: gapof(r, "planner", "instinct")), 1)
    X6 = m6["X"]; ng = len(X6["win"])
    cards = [{"name": "Pass (Paddle)", "played_rate": round(sum(X6["pass"]) / (ng * 14), 3), "win_correlation": round(pearson(X6["pass"], X6["win"]), 3), "flag": None}]
    for lo, hi in ((1, 3), (4, 6), (7, 9), (10, 12)):
        v = [sum(X6["bid"][x][i] for x in range(lo, hi + 1)) for i in range(ng)]
        cards.append({"name": "Bid value %d-%d" % (lo, hi), "played_rate": round(sum(v) / (ng * 14), 3), "win_correlation": round(pearson(v, X6["win"]), 3), "flag": None})
    for v in range(2, 6):
        cards.append({"name": "Lot printed value %d" % v, "played_rate": 1.0, "win_correlation": round(pearson(X6["lotval"][v], X6["win"]), 3), "flag": None})
    for c, nm in enumerate(("Clocks", "Silver", "Paintings", "Books")):
        cards.append({"name": "Category lots: " + nm, "played_rate": 1.0, "win_correlation": round(pearson(X6["lotcat"][c], X6["win"]), 3), "flag": None})
    mins = both("mixed", lambda r: r["minutes"])
    a5, a6 = h["5p-allS"], h["6p-allS"]
    seat = {str(k): round(v, 3) for k, v in a6["seat"].items()}
    nj = len(h) * N + len(out["experiments"]) * (N // 2)
    man = os.path.join(HERE, "manual_findings.json")
    M = json.load(open(man)) if os.path.exists(man) else {}
    j = {"verdict": M.get("verdict", "NEEDS-FIXES (bots only, unvalidated)"), "revision": 1, "games_simulated": nj,
         "seat_win_rates": seat, "seat_balance_gap": round(max(spread(a5), spread(a6)), 1),
         "bot_win_rates": bw, "skill_expression": skill,
         "skill_detail": {"lone_strategic_vs_5_random": skill, "lone_no_memory_vs_random": skill_mem, "lone_greedy_vs_random": skill_g,
                          "mixed_3S_3R_gap": mixed_gap, "planner_minus_instinct_at_PvI_table": pvi, "ablation_full_minus_ablated_points": abl},
         "length": {"mean_turns": 14.0, "stdev": 0.0, "estimated_minutes": round(mins), "target_minutes": TARGET_MIN},
         "length_histogram": [{"turns": 14, "games": nj}],
         "ties": round(both("allS", lambda r: r["ties"]), 3), "turn_cap_hits": 0,
         "lead_changes_mean": round(both("mixed", lambda r: r["lead_changes"]), 2),
         "runaway_leader_rate": round(both("mixed", lambda r: r["runaway_half"]), 3),
         "hype_share_of_points": round(both("allS", lambda r: r["hype_share_of_points"]), 3),
         "forced_pass_rate": round(both("allS", lambda r: r["forced_pass_rate"]), 3),
         "unsold_lots_per_game": round(both("allS", lambda r: r["unsold_per_game"]), 2),
         "last_round_winner_flip": round(both("allS", lambda r: r["last_round_winner_flip"]), 3),
         "cards": cards, "previous": ps.get("previous", {}),
         "ambiguities": M.get("ambiguities", []), "problems": M.get("problems", [])}
    json.dump(j, open(os.path.join(ROOT, "games", SLUG, "playtest.json"), "w"), indent=2)
    return j

if __name__ == "__main__":
    main()
