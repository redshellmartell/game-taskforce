# Playtest report: Last Bid Standing (revision 0)

**Verdict: NEEDS-FIXES.** Mechanically sound (no crashes, 14 rounds always, fair seats, good lead changes), but decisions barely separate good from random play, Hype swamps printed values, and a quarter of lots go unsold when bots play carefully.

## Key numbers (24,000 headline games: 2,000 per table type at 5 and 6 players; 10,000 experiment games)
| KPI | Target | Result | Status |
|---|---|---|---|
| Seat balance gap | <= 5 pts | 1.4 (6p all-strategic); 0.7 to 2.5 across all tables | pass |
| Strategic vs random gap | >= 20 pts | 17.5 mean for a lone strategic bot (20.7 at 5p, 14.3 at 6p). At a 50/50 mixed table only 0.8 (5p) and 2.3 (6p) | FAIL |
| Length | 16-24 min | about 16 min by my timing model (19.3 with the designer's 70 s/round); 14 turns always | edge of pass, untested with humans |
| Runaway leader (leader after round 7 wins) | <= 65% | 49% mean; 59-65% for the leader after round 11 | pass (late value at limit) |
| Lead changes | >= 2 | 2.98 mean (2.5 to 3.5) | pass |
| Dead cards | 0 | None fully dead; lot value 1 weak | pass, with a flag |
| Ambiguities | 0 | 7 listed in playtest.json | FAIL |
| Ties for first | low | 2.5% | ok |
| Turn-cap hits | 0 | 0 | pass |

Bots, pooled mixed tables (fair is 16.7-20): strategic 20.3%, random 18.4%, greedy (always plays highest card) 16.4%.

## The designer's flagged risks
- **Hype swamping lot values: confirmed.** Hype is 55% (5p) and 64% (6p) of all points after the crash. Lot value 1 correlates 0.13 with winning vs 0.27 for value 3.
- **Tied bids leaving lots unsold: confirmed.** 5.2 (5p) / 4.6 (6p) of 28 lots go unsold with mixed bots, 7.8 (6p) with all-strategic bots. About 10-16 bids per game are cancelled by ties.
- **Coin supply drying up: partly.** Mean hand is 1.6 cards; players have no card to bid in 22-23% of player-rounds. The "nobody draws" rule almost never fires (0 to 0.13 per game); the discard reshuffles 1-2 times a game. The real problem is empty hands, not an empty deck.
- **Last-round kingmaking: swingy.** The leader before round 14 loses 26% (5p) / 31% (6p) of games; the crash category changes in round 14 in 41% / 49%. I did not build a deliberate kingmaking bot, so spite play is untested.
- **Bubble:** each category crashes 34-39% of the time, so no category is a safe bet. Good.

## Problems (ranked)
1. **High: skill expression.** Lone strategic bot 28.6-36.6% vs random 14-16%, but three strategic bots vs three random only 17.8% vs 15.5% at 6p. Passive play loses: in the persona rotation the noisy casual bot (30% win) and the story bot (27%) beat the planner (15%), cautious (11%) and optimiser (17%). The best simple line (pass 5 rounds, then bid high) scores 26% at 6p against randoms, yet three bankers get 4 to 8% each, so any pattern stops working once copied. Fix: add leverage or information (for example a public count of Paddles passed, or two bid cards per round), then retest. E4 (bids 1-12) lifted the lone-strategic share to 33% at 6p.
2. **High: Hype swamps values.** Fix: raise printed values moderately (2-5), not +2 across the board (E1 cut Hype to 46-53% but unsold rose to 9.9 and forced passes to 34% at all-strategic).
3. **High: unsold lots and empty hands.** Fix: income 2 per pass (E2: unsold 7.8 to 6.4, forced passes 22% to 13%, last-round flips 29% to 19%, ties 2.2% to 1.2%, seat gap 0.4 to 1.8). Alternatively carry unsold lots over.
4. **Medium: last round decides too much** (see above). E2 and E5 (starting hand 5: flips 11% at 6p all-strategic) both reduce it.
5. **Medium: ambiguities** (see playtest.json): reshuffle timing mid-draw, "nobody draws" scope, tied top-Hype categories all crash (very swingy: if the top two tie, both crash), tiebreak order, which lot the second bidder gets.
6. **Low: length** near the low edge; real timing needs humans.

## Experiments (5 of 5 used; 6 players, 1,000 games each, one change at a time)
| Change | Hype share | Unsold (all-strat) | Forced pass | Last-round flip | Lone strategic share |
|---|---|---|---|---|---|
| Base | 61-66% | 7.8 | 22% | 29% | 28.6% |
| E1 lot values +2 | 46-53% | 9.9 | 34% | 24% | 26.2% |
| E2 income 2 | 66% | 6.4 | 13% | 19% | 29.5% |
| E3 halve (not zero) on crash | 68-72% | 7.7 | 21% | 23% | 28.7%, runaway 0.55/0.66 (worse) |
| E4 bids 1-12 | 60-66% | 6.9 | 17% | 26% | 33.2% |
| E5 start hand 5 | 63-67% | 8.0 | 19% | 11% | 26.8% |

Best single fix: E2. Untested suggestions: E2 plus lot values 2-5 together; bids 1-12 with income 2; carry-over of unsold lots; a deliberate kingmaking bot.

## Narrated play (one 6-player game, bots in four of the seats, read from the log)
Rounds 1 to 4 felt lively: five or six bids a round, ties cancelling a 9 and a 10 early, and the burned cards piling into Clocks (5 Hype by round 3). Round 4 onward the table thinned: hands ran down to 1 or 2 cards and the rounds shrank to three bids or fewer. Round 9 had one bid (an unwanted unsold lot) and rounds 11 and 13 had no bids at all, so two lots worth up to 4 were wasted: dead rounds, boring and a little frustrating. The seat-4 player led from round 3 and still won, but round 14 pushed Silver to a tie with Clocks at 8 Hype, so both crashed and the final standings shuffled: the dramatic moment of the game, but it came from a lucky tie, not from planning. No downtime at all, and the rules are short. I did not play a second game.

## Rule interpretations
Second bidder takes the other lot; lots come off a pre-shuffled deck two per round; draws resolve one passer at a time, reshuffling only when the deck is empty at the moment of the draw; tie for first place is shared only after both tiebreakers tie. The length figure uses my own timing model (25 s bid, 15 s reveal, 4 s per burned card, 6 s per lot, 3 min setup and scoring).

## What simulation cannot test
Reading opponents and bluffing (bots do not model psychology or table talk), human memory of what was burned, deliberate kingmaking, how the shared tie rule feels when your 10 is cancelled, real length, and whether the Paddle and Bid cards looking the same matters in play. Bots are simple; the "strategic" bot is my best effort, and a stronger human line may exist, so the skill gap may be understated.

## Panel (free bots only)
Average predicted fun 3.04 (spread 0.85). Best fit: competitor (3.57). Worst fit: story (2.72). Family and strategist and story would-buy "no". No Bar Raiser veto active (fun 3.29), but its numbers hit the "runaway/kingmaking" and "ambiguous rules" peeves. Files: sim/panel-results.json, sim/logs/, panel.json.
