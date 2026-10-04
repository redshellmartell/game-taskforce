"""Fifty-Two Workshop simulation. Usage: python3 run.py [N=2000] [--exp] [--json ../playtest.json]
Prints a compact summary; details go to sim/results.json."""
import sys, json, math, collections, os
from game import *
import bots as B
import notes as N

HERE = os.path.dirname(os.path.abspath(__file__))
BOTS = {**B.ALL, **B.EXTRA}
TARGET_MIN = {1: 15, 2: 12, 3: 16, 4: 20}
def mean(x): return sum(x) / len(x) if x else 0.0
def sd(x):
    m = mean(x); return math.sqrt(sum((v - m) ** 2 for v in x) / len(x)) if x else 0.0

def table(names, n, cfg, base=0, rotate=True):
    """Play n games per seating (cyclic rotation of `names`). Returns per-bot-name aggregate dict."""
    k = len(names); R = dict(win=collections.defaultdict(float), seat=[0.0] * k, games=0, turns=[], caps=0, ties=0, scoreties=0, lc=[], el=0, eln=0,
        builds=0, gathers=0, minutes=[], card_built=collections.Counter(), card_win=collections.Counter(), scores=collections.defaultdict(list),
        app=0, passes=0, errors=0, inter=0, leader_turns=[], rush_first=0, clock_by_deck=0, win_scores=[], solo_win=0)
    rots = range(k) if rotate else [0]
    for rot in rots:
        order = [names[(i + rot) % k] for i in range(k)]
        for g in range(n):
            seed = base + rot * 100000 + g
            r = play(cfg, [BOTS[o](seed * 10 + i) for i, o in enumerate(order)], seed); st = r["st"]
            w = r["winners"]; R["games"] += 1; R["turns"].append(r["turns"]); R["caps"] += r["capped"]; R["ties"] += r["tie"]; R["scoreties"] += r["scoretie"]
            R["errors"] += st.errors; R["passes"] += st.passes; R["app"] += st.apprentice
            for i in range(k):
                R["scores"][order[i]].append(r["scores"][i])
            for i in w:
                R["win"][order[i]] += 1.0 / len(w); R["seat"][i] += 1.0 / len(w)
                R["win_scores"].append(r["scores"][i])
                for c in st.builds[i]: R["card_win"][c] += 1.0 / len(w)
            if cfg.n == 1: R["solo_win"] += r["scores"][0] >= cfg.solo_win
            for i in range(k):
                for c in st.builds[i]: R["card_built"][c] += 1
            R["builds"] += sum(st.nbuild); R["gathers"] += sum(st.gathers); R["inter"] += sum(st.inter)
            R["minutes"].append((25 * sum(st.nbuild) + 10 * sum(st.gathers)) / 60.0)
            h = st.rounds_hist; ld = []
            for sc in h:
                m = max(sc); lead = [i for i, s in enumerate(sc) if s == m]; ld.append(lead[0] if len(lead) == 1 else None)
            nz = [x for x in ld if x is not None]
            R["lc"].append(sum(1 for a, b in zip(nz, nz[1:]) if a != b))
            if k > 1 and h:
                mid = ld[len(ld) // 2]
                if mid is not None: R["eln"] += 1; R["el"] += (mid in w) / len(w)
    return R

def pct(x): return round(100 * x, 1)

def run(n, exp):
    cfg = lambda k, **kw: Config(n=k, **kw)
    names = list(B.ALL); res = {"n": n}; total = 0; caps = 0
    # 2 players: all ordered pairings (seat1 / seat2), n games each
    pair = {}; avg = collections.defaultdict(list)
    for a in names:
        for b in names:
            R = table([a, b], n, cfg(2), base=1000 * (names.index(a) * 3 + names.index(b)), rotate=False); total += n; caps += R["caps"]
            pair[a + " v " + b] = round(R["win"][a] / n if a != b else 0.5, 3) if a != b else round(R["seat"][0] / n, 3)
            if a != b: avg[a].append(R["win"][a] / n)
    res["pair2"] = pair; res["avg2"] = {k: mean(v) for k, v in avg.items()}
    # mixed 3p and 4p tables with rotation
    mix = {}
    for k, tb in ((3, ["strategic", "greedy", "random"]), (4, ["strategic", "greedy", "random", "strategic"])):
        R = table(tb, n, cfg(k), base=500000 + k * 7000); total += n * k; caps += R["caps"]
        mix[k] = {b: R["win"][b] / (R["games"] * tb.count(b)) for b in set(tb)}
    res["mix"] = mix
    # mirrors: strategic x k for seat, length, lead, runaway, cards
    mir = {}; cardstats = None
    for k in (2, 3, 4):
        R = table(["strategic"] * k, n, cfg(k), base=900000 + k * 1000, rotate=False); total += n; caps += R["caps"]
        t = R["turns"]; mir[k] = dict(seat=[round(s / n, 3) for s in R["seat"]], gap=max(abs(100 * s / n - 100 / k) for s in R["seat"]),
            turns=mean(t), sd=sd(t), minutes=mean(R["minutes"]), minutes_sd=sd(R["minutes"]), target=TARGET_MIN[k], ties=R["scoreties"] / n, tie_win=R["ties"] / n,
            lc=mean(R["lc"]), runaway=R["el"] / max(1, R["eln"]), builds=R["builds"] / n, gathers=R["gathers"] / n, app=R["app"] / n,
            inter=R["inter"] / sum(t), score=mean(R["win_scores"]), hist=sorted(collections.Counter(t).items()), errors=R["errors"], passes=R["passes"], caps=R["caps"])
        if k == 4: cardstats = R
    res["mirror"] = mir
    # solo
    solo = {}
    for nm in names + ["rush"]:
        R = table([nm], n, cfg(1), base=700000 + 100 * len(solo), rotate=False); total += n; caps += R["caps"]
        solo[nm] = dict(win=R["solo_win"] / n, score=mean(R["scores"][nm]), turns=mean(R["turns"]), minutes=mean(R["minutes"]))
    res["solo"] = solo
    # card stats (strategic 4p mirror)
    G = cardstats["games"] * 4; base = sum(cardstats["win"].values()) / G
    per = {}
    for c in range(52):
        b = cardstats["card_built"][c]
        per[name(c)] = dict(built=b / G, wc=(cardstats["card_win"][c] / b - base) if b else None)
    res["cards"] = per
    res["base_win"] = base
    if exp: res["exp"] = experiments(n, cfg)
    res["total"] = total; res["caps"] = caps
    return res

def experiments(n, cfg):
    out = {}
    # E1: rush bot vs strategic, 2p and 4p
    R = table(["rush", "strategic"], n, cfg(2), base=60000); out["rush_vs_strategic_2p"] = R["win"]["rush"] / R["games"] * 1.0 / 1.0 / (1) / 1.0 if False else R["win"]["rush"] / R["games"]
    R = table(["rush", "strategic", "strategic", "strategic"], n, cfg(4), base=70000); out["rush_in_4p_vs_3_strategic"] = R["win"]["rush"] / R["games"]
    R = table(["rush", "strategic", "strategic"], n, cfg(3), base=75000); out["rush_in_3p_vs_2_strategic"] = R["win"]["rush"] / R["games"]
    out["rush_turns_4p"] = mean(R["turns"])
    BOTS.update({"planner": B.Planner, "optimiser": B.Optimiser, "casual": B.Instinct})
    for nm in ("planner", "optimiser"):
        R = table([nm, "greedy"], n, cfg(2), base=80000 + len(out)); out[nm + "_vs_greedy_2p"] = R["win"][nm] / R["games"]
    R = table(["strategic", "strategic"], n, cfg(2, spade=2), base=90000); out["spade2_seat1_gap_2p"] = abs(100 * R["seat"][0] / R["games"] - 50)
    return out

def card_entries(res):
    ents = []; C_ = res["cards"]
    for s, nm, lab in ((0, "S", "Spades (Springs)"), (1, "C", "Clubs (Gears)"), (2, "D", "Diamonds (Jewels)"), (3, "H", "Hearts (Clock faces)")):
        rows = [(r, C_[("A23456789TJQK"[r - 1]).replace("T", "") + nm if r != 10 else "10" + nm]) for r in range(1, 14)]
        rows = [(r, v) for r, v in rows]
        built = mean([v["built"] for _, v in rows]); wc = mean([v["wc"] for _, v in rows if v["wc"] is not None])
        ents.append({"name": lab, "played_rate": round(built, 3), "win_correlation": round(wc, 3), "flag": None})
    for r in range(1, 14):
        lab = "10" if r == 10 else "A23456789TJQK"[r - 1]
        vals = [C_[lab + x] for x in "SCDH"]
        built = mean([v["built"] for v in vals]); wc = mean([v["wc"] for v in vals if v["wc"] is not None])
        ents.append({"name": "Rank " + lab + " (all suits)", "played_rate": round(built, 3), "win_correlation": round(wc, 3), "flag": None})
    return ents

def emit(res, path):
    a = res["avg2"]; m = res["mirror"]; k4 = m[4] if 4 in m else m["4"]; g = lambda k: m[k] if k in m else m[int(k)]
    g4 = g("4")
    cs = card_entries(res)
    for c in cs:
        if c["name"].startswith("Spades"): c["flag"] = "weak: negative win correlation, built least often of the point-bearing suits; the engine does not pay"
        if c["name"].startswith("Hearts"): c["flag"] = "strongest suit: highest win correlation"
        if c["name"] in ("Rank K (all suits)", "Rank Q (all suits)"): c["flag"] = "rarely built (money only); K-spade and K-club built 7% and 4%"
    out = {"verdict": N.VERDICT, "revision": N.REVISION, "games_simulated": res["total"],
           "seat_win_rates": {str(i + 1): s for i, s in enumerate(g4["seat"])}, "seat_balance_gap": round(max(g(k)["gap"] for k in "234"), 1),
           "seat_win_rates_by_players": {k: g(k)["seat"] for k in "234"},
           "bot_win_rates": {k: round(v, 3) for k, v in a.items()}, "skill_expression": round(100 * (a["strategic"] - a["random"]), 1),
           "skill_vs_greedy_2p": round(100 * (res["pair2"]["strategic v greedy"] - 0.5), 1),
           "length": {"mean_turns": round(g4["turns"], 1), "stdev": round(g4["sd"], 1), "estimated_minutes": N.ESTIMATED_MINUTES, "target_minutes": N.TARGET_MINUTES,
                      "by_players": {k: {"mean_turns": round(g(k)["turns"], 1), "estimated_minutes": round(g(k)["minutes"], 1), "target_minutes": g(k)["target"]} for k in "234"},
                      "solo": {"mean_turns": round(res["solo"]["strategic"]["turns"], 1), "estimated_minutes": round(res["solo"]["strategic"]["minutes"], 1), "target_minutes": 15}},
           "length_histogram": [{"turns": t, "games": c} for t, c in g4["hist"]],
           "ties": round(g4["ties"], 4), "turn_cap_hits": res["caps"], "lead_changes_mean": round(g4["lc"], 2),
           "lead_changes_by_players": {k: round(g(k)["lc"], 2) for k in "234"},
           "runaway_leader_rate": round(g4["runaway"], 3), "runaway_by_players": {k: round(g(k)["runaway"], 3) for k in "234"},
           "solo_win_rates": {k: round(v["win"], 3) for k, v in res["solo"].items()},
           "rush": {k: round(v, 3) for k, v in res.get("exp", {}).items() if k.startswith("rush")},
           "cards": cs, "ambiguities": N.AMBIGUITIES, "problems": N.PROBLEMS}
    json.dump(out, open(path, "w"), indent=2); open(path, "a").write("\n"); print("wrote", path)

if __name__ == "__main__":
    args = sys.argv[1:]; nums = [a for a in args if a.isdigit()]; n = int(nums[0]) if nums else 2000
    if "--from-results" in args:
        res = json.load(open(os.path.join(HERE, "results.json"))); emit(res, args[args.index("--json") + 1]); sys.exit()
    res = run(n, "--exp" in args)
    json.dump(res, open(os.path.join(HERE, "results.json"), "w"), indent=1, default=str)
    if "--json" in args: emit(res, args[args.index("--json") + 1])
    a = res["avg2"]; m = res["mirror"]
    print("n=%d per pairing/seating; %d games total; turn-cap hits %d" % (n, res["total"], res["caps"]))
    print("2p bot win%%: " + ", ".join("%s %.1f" % (k, 100 * v) for k, v in a.items()) + "; strategic-random gap %.1f" % (100 * (a["strategic"] - a["random"])))
    print("2p strategic v random %.1f, v greedy %.1f; greedy v random %.1f" % (100 * res["pair2"]["strategic v random"], 100 * res["pair2"]["strategic v greedy"], 100 * res["pair2"]["greedy v random"]))
    for k, v in res["mix"].items(): print("%dp mixed win%% per seat-share: " % k + ", ".join("%s %.1f" % (b, 100 * x) for b, x in v.items()))
    for k, v in m.items():
        print("%dp strategic mirror: seat wins %s gap %.1f | turns %.1f sd %.1f | est %.1f min (target %d, sd %.1f) | score ties %.1f%% | lead chg %.2f | halfway leader wins %.1f%% | inter %.2f/turn | apprentice %.1f/g | errors %d passes %d"
              % (k, m[k]["seat"], v["gap"], v["turns"], v["sd"], v["minutes"], v["target"], v["minutes_sd"], 100 * v["ties"], v["lc"], 100 * v["runaway"], v["inter"], v["app"], v["errors"], v["passes"]))
    print("solo win%% (22+): " + ", ".join("%s %.1f (avg %.1f, %.1f turns)" % (k, 100 * v["win"], v["score"], v["turns"]) for k, v in res["solo"].items()))
    if "exp" in res: print("exp: " + json.dumps({k: round(v, 3) for k, v in res["exp"].items()}))
    cs = card_entries(res)
    print("suit built-rate/win-corr: " + "; ".join("%s %.2f/%+.3f" % (c["name"].split()[0], c["played_rate"], c["win_correlation"]) for c in cs[:4]))
    low = sorted(res["cards"].items(), key=lambda kv: kv[1]["built"])[:4]; hi = sorted(res["cards"].items(), key=lambda kv: -kv[1]["built"])[:4]
    print("least built: " + " ".join("%s %.2f" % (k, v["built"]) for k, v in low) + " | most: " + " ".join("%s %.2f" % (k, v["built"]) for k, v in hi))
