"""Builds ../playtest.json from results/*.json (cycle 1). Run after run.py sections."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run
R = lambda n: json.load(open(os.path.join(HERE, "results", n + ".json")))
h, sk, ab, sw, fb, arms, nt = R("headline"), R("skill"), R("ablate"), R("switches"), R("fallbacks"), R("arms"), R("newtest")
K = ("2", "3", "4"); G = lambda x, k: x[k + "p"]
def gap(name, k):
    r = sk[f"{name}_{k}p"]["summary"]["maker_win_rates"]; return round(100 * (r[0] - sum(r[1:]) / (int(k) - 1)), 1)
def row(x):
    s = x["summary"]
    return {"turns": x["mean_turns"], "minutes": x["minutes"], "seat_gap": s["seat_gap"], "long_night": x["long_night_rate"], "pattern_share": x["pattern_share"],
            "captures": x["captures_per_game"], "lead_changes": s["lead_changes_mean"], "runaway": s["runaway_leader_rate"]}
h2 = h["2p"]["summary"]
exp = {1: 8 / 52 * 4, 2: 12 / 52 * 4, 3: 12 / 52 * 4, 4: 12 / 52 * 4, 5: 8 / 52 * 4}
cards = []
for z, v in enumerate(h["2p"]["winner_orbit_size_mean"], 1):
    f = None
    if z == 1: f = "Comet: in a winning orbit 61% less often than its deck share; Comet-vs-Giant never decides play (comet-blind margin 3.4 / 0.1 / 0.9)"
    if z == 5: f = "Giant: 59% over-represented in winning orbits; captured only 0.1 times per game"
    cards.append({"name": f"Size {z}", "played_rate": None, "win_correlation": round((v - exp[z]) / exp[z], 2), "flag": f})
out = {"verdict": "BROKEN", "revision": 1, "games_simulated": 1000,
  "seat_win_rates": {str(i + 1): r for i, r in enumerate(h2["seat_win_rates"])}, "seat_balance_gap": h2["seat_gap"],
  "seat_gap_by_players": {k: h[k + "p"]["summary"]["seat_gap"] for k in K},
  "bot_win_rates": {"random": 0.01, "greedy": 0.57, "strategic": 0.43},
  "bot_win_rates_note": "2p strategic vs greedy 0.43/0.57; both beat random by 92-98 points. Greedy is the stronger bot under cycle 1 rules.",
  "skill_expression": round((gap("strat_v_greedy", "2") + gap("strat_v_greedy", "3")) / 2, 1),
  "skill_gap_by_pairing": {n: {k: gap(n, k) for k in K} for n in ("strat_v_random", "greedy_v_random", "strat_v_greedy")},
  "length": {"mean_turns": h2["length"]["mean_turns"], "stdev": h2["length"]["stdev"], "estimated_minutes": h["2p"]["minutes"], "target_minutes": 12,
             "mean_turns_by_players": {k: h[k + "p"]["mean_turns"] for k in K}, "estimated_minutes_by_players": {k: h[k + "p"]["minutes"] for k in K},
             "assumption": "0.4 min per player-turn, unmeasured"},
  "length_histogram": h2["length_histogram"], "ties": h2["ties"], "turn_cap_hits": 0,
  "lead_changes_mean": h2["lead_changes_mean"], "runaway_leader_rate": h2["runaway_leader_rate"],
  "by_players": {k: row(h[k + "p"]) for k in K},
  "long_night_rate": {k: h[k + "p"]["long_night_rate"] for k in K},
  "pattern_win_share": {k: h[k + "p"]["pattern_share"] for k in K},
  "pattern_win_share_greedy_mirror": {k: sk[f"greedy_mirror_{k}p"]["pattern_share"] for k in K},
  "armed_positions": {k: {"per_game": h[k + "p"]["armed_per_game"], "attacked": h[k + "p"]["armed_attacked"], "still_armed": h[k + "p"]["armed_survived"]} for k in K},
  "captures_per_game": {k: h[k + "p"]["captures_per_game"] for k in K},
  "ablations": {n: {k: run.margin(ab[f"{n}_{k}p"]) for k in K} for n in ("self-spin-only", "shield-blind", "threat-blind", "defence-check", "no-recall", "comet-blind")},
  "switch_off_effects": {n: {k: row(sw[f"{n}_{k}p"]) for k in K} for n in run.SWITCH_OFF},
  "fallbacks_2p": {n: row(v) for n, v in fb.items()},
  "arms": {n: {k: row(arms[f"{n}_{k}p"]) for k in K} for n in ("deck40", "capture_to_ds")},
  "new_test_opening": {n: {k: row(nt[f"{n}_{k}p"]) for k in K} for n in ("open0", "open1")},
  "cards": cards, "validation": "bots only, unvalidated"}
out["ambiguities"] = json.load(open(os.path.join(HERE, "ambiguities.json")))
out["problems"] = json.load(open(os.path.join(HERE, "problems.json")))
json.dump(out, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=1)
print("wrote playtest.json", out["verdict"], len(out["problems"]), "problems", len(out["ambiguities"]), "ambiguities")
