# Playtest report: Dead Reckoning, revision 1 (rules v2)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** Sim updated to rules v2; 20,000 headline games (2,000 per pairing, 10 pairings), 6 ablation runs of 2,000, 4 extra configs of 600 (`sim/experiments/exp-results.json`). Targets from CLAUDE.md.

## Key numbers (strategic-bot pairings unless noted)
| KPI | Target | Rev 0 | Rev 1 | Result |
|---|---|---|---|---|
| Runaway leader (mid-game leader wins) | <= 0.65 | 0.795 | **0.831** (every pairing 0.76-0.92) | FAIL, worse |
| Lead changes per game | >= 2 | 1.5 | **1.50** | FAIL, unchanged |
| Seat balance gap (mirrors) | <= 5 | 1.4 | 1.8 | pass |
| Strategic v random gap | >= 20 | 75 | 88.7 | pass |
| Spread of reference bots | | | random < greedy < mid ~ strategic: S v G 78.8%, mid v G 77.7%, S v mid 50.8%, G v R 89.2% | skill step is greedy to mid; depth beyond 2 rival plans adds nothing |
| Length | 15 min +-20% | 9.7 rounds, 14.8 min | 11.0 rounds, 17.1 min (+14%; 85 s/round is a guess) | pass |
| Ties / turn-cap | | 0.4% / 0 | 0.2% / 0 non-ending; 71% of games (58% mirror) end on the round-12 cap | note |
| Round 1 | | | collision in 41.5% of games; round-1 leader wins 58.2% | mild effect |

## Ablations (designer's table; ablated bot's win rate vs full strategic)
| Feature | Must be | Result |
|---|---|---|
| Cooling-blind | <= 45% | 41.4% pass (reading worth ~17 pts, up from ~5) |
| No ping | <= 45% | **49.4% FAIL** (52% with 3-step ping, X2) |
| No torpedo | <= 45% | 29.9% pass |
| No middle row | <= 45% | 29.2% pass |
| Camper | <= 55% | 48.8% pass |
| v1 single-shuffle deal | runaway "clearly higher" | 0.794 vs 0.78: **not clearly higher**; the zoned deal did almost nothing |
Extra: torpedo-spam bot 48.4% vs strategic (no exploit); 8-round cap leaves runaway at 0.78; 3-step ping leaves runaway at 0.76.

## Problems
1. **HIGH: runaway leader 0.83 and lead changes 1.5.** Mirrored deal and middle 3s did not help; the result is flat across all bots, so this is the design (a race to a finite pile, no catch-up keyed to the score gap). Untried fixes: bigger steal (2 cards), leader-only Mine penalty, shared scoring that keeps moving. Critic's stop rule (park if runaway stays above 0.70) applies.
2. **HIGH: Sonar is dead.** No-ping bot wins 49.4%; pings 0.35 per player per game; ping spent correlates -0.17 with winning (only trailers can ping, so it marks losing). Cut it or give it a stronger effect.
3. **MEDIUM: coasting.** In the sampled game P1 sat at 7-15 for three rounds with nothing reachable. Shorten the cap to 9-10 or end when the gap exceeds remaining salvage.
4. **MEDIUM: round 1 is a home-waters race.** Subs went home, grabbed their own mirrored 9 points and did not meet until round 3.
5. Healthy: torpedo (hits link to winning, +0.35), middle row, cooling-read, no camper or spam exploit. Dead cards: Sonar only (Mine, Reef, Salvage all used 86-98% of games).

## Ambiguities hit (6)
Mine for a sub with no salvage; whether a cancelled T step fires (I assumed not); whether the rival is told a ping is coming before plotting (I assumed yes, announced in phase 1); steal timing when a salvage is taken and fired on in the same step (enter then fire); a revealed ping card that is later blocked stays locked; no rule for a round-12 stalemate when nobody can reach salvage.

## Narrated play (1 game, strategic bots, seed 42)
Round 1: Blue went N N E, Red S S E; both grabbed home-water cards (2 and 1), no contact, a quiet start. Round 2 I took the east column while the rival did the same on its side: tidy, but it felt like two solitaire games on mirrored boards. Round 3 was the highlight: the trailing Red pinged, saw my two Norths, and torpedoed to reach 6-6. The hand-reading puzzle (their Torpedo is cooling, so I can walk past) is the real fun and I enjoyed it. Then by round 6 Red led 15-7 and I could not catch up: no wreck was near and I walked home for three rounds with no choices that mattered. Boring and frustrating late, which matches the runaway number. Rounds are simultaneous, so there is no downtime.

## What simulation cannot test
Fun, teaching time (about 100 lines of teach text), real-player bluffing and table talk, whether the 85 s round estimate holds, the card layout readability, and whether humans read the open hands better or worse than bots.

## What worked / did not
Worked: cooling-blind ablation (41%), torpedo and middle-row value, seat balance, skill gap, length. Did not work: zoned mirrored deal (runaway 0.83, not 0.65), trailer-only ping (Sonar dead), cap 12 (coasting rose to 71% of games ending on the cap).

BUDGET REQUEST: none needed; suggested untested ideas are listed under Problem 1.
