"""Whiskerdark (rules v2) headline simulation.
Usage: python3 run.py [--quick] [key=value config overrides]  (e.g. base_claws=3)
Exhaustive over all 362,880 layouts for the empty Ghost set and each single-Ghost set (strategic bot), plus
random and greedy bots on the empty set, sessions with Ghost carry-over, and a time model.
Writes results.json, ../playtest.json is written by finish.py."""
import itertools, json, os, random, statistics, sys, time
from collections import Counter
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from game import Config, Run, play, NAMES, TRICKS
import bots as B

BOTS = {"random": B.Random, "greedy": B.Greedy, "strategic": B.Strategic, "lookahead": B.Lookahead}
def make_bot(spec):
    """'strategic' or 'strategic:off=glow+silk' (ablations) or 'lookahead:off=silk' -> factory(seed)."""
    name, _, opt = spec.partition(":"); off = opt[4:].split("+") if opt.startswith("off=") else []
    cls = BOTS[name]
    if not off: return cls
    return lambda seed: cls(seed, off=off)
N = 362880

def parse_cfg(args):
    kw = {}
    for a in args:
        if "=" in a and not a.startswith("--"):
            k, v = a.split("="); kw[k] = v if k == "hunt" else (v == "True" if v in ("True", "False") else int(v))
    return kw

def work(job):
    bot, ghosts, start, stop, kw, step = job
    cfg = Config(**kw); Bot = make_bot(bot)
    agg = dict(n=0, wins=0, caps=0, turns=Counter(), killers=Counter(), first=Counter(), win_feint=0, win_hypno=0,
               win_neither=0, beaten=Counter(), shoved=Counter(), thief_runs=0, used=Counter(), ever=Counter(),
               wise=0, wise_ready_runs=0, wise_changed_runs=0, owl_ever=0, trick_total=0, hunt=0, tricks_per_run=0,
               first_shove_wins=0, thief_hit=0, ready_end=0, silk=0, carry_swap=0, drift=0, drift_runs=0, swap_runs=0, deaths_turn=0)
    for idx, pm in enumerate(itertools.islice(itertools.permutations(range(1, 10)), start, stop, step), start):
        r = play(pm, ghosts, Bot(idx), cfg)
        s = r.stats; a = agg
        a["n"] += 1; a["wins"] += r.won; a["caps"] += r.capped; a["turns"][r.turns] += 1
        if not r.won and r.killer: a["killers"][r.killer] += 1
        a["first"][s["first"]] += 1
        if r.won:
            a["win_feint"] += s["feint_win"]; a["win_hypno"] += s["hypno_win"]; a["win_neither"] += not (s["feint_win"] or s["hypno_win"])
        for c in set(s["beaten"]): a["beaten"][c] += 1
        for c in set(s["shoved"]): a["shoved"][c] += 1
        a["thief_runs"] += s["thief"] > 0
        for c in set(s["tricks"]): a["used"][c] += 1
        for c in s["ever_ready"]: a["ever"][c] += 1
        if 6 in s["ever_ready"]:
            a["owl_ever"] += 1; a["wise_changed_runs"] += s["wise"] > 0
        a["trick_total"] += len(s["tricks"]); a["hunt"] += s["hunt"] > 0
        a["drift_runs"] += s["drift"] > 0; a["swap_runs"] += s["carry_swap"] > 0
    return agg

def merge(parts):
    out = None
    for p in parts:
        if out is None: out = p; continue
        for k, v in p.items():
            out[k] = out[k] + v if not isinstance(v, Counter) else out[k] + v
    return out

