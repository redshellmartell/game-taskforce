"""Compact summary of sim/results/*.json. Usage: python3 summary.py"""
import json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
L = lambda n: json.load(open(os.path.join(R, n + ".json"))) if os.path.exists(os.path.join(R, n + ".json")) else None
def line(tag, k, x):
    s = x["summary"]
    print(f"{tag} {k}p n={x['n']} seat={s['seat_win_rates']} gap={s['seat_gap']} len={s['length']['mean_turns']}({s['length']['min']}-{s['length']['max']}) LN={x['long_night_rate']} "
          f"pat={x['pattern_wins']} caps/g={x['captures_per_game']} crash%={x['crash_spin_share']} oth%={x['other_spin_share']} formed/g={x['formed_per_game']} surv={x['formed_survival']} "
          f"fullsurv={x['full_survival']} lc={s['lead_changes_mean']} run={s['runaway_leader_rate']} rebound/g={x['rebound_per_game']} >bound={x['turns_exceed_deck_bound']}")
h = L("headline")
for k in "234": line("HEAD", k, h[k])
sk = L("skill")
if sk:
    for pair, d in sk.items():
        if pair.startswith("_"): continue
        for k in "234":
            r = d[k]["maker_rates"]; n = int(k); s0 = r[0]; oth = (1 - s0 - d[k]["summary"]["ties"]) / (n - 1)
            print(f"SKILL {pair} {k}p first-bot win {s0:.3f} each other {oth:.3f} gap {100*(s0-oth):.1f}")
for sec in ("ablate", "variants", "variants_ablate"):
    d = L(sec)
    if not d: continue
    for name, v in d.items():
        if name.startswith("_"): continue
        for k in "234":
            x = v[k]; r = x["maker_rates"]; n = int(k)
            if sec.endswith("ablate") or sec == "ablate":
                full = [r[i] for i in range(0, n, 2)]; ab = [r[i] for i in range(1, n, 2)]
                print(f"{sec} {name} {k}p full {sum(full)/len(full):.3f} ablated {sum(ab)/len(ab):.3f} margin {100*(sum(full)/len(full)-sum(ab)/len(ab)):.1f} pts LN={x['long_night_rate']}")
            else:
                line(name, k, x)
