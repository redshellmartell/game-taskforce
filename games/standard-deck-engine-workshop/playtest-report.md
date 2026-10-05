# Playtest report: Fifty-Two Workshop, revision 1

**Verdict: NEEDS-FIXES.** Multiplayer is sound (seats, length, runaway, no stalls). Solo still fails its main KPI, and the engine suit (Spades) still does not pay. 62,000 games in the headline run, plus 3 configurations (2,000 per pairing each) and one solo check. Bots: random, greedy, strategic, lookahead (reference bots of different strength), rush; 6 persona bots. Seeds fixed; code in `sim/`.

## Key numbers (v2 as written)
| KPI | Target | Result |
|---|---|---|
| Seat gap (2/3/4p) | <= 5 | 1.2 / 0.6 / 1.2 PASS |
| Strategic v random | >= 20 pts | 67.8 pts (99.9% 2p head to head) PASS |
| Strategic v greedy (2p) | >= 60% | 59.0% (lookahead v greedy 61.3%, lookahead v strategic 54.5%) MISS by 1 |
| Spade / Club win correlation | >= 0 | Spades -0.035 FAIL; Clubs +0.049 ok (Hearts +0.098, Diamonds -0.026) |
| Solo strategic / random win | 45-55% / < 15% | 98.8% / 0.6% FAIL (greedy 97.4%, lookahead 99.1%) |
| Solo length | designer 7-8 min | 23.8 turns (12 builds, 12 gathers), 7.5 min by formula |
| Turn-cap hits, bot patches | 0 | 0 in 62,000 games (and no patches), PASS |
| Lead changes (2/3/4p) | >= 2.5 | 2.10 / 2.49 / 2.32 MISS (4p) |
| Runaway leader (halfway) | <= 65% | 54.8 / 40.9 / 33.7% PASS |
| 4p length | 20 min +-20% | 57.2 turns, 17.7 min (-11.5%) PASS; 3p 14.8 v 16, 2p 11.3 v 12 |
| Ties | n/a | top-score ties 6.2 / 10.5 / 12.9%; shared wins < 1% |
| Dead cards | 0 | none; K/A Clubs built 5%, Kings 10% (money) |
| Ambiguities | 0 | 4 minor (see below) |

## Configurations tried (3 of 5 budget, plus a solo check)
| Config | Strat v greedy | Spade corr | Lead chg 4p | Solo strat / random |
|---|---|---|---|---|
| v2 as written | 59.0 | -0.035 | 2.32 | 98.8 / 0.6 |
| Retool off | 51.1 | -0.040 | 2.29 | 88.5 / 4.7 |
| Spade discount 3, 2 points | 61.2 | -0.015 | 2.61 | 99.3 / 1.5 |
| ... plus 3-card Gear Gather | 60.9 | -0.020 | 2.46 | 99.3 / 1.7 |
| Solo Rival takes 3 (solo only) | | | | strategic median 41 v 40: no change |

Retool is worth about 8 points of strategic-over-greedy skill and gives the lead-change lift; keep it. Spade correlation stays below 0 in every config, so it is not a numbers problem alone.

## Problems, ranked
1. **High, solo is a free win.** 98.8% at line 31; greedy is almost as good as strategic (median 38 v 40). Rival taking 3 cards does nothing. Fix: win line to about 40 (strategic about 52%, greedy about 40%, random about 0%), rescale the ladder, and add real solo pressure (Rival also takes Diamonds/Hearts, or a smaller solo hand limit); re-test.
2. **Medium, Spades do not pay** (-0.035; -0.015 even with 2 points). They are mostly spent as payment. Fix: Spade 3 + 2 points (+ Gear Gather) is the best of the three; if still below 0, accept Spades as the currency suit and drop "engine first is strongest". Bots do not plan trains, so a human test of the engine line is needed. The Story bot (long mixed trains, Hearts) still wins most in the panel (44%) v Strategist 34%, Competitor 33%, Barraiser 32%.
3. **Medium, skill gap vs greedy 59.0%** (1 point short); the Spade 3 / 2-point config passes on both strategic (61.2) and lookahead (63.5).
4. **Medium, 4p clock target 10 is vestigial:** 85% of 4p games end by the deck emptying (3p 2%, 2p 0%); Retool is used 0.4 times per game. Lead changes 2.32 at 4p. Fix: say "deck runs out" is the 4p end, or add deck pressure.
5. **Low:** 3-4p top-score ties 10-13% (tiebreakers fine); solo 7.5 min by formula vs designer 10 (check with a human).

## Rule ambiguities (4, minor)
Retool Spade cost when the replaced card is a Spade (simulated: only the new card counts); hand-limit scrap can hit cards just taken by Gears; solo "24th turn" v "pile holds 24" wording; deck-empty clock when a trimmed card re-fills the deck. The 11 old ones are closed; the sim ran with 0 illegal actions.

## How it felt (one 4p game, strategic bots, seed 42; 56 turns)
Opening was fast and clear (take two, pay a big card). Fun: the Bench flip, since every payment is public. Boring: Spades and Clubs were spent as payment immediately; no train longer than 3 appeared and no Retool happened; four players finished 18/18/17/18, a flat finish with no peak, and the game ended on an empty deck at 6-8 workshop cards, not at the printed target of 10. Frustrating: a 9-cost build burned a Queen because nothing cheaper fit. Downtime is low (about 5.6 opponent decisions between turns at 4p per the panel bot), turns take 1 decision.

## What simulation cannot test
Whether the Spade engine and Retool timing are fun or intuitive for humans (bots do not plan trains or bluff the clock); real time per action (25 s / 10 s are estimates, so 4p length and the solo 7-8 minutes need a stopwatch); table talk, rules teaching, the feel of the shared Bench, and solo satisfaction beyond win rate.

## Panel (free bots)
`panel.json` refreshed: average predicted fun 3.93; best fit Competitor (4.69), worst fit Family (2.96); Bar Raiser veto not active.
