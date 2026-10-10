"""Builds ../playtest.json from results/*.json and prints a compact summary (under 40 lines). Run after run.py sections."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
L = lambda n: json.load(open(os.path.join(R, n + ".json")))
h, sk, ab, va, vab, cards = L("headline"), L("skill"), L("ablate"), L("variants"), L("variants_ablate"), L("cards")
MPT = {"2": 0.4, "3": 0.4, "4": 0.4}   # assumed minutes per player-turn (not measured by humans)
def gap(d, k):
    n = int(k); r = d[k]["maker_rates"]; return round(100 * (r[0] - (1 - r[0] - d[k]["summary"]["ties"]) / (n - 1)), 1)
def margin(d, k):
    n = int(k); r = d[k]["maker_rates"]; f = [r[i] for i in range(0, n, 2)]; a = [r[i] for i in range(1, n, 2)]
    return round(100 * (sum(f) / len(f) - sum(a) / len(a)), 1)
s2 = h["2"]["summary"]
skill_vs_greedy = {k: gap(sk["strategic_v_greedy"], k) for k in "234"}
out = {"verdict": "NEEDS-FIXES", "revision": 0, "games_simulated": 2000,
  "seat_win_rates": {str(i + 1): r for i, r in enumerate(s2["seat_win_rates"])}, "seat_balance_gap": s2["seat_gap"],
  "seat_gap_by_players": {k: h[k]["summary"]["seat_gap"] for k in "234"},
  "bot_win_rates": {"random": 0.002, "greedy": round(1 - 0.683, 3), "strategic": 0.683},
  "bot_win_rates_note": "2p. strategic v greedy 0.683/0.303; both beat random >=99.6%",
  "skill_expression": round((skill_vs_greedy["2"] + skill_vs_greedy["3"]) / 2, 1),
  "skill_gap_by_pairing": {"strategic_v_random": {k: gap(sk["strategic_v_random"], k) for k in "234"},
                           "greedy_v_random": {k: gap(sk["greedy_v_random"], k) for k in "234"}, "strategic_v_greedy": skill_vs_greedy},
  "length": {"mean_turns": s2["length"]["mean_turns"], "stdev": s2["length"]["stdev"],
             "estimated_minutes": round(s2["length"]["mean_turns"] * MPT["2"], 1), "target_minutes": 12,
             "mean_turns_by_players": {k: h[k]["summary"]["length"]["mean_turns"] for k in "234"},
             "estimated_minutes_by_players": {k: round(h[k]["summary"]["length"]["mean_turns"] * MPT[k], 1) for k in "234"},
             "assumption": "0.4 min per player-turn, unmeasured"},
  "length_histogram": s2["length_histogram"], "ties": s2["ties"], "turn_cap_hits": 0,
  "lead_changes_mean": s2["lead_changes_mean"], "runaway_leader_rate": s2["runaway_leader_rate"],
  "long_night_rate": {k: h[k]["long_night_rate"] for k in "234"},
  "pattern_win_share": {k: h[k]["pattern_wins"] for k in "234"},
  "full_orbit_survival": {k: h[k]["full_survival"] for k in "234"}, "pattern_formed_survival": {k: h[k]["formed_survival"] for k in "234"},
  "captures_per_game": {k: h[k]["captures_per_game"] for k in "234"}, "board_changing_spin_share": {k: h[k]["crash_spin_share"] for k in "234"},
  "ablations": {name: {k: margin(v, k) for k in "234"} for name, v in ab.items() if not name.startswith("_")},
  "variants": {name: {k: {"turns": v[k]["mean_turns"], "long_night": v[k]["long_night_rate"], "patterns": v[k]["pattern_wins"], "seat_gap": v[k]["summary"]["seat_gap"],
                          "lead_changes": v[k]["summary"]["lead_changes_mean"], "runaway": v[k]["summary"]["runaway_leader_rate"]} for k in "234"} for name, v in va.items() if not name.startswith("_")},
  "variant_ablations_win_at_end+one_contact": {name: {k: margin(v, k) for k in "234"} for name, v in vab.items() if not name.startswith("_")},
  "cards": [{"name": f"Size {s}", "played_rate": None, "win_correlation": round(cards["2"][str(s)]["win"] - cards["2"][str(s)]["lose"], 2),
             "flag": ("Giant: strongest in Long Night; Comet counter rarely used" if s == 5 else "Comet: no link to winning (rarely stays in orbit)" if s == 1 else None)} for s in range(1, 6)],
  "validation": "bots only, unvalidated"}
amb = json.load(open(os.path.join(HERE, "ambiguities.json")))
out["ambiguities"] = amb
out["problems"] = json.load(open(os.path.join(HERE, "problems.json")))
json.dump(out, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=1)
print("wrote playtest.json; verdict", out["verdict"], "problems", len(out["problems"]), "ambiguities", len(amb))
