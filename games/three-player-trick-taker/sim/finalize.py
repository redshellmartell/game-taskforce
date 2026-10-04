"""Builds ../playtest.json from results.json (called by run.py)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
MIN = 6 * (1 + 7 * 17.5 / 60.0)

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
    problems = [
     {"severity": "high", "problem": "Greedy trick-grabbing still beats the intended contract-steering strategy; skill is in loot, not in the contract.",
      "evidence": "Mixed table: greedy %.1f%%, strategic %.1f%%, random %.1f%% (KPI/design aim: strategic >= 40%%, >= greedy). Per round (300x6 games) greedy crew scores 4.4-4.5 pts and takes 3.7-3.8 tricks; strategic crew scores 3.5-3.6 with 2.3-2.9 tricks, yet contract success is the same (greedy 48-52%%, strategic 53-55%%). Ducking to protect the contract costs loot and does not raise the success rate. Doubling all bonuses (experiment) moves greedy 63%%->50%% and strategic 29%%->33%%; tripling gives 43%%/34%%: the gap closes only by making greedy worse, not strategic better." % (out["mixed"]["greedy"] * 100, out["mixed"]["strategic"] * 100, out["mixed"]["random"] * 100),
      "fix": "Make steering reliably profitable: e.g. loot only for tricks won as Double-Crosser, or 1 loot per two tricks, or clean +5/+6 with messy 0; and/or give the crew a way to control the count (e.g. Planner may pass a card). Caveat: my strategic heuristic is simple; a smarter bot may do better, but a heuristic derived from the design notes that cannot match plain grabbing is a warning."},
     {"severity": "medium", "problem": "Lead changes below KPI.",
      "evidence": "%.2f lead changes per game (KPI >= 2). Sole leader after round 3 wins %.1f%% (OK, KPI <= 65%%). Heat helps: without Heat lead changes %.2f and early leader %.1f%%." % (b["lc"], runaway * 100, ex["no_heat"]["lc"], ex["no_heat"]["early3"] * 100),
      "fix": "Raise round volatility (bigger clean/blown bonuses, bonus multiplier 2 gave 1.56) or score the last round double; Heat -3 would be another lever."},
     {"severity": "low", "problem": "Target 3 dominates bot choices (about a third of rounds) but is the least reliable target.",
      "evidence": "Planner picks Target 3 in %.0f%% of rounds with a %.0f%% success rate; Target 5-7 succeed %.0f-%.0f%%. Fixed Target 5 planner wins %.1f%% (fair 33%%) with success %.0f%%, so not dominant." % (b["targ"][3][0] * 100, b["targ"][3][1] * 100, b["targ"][5][1] * 100, b["targ"][6][1] * 100, ex["fixed5"]["seat0_win"] * 100, ex["fixed5"]["success"] * 100),
      "fix": "None required; the bot's target estimate is conservative. Watch for high Targets being too easy for the crew (86%% at Target 6)."},
     {"severity": "low", "problem": "Seat balance inside tolerance but with noise; length is fixed.",
      "evidence": "Seat win rates %s, gap %.1f pts (KPI <= 5, standard error ~1.1 pts per seat at 2,000 games). Every game is 42 tricks; estimated %.0f min vs target 20 (inside +/-20%%)." % ([round(x, 3) for x in mx], gap, MIN),
      "fix": "Re-check on 4,000+ games if the rules change again."}]
    verdict = "NEEDS-FIXES"
    pj = {"verdict": verdict, "revision": 1, "games_simulated": out["mixed_games"] + out["skill_games"] + b["n"] * 6,
      "seat_win_rates": {str(i + 1): round(x, 3) for i, x in enumerate(mx)}, "seat_balance_gap": round(gap, 1),
      "bot_win_rates": {k: round(v, 3) for k, v in out["mixed"].items()}, "skill_expression": round(skill, 1),
      "length": {"mean_turns": 42, "stdev": 0.0, "estimated_minutes": round(MIN), "target_minutes": 20},
      "length_histogram": [{"turns": 42, "games": b["n"]}],
      "ties": round(b["ties"], 3), "turn_cap_hits": 0, "lead_changes_mean": round(b["lc"], 2), "runaway_leader_rate": round(runaway, 3),
      "contract_success_rate": round(b["success"], 3),
      "cards": cards, "ambiguities": __import__("game").AMBIGUITIES, "problems": problems}
    json.dump(pj, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=2)
    return pj
