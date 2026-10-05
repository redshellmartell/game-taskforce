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
        app=0, retools=0, solos=[], deckend=0, passes=0, errors=0, inter=0, leader_turns=[], rush_first=0, clock_by_deck=0, win_scores=[], solo_win=0)
    rots = range(k) if rotate else [0]
    for rot in rots:
        order = [names[(i + rot) % k] for i in range(k)]
        for g in range(n):
            seed = base + rot * 100000 + g
            r = play(cfg, [BOTS[o](seed * 10 + i) for i, o in enumerate(order)], seed); st = r["st"]
            w = r["winners"]; R["games"] += 1; R["turns"].append(r["turns"]); R["caps"] += r["capped"]; R["ties"] += r["tie"]; R["scoreties"] += r["scoretie"]
            R["errors"] += st.errors; R["passes"] += st.passes; R["retools"] += st.retools; R["deckend"] += st.struck_deck
            for i in range(k):
                R["scores"][order[i]].append(r["scores"][i])
            for i in w:
                R["win"][order[i]] += 1.0 / len(w); R["seat"][i] += 1.0 / len(w)
                R["win_scores"].append(r["scores"][i])
                for c in st.builds[i]: R["card_win"][c] += 1.0 / len(w)
            if cfg.n == 1: R["solo_win"] += r["scores"][0] >= cfg.solo_win; R["solos"].append(r["scores"][0])
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

