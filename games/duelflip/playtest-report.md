# Duel Flip playtest report - revision 2

**Verdict: NEEDS-FIXES.** Seat balance, skill, length and lead changes pass. The headline change (the bait hurdle) does not work, because the bait is claimed 99% of the time. Runaway leader is over the KPI.

Sim: `sim/` (game.py, bots.py, run.py, panel_run.py). 72,000 headline games (2,000 per pairing, 6 bots, alternating seats), plus 5 experiments.

| KPI | Target | Result | Status |
|---|---|---|---|
| Seat gap (worst mirror) | <= 5 pts | 1.2 (strategic mirror seat 1 wins 51.2%) | pass |
| Strategic vs random | >= 20 pts | 44.3 (strategic 72.8%, random 28.4%, greedy 60.9%) | pass |
| Length | 12.5 min +-20% | 23.2 turns (sd 1.6, range 17-28), about 12 min | pass |
| Runaway leader | <= 65% | 74.8% (halfway leader), 68.6% (one-third leader) | FAIL |
| Lead changes | >= 2 | 3.4 | pass |
| Ties / caps | - | 0.65% full score+card ties (shared win), 0 caps | ok |
| Leave-lowest vs smart leaver | < 60% | 50.1% | met, but see problem 1 |
| Leave-highest dominant? | not > 60% | 20.9% against smart; lowest beats highest 80.8% | not dominant |
| Dead cards / ambiguities | 0 | no dead values; no rule gaps found | pass on the letter (inert hurdle, see below) |

## Experiments (5 of 5 used)
1. Leave-lowest vs smart: 50.1%.
2. Leave-highest vs smart: 20.9%.
3. Leave-lowest vs leave-highest: 80.8%.
4. Random leave vs smart: 34.5%.
5. Hurdle variant (claim only if pile > bait + 3): low vs smart 49.3%, high vs smart 31.8%, claim rate still 98%, runaway 72.7%. Script: `sim/experiments/hurdle.py`.

## Problems, ranked
1. **High: the bait hurdle is inert.** The bait is claimed on 99% of tries (value 1-5: 100%, 9: 95%, 10: 89%). A bot that knows the hurdle just flips until its pile beats the bait, and the Lifebuoy covers the clash. The smart leaver (Monte Carlo of the opponent's claim chance) picks a card other than the lowest in only 5% of choices and gains about 0 points. So "leave lowest" is still the answer about 19 times in 20. The 60% target is met only because no alternative beats it. Not dominant in the leave-highest sense, but the bait decision is still not a real choice. Fix: make the hurdle bind (claim needs pile >= 2x bait, or a failed claimer also pays a card from their pile). A flat +3 is not enough (experiment 5).
2. **Medium: runaway leader.** 74.8% at halfway. Scoring only accumulates and busts are small (average pile 5.9). Fix: a catch-up rule, or accept and document.
3. **Low: leave-highest is a trap** (20.9%). It would resolve with fix 1.
4. **Low: busts.** 4.3 per game (1.8 on the bait). Fine; the Lifebuoy is spent every game (2.0 per game).

## Interpretations (none are rule gaps)
rules.md revision 2 was unambiguous in every case I hit: bait at game end goes to its owner; scout running dry ends the game with the bait going to its owner; Lifebuoy on a bait clash keeps the bait for the claim test; a one-card pile takes the card and leaves no bait. The tiebreak is +3, then cards, then shared win (counted as half a win). Zero ambiguities found.

## How it felt (simulated trace, one game, strategic vs strategic)
Turn 0 the first player flipped 6 cards for 29 points: exciting but nothing stopped it, because the river was empty and there was no bait. Turns 1-3 felt like a routine: flip two or three, take the bait because the pile always beats it, leave a 1 or 2. Turns 4-7 was a run of four busts in a row (1, 2, 1 and 1 cards): fun for the player who gets the cards, flat for the one who busts, with almost no decision. The leave choice had nothing to think about. Downtime is short; turns take 20-30 seconds.

## Panel (free bots, panel.json refreshed)
Predicted fun: competitor 4.02, strategist 3.91, barraiser 3.66, casual 3.60, story 3.36, family 3.14. Best fit competitor; worst fit family. Barraiser veto not active (numbers only; the veto-by-dominant-strategy flag is based on the flagged cards).

Untested suggestions: claim at pile >= 2x bait; failed claimer pays a pile card; bust pile counts half for the trailing player; second-player bonus +2.
