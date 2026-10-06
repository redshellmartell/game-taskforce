# Playtest report: Silent Duo, revision 1 (rules v2)

**Verdict: NEEDS-FIXES, bots only, unvalidated.** Main numbers moved into band; Trim is still a waiting action and the Beacon is not a skill decision. 2,000 games per config, fixed seeds, sim in `sim/` (`run.py`).

## Key numbers (team win %, Honest / Greedy; target 40-60%)
| Config | Honest | Greedy | Previous (v1) |
|---|---|---|---|
| 2p F4 | 64.1 | 69.6 | - |
| 2p F8 (Standard) | 55.8 | 58.4 | 73.0 / 81.6 |
| 2p F12 | 42.0 | 47.0 | 57.5 / - |
| 3p F4 | 48.5 | 57.8 | - |
| 3p F8 | 38.0 | 47.4 | 53.2 / - |
| 3p F6 (extra) | 43.0 | 52.6 | - |
| 3p F12 | 26.9 | 33.3 | - |

- Spread of two reference bots: 2p F8 56-58 (in band), 3p F8 38-47 (Honest under), 3p F6 43-53 (in band). Greedy minus Honest: +2.5 (2p), +9.4 (3p F8), +9.7 (3p F6); target <=5 fails at 3p.
- Random: 1.2% (2p), 0.8% (3p); skill gap 54.7 points (target >=20, was 72).
- Code attack (hat-guessing code, 2p): +1.0 at F8, +3.0 at F12 over Honest (previous +3.6 at F8, +12.1 at F16). Passes (<=10). F16 not re-run.
- Ablations at F8 / F12 (points lost vs Honest, need >=5): Pair-blind 8.9 / 7.9 pass; Trim-blind 15.9 / 12.0 pass; No card counting 13.8 / 10.0 pass (was 8.6); Beacon-blind 0.5 / 0.9 FAIL. Beacon-hunter (waits for exact hits) -0.9/-0.1. Beacon rule removed outright: Honest 44.6 (-11.3) at F8, 29.5 at F12.
- Trim: 30% of turns (previous 38%, target <25%); 3+ Trim runs in 61% of 2p games (target <10%); 60% of Trims happen with no legal Offer.
- Beacons 2.0 per game (target about 2 or fewer). Length 23.5 turns (sd 2.2), about 18.1 min vs 20 (-9%). Turn cap hits 0 in about 50,000 games.
- Close games: see sim/results.json (late-win and near-loss shares).

## Problems (ranked)
1. HIGH Trim still waiting action (above). Cause is the v2 Offer legality, not bot taste: Greedy does it too. Fix: loosen Offer legality or allow Offer after Trim; re-test Code attack.
2. MEDIUM 3p Standard F=8 Honest 38%; use F=6 (43/53). Greedy beats Honest by 9+ at 3p: risk-taking pays.
3. MEDIUM Beacon is a flat time gift, not a decision (ablation 0.5-0.9). Reframe or cut and lower Fog.
4. LOW Rules contradiction 4A vs 5.2 on Offer legality.

## What worked
Reefs 3 to 2, Trim draw-2-keep-1 and hopeless-Light ban moved Honest 73% to 56% at F8. The Trim keep choice and pair choice are real skills. Code attack no longer pays. Reveal token cannot be tested with bots beyond 50/50 randomness.

## Ambiguities hit (see playtest.json)
Offer legality text (3 vs 2 values); same-side pair cases; Trim-with-1-card; Trim-card visibility in 3p; Beacon timing in Last Watch; Light window includes equal-to-edge cards; turn-cap formula; 3p third-player role.
Dead cards: none (values 1-10 identical); Beacon (see 3) is the only near-dead rule.

## Narrated play (one bot-assisted game, seed 3, 2p F8)
T1-T9 are all Offers and two Lights: engaging, every offer feels like a puzzle (pair choice, which ship). T2 a Beacon lit early: a happy moment. T5 a miss on 9 (value 8): first Reef, tension rises. Then T11-T19: nine turns, seven are Trims; nothing legal to say, nothing to light: boring, repeated, and the game was decided by luck of the draw. Loss in the Last Watch with two forced misses on the same 10: frustrating and anticlimactic. Downtime is low (2p alternate). Feels good for 10 turns, flat for the rest.

## Panel (free bots)
Average predicted fun 3.98; best fit competitor (4.69), worst fit family (3.07). Panel Fog set to 2p F8, 3p F6.

## What simulation cannot test
Fun, teaching time and rulebook readability (about 227 lines), table talk and how well humans deduce (human teams will do worse than Honest, so real win rates will be lower than shown), the Silence rule being kept, human-made codes beyond the one hat code, and the physical Reveal token flip.

## Untested suggestions
Offer legality loosening; F=16 Code re-run; 3p third-player role; Pair-blind at 3p.
