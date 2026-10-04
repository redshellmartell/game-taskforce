# Critique: Last Bid Standing (revision 0)

**Verdict: REVISE-MAJOR**

| Area | Score |
|---|---|
| Originality | 3 |
| Rules clarity | 3 |
| Fun | 2 |
| Balance | 2 |
| Market fit | 3 |
| Production | 5 |
| **Average** | **3.0** (target 3.5 at pitch) |

## Originality (3)
Searches (2 of 5 used, no pages read) found no game with the same combination. The nearest mechanics are separate:
- Burnout/Pairs (Crab Fragment Labs): tied bids and the target card are discarded, and the loser's bid goes to a reserve pile. This is the closest to the tie-cancel rule.
- Modern Art: hidden simultaneous bidding. QE: tied top bidders rebid.
- Speculation: collections that can turn out worthless.

"Ties cancel" is a known device. The new part is "losing bids become Hype, and the hottest category crashes", and I found no direct precedent for it. Similarity is low to medium. There is no copied text or rules, so no KILL on this ground. The idea is genuinely distinctive, but it is only one hook.

## Rules clarity (3)
The rules are short and well organised, and the example is good. A new player could learn the flow from them. The problems are:
- The Hype rule has a second layer that is hard to see on first read. The Hype goes to the category on the Bid card, not on the lot.
- If the top categories tie, all of them crash. This is written down but very swingy. The playtest says it decides games.
- The reshuffle happens mid-draw, so the order in which passers draw changes what they get. Seat order is claimed not to matter, so this contradicts the design.
- The "nobody draws" scope is ambiguous, and so is "second bidder gets the other lot" if the first bidder is the only one standing.
- The Paddle and Bid cards share a card back. This is a useless complication, because a hand count is already public.
- The brief asked for zero ambiguities and the playtest lists 7, so that KPI fails.

## Fun (2)
- Rounds 1-4 sound lively.
- After that, hands shrink to 1-2 cards. Players have no card to bid in 22-23% of player-rounds.
- Rounds 9, 11 and 13 had 0-1 bids, so two lots worth up to 4 went unsold. These are dead rounds.
- 4.6-7.8 of 28 lots go unsold. 10-16 bids per game are cancelled by ties.
- The big moment in the narrated game was a lucky tie that crashed two categories at once. That is not a good ending.
- The leader before round 14 loses 26-31% of the time, and the crash category flips in round 14 in 41-49% of games.
- Hype is 55-64% of points. Hype comes from losing, so the central decisions feel like noise.
- Panel fun is 3.04, and family, strategist and story would not buy. The Bar Raiser did not veto (fun 3.29), but it flags runaway/kingmaking and ambiguity peeves.

## Balance (2)
Seat balance is fine (gap 1.4). Lead changes (2.98) and runaway leader rate (49%) pass. But:
- The strategic-vs-random gap is 17.5 against a target of 20. That figure only comes from a lone strategic bot at a table of randoms. At mixed 50/50 tables the gap collapses to 0.8 (5p) and 2.3 (6p).
- The casual bot (30% win) and the story bot (27%) beat the planner (15%) and the optimiser (17%). This is the most serious finding: careful play does not win.
- The "pass then bid high" exploit stops working once copied (3 bankers get 4-8% each).
- Hype swamps lot values (55-64% of points), and lot value 1 is weak.
- Skill barely matters, so this is a structural problem and not a tuning issue. The best single fix, E2 (income 2), moved the lone-strategic share only from 28.6% to 29.5%.

## Market fit (3)
The game still matches the brief: 5-6 players, simultaneous play, no downtime, 74 cards, 20 minutes. Length is unproven. The playtest estimate is 16 minutes by its own model, or 19.3 minutes at the designer's 70 s per round. Nothing has drifted. But a game where the planner loses to the casual player will not serve the "strategist" audience, and family and story players also decline. That leaves competitor (3.57) as the only fit.

## Production (5)
74 cards, no board and no tokens, which fits the owner's focus. The cost is roughly $15 for a prototype. Nothing is hard to make.

## Biggest strength
A distinctive, rules-light hook: sunk bids feed a category's value, and the hottest category crashes. It is clear, cheap and new in combination.

## Biggest weakness
Decisions do not separate good play from random play. The mixed-table gap is 0.8-2.3 points, and the planner bot loses to the casual bot.

## Required changes
1. **Make skill matter.** KPI: strategic-vs-random gap at mixed tables (now 0.8-2.3 points). Target 20+ for the lone-bot measure and at least 8-10 at mixed tables.
   - Put E2, bids 1-12 and a public information element together. Options are a visible tally of Paddles passed, or a choice of two bid cards per round.
   - Retest as a combination, since single changes moved little.
2. **Rebalance Hype against printed values.** KPI: Hype share of points of 45-50% (now 55-64%), with unsold lots no higher than 6.
   - Raise lot values to 2-5, together with E2.
   - Retest unsold lots at the same time.
3. **Fix dead rounds and empty hands.** KPI: forced passes at or below 13% (now 22%), and unsold lots of 5 or fewer per game (now 4.6-7.8). Adopt income 2 per pass and test carrying unsold lots over to the next round.
4. **Remove the swingy end.** KPI: last-round winner flips at or below 20% (now 26-31%).
   - Replace "all tied top categories crash" with a deterministic single crash, for example the tied category with the lowest total printed value in play.
   - Consider revealing the Hype count publicly each round, which is already implied, and stating that clearly.
5. **Clear all 7 ambiguities.** KPI: ambiguities at zero.
   - Fix reshuffle timing so seat order cannot matter (reshuffle before drawing).
   - Define the scope of "nobody draws" in one sentence.
   - Drop the identical card backs for Paddle and Bid, or justify them with a real purpose.
   - Add the tiebreak order.
6. **Re-run with a kingmaking/spite bot** to test the last-round swing and the saboteur strategy the design notes rely on.

## Is another revision worth it?
**Yes, but only one, with a hard stop.** The hook is worth keeping and the fixes are concrete. The skill gap is structural, so require that the mixed-table gap improves clearly in the next playtest. If it stays under about 5 points, kill the game.

This is a first pass and every playtester suggestion is untested in combination. The mixed-table result is the number to watch.
