"""Ablation battery (designer's rules.md section 7). Usage: python3 experiments/ablate.py <bot> <step> [ghosts e.g. 1,2,3] [key=val cfg]
Prints win rate and trick use for the full bot and each ablation; writes experiments/ablate-<bot>-<step>-<ghosts>.json"""
import json, os, sys
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, ".."))
import run as R
from game import NAMES
bot, step = sys.argv[1], int(sys.argv[2])
ghosts = tuple(int(x) for x in sys.argv[3].split(",")) if len(sys.argv) > 3 and sys.argv[3] not in ("-", "") else ()
extra = [a for a in sys.argv[4:] if "=" in a]; kw = R.parse_cfg(extra)
VARS = ["", "glow", "dart", "silk", "scav", "carry", "swap", "hypno", "feint", "drift", "owlfirst", "shove"]
if "only" in os.environ: VARS = os.environ["only"].split(",")
res = {}
with Pool(4) as pool:
    for v in VARS:
        spec = bot + (":off=" + v if v else "")
        a = R.exhaustive(spec, ghosts, kw, pool, step); s = R.summarise(a)
        res[v or "full"] = dict(win=round(s["win_rate"], 4), n=s["runs"], med=s["median_turns"], caps=s["turn_cap_hits"], use=s["trick_use_given_ready"], drift=round(s["drift_run_rate"], 3), swap=round(s["carry_swap_run_rate"], 3), wf=round(s["wins_feint"], 3), wh=round(s["wins_hypno"], 3))
        print("%-9s win %.4f n=%d med %s use %s" % (v or "full", s["win_rate"], s["runs"], s["median_turns"], s["trick_use_given_ready"]), flush=True)
json.dump(res, open(os.path.join(HERE, "ablate-%s-%d-%s.json" % (bot, step, "".join(map(str, ghosts)) or "none")), "w"), indent=1)
