"""Playtester's judgement text for playtest.json (revision 2). Numbers come from run.py; words from playtest-report.md."""
VERDICT = "NEEDS-FIXES"; REVISION = 2
ESTIMATED_MINUTES = 12   # about 23 turns at roughly 30 seconds each; brief asks 10-15 (target 12.5)
TARGET_MINUTES = 12.5
AMBIGUITIES = []   # none found in rules.md revision 2; interpretations used are listed in the report (not rule gaps)
PROBLEMS = [
 {"severity": "high", "problem": "Bait hurdle is inert: the bait is claimed 99% of the time, so 'leave lowest' is still the answer",
  "evidence": "Claim rate by bait value 1-10: 1.00 for 1-5, 0.99/0.98/0.96/0.95 for 6-9, 0.89 for 10. Smart leaver picks a non-lowest card in only 5% of choices; leave-lowest scores 50.1% against it (target <60% met, but only because there is nothing to gain from leaving anything else). Bots simply flip until the pile beats the bait. Variant claim needs pile > bait+3: low still 49.3% vs smart, claim still 98%.",
  "fix": "The hurdle must bind. Options: claim needs pile total >= 2x bait value (a 10 bait needs 20), or the failed claimer also pays a cost (bait returns with 1 card from their pile). Re-test leave-lowest vs smart."},
 {"severity": "medium", "problem": "Runaway leader above KPI",
  "evidence": "Halfway leader wins 74.8% (strategic mirror), one-third leader 68.6%; KPI is 65% or less. Haul-based scoring only accumulates and busts are small (average pile 5.9).",
  "fix": "Add catch-up: bust pile counts less for the trailing player, or the trailing player claims bait on pile >= bait. Alternatively accept and document; v1 was about the same."},
 {"severity": "low", "problem": "Leave-highest is not dominant, but it is a trap rather than a choice",
  "evidence": "Leave-highest wins 20.9% against smart; leave-lowest beats leave-highest 80.8%; random leave 34.5%.",
  "fix": "Resolved if the hurdle fix makes mid-high baits viable."},
 {"severity": "low", "problem": "Busts are frequent and small",
  "evidence": "4.3 busts per game (1.8 on the bait), average bust pile 5.9. Every Lifebuoy is spent in every game (2.0 per game).",
  "fix": "None needed; the Lifebuoy is a guaranteed-use token, so it is fine as a one-shot."},
]
def cards(res):
    return [
     {"name": "Bait hurdle (claim only if pile > bait)", "played_rate": round(res["bait_turn_rate"], 3), "win_correlation": None,
      "flag": "inert: bait claimed %.0f%% of tries, so the hurdle rarely bites" % (100 * res["claim_rate"])},
     {"name": "Bait (leave one card)", "played_rate": 1.0, "win_correlation": None,
      "flag": "dominated: leave-lowest is about optimal (smart leaver deviates 5% of the time, gain about 0 points)"},
     {"name": "Lifebuoy (one-shot)", "played_rate": round(res["buoys_per_game"] / 2, 3), "win_correlation": None, "flag": None},
    ]
