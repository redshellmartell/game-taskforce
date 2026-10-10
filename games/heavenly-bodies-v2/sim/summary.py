"""Compact summary of sim/results/<section>.json. Usage: python3 summary.py <section> [key-substring]"""
import json, os, sys
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
d = json.load(open(os.path.join(R, sys.argv[1] + ".json"))); sub = sys.argv[2] if len(sys.argv) > 2 else ""
for k, x in d.items():
    if sub not in k: continue
    s = x["summary"]; r = s["maker_win_rates"]
    print(f"{k:28s} gap={s['seat_gap']:5.1f} turns={x['mean_turns']:5.1f}({s['length']['min']}-{s['length']['max']}) min={x['minutes']:4.1f} LN={x['long_night_rate']:.3f} "
          f"pat={x['pattern_share']['mass']:.2f}/{x['pattern_share']['const']:.2f}/{x['pattern_share']['align']:.2f} cap={x['captures_per_game']:5.2f} lc={s['lead_changes_mean']} run={s['runaway_leader_rate']} "
          f"mk0={r[0]:.3f} arm={x['armed_per_game']}/{x['armed_attacked']}/{x['armed_survived']}")
