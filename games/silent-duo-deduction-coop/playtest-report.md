# Playtest report: Silent Duo, revision 2 (rules v3)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** 2,000 games per configuration, 24 headline configs plus 3 Fog experiments (2p F8, F9; 3p F8). Reference bots: Honest (strong), Greedy (no counting, lights at 50%), Random. Nothing here tests human deduction, the silence rule, teaching or fun.

## Key numbers (2p Standard F6 unless stated; previous = cycle 1 at F8)
| KPI | Target | v3 | Previous | Met |
|---|---|---|---|---|
| Honest / Greedy 2p Standard | 40-60 | 63.0 / 73.8 | 55.8 / 58.4 (F8) | NO |
| Honest / Greedy 3p Standard F2 | 40-60 | 61.9 / 72.9 | 38.0 / 47.4 (F8) | NO |
| Greedy minus Honest 2p / 3p | <=5 / <=5 | +10.8 / +11.0 | +2.6 / +9.4 | NO |
| Random gap (2p) | >=20 | 61.8 | 54.6 | yes |
| Code attack minus Honest F6 / F10 | <=10 | +2.8 / +2.3 | +1.0 / +3.0 | yes |
| Trim share 2p / 3p | <25% | 25% / 26% | 30% | borderline/NO |
| 3+ Trim runs 2p / 3p | <10% | 54% / 49% | 61% | NO |
| Length 2p / 3p (turns) | 22-26 | 23.1 / 25.2 | 23.5 | yes |
| Turn-cap hits | 0 | 0 | 0 | yes |

Fog sweep (Honest / Greedy): 2p F3 72.9/84.5, F6 63.0/73.8, F8 57.4/65.8, F9 52.1/62.1, F10 48.6/56.2. 3p F0 66.8/79.6, F2 61.9/72.9, F6 45.8/60.4, F8 40.6/51.9. Length at 2p: F3 24.4, F6 23.1, F8 22.2, F9 21.7, F10 21.0.

## Ablations (loss vs Honest at Standard; need >=5)
| Bot | 2p F6 | 3p F2 |
|---|---|---|
| Pair-blind | -6.9 | -6.0 |
| Trim-blind | -12.9 | -16.4 |
| No counting | -9.4 | -8.3 |
| Single-blind (not a twist test) | -12.9 | -12.6 |

All three required ablations pass. Single-blind shows the Single Offer is used and valuable, but it moves Trim share only 29% to 25% and 3+ runs 60% to 54% (2p), so it explains about 4 points of the Trim drop (L10).

## Problems
1. **High: Trim stall not fixed.** 3+ Trim runs in 54% (2p) and 49% (3p) of games against a <10% target. Greedy, which Trims only when no Offer is legal, still Trims 18% of turns with runs in 40% of games, so many Trims are forced (hands with no fitting card). Honest's Trims are 66% voluntary (an Offer existed but costs a needed lamp). The Known-gaps rule applies: stop bot-side iteration and take a human playtest.
2. **High: Fog Standard values are wrong.** Both bots are in band only at 2p F10 and 3p F8; at F6/F2 Honest is 63/62 and Greedy 74/73. Greedy beats Honest by 11 at both counts, a gap Fog does not close (same at every F). Likely a cautious-Honest artefact (L2), but it means "decisions reward care" is unproven.
3. **Medium: length conflicts with band.** The band-correct Fog (F10) gives 21.0 turns, below 22-26. F8 gives 22.2 turns but Honest 57/Greedy 66.
4. **Low:** Beacon cut verified (no Beacon stat); no dead action: Pair, Single, Light, Trim all used; Single share and correlations in playtest.json `cards`.

## Ambiguities hit (coded interpretation in sim/game.py AMBIGUITIES)
Single Offer with two copies of one fitting value (counted as one value, Single legal); Single on one ship while Pair is legal on another (allowed); Single card equal to L or H (impossible by strictness); skip during Last Watch (counter still advances); plus the 10 v2 items. Dead cards: none; Beacon bonus weighting in Honest's light score is now a harmless tie-break toward exact hits.

## Narrated play (seed 11, 2p F6, Honest vs Honest, lost on turn 24)
Turns 1-7 were pleasant: both of us poured Offers on each other's ships, the range narrowing felt like real deduction. Turn 10 was the first Trim: I held cards that no longer fitted any partner ship; boring, a waiting turn. Turn 11 the Single Offer let my partner signal 4 with their lone fitting card, a good moment (no waste). Then turns 13, 16, 17, 19, 21 were Trims: five of the last 12 turns were "discard and hope", which felt like downtime with no decision of consequence. The loss came from a forced 10 Light on a wide range as the deck ran out (T24, second Reef). Frustrating, mid-game stall as the previous cycle warned. Single Offer is a fun moment but too rare to cure it.

## What simulation cannot test
Whether humans can read pair choices or find a code under the silence rule, teach time (rules are ~200 lines), real Fog calibration (human teams deduce worse than bots), and fun of the Trim downtime. The code attack is only the hat-guessing family I coded. Untested suggestions: a no-discard draw action to replace forced Trims; hand size 6; a Honest variant with Greedy's Light threshold, to separate bot artefact from rule effect.

## Panel bots
Free panel run: average fun 3.99, best fit competitor, worst fit family (3.11); file panel.json.
