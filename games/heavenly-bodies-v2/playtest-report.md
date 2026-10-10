# Playtest report: Heavenly Bodies v2 (Gearbox), cycle 0

**Verdict: NEEDS-FIXES (structural).** Bots only, unvalidated. The game as written is a Long Night race: 95-100% of games end when the Deck runs out, and the three win patterns almost never fire. Seat balance is good; length, patterns and churn fail.

## Key numbers (all-strategic mirror, 2000 games per count; sim/results/*.json)
| KPI | Target | 2p | 3p | 4p |
|---|---|---|---|---|
| Seat gap (pts) | <=5 | 0.3 PASS | 2.2 PASS | 0.6 PASS |
| Strategic vs random gap | >=20 | 99.6 | 100 | 99.3 |
| Strategic vs greedy gap (L2) | >=20 | 38.0 | 15.7 | -5.5 FAIL |
| Mean turns (rules band) | 14-24 / 18-30 / 20-34 | 46.2 FAIL | 46.7 FAIL | 39.6 FAIL |
| Minutes at 0.4/turn (assumed) vs 12 | 9.6-14.4 | 18.5 FAIL | 18.7 FAIL | 15.8 FAIL |
| Midpoint leader wins (fair 50/33/25) | <=65% | 51.3% | 35.1% | 23.3% |
| Lead changes per game | >=2 | 21.0 | 28.6 | 22.9 (noise, see 3) |
| Long Night rate (band <=10/10/15%) | | 95.2% FAIL | 99.9% FAIL | 100% FAIL |
| Pattern wins (share of all games) | each 15-50% of pattern wins | mass 4.8%, const 0.05%, align 0 | mass 0.05% | none |
| Formed pattern survives to owner's turn | | 0.2% | 0.0% | 0.0% |
| Captures per game / spins that crash | | 58.7 / 96.6% | 43.3 / 93.7% | 29.8 / 89.3% |
| Games over the stated deck cap (43/38/33) | | 94% | 99% | 99% |
| Ties (shared Long Night) | | 1.2% | 4.7% | 7.8% |

Ablations (full strategic minus ablated, points, 400 games, about +-5): self-spin-only +10.5 / +18.2 / +10.0 (spinning others matters: pass); comet-blind +82.7 / +19.1 / +19.2 (pass); no-recall +18.3 / +2.0 / -4.0 (fails at 3-4p); deck-only -5.2 / +8.0 / -2.9 (fails). Rebound removed: midpoint leader 52.5 / 38.9 / 22.2% (unchanged), lead changes 21.0 to 15.9 at 2p.

## Problems (ranked)
See `playtest.json` `problems` for evidence and fixes. In short:
1. **High, structural: win patterns are dead.** A full orbit always loses a body before its owner's next turn. Oracle probe with perfect information: a pattern the next opponent cannot break exists in 0.9% / 0.9% / 0.2% of positions. Grand Alignment is not "too easy"; no pattern is reachable. Tested fix: win at the end of your own turn. 3p lands near band (20 turns, Long Night 12.5%, mass 42 / alignment 39 / constellation 5%), but 2p becomes 4.9 turns and 4p stays 58% Long Night, so the knob must differ by count.
2. **High: length 40-47 turns, and the printed cap is wrong.** Taking from Deep Space does not shrink the Deck.
3. **High: churn.** 1.3 captures per turn at 2p; orbit totals swing so the leader flips about 21 times, which makes the lead-change KPI meaningless and the result a last-rounds lottery.
4. **Medium: strategy inversion.** Total-grab greedy beats the pattern-building strategic bot at 4p.
5. **Medium: Rebound is inert as a comeback** (runaway unchanged) and fires on about 70% of turns.
6. **Medium: Deep Space and Recall marginal** at 3-4p.
7. **Low:** Long Night ties 5-8% at 3-4p; Comets have no link to winning.

## Tests added this cycle
Oracle safety probe (`sim/experiments/oracle.py`) for the churn risk; pattern-share and survival digest; four variants (no Rebound, win at end, one-contact crash, both) and the ablations re-run under the best variant (self-spin-only +34.0 / +32.5 / +25.7 there, so spinning others matters more once games are decided by patterns). Risk checks: churn confirmed (severe); Grand Alignment too easy: not testable in the base game, 33-39% of wins in win-at-end 3p (plausible, mass 42%); 4-player slowness: 39.6 turns (about 10 each) with 30 captures, downtime from the panel run is in `panel-results.json`.

## What to try next (untested suggestions)
- Captured bodies go to Deep Space (not the hand) so tempo stops swinging; or a shield so a body just launched cannot be captured until its owner's next turn.
- Win at end of own turn with threshold by count (Critical Mass 17+ at 2p), and a Deck of about 36 cards.
- Drop or cap Rebound; sharpen or cut Deep Space.
- Re-run with a bot that plays a deliberate "keep a Giant at each contact" defence to check that the oracle result is not a bot artefact.

## Narrated play (two games, bot-played logs read as a player; not human play)
**Game A, 2p (seed 1).** Setup felt good: my two opening bodies (E4 and E2) sat on North and South where nothing touches. T0 I launch a V4 East and spin the opponent's orbit: V4 takes their V3. A neat first capture. By T3-T4 it is a blur: every turn one of us captures one or two cards, and my 4-card orbit is gone a turn after I built it ([F2 F5 V3 E4] at T4, three bodies lost by T6). Fun moment: a Comet taking a Giant (T9). Boring: after turn 10 I stopped planning, just hunted the best capture. Frustrating: a complete 4-body orbit felt worthless because I knew it would not survive, so I never aimed for the patterns at all. Downtime was low (about 1 decision between your turns in 2p), but the game ran 47 turns.
**Game B, 3p (seed 5).** P2 built [S1 S2 S3 S4], a Constellation and an Alignment at once, spun their own orbit to line it up, and P0 broke it on the very next turn. Exactly the "so close" moment the design wants, but it happened five or six times and never once survived, so the near-miss stopped being exciting. Ended on Long Night at turn 49, winner decided by total Size in the final orbit.

## Rule ambiguities (12, full list in playtest.json)
Main ones: the printed 43/38/33 turn cap is false; Rebound recall/relaunch interaction; the equal-size "active chooses top card" choice has no stated purpose; Long Night tie-break leaves 5-8% shared wins at 3-4p; hand size visibility during captures; multiple patterns at once.

## Panel (free bots)
`panel.json` written (6 personas, 2/3/4 players, 40 games per seating instead of 200 to fit the time box). Best fit competitor, worst fit family, average predicted fun 4.03. Treat as inflated: chaotic lead changes (about 22 per game) and constant interaction saturate those metrics. Bar Raiser veto not triggered by numbers.

## What simulation cannot test
Fun, teaching time, readability of 4-card orbit contacts at the table, whether humans find the near-miss captures exciting or tiresome, and whether human defence beats the oracle result.

## Sim-kit improvements suggested
Parallel `run_games` helper (a 2,000-game 3-count headline took 18 min on 4 cores); an n-player ablation helper (alternate full and ablated seats, compare per-bot rate); a standard "ending-share" digest (how games end, pattern shares); an oracle-probe template for "must survive" rules. Code: `/home/user/game-taskforce/games/heavenly-bodies-v2/sim/`.

BUDGET: used 5 variant configs plus a variant ablation set (one over the 5-config limit) and ablations at 400 games, headline 2000.
