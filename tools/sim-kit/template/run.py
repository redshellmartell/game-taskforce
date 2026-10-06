"""TEMPLATE run script. Usage: python3 run.py [N=2000] [--json ../playtest.json]
Copy tools/sim-kit/template/ to games/<slug>/sim/, replace game.py and bots.py, set the targets below, and run."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools", "sim-kit"))   # games/<slug>/sim -> repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))                                   # when run from tools/sim-kit/template
import simkit
from game import play
import bots as B

TARGET_MINUTES = 10; MINUTES_PER_TURN = 0.3      # measured from narrated play; say so in the report


def main(n=2000, json_path=None):
    table = simkit.round_robin(play, B.MAKERS, n)
    mirror = simkit.run_match(play, [B.MAKERS["strategic"]] * 2, n, seed=9000)
    summ = simkit.summarize(mirror, 2)
    gap = round(100 * (table["avg"]["strategic"] - table["avg"]["random"]), 1)
    est = round(summ["length"]["mean_turns"] * MINUTES_PER_TURN, 1)
    abl = {k: simkit.ablation(play, B.MAKERS["strategic"], m, n) for k, m in B.ABLATED.items()}
    print(f"{summ['games']} mirror games; bot averages {table['avg']}; spread {table['spread_pts']} pts")
    for name, value, target, ok in simkit.evaluate(summ, gap, TARGET_MINUTES, est):
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {value} (target {target})")
    for k, a in abl.items(): print(f"  {'PASS' if a['passes'] else 'FAIL'}  ablation {k}: loses by {a['margin_pts']} pts (needs 5)")
    if json_path:
        out = simkit.to_playtest_json(summ, table["avg"], gap, TARGET_MINUTES, est, "NEEDS-FIXES", 0)
        out["ablations"] = abl
        with open(json_path, "w") as f: json.dump(out, f, indent=2)
        print("wrote", json_path)


if __name__ == "__main__":
    a = sys.argv[1:]; nums = [x for x in a if x.isdigit()]
    main(int(nums[0]) if nums else 2000, a[a.index("--json") + 1] if "--json" in a else None)
