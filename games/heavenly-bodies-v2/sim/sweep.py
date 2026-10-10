"""Cycle 2 sweep. python3 sweep.py <cellname...> ; results/sweep.json. Each cell: strategic mirror + greedy mirror + strategic-vs-greedy at 2,3,4p."""
import sys, json, os, time
import run as R
CELLS = {
 "c1_full_o0": dict(opening=0),
 "c2_none_o0": dict(opening=0, shield=False),
 "c3_big_o0": dict(opening=0, shield_mode="big"),
 "c4_spin_o0": dict(opening=0, shield_mode="spin"),
}
def add(name, base, **kw): CELLS[name] = dict(base, **kw)
if os.path.exists("results/sweep_cells.json"): CELLS.update(json.load(open("results/sweep_cells.json")))
def run(name, N=1000):
    path = "results/sweep.json"; res = json.load(open(path)) if os.path.exists(path) else {}
    if name in res: return
    kw = CELLS[name]; out = {"cfg": kw}
    for k in (2, 3, 4):
        m = R.cell(["strategic"] * k, N, kw, 10 * k)
        g = R.cell(["greedy"] * k, N, kw, 500 + k)
        v = R.cell(["strategic"] + ["greedy"] * (k - 1), N, kw, 300 + k)
        sw = v["summary"]["maker_win_rates"][0]
        out[f"{k}p"] = dict(turns=m["mean_turns"], minutes=m["minutes"], caps=m["captures_per_game"], ln=m["long_night_rate"],
            share=m["pattern_share"], gap=m["summary"]["seat_gap"],
            runaway=m["summary"]["runaway_leader_rate"], lead=m["summary"]["lead_changes_mean"],
            stdev=m["summary"]["length"].get("stdev"), g_turns=g["mean_turns"], g_caps=g["captures_per_game"], g_gap=g["summary"]["seat_gap"],
            sv_greedy_pts=round(100 * (sw - 1 / k), 1), recall=m["recall_per_game"], mn=m["summary"]["length"].get("min") )
    res = json.load(open(path)) if os.path.exists(path) else {}
    res[name] = out; json.dump(res, open(path, "w"), indent=1)
    print(name, {k: (v["turns"], v["caps"], v["gap"]) for k, v in out.items() if k != "cfg"}, flush=True)
if __name__ == "__main__":
    for n in sys.argv[1:]: t=time.time(); run(n); print(n, round(time.time()-t), "s")
