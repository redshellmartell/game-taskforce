# Duel Flip playtest report, revision 3

**Verdict: PASS (with one known KPI miss, runaway leader 74%, which the designer accepted and the Director asked me only to report).**
Sim: 72,000 games (2,000 per bot pairing, fixed seeds) plus 4 leave-strategy matchups of 2,000 games. No extra configurations used; the 1.5x fallback was not needed.

| Check | Result | Target |
|---|---|---|
| Leave-lowest vs smart leaver | 44.7% (smart wins 55.3%) | under 60% - met |
| Leave-highest vs smart leaver | 46.5% | under 60% - met, not dominant |
| Leave-lowest vs leave-highest | 51.0% | no free gift - met |
| Non-lowest card left by smart leaver | 27.9% of choices (highest card 26.0%) | 25%+ - met |
| Bait claim rate by value 1-10 | 1.00 1.00 .99 .99 .97 .91 .78 .65 .39 .17 (8-10 baits: 65/39/17%) | well below 99% - met |
| Seat gap (worst mirror) | 2.0 pts (strategic mirror 52.0% seat 1) | 5 or less - met |
| Strategic vs random | 73.7% vs 35.6% avg win rate, gap 38.1 pts (greedy 58.8) | 20+ - met |
| Length | 21.9 turns, sd 1.6 (16-27), about 12 min | brief 10-15 min - met |
| Ties / turn cap | 0.15% (full score ties 0.40%) / 0 caps | fine |
| Lead changes | 2.80 per game | 2+ - met |
| Runaway leader | halfway leader wins 74.0%, one-third leader 68.5% | 65% or less - MISSED (known, unchanged from 74.8%) |
| Dead cards / components | none; Lifebuoy used 2.0 per game (every one), 1.9 failed claims per game | zero - met |
| Ambiguities | 0 found | zero - met |

## Problems
1. **Medium: runaway leader 74.0%.** Scoring accumulates and busts are small (average bust pile 6.7). Not touched this revision. Untested ideas: shrink a trailing player's bust loss, or let the trailing player claim at 1.5x.
2. **Low: leave choice is worth only a few points.** The smart leaver beats leave-lowest by 10.6 points and leave-highest by 7 points per head-to-head (55.3% and 53.5%). It matters now (it was a 5% deviation and about 0 gain in rev 2), but it is a modest skill edge.
3. **Low: bot limits.** The strategic bot is a one-step lookahead, so it under-plans pushes to 18-20. Humans may reach 9-10 baits more often, which would favour leave-lowest again. The 1.5x (rounded up) knob is ready if leave-highest later grows too strong.

## Rule ambiguities
None found. Interpretations used: a failed claim with a one-card pile takes the card and leaves no bait (as written); bots decide the flip count before knowing the claim result; a bait clash with a ready Lifebuoy is allowed, then the claim test runs on the pile.

## How it felt (one simulated narrated game, seed 7, strategic vs strategic)
Early turns are safe and routine (claims 11-16 pile against 1-6 baits). Fun moment: turn 10, a player left a 10 bait, the rival pushed to 16 and fell short; the 10 went back and they banked a full pile. Turn 4 and 8 busts hand over 2 to 4 cards at once, which swings the game. Boring: low baits are claimed automatically, so the first half is mostly "flip twice, bank". Late game has a bust streak of four in a row on turns 15-20, tense but a little chaotic. Downtime is low (all information public, short turns).

## What simulation cannot test
Whether people enjoy the hurdle arithmetic (2x a bait), whether a trailing player feels out of the game (the 74% number says they often are), whether humans read the "no new bait" clause as fair, true skill ceilings beyond one-step bots, and how it feels to play.

## Panel (free bots)
Average predicted fun 3.60, spread 1.67; best fit competitor, worst fit family. Details in panel.json.
