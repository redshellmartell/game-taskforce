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
    u, s = b["trump"].get("NT", (0.0, b["success"])); cards.append({"name": "No Trump", "played_rate": round(u, 2), "win_correlation": round(s - b["success"], 2), "flag": None})
    cards.append({"name": "Heat", "played_rate": round(b["heat_rate"], 2), "win_correlation": None, "flag": None})
    cards.append({"name": "The Swap", "played_rate": 1.0, "win_correlation": None, "flag": None})
    runaway = b["early3"]
    problems = [
     {"severity": "high", "problem": "The exact-contract twist almost never succeeds, so the Double-Crosser bonus is nearly free.",
      "evidence": "Crew hits the Target %.0f%% of rounds (design aim 40-60%%); random bots 17%%, greedy 19%%, strategic 20%%. Double-Crosser earns %.1f pts/round vs Safecracker %.1f and Planner %.1f." % (b["success"] * 100, b["role"]["Double-Crosser"][0], b["role"]["Safecracker"][0], b["role"]["Planner"][0]),
      "fix": "Make hitting the target far likelier: accept Target +/-1 for a smaller bonus, or let the crew hit if tricks fall in a band; or cut the Double-Crosser bonus to +2 and raise the crew bonus."},
     {"severity": "high", "problem": "Intended strategy (hit the exact Target, duck to avoid overshoot) loses to plain trick-grabbing.",
      "evidence": "Mixed table: greedy %.1f%%, strategic %.1f%%, random %.1f%%. Greedy beats two randoms %.0f%% of games vs strategic %.0f%%. Four tuned variants of strategic (greedy swap/plan/lead, no-duck) stayed at 13-17%% vs two greedy bots (fair is 33%%)." % (out["mixed"]["greedy"] * 100, out["mixed"]["strategic"] * 100, out["mixed"]["random"] * 100, sk["greedy"] * 100, sk["strategic"] * 100),
      "fix": "Same as above: exactness must be achievable. Caveat: my strategic heuristic is a simple one and a smarter bot (card tracking, partner signalling) might do better."},
     {"severity": "medium", "problem": "Role imbalance within a round: Safecracker is the worst role, Double-Crosser the best.",
      "evidence": "Points per round %.2f (Safecracker) vs %.2f (Double-Crosser); roles rotate so seats stay fair, but every player spends a third of the game in a role with little chance." % (b["role"]["Safecracker"][0], b["role"]["Double-Crosser"][0]),
      "fix": "Rebalance bonuses; consider giving the Safecracker a keep-3 swap or a loot bonus."},
     {"severity": "medium", "problem": "Too few lead changes and a borderline runaway rate.",
      "evidence": "%.2f lead changes per game (KPI >= 2); sole leader after round 3 wins %.1f%% (KPI <= 65%%). Removing Heat changes it little (lead changes %.2f, early leader %.1f%%): Heat does almost nothing, it is held in 73%% of rounds and costs the holder ~0.45 pts." % (b["lc"], runaway * 100, out["experiments"]["no_heat"]["lc"], out["experiments"]["no_heat"]["early3"] * 100),
      "fix": "Make Heat bite harder (-2, or also -1 loot) or drop it to simplify; more volatile bonuses would also help."},
     {"severity": "low", "problem": "Seat gap close to the limit and game length is fixed.",
      "evidence": "Seat win rates %s (gap %.1f pts, standard error about 1.1 pts per seat at 2,000 games). All games last exactly 42 tricks; length is not variable, estimated %.0f min vs target 20 (inside +/-20%%)." % ([round(x, 3) for x in mx], gap, MIN),
      "fix": "Re-check seat gap on a larger run after the next revision; no change needed now."},
     {"severity": "low", "problem": "Target choice: low targets dominate bot choices but are mostly misses.",
      "evidence": "Strategic planners pick Target 3 in %.0f%% of rounds with a %.0f%% hit rate; best hit rate is Target 6 (%.0f%%). A fixed Target 5 planner wins %.1f%% vs two adaptive bots (fair 33%%), so fixed targets are not dominant." % (b["targ"][3][0] * 100, b["targ"][3][1] * 100, b["targ"][6][1] * 100, out["experiments"]["fixed5"]["seat0_win"] * 100),
      "fix": "Improve the bot's target estimate when revising; the real fix is the exactness issue above."}]
    verdict = "NEEDS-FIXES"
    pj = {"verdict": verdict, "revision": 0, "games_simulated": out["mixed_games"] + out["skill_games"] + b["n"] * 6,
      "seat_win_rates": {str(i + 1): round(x, 3) for i, x in enumerate(mx)}, "seat_balance_gap": round(gap, 1),
      "bot_win_rates": {k: round(v, 3) for k, v in out["mixed"].items()}, "skill_expression": round(skill, 1),
      "length": {"mean_turns": 42, "stdev": 0.0, "estimated_minutes": round(MIN), "target_minutes": 20},
      "length_histogram": [{"turns": 42, "games": b["n"]}],
      "ties": round(b["ties"], 3), "turn_cap_hits": 0, "lead_changes_mean": round(b["lc"], 2), "runaway_leader_rate": round(runaway, 3),
      "contract_success_rate": round(b["success"], 3),
      "cards": cards, "ambiguities": __import__("game").AMBIGUITIES, "problems": problems}
    json.dump(pj, open(os.path.join(HERE, "..", "playtest.json"), "w"), indent=2)
    return pj
