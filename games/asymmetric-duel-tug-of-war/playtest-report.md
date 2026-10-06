# Playtest report: Tug of Crowns, revision 2 (rules v3)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** 20,000 headline games (2,000 per pairing x 9 pairings + mirrors), 2 reference bots of different strength (greedy, strategic) plus random and a stronger "plus" bot for ablations.

| KPI | Target | Rev 1 | Rev 2 | Result |
|---|---|---|---|---|
| Treasurer win, strategic mirror | 45-55 (gap <= 5) | 37.9 | 40.5 (44.0 on a second seed run) | FAIL (gap ~11-19) |
| Treasurer win, greedy mirror | gap <= 10 | 38.1 | 35.3 | FAIL |
| Treasurer win, random mirror | gap <= 10 | 57.8 | 60.2 | FAIL |
| Seat gap, 3-mirror average (2x deviation) | <= 5 / <= 10 | 10.9 | 9.3 | hides cancellation (+20, -29, -19) |
| Games over by round 3 | < 20% | 31% | 18.5% all pairings (14.8% strategic mirror) | PASS |
| Lead changes | >= 2 | 1.83 | 2.22 (strategic 2.5) | PASS |
| Runaway leader (R2 leader wins) | <= 65% | n/a | 44.1% | PASS |
| Skill gap strategic vs random | >= 20 | 56 | 45.4 (strategic beats greedy only 62%) | PASS |
| Length | 15 min +-20% | 12.7 | 13.1 (5.7 rounds) | PASS |
| Turn cap hits / ties | 0 | 0 | 0 / 2.8% 0-0 rounds | PASS |

Treasury cap sensitivity (mirror Treasurer win, random/greedy/strategic/plus): cap 2 = 57/35/41/42, cap 3 = 57/36/42/43. The "one knob" moves nothing. Other single levers: Whisper 5->4 = 62/35/46/43; Gold Purse 5 = 63/34/42/43.
Court draws off: strategic lead changes 2.63 vs 2.54 on (+0.09, needs +0.3); greedy +0.57, random +0.57.

Ablations (bot without the feature vs full "plus" bot, same side; must lose >= 5): never-Spend -0.1 FAIL; ignore-Steady -0.9 FAIL; no-Echo-throw -3.1 (does better) FAIL; random Hush target 3.1 FAIL; never-Retort 1.9 FAIL. All five keywords are weak or inert for bots.

Dead cards: none unplayed. Outliers: The Whisper (+20 pts, played 81%), Chancellor's Seal (+23, 77%). Ambiguities hit in the sim: none new (v3 wording was enough); interpretation notes unchanged (step counting from T1, 0-0 ties).

## Problems (ranked)
1. HIGH: side gap not fixed; flips with skill (Treasurer 60% random, 35% greedy, 40-44% strategic). See `playtest.json` for levers tried; Whisper 4 is the best single one (+4) but not enough alone.
2. HIGH: Spend, Steady, Echo inert; Hush, Retort under 5 points. The twist keywords do not carry decisions.
3. MEDIUM: the court draws do not create lead changes for skilled play; the track shape does. Comeback is real (R2 leader wins 44%) but not from the advertised mechanism.
4. MEDIUM: feast-famine rounds (round 1 empties hands, rounds 2-4 decided by 1-2 points).
5. LOW: outliers Whisper/Seal.

## Narrated play (one logged game, plus vs plus)
Round 1 was a 6-card dump on both sides (T 20, W 16): exciting auction, the Whisper hushing my Patron felt good. Then rounds 2-4 were flat: one Gossip against nothing, crown shifting by a point. I stopped caring about each round until round 5, when Whisperer played 3 cards for a double step. Retort never came up; the Treasurer had no meaningful Spend choice (Vault for 1). Downtime low, decisions mostly "play or pass".

## Cannot be tested by simulation
Fun, readability, teaching time, whether Retort bluffing feels clever, how abrupt short games feel. The ablation bots are my heuristics; a human may use the keywords better. Bots only, unvalidated.

Panel: average fun 3.51 (best competitor 4.08, worst casual 3.05); Bar Raiser veto active (seat advantage 9.3).
Untested suggestions: fewer Hush cards; Hush cannot target the highest card; Spend +3 per coin; hand limit; side-swap two-game format.
