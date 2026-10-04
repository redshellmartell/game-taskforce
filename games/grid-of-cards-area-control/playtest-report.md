# Playtest report: Nine Fields (rules v1, revision 0)

**Verdict: NEEDS-FIXES.** Seat balance, skill and length are fine at 3-4 players. At 2 players the game mostly ends on the stall limit, not the deck, and fails two KPIs (lead changes, runaway leader).

Method: Python sim in `sim/` (game.py, bots.py, run.py, panel_run.py). 2,000 games per set, fixed seeds, 28,000 headline games plus experiments. The brief gives 2-4 players with no single main count, so I treated 3 as the headline and report 2 and 4 too. Seat rates come from strategic-bot mirror games.

## Key numbers

| Players | Seat win rates (gap to fair) | Strategic-vs-random gap | Floods per game | Turns (sd) / est. minutes | Lead changes | Early leader wins | Score ties | Ended by stall limit |
|---|---|---|---|---|---|---|---|---|
| 2 | 48.7 / 51.2 (1.3) | 97.3 | 14.5 of 22 | 41.8 (17.6) / 16.8 | 1.77 (KPI fail) | 68.7% (KPI fail) | 7.5% | 58% |
| 3 | 31.9 / 32.9 / 35.2 (1.9) | 59.6 | 21.4 | 54.2 (8.5) / 22.2 | 3.37 | 53.6% | 11.4% | 5% |
| 4 | 22.2 / 24.4 / 25.2 / 28.2 (3.2) | 37.9 | 22.0 | 55.3 (5.4) / 22.6 | 3.69 | 43.2% | 17.4% | 0% |

- Turn cap (600) hits: 0. Greedy and random mirrors are also within 5 points at every count except 3p greedy seat 1 at 28.1% (about 5 points under fair; greedy-only).
- Length against 20 min: 3p +11%, 4p +13%, 2p -16%. All inside the 20% band, but the minutes rest on an assumed pace (15 s per turn, 20 s per flood, 90 s setup).
- Skill: strategic beats greedy 83% at 2p and greedy beats random 94%. A 2-ply bot beats the 1-ply strategic 68% at 2p (depth is rewarded).
- Actions: Land 34% / 49% / 62% of actions at 2 / 3 / 4 players (rest is Sail), so both actions are used.
- Island classes (3p claimer win-rate vs fair): v1 cap2 -4.5, v2 cap2 +1.6, v2 cap3 +1.7, v3 cap3 +8.5, v3 cap4 +6.7, v4 cap4 +13.4. No dead or dominant card class.

## Experiments (4 experiments, 6 runs)

1. Staller (avoids every flood when ahead) vs strategic: loses (42.9% at 2p, 28.6% vs 35.7% at 3p). No stalling exploit, but it pushed 2p stall-ends to 73%.
2. 2p stall limit 6 x players: stall-end falls to 37%, length 51 turns (sd 15.4), lead changes 2.16, but runaway stays 69.4%. Not a fix on its own.
3. 2-ply vs 1-ply: 67.7% at 2p. At 3p the 2-ply bot (41.3%) is level with greedy (40.3%) and 1-ply gets 18.4%.
4. Expert (barraiser bot) vs strategic at 2p: 68.0%; 88% of those games end on the stall limit.

Untested suggestions: a "storm" flood on stall instead of ending; a neutral last tiebreak; fewer islands dealt (18) if humans run long.

## Problems, ranked

1. **High: 2-player games end on the stall limit.** Only about 14.5 of 22 floods happen, so a third of the deck never appears and length swings (sd 17.6 turns). Lead changes 1.77 and early-leader wins 68.7% both miss KPI. The leader can sit back, and the trailing player cannot easily force a flood. Fix (untested): on a stall, a storm floods the fullest island and the next player picks the direction, so the deck always completes. Lengthening the limit alone does not fix it (experiment 2).
2. **Medium: ties and thin margins.** 7.5% / 11.4% / 17.4% of games tie on points; average winning margin is 4.5 / 3.0 / 2.2 pearls. Ties go to most trophy cards, then the later seat. Consider a neutral last tiebreak.
3. **Medium: length at 3-4 players is 22 minutes against a 20 target** (cap 25), on an assumed pace. Levers: deal 18 islands, or stall limit 2 x players.
4. **Low: depth barely helps at 3p against greedy** (experiment 3). Could be a bot limit; confirm with humans.
5. **Low: v1 cap2 islands are the weakest class, v4 the strongest.** Nothing is dead.

## Rule ambiguities found (resolve in rules.md)

- "Full" vs "floods": I read flood as the pawn count becoming equal to capacity; a full island can never be Landed on.
- Flooded island that itself falls off: no turn (it is gone). Rules imply this but never say it.
- Stall counter: I count passes and non-flood turns; opening pawns do not count. Rules do not say whether the game ends before or after the 3 x players-th turn is played.
- Final tide scores in reading order with pile sizes updated as each island is claimed, so order matters for the fewest-trophies tiebreak. Easy to miss.
- Two tied players with equal pile sizes: nobody claims, island removed. Rare but unspecified for the final tide.
- Hidden trophy values plus "count is public": bots needed an estimate; humans will have to bluff or guess. Not a rule problem, but the table talk rule ("no asking") is untestable in a sim.
- The flooded island stays full after turning. Crown Island (card 29) was seen to flood three times in 6 turns in the narrated game, because pawns return to the supply and are re-Landed on a still-full-minus-one island. Not a bug, but worth a rules example.

## Narrated play (one 3-player game stepped through from the sim log, reasoning as a player; 20 turns)

Opening: I (seat 1, placed last) took the centre. The first four turns were calm Landing. Turn 4 was the first real decision: Landing on the 3-capacity island floods, and I had to choose which end falls. Working out which line moves from the card's axis, then which end falls, is the step a new player will stumble on (reasoned from the log, not played at a table). Fun moment: turn 8, a value-4 island dropped to seat 2 on a flood they triggered by Landing, a clear swing. Boring: turns 12 to 19 in this game were Sail-shuffling between cells 3 and 6 with no flood, until the stall limit ended it at 20 turns with four floods, scores 8-7-9. That was the 2p problem showing up at 3p as well: nobody wanted to be the one to trigger. Frustrating: the final tide gave the winner about half their points, so the middle game barely mattered. Downtime was low: one decision a turn, rarely two.

## Panel

50 tables (15 at 2p, 20 at 3p, 15 at 4p), seats rotated, 200 games per seating, 16,000 games per persona, no filler bots. Average predicted fun 3.82. Best fit: competitor 4.52 (strategist 4.09, barraiser 4.17). Worst fit: family 3.11 (story 3.43, casual 3.61). **Bar Raiser veto: not active** (fun 4.17; seat gap, originality and dominant-strategy limits not crossed). Casual, family and story bots win only 6-15% of games because their noisy play loses to the planners, which says depth is rewarded but also that mixed tables are hard on casual players. Details in `panel.json`; sample logs in `sim/logs/`.
