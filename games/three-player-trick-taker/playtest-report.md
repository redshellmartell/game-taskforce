# Playtest report - Split the Take (revision 1, rules v2)

**Verdict: NEEDS-FIXES** (big improvement over revision 0; two KPIs still missed).

| KPI | Target | Rev 0 | Rev 1 | Result |
|---|---|---|---|---|
| Seat gap (strategic mirror, 2,000 games) | <= 5 pts | 2.7 | 3.5 (35.1/33.2/31.7) | pass |
| Strategic vs random (1 vs 2) | >= 20 pts | ~ | 51.6 pts (67.7% vs 16.1%) | pass |
| Mixed table R/G/S | strategic >= greedy | 27% vs 68% | 28.5% strategic, 63.5% greedy, 8.1% random | FAIL |
| Length | 20 min +/-20% | 18 | 18.2 min (42 tricks, fixed) | pass |
| Runaway (leader after R3 wins) | <= 65% | 64.4% | 52.3% | pass |
| Lead changes | >= 2 | 1.27 | 1.49 | FAIL |
| Contract success (clean or messy) | 40-60% | 19.7% | 56.6% (DC paid 43.4%) | pass |
| Role pts/round P / S / DC | within ~1 | 3.5/2.7/4.8 | 3.84 / 3.53 / 3.95 | pass |
| Ties | low | | 0.75% | pass |
| Dead options | 0 | No Trump | none | pass |

## Problems
1. **High: greedy still beats strategic.** Greedy 63.5% vs strategic 28.5% at a mixed table. Per-round data: a greedy crew member scores 4.4-4.5 pts (3.7-3.8 tricks); a strategic one 3.5-3.6 pts (2.3-2.9 tricks) with the same contract success (about 50-55%), so ducking to protect the contract costs loot and buys nothing. Swapping individual strategic components for greedy ones (plan, swap, play) each gave 32-38% vs greedy+random, no single culprit. Doubling all bonuses gave greedy 50%/strategic 33%/random 17%; tripling 43/34/23: greedy falls but strategic does not rise. Contract success is about a coin flip whatever the bot does, so steering skill is not rewarded. Fix: make steering pay clearly (loot worth less, e.g. half or only DC loot, with clean +5/+6; or give the crew a count-control tool). Caveat: my strategic bot is simple, a smarter one might do better.
2. **Medium: lead changes 1.49 (KPI 2).** Heat helps (without Heat 0.98 lead changes, early leader 67.4%). Bonus x2 gave 1.56. Try Heat -3, or double scoring in the last round.
3. **Low:** Target 3 is chosen 34% of rounds (36% success); Target 6 succeeds 86%. Not dominant (fixed Target 5 planner wins 37.6%, fair 33%, within noise of variant bots).
4. **Low:** all games are exactly 42 tricks, no length variance.

## Rule ambiguities
None blocking in v2. Interpretations used: revokes impossible; Heat on 0 bonus does nothing; no Heat in round 1 (tied); deal order irrelevant to a random shuffle.

## Experiments run (5 configs max)
no Heat; fixed Target 5; offset -1; offset +1; DC always-wins (all within 0.33-0.38 seat-0 win vs two strategic bots: no exploit); plus component swaps and bonus x2/x3 (scratch scripts in sim/experiments/). Untested: loot halved with clean +5/+6; Heat -3; double final round; smarter strategic bot with card counting.

## Narrated play
Not replayed this pass (rules change affected scoring, not turn feel). Sample logs in sim/logs show the round now has a clear tension: a crew on target-1 with one trick left either takes it (clean) or ducks (messy), and the DC's choice to push away is visible. The Swap of 3 now regularly reshapes a hand, but cheap-win greedy play makes most rounds read as "take tricks" regardless of the contract.

## Panel (free bot rotation)
20 tables x 6 seatings x 200 games, 12,000 per persona. Average predicted fun 3.54 (competitor 4.31 best fit, family 3.07 worst fit; Bar Raiser 3.90, **veto not active**). Results in panel.json.
