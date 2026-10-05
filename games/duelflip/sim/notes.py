"""Playtester's judgement text for playtest.json (revision 3). Numbers come from run.py; words from playtest-report.md."""
VERDICT = "PASS"; REVISION = 3
ESTIMATED_MINUTES = 12   # about 22 turns at roughly 30 seconds each; brief asks 10-15 (target 12.5)
TARGET_MINUTES = 12.5
AMBIGUITIES = []   # none found in rules.md revision 3; interpretations used are listed in the report
PROBLEMS = [
 {"severity": "medium", "problem": "Runaway leader above KPI (known, accepted by the designer)",
  "evidence": "Halfway leader wins 74.0% (strategic mirror), one-third leader 68.5%; KPI is 65% or less. Unchanged from rev 2 (74.8%).",
  "fix": "Not fixed this revision. Human playtests should check whether trailing players feel out of it. Untested idea: trailing player's bust pile is cut, or a catch-up bonus to the trailing player's claim test."},
 {"severity": "low", "problem": "Smart leaver edge is modest",
  "evidence": "Smart leaver beats leave-lowest 55.3% and leave-highest 53.5%; non-lowest card left in 27.9% of choices. Leave choice now matters but is worth a few points, not a decisive skill.",
  "fix": "None needed for the KPIs. Watch in human play whether the leave choice feels meaningful."},
 {"severity": "low", "problem": "Strategic bot is a one-step lookahead and cannot plan a push to the 2x hurdle",
  "evidence": "Claim rate for 9 and 10 baits is 39% and 17%; real players planning a multi-flip push may claim more, which would tilt towards leave-lowest. Not testable with these bots.",
  "fix": "Human playtest focus: do players leave 9-10 baits and do rivals reach 18-20? Fallback knob (1.5x rounded up) is ready if leave-highest grows too strong."},
]
def cards(res):
    return [
     {"name": "Bait hurdle (claim needs pile >= 2x bait)", "played_rate": round(res["bait_turn_rate"], 3), "win_correlation": None,
      "flag": None},
     {"name": "Bait (leave one card)", "played_rate": 1.0, "win_correlation": None, "flag": None},
     {"name": "Lifebuoy (one-shot)", "played_rate": round(res["buoys_per_game"] / 2, 3), "win_correlation": None, "flag": None},
    ]
