# Dead Reckoning - Playtest report (revision 0)

**Verdict: NEEDS-FIXES.** The rules run cleanly and fit the length and seat targets, but the game fails two KPIs (runaway leader, lead changes) and one card (Sonar ping) does nothing measurable.

Code: `sim/` (game.py, bots.py, run.py, panel_run.py, finalize.py, experiments/exp.py). Runs are seeded and repeatable (checked by running the headline twice with identical output).

## Key numbers (12,000 games: 6 bot pairings x 2,000, seats alternated)
| Measure | Result | Target | Status |
|---|---|---|---|
| Seat 1 win rate (3 mirror pairings) | 49.3% (gap 1.4 pts) | gap <= 5 | OK |
| Strategic vs random | 87.5% (gap 75 pts) | >= 20 | OK |
| Strategic vs greedy / greedy vs random | 71.8% / 84.8% | - | OK |
| Length | 9.6 rounds avg (sd ~0.9), est. 14.8 min | 15 +-20% | OK (assumes 85 s per round) |
| Ties | 0.4% (strategic games) | - | OK |
| Games that never end | 0. About 75% end at the round-10 cap with Salvage left | - | See problem 4 |
| Lead changes per game | 1.50 | >= 2 | FAIL |
| Runaway leader rate | 0.79 (mirror strategic 0.77) | <= 0.65 | FAIL |
| Dead cards | Sonar ping has no measurable value | 0 | FAIL |
| Rule ambiguities | 6 listed in playtest.json | 0 | FAIL (all minor) |

Per game (strategic games): 1.9 torpedo hits, 6.8 torpedoes fired, 3.4 mines triggered, 2.6 reefs found, 6.1 blocked moves, 0.5 collisions, 1.4 pings.

## Experiments (1,000 games each, A vs strategic)
| Config | A wins | Reading |
|---|---|---|
| E1 torpedo spammer | 47.8% | Not dominant |
| E2 harbour camper (home 3.6 of 10 rounds) | 52.3% | Not punished; within noise (+-3) |
| E3 strategic blind to cooling rows | 45.1% | Reading cooling info is worth only ~5 points |
| E4 strategic that never pings | 50.0% | Ping is worthless |
| E5 mirror, torpedo orthogonal only | seat 1 49.7% | Hits drop 1.9 to 1.1 per game; no balance effect |

## Problems (worst first)
1. **High - runaway leader and few lead changes.** 0.79 and 1.50 against targets of 0.65 and 2. First flips of face-down cards decide most games; the final score gap averages 7.4 of 24 points. Torpedo hits (the only comeback, 1.9 per game) are too rare. Fix ideas, one at a time: victim cannot be hit the round after a hit; fewer Mines or more 1-point Salvage so first flips swing less; a catch-up for the trailer beyond the ping order.
2. **Medium - Sonar ping is dead.** E4: never pinging wins 50.0%. Fix: reveal two steps, or replace with "peek at one face-down card".
3. **Medium - the simultaneous guessing is not where the skill is.** Route efficiency gives most of the skill (greedy beats random 85%). The blind bot loses only 55-45 to the reading bot, so the cooling row matters but modestly. Luck of the fog is the big noise. Humans may read much better than these bots.
4. **Medium - the round cap, not Salvage, ends about 75% of games.** The designer expected Salvage to run out in rounds 8-10. Length is fine, but a leader can coast.
5. **Low - Harbour camping and torpedo spam** are not dominant in these tests (E1, E2). Watch in human play.

## Ambiguities found
Listed in playtest.json (6): Sonar counting for lead/ping order; reef bounce clash wording; cooling of cancelled cards; same face-down target; tiebreak counting after thefts; ping priority. None changes a headline number.

## How it felt (one narrated game, from the sample log strategist-1, no live human)
Round 1 was a coin flip: Red entered three Salvage squares in three steps and led 6-0, while Blue's plan found nothing. Boring, since nothing either player did could change that. Round 2 felt good: Red pinged, I saw their step-1 card, and I used my own T plus a forced collision to take back 6 points in one round. That was the tense moment. Rounds 5-6 dulled: at 10-1 the trailer kept pinging into nothing and the leader walked away. Downtime was near zero (both plot at once). Confusing point: the ping cost (1 point) never felt worth it.

## What simulation cannot test
Bluffing feel and table talk; whether the 6 visible helm cards are readable at a glance or tiring to track; whether the plotting feels like clever reading or a coin flip; real timing (the 85 s per round figure is the designer's estimate, not measured); fun and frustration of getting bounced off a Reef or Mined. The panel numbers are bot-derived and reward the bots' high skill gap (75 pts), which flatters the game. Only a human test settles these.

## Panel (free bots)
15 tables x 400 games; average predicted fun 3.75, best fit competitor (4.45), worst fit family (2.91). No Bar Raiser veto triggered. Details in panel.json.

## Untested suggestions
Cap of 12 rounds; fewer Mines; Mine penalty variants; a deeper strategic bot to see whether more reading raises the skill gap.
