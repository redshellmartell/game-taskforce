# Playtest report: Fifty-Two Workshop (revision 0)

**Verdict: NEEDS-FIXES.** The core loop works and is well balanced across seats, but the solo mode is broken, the engine suits do not pay off as designed, and the rules contain an open no-progress loop.

Simulation: `sim/` (game.py, bots.py, run.py, panel_run.py). 46,000 headline games (2,000 per pairing or seating), 6 extra experiment configurations, 30,000 panel games. 0 turn-cap hits after one bot fix (see problem 3).

## Key numbers

| KPI | Target | Result | Status |
|---|---|---|---|
| Seat balance (max deviation, strategic mirrors) | <= 5 | 2p 4.0, 3p 3.9, 4p 3.3 (last seat favoured) | pass, trend |
| Strategic vs random (2p avg win) | gap >= 20 | 72.1 pts (74.9% v 2.8%) | pass |
| Strategic vs greedy (2p) | n/a | 53.1% | weak depth |
| Length vs target (est. minutes) | within 20% | 2p 11.1/12, 3p 14.5/16, 4p 16.6/20 (-17%), solo 6.0/15 | pass multi, FAIL solo |
| Turns (mean, sd) | | 2p 35.3 (3.3), 3p 46.5 (4.0), 4p 53.6 (4.1), solo 19.5 | |
| Runaway leader (halfway leader wins) | <= 65% | 2p 59.5%, 3p 42.6%, 4p 36.4% | pass |
| Lead changes per game | >= 2 | 2.03 / 2.31 / 2.08 | pass (on the floor) |
| Score ties / shared wins | | 6.2-13.4% score ties, about 1% shared wins | ok |
| Rush strategy (always build cheapest) | not dominant | wins 18% (2p v strategic), 11% (3p), 9% (4p) | pass |
| Solo win rate (22+) | about 50% for strategic | strategic 98.6%, greedy 98.4%, random 68.0% | FAIL |
| Dead cards | 0 | none dead (every card is also money); K-club built 4%, K-spade 7% | pass, see 2 |
| Ambiguities | 0 | 11 listed in playtest.json | FAIL |

Estimated minutes use the designer's 25 s per build and 10 s per Gather; not measured with humans.

## Problems, ranked

1. **HIGH, solo mode is not a game yet.** Random wins 68% at the 22-point line, strategic 98.6% (average score 30.4). Ladder titles Journeyman to Grandmaster are meaningless. Solo also lasts about 19.5 turns (about 6 estimated minutes) against a 15-minute target. Fix (untested): win line about 31+, and a harsher Rival (2 cards per turn, or highest 2); re-measure for about 50% strategic.
2. **MEDIUM, the engine does not pay.** Win correlation by suit: Spades -0.056 (K-spade -0.15), Clubs +0.031, Diamonds -0.013, Hearts +0.100. Spades are built 14% of the time, Clubs 11%, Diamonds 19%, Hearts 14%. Engine-heavy bots barely beat greedy (planner 55.6%, optimiser 57.6% v greedy, 2p), and in the panel rotation the Flavour bot (long mixed Heart trains) is the best persona bot (40.6% against 32-33% for Planner, Optimiser, Expert). "Engine first" is the pitch, but Hearts-in-a-long-train is the line that wins. Strategic beating greedy by only about 3-9 points means decisions beyond "most points now" are shallow (caveat: my heuristic bots are not optimal). Fix (untested, one at a time): Spade discount 4, or Spade worth 2 points; make Clubs pull 1 plus a 0-cost pull.
3. **MEDIUM, rules allow a no-progress loop.** Gather, then hand-limit discards return the same cards to the Bench; the Bench stays at 5, the deck never shrinks and the clock never strikes. Before I fixed the strategic bot (a full hand now forces a build), 8 of 2,000 two-player games hit the 600-turn cap. Humans will rarely do it, but the rules have no breaker. Fix: remove the leftmost Bench card whenever the Bench holds more than 5 at end of turn, or forbid Gathering with a full hand.
4. **LOW, last seat advantage.** 2p seat 2 wins 54.0%; 3p seat 3 37.2%; 4p seat 4 28.3%. Within the KPI, but it is consistent. If it grows after fixes, 4-card start for the last seats.
5. **LOW, 4-player length** is close to the lower bound (-17%). Consider a target of 10 cards, or confirm with a human game.
6. **LOW, lead changes are on the 2.0 floor** (2.03 at 2p). Recheck after fixing 2.

## Rule ambiguities (11, full list in playtest.json)
Main ones: clock strike timing when it happens before the last seat; deck-empty strike after the refill; Apprentice on a tie for fewest (read literally: no bonus); Club pulls cannot make an otherwise illegal build legal (legality uses the hand before the pulls); no stall breaker (problem 3); "provisional score" has no live score on the table (lead changes are my measure).

## What the panel bots say (free bots only, no AI reviews)
Average predicted fun 3.99 (competitor 4.67, strategist 4.45, barraiser 4.36, story 3.74, casual 3.53, family 3.22). Best fit: competitor; worst fit: family. Barraiser veto not active. Interaction is real but mild: about 0.3-0.5 turns in 1 take a card a rival paid. Downtime (opponent decisions between my turns) is about 5.9 at the mixed tables, driven by 4-player tables.

## How it felt (narrated, one simulated 2-player game, 40 turns)
Early turns are Gather-heavy: first 4 turns each had only one cheap build. Fun moment: P1 built 8-spade then 7-spade (cost 1) in a 7-8-9 train, then 10-club pulled the K-spade off the Bench. Chain turns feel good. Moment of frustration: P1 held KH, KS, and 9H in a full hand and had to dump 3C to the Bench, which P2 took, so the hand limit gives away info and cards. Boring stretch: turns 20-30 were largely forced; each player has one real decision per turn and many of them are "which of 5 cards". Downtime is low at 2p (about 2 decisions between turns) and grows with players. The finish was close (29 to 23) with the leader never changing after the middle. I did not play a second game.

## What simulation cannot test
Whether trains and the cost maths are readable at the table (I count 11 ambiguities, humans will find more); real turn times; whether payment-to-Bench interaction feels like play or bookkeeping; fun of the solo game; how people mix suits for Hearts in practice (my bots use fixed weights); whether kids can do the sum-to-cost payments quickly. Bots are heuristic, so "Strategic only matches greedy" may partly be a bot limit.

## Untested suggestions
Spade discount 4 or 2; Diamonds worth 2; hand limit 6 or 8; last-seat starting card; solo win line 31; Rival takes 2 per turn. Experiments used 6 configurations (rush at 2p, 3p, 4p; planner v greedy; optimiser v greedy; spade discount 2 seat check), one over the 5 allowed.
