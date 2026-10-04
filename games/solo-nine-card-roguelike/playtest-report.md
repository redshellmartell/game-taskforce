# Nine Lives Dungeon - Playtest report (revision 0)

**Verdict: NEEDS-FIXES** (not broken: rules run cleanly, no turn-cap hits, max 14 turns)

## Key numbers
All exhaustive over 362,880 layouts, empty Ghost set, unless noted. Seat balance, lead changes and runaway leader do not apply (solo).

| Measure | Target | Result |
|---|---|---|
| Outline strategic bot (designer's) win rate | 40-60% | **19.1%** |
| Lookahead bot (determinised Monte Carlo, 3,632 layouts, every 100th) | 40-60% | **80.8%** |
| Random / greedy | random >=20 pts under strategic | 0.0% / 4.9% (gap 19 pts outline, 81 pts lookahead) |
| Median turns / est. minutes (time model) | 7-12 turns, 8-12 min | outline 6 / 6.4 min; lookahead 9 / 8.3 min |
| Wins by Feint / Hypnotise / neither | >=10 / >=10 / >=25% | outline 2 / 15 / 83%; lookahead 16 / 21 / 63% |
| First action is Shove | 20-60% | outline 36%; lookahead 91% |
| Hound share of deaths; cards over 5% | 40-75%; >=4 cards | outline 55%, 3 cards; lookahead 12%, 8 cards |
| Single-Ghost lift (outline) | +5 to +25 | Moth 0, Mouse +0.2, Spider +1.4, Rat +21, Hound +19, Snake +29, Crow +38, Fox +43, Owl +44 |
| Sessions (outline) | 3-4 runs, no score over 40% | 4.1 runs, top score share 38% (lookahead: 2.3 runs, 72% score 9) |
| Turn-cap hits | 0 | 0 |

## Experiments (5, one change each; outline exhaustive, lookahead 1,210 layouts)
| Config | Outline | Lookahead |
|---|---|---|
| Baseline | 19.1% | 80.8% |
| Base Claws 1 | 1.4% | 6.5% |
| Base Claws 3 | 48.1% | 98.6% |
| Hunt lethal | 19.1% | 60.3% |
| Anger +3 | 19.1% | 67.1% |
| Hound swap off | 16.0% | 78.5% |

## Problems (by severity)
1. **High: the win rate depends on how well you solve it, and the band lies in the gap.** 19% vs 81% between two competent bots; random never wins in 362,880 runs. The real win rate for humans is unknown and sim cannot tell. Claws is a knife edge (1: 1-7%, 3: 48-99%). Fix: keep Claws 2, run human sessions first; if humans resemble the outline bot, try Claws 3 plus Hunt lethal (untested together).
2. **High: the designer's outline bot misses four targets** (win rate, median length 6, Feint share 2%, only 3 killer cards). It loops by Shoving into the cell that holds the known Hound. A shove-target fix reached 24.7% in a 3,000-run check (not run exhaustively). The lookahead bot meets Feint, Hypnotise, no-forced-route and length targets. So the variety targets are reachable, but only by strong play.
3. **Medium: Ghost effect out of range and uneven.** Ghost Moth/Mouse/Spider do nothing; Owl/Fox/Crow Ghosts nearly double the win rate. Fix: give low Ghosts an effect (start with that trophy Ready); raise Owl/Fox/Crow Ghost Danger to 2.
4. **Medium: near-dead tricks.** Strong-bot use when Ready: Moth 0.5%, Spider 0.3%; Crow's Carry 0.15% (outline) and not modelled by the lookahead bot, so Carry is untested. Mouse 82%, Rat 86%, Snake 98%, Fox 100% (Fox/Snake are required). Fix: cheaper Glow/Silk, rework Carry. Win-link figures in playtest.json are confounded (tricks are used in trouble).
5. **Medium: grindy opening.** Layouts with no Moth/Mouse in the doorway force Shoves (36% outline, 91% lookahead). Fix: free peek or one starting Ready trophy.
6. **Low: length.** Competent play is 8.3 min (-17%, inside band). Human deliberation is not modelled.

## Rule ambiguities
- "You know where the Hound is": simulated as true only when the setup swap moved it.
- A Ghost must still be fought to gain its trophy (design note calls it free).
- Scavenge readying a trick already used this turn: still once per turn.
- Hound lit by a Shove is hunted in the same turn.
- Outline steps 5 and 6 are unclear on whether the new trophy counts as Ready.
- Run-length claim "within 20 turns" holds (max 14 observed).

## How it felt (one narrated run, seed 77)
Doorway Rat, Spider, Crow, Hound known at bottom-right: nothing safe at Claws 2. I Shoved the Crow (so Thief stays dark), got the Fox up, Shoved it, got the Moth: three turns without a Fight, a puzzle but a slow start. Fighting the Moth then the Spider felt good, but the Spider lit the Crow and Thief took my Moth: a real "oh no" moment. The outline bot then ping-ponged the Snake and Hound and died on turn 9, which showed that a bad shove target is fatal. No downtime (solo). The first turns feel like pure hidden-card luck.

## What simulation cannot test
Fun, freshness over many sessions, whether deaths feel fair, human memory/deduction burden, handling of sideways cards, real deliberation time, whether the Ghost story motivates a second run. Human playtests are needed. Carry-over was tested with bots only.

## Panel scoring (weak for a solo game)
Persona bots ran alone, 300-1,000 runs each. Interaction and downtime are 0 and lead changes/comebacks are proxies, so scores are biased low and are weak evidence. Average fun 2.69 (best fit competitor 3.69, worst fit family 1.74). Competitor and Bar Raiser bots use the lookahead bot (72% and 88% win rate); the other four win 10-18%.