def run(n, ckw):
    cfg = lambda k, **kw: Config(n=k, **{**ckw, **kw})
    names = list(B.ALL) + ["lookahead"]; res = {"n": n}; total = 0; caps = 0
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
    for k, tb in ((3, ["strategic", "greedy", "random"]), (4, ["strategic", "greedy", "random", "lookahead"])):
        R = table(tb, n, cfg(k), base=500000 + k * 7000); total += n * k; caps += R["caps"]
        mix[k] = {b: R["win"][b] / (R["games"] * tb.count(b)) for b in set(tb)}
    res["mix"] = mix
    # mirrors: strategic x k for seat, length, lead, runaway, cards
    mir = {}; cardstats = None
    for k in (2, 3, 4):
        R = table(["strategic"] * k, n, cfg(k), base=900000 + k * 1000, rotate=False); total += n; caps += R["caps"]
        t = R["turns"]; mir[k] = dict(seat=[round(s / n, 3) for s in R["seat"]], gap=max(abs(100 * s / n - 100 / k) for s in R["seat"]),
            turns=mean(t), sd=sd(t), minutes=mean(R["minutes"]), minutes_sd=sd(R["minutes"]), target=TARGET_MIN[k], ties=R["scoreties"] / n, tie_win=R["ties"] / n,
            lc=mean(R["lc"]), runaway=R["el"] / max(1, R["eln"]), builds=R["builds"] / n, gathers=R["gathers"] / n, retools=R["retools"] / n, deckend=R["deckend"] / n,
            inter=R["inter"] / sum(t), score=mean(R["win_scores"]), hist=sorted(collections.Counter(t).items()), errors=R["errors"], passes=R["passes"], caps=R["caps"])
        if k == 4: cardstats = R
    res["mirror"] = mir
    # solo
    solo = {}
    for nm in names + ["rush"]:
        R = table([nm], n, cfg(1), base=700000 + 100 * len(solo), rotate=False); total += n; caps += R["caps"]
        solo[nm] = dict(win=R["solo_win"] / n, wins_by_line={str(w): sum(1 for x in R["solos"] if x >= w) / n for w in range(27, 36)}, p10=sorted(R["solos"])[n // 10], p90=sorted(R["solos"])[9 * n // 10], score=mean(R["scores"][nm]), turns=mean(R["turns"]), minutes=mean(R["minutes"]))
    res["solo"] = solo
    # card stats (strategic 4p mirror)
    G = cardstats["games"] * 4; base = sum(cardstats["win"].values()) / G
    per = {}
    for c in range(52):
        b = cardstats["card_built"][c]
        per[name(c)] = dict(built=b / G, wc=(cardstats["card_win"][c] / b - base) if b else None)
    res["cards"] = per
    res["base_win"] = base
    res["total"] = total; res["caps"] = caps
    return res

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
    a = res["avg2"]; m = res["mirror"]; g = lambda k: m[k] if k in m else m[int(k)]
    g4 = g("4"); cs = card_entries(res)
    for c in cs:
        if c["name"].startswith("Spades"): c["flag"] = "negative win correlation (-0.035) although the discount is now 4 and Retool exists; Spades are mostly spent as payment"
        if c["name"].startswith("Hearts"): c["flag"] = "strongest suit: highest win correlation (+0.098)"
        if c["name"] in ("Rank K (all suits)", "Rank Q (all suits)"): c["flag"] = "rarely built (money only): K 10%, Q 14% of workshops; negative win correlation"
    ex = {}
    for t in ("noretool", "spade2", "spade2gear"):
        e = json.load(open(os.path.join(HERE, "exp-%s.json" % t)))
        ex[t] = {"cfg": e["cfg"], "strat_v_greedy_2p": round(e["pair2"]["strategic v greedy"], 3), "strat_v_random_2p": round(e["pair2"]["strategic v random"], 3),
                 "lead_changes_4p": round(e["mirror"]["4"]["lc"], 2), "seat_gap_max": round(max(e["mirror"][k]["gap"] for k in "234"), 1),
                 "solo_strategic_win": round(e["solo"]["strategic"]["win"], 3), "solo_random_win": round(e["solo"]["random"]["win"], 3)}
    out = {"verdict": N.VERDICT, "revision": N.REVISION, "games_simulated": res["total"],
           "seat_win_rates": {str(i + 1): s for i, s in enumerate(g4["seat"])}, "seat_balance_gap": round(max(g(k)["gap"] for k in "234"), 1),
           "seat_win_rates_by_players": {k: g(k)["seat"] for k in "234"},
           "bot_win_rates": {k: round(v, 3) for k, v in a.items()}, "skill_expression": round(100 * (a["strategic"] - a["random"]), 1),
           "skill_vs_greedy_2p": round(100 * res["pair2"]["strategic v greedy"], 1), "lookahead_v_strategic_2p": round(100 * res["pair2"]["lookahead v strategic"], 1),
           "length": {"mean_turns": round(g4["turns"], 1), "stdev": round(g4["sd"], 1), "estimated_minutes": round(g4["minutes"], 1), "target_minutes": 20,
                      "by_players": {k: {"mean_turns": round(g(k)["turns"], 1), "estimated_minutes": round(g(k)["minutes"], 1), "target_minutes": g(k)["target"]} for k in "234"},
                      "solo": {"mean_turns": round(res["solo"]["strategic"]["turns"], 1), "estimated_minutes": round(res["solo"]["strategic"]["minutes"], 1), "target_minutes": 10}},
           "length_histogram": [{"turns": t, "games": c} for t, c in g4["hist"]],
           "ties": round(g4["ties"], 4), "turn_cap_hits": res["caps"], "lead_changes_mean": round(g4["lc"], 2),
           "lead_changes_by_players": {k: round(g(k)["lc"], 2) for k in "234"},
           "runaway_leader_rate": round(g4["runaway"], 3), "runaway_by_players": {k: round(g(k)["runaway"], 3) for k in "234"},
           "solo_win_rates": {k: round(v["win"], 3) for k, v in res["solo"].items()},
           "solo_strategic_win_by_line": res["solo"]["strategic"]["wins_by_line"],
           "deck_empty_end_rate": {k: round(g(k)["deckend"], 3) for k in "234"}, "retools_per_game": {k: round(g(k)["retools"], 2) for k in "234"},
           "experiments": ex,
           "cards": cs, "ambiguities": N.AMBIGUITIES, "problems": N.PROBLEMS}
    json.dump(out, open(path, "w"), indent=2); open(path, "a").write("\n"); print("wrote", path)

def summary(res, tag):
    a = res["avg2"]; m = res["mirror"]; p = res["pair2"]
    L = ["[%s] n per pairing/seating; %d games; turn-cap hits %d" % (tag, res["total"], res["caps"])]
    L.append("2p avg win%: " + ", ".join("%s %.1f" % (k, 100 * v) for k, v in a.items()) + "; strat-random gap %.1f" % (100 * (a["strategic"] - a["random"])))
    L.append("2p strat v random %.1f, v greedy %.1f, v lookahead %.1f; lookahead v greedy %.1f, v random %.1f" % tuple(100 * p[x] for x in ("strategic v random", "strategic v greedy", "strategic v lookahead", "lookahead v greedy", "lookahead v random")))
    for k, v in res["mix"].items(): L.append("%sp mixed win%%: " % k + ", ".join("%s %.1f" % (b, 100 * x) for b, x in v.items()))
    for k, v in m.items():
        L.append("%sp mirror: seats %s gap %.1f | turns %.1f sd %.1f | %.1f min (target %d) | lead chg %.2f | runaway %.1f%% | ties %.1f%% | retools %.1f/g deck-end %.0f%% | inter %.2f | err %d pass %d cap %d"
              % (k, v["seat"], v["gap"], v["turns"], v["sd"], v["minutes"], v["target"], v["lc"], 100 * v["runaway"], 100 * v["ties"], v["retools"], 100 * v["deckend"], v["inter"], v["errors"], v["passes"], v["caps"]))
    L.append("solo win% (31): " + ", ".join("%s %.1f (avg %.1f, %.1f turns, %.1f min)" % (k, 100 * v["win"], v["score"], v["turns"], v["minutes"]) for k, v in res["solo"].items()))
    st = res["solo"]["strategic"]["wins_by_line"]; rn = res["solo"]["random"]["wins_by_line"]
    L.append("solo strat win by line: " + " ".join("%s:%.0f" % (w, 100 * x) for w, x in st.items()) + " | random: " + " ".join("%s:%.0f" % (w, 100 * x) for w, x in rn.items()))
    cs = card_entries(res)
    L.append("suit built-rate/win-corr: " + "; ".join("%s %.2f/%+.3f" % (c["name"].split()[0], c["played_rate"], c["win_correlation"]) for c in cs[:4]))
    return "\n".join(L)

if __name__ == "__main__":
    args = sys.argv[1:]; nums = [a for a in args if a.isdigit()]; n = int(nums[0]) if nums else 2000
    tag = args[args.index("--tag") + 1] if "--tag" in args else "base"
    ckw = {}
    for a in args:
        if a.startswith("--cfg="):
            for kv in a[6:].split(","):
                k, v = kv.split("="); ckw[k] = (v == "True") if v in ("True", "False") else int(v)
    if "--from-results" in args:
        res = json.load(open(os.path.join(HERE, "results.json"))); emit(res, args[args.index("--json") + 1]); sys.exit()
    res = run(n, ckw); res["cfg"] = ckw
    fn = "results.json" if tag == "base" else "exp-%s.json" % tag
    json.dump(res, open(os.path.join(HERE, fn), "w"), indent=1, default=str)
    txt = summary(res, tag + " " + json.dumps(ckw)); print(txt); open(os.path.join(HERE, fn.replace(".json", ".txt")), "w").write(txt + "\n")
    if "--json" in args: emit(res, args[args.index("--json") + 1])
