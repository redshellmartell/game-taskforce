import json,sys
r=json.load(open("results/sweep.json"))
for n in (sys.argv[1:] or r):
    for k in ("2p","3p","4p"):
        x=r[n][k]; s=x["share"]
        print(f'{n:14s}{k} t={x["turns"]:5.1f}({x["minutes"]}m) sd={x["stdev"]} cap={x["caps"]} LN={x["ln"]:.3f} M/C/A={s["mass"]:.2f}/{s["const"]:.2f}/{s["align"]:.2f} gap={x["gap"]} run={x["runaway"]} lc={x["lead"]} svg={x["sv_greedy_pts"]} gt={x["g_turns"]} ggap={x["g_gap"]} rec={x["recall"]}')