def exhaustive(bot, ghosts, kw, pool, step=1):
    chunks = 16; size = -(-N // chunks)
    jobs = [(bot, ghosts, i * size, min(N, (i + 1) * size), kw, step) for i in range(chunks)]
    return merge(pool.map(work, jobs))

def summarise(a):
    n = a["n"]; w = a["wins"]
    turns = sorted(a["turns"].elements()); med = statistics.median(turns)
    tt = sum(t * c for t, c in a["turns"].items()) / n
    mins = 0.5 + (tt * 50 + a["trick_total"] / n * 15) / 60 + 0.25
    deaths = n - w
    nm = lambda d: {NAMES[c]: round(v, 4) for c, v in sorted(d.items())}
    return dict(runs=n, win_rate=w / n, turn_cap_hits=a["caps"], mean_turns=tt, median_turns=med,
                stdev_turns=statistics.pstdev(turns), est_minutes=mins, drift_run_rate=a['drift_runs'] / n, carry_swap_run_rate=a['swap_runs'] / n,
                length_hist=sorted(a["turns"].items()),
                killers=nm({c: v / deaths for c, v in a["killers"].items()}) if deaths else {},
                first_shove=a["first"]["shove"] / n,
                wins_feint=a["win_feint"] / w if w else 0, wins_hypno=a["win_hypno"] / w if w else 0, wins_neither=a["win_neither"] / w if w else 0,
                beaten=nm({c: v / n for c, v in a["beaten"].items()}), shoved=nm({c: v / n for c, v in a["shoved"].items()}),
                thief_run_rate=a["thief_runs"] / n, hunt_run_rate=a["hunt"] / n,
                trick_use_given_ready={NAMES[c]: round(a["used"][c] / a["ever"][c], 4) for c in TRICKS if a["ever"][c]},
                wise_change_rate=(a["wise_changed_runs"] / a["owl_ever"]) if a["owl_ever"] else 0,
                owl_ready_rate=a["owl_ever"] / n)

def session(rng, Bot, kw, seed):
    cfg = Config(**kw); ticks = []; esc = 0; runs = []
    while esc < cfg.escapes and len(ticks) < 9:
        pm = list(range(1, 10)); rng.shuffle(pm)
        r = play(pm, ticks, Bot(rng.random()), cfg)
        runs.append((len(ticks), r.won))
        if r.won: esc += 1
        else:
            k = r.killer if r.killer not in ticks else min(c for c in range(1, 10) if c not in ticks)
            ticks.append(k)
    return (9 - len(ticks) if esc >= cfg.escapes else 0), runs

def sessions(kw, n=20000, bot="strategic"):
    rng = random.Random(4242); scores = Counter(); nruns = []; by_g = {}
    for i in range(n):
        sc, runs = session(rng, BOTS[bot], kw, i)
        scores[sc] += 1; nruns.append(len(runs))
        for g, won in runs:
            t = by_g.setdefault(g, [0, 0]); t[0] += 1; t[1] += won
    return dict(score_dist={k: v / n for k, v in sorted(scores.items())}, mean_runs=sum(nruns) / n,
                max_score_share=max(scores.values()) / n, session_win=1 - scores[0] / n,
                win_by_ghosts={g: round(w / c, 3) for g, (c, w) in sorted(by_g.items())})

def main(argv):
    kw = parse_cfg(argv); quick = "--quick" in argv; step = 8 if quick else 1
    t0 = time.time(); res = {"config": kw, "step": step}
    with Pool(4) as pool:
        for bot in ("strategic", "random", "greedy") if "--lean" not in argv else ("strategic",):
            res[bot] = summarise(exhaustive(bot, (), kw, pool, step)); print(bot, "win %.3f" % res[bot]["win_rate"], "%.0fs" % (time.time() - t0), flush=True)
        la_step = int(next((a[5:] for a in argv if a.startswith('--la=')), 400 if quick else 100))          # lookahead bot is slow (0.35 s/run): every 100th layout = 3,629 layouts
        res["lookahead"] = summarise(exhaustive("lookahead", (), kw, pool, la_step)); res["lookahead"]["layout_step"] = la_step
        print("lookahead win %.3f (every %dth layout)" % (res["lookahead"]["win_rate"], la_step), "%.0fs" % (time.time() - t0), flush=True)
        if "--noghost" not in argv:
            res["ghost"] = {}
            for g in range(1, 10):
                res["ghost"][NAMES[g]] = summarise(exhaustive("strategic", (g,), kw, pool, step))["win_rate"]
            print("ghosts", {k: round(v, 3) for k, v in res["ghost"].items()}, "%.0fs" % (time.time() - t0), flush=True)
    if "--noghost" not in argv:
        res["sessions"] = sessions(kw, 3000 if quick else 20000)
        res["sessions_lookahead"] = sessions(kw, 100 if quick else 150, "lookahead")
    res["seconds"] = time.time() - t0
    out = os.path.join(HERE, "results.json" if not kw and not quick else "experiments/res-%s.json" % ("_".join(a for a in argv if not a.startswith("--")).replace("=", "") or "quick"))
    json.dump(res, open(out, "w"), indent=1, default=str)
    s = res["strategic"]
    res.setdefault("random", {"win_rate": 0}); res.setdefault("greedy", {"win_rate": 0})
    print("strategic win %.3f random %.3f greedy %.3f | median turns %s mean %.2f | min %.1f | first shove %.2f" % (
        s["win_rate"], res["random"]["win_rate"], res["greedy"]["win_rate"], s["median_turns"], s["mean_turns"], s["est_minutes"], s["first_shove"]))
    print("killers", s["killers"]); print("wins feint/hypno/neither %.2f %.2f %.2f" % (s["wins_feint"], s["wins_hypno"], s["wins_neither"]))

if __name__ == "__main__":
    main(sys.argv[1:])
