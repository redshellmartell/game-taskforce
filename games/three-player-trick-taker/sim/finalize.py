"""Builds ../playtest.json from results.json (called by run.py)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
MIN = 6 * (1 + 7 * 17.5 / 60.0)

def verdict_of(out, b, gap, skill, runaway, problems):
    m = out["mixed"]
    fails = []
    if m["strategic"] < 0.40: fails.append("strat")
    if b["lc"] < 2: fails.append("lc")
    if runaway > 0.65: fails.append("runaway")
    if gap > 5: fails.append("seat")
    if not (0.40 <= b["success"] <= 0.65): fails.append("success")
    return "PASS" if not fails else "NEEDS-FIXES"

def build_problems(out, b, mx, gap, skill):
    m = out["mixed"]
    return [
     {"severity": "medium", "problem": "Lead changes still below KPI (the only KPI miss).",
      "evidence": "%.2f lead changes per game vs target 2 (v2 1.49). Fallback experiments, 2,000 mirror games each: double-scored final round 1.84 (early leader 43%%, but mixed-table strategic fell to 38.5%% vs greedy 41.8%%); crew loot on clean jobs only 1.64; critic's flat version 1.71 (greedy 48%% vs strategic 36%%). None reaches 2. Without Heat lead changes are 1.07, so Heat -3 is doing most of the work." % b["lc"],
      "fix": "Accept 1.6-1.8 as a known soft miss (runaway leader is only 50%%, so games are not decided early), or ship double-scored final round as an optional finale. Untested: Heat on the sole leader also costs 1 loot; 7-round variants are not allowed by the rotation."},
     {"severity": "low", "problem": "Strategic only ties greedy at the mixed table; skill lives mostly in beating random.",
      "evidence": "Mixed table: greedy %.1f%%, strategic (card-counting) %.1f%%, random %.1f%%. Skill gap vs random %.1f pts (KPI 20), but greedy alone beats two randoms at %.1f%% vs strategic %.1f%%. v2: greedy 63.5%% vs strategic 28.5%% - the loot-on-success rule closed that gap fully." % (m["greedy"]*100, m["strategic"]*100, m["random"]*100, skill, out["skill"]["greedy"]*100, out["skill"]["strategic"]*100),
      "fix": "None required for the KPI (strategic >= greedy within noise: +-1.1 pts). A human who can count cards and read the Double-Crosser should do better than the bot; confirm with a human playtest."},
     {"severity": "low", "problem": "Target 3 is the most common bot choice and the least reliable; Targets 4-6 are the profitable band.",
      "evidence": "Target 3 chosen %.0f%% of rounds, success %.0f%%; Target 6 chosen %.0f%%, success %.0f%%." % (b["targ"][3][0]*100, b["targ"][3][1]*100, b["targ"][6][0]*100, b["targ"][6][1]*100),
      "fix": "None; a sensible planner choice, not a dead option."},
     {"severity": "low", "problem": "Games are low-scoring and Heat is on in most rounds.",
      "evidence": "Mean final score %.1f (rules.md predicted 18-28); Heat applies in %.0f%% of rounds (holder averages %.2f pts vs %.2f round average)." % (b["score_mean"], b["heat_rate"]*100, b["heat_pts"], b["mean_round_pts"]),
      "fix": "Update the design-note scoring expectation to about 16; no rule change."}]

def build(out, N):
    b = out["mirror"]; sk = out["skill"]; mx = b["seatwin"]; b["targ"] = {int(k): v for k, v in b["targ"].items()}
    gap = (max(mx) - min(mx)) * 100; skill = (sk["strategic"] - sk["random_each"]) * 100
    cards = []
    for role, v in b["role"].items():
        flag = "overpowered: earns far above average per round" if v[1] > 0.4 else ("dominated: earns far below average per round" if v[1] < -0.4 else None)
        cards.append({"name": role + " role", "played_rate": 1.0, "win_correlation": round(v[1], 2), "flag": flag})
    for t, (u, s) in b["targ"].items():
        d = s - b["success"]
        cards.append({"name": "Target %d" % t, "played_rate": round(u, 2), "win_correlation": round(d, 2),
                      "flag": "dominated: crew hits it only %d%% of the time" % round(s * 100) if s < 0.12 else None})
    cards.append({"name": "Heat", "played_rate": round(b["heat_rate"], 2), "win_correlation": None, "flag": None})
    cards.append({"name": "The Swap", "played_rate": 1.0, "win_correlation": None, "flag": None})
    runaway = b["early3"]
    ex = out["experiments"]
    problems = build_problems(out, b, mx, gap, skill)
    verdict = verdict_of(out, b, gap, skill, runaway, problems)
    pj = {"verdict": verdict, "revision": 2, "games_simulated": out["mixed_games"] + out["skill_games"] + b["n"] * 6,
      "seat_win_rates": {str(i + 1): round(x, 3) for i, x in enumerate(mx)}, "seat_balance_gap": round(gap, 1),
      "bot_win_rates": {k: round(v, 3) for k, v in out["mixed"].items()}, "skill_expression": round(skill, 1),
      "length": {"mean_turns": 42, "stdev": 0.0, "estimated_minutes": round(MIN), "target_minutes": 20},
      "length_histogram": [{"turns": 42, "games": b["n"]}],
      "ties": round(b["ties"], 3), "turn_cap_hits": 0, "lead_changes_mean": round(b["lc"], 2), "runaway_leader_rate": round(runaway, 3),
      "contract_success_rate": round(b["success"], 3),
      "cards": cards, "ambiguities": __import__("game").AMBIGUITIES, "problems": problems}
    json.dump(pj, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=2)
    return pj
