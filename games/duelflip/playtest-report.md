# Duel Flip - Playtest Report

**Verdict: NEEDS-FIXES.** The game runs, always ends, and skill matters. But the setup is unfair (the second seat wins about 57%), the Lifebuoy count is the strongest lever in the game, and the "leave bait" twist collapses into "always leave the lowest card". The species bonus and unused-Lifebuoy points barely matter.

Code: `/home/user/game-taskforce/games/duelflip/sim/` (`game.py` rules, `bots.py` 7 bots, `run.py` round robin and mirrors, `experiments.py` and `fair.py` knob sweeps, `trace.py` move logs). All runs use fixed seeds. Run with `python3 run.py 2000`.

## Key numbers

Bots: random, greedy (flip to 12, leave lowest), bank_early (flip exactly 1 card), bank_early_bait, pusher (flip to a target), collector (2 flips, species-aware leave), strategic (EV flip rule, buoy threshold, bait/species-aware leave). n=1000-2000 games per measurement.

| Metric | Result |
|---|---|
| Strategic vs random | 95% win (beats every other bot too; average 84%) |
| Strategic vs greedy / pusher-12 / collector | 61% / 64% / 80% |
| First-seat win rate, mirrors, rules as written (1 buoy first, 2 second) | strategic 42-43%, greedy 44%, pusher 37%, random 45%. Second seat is about 7 points above fair (more for good players). Flagged (>5). |
| Same, both players 1 Lifebuoy | 51-55%. Within tolerance, a slight first-seat edge. |
| Game length (turns) | random 34 (24-46), greedy 26.5 (23-30), strategic 27.7 (19-39), pusher 20, bank_early 60 (always) |
| Ties | 0.5-0.8% (bank_early mirror 2.6%). Tiebreakers rarely matter. |
| Games that never end | 0 hits of the 500-turn cap |
| Busts per game | 5.6-8.6. About 9-12% of all turns are "dead turns": bust on the first flip, nobody gains anything. |
| Lead changes per game | 3-5 (bank_early 7.7) |
| Leader after the first third wins | 67-75%. Mild snowball, not a runaway. |

## Questions asked

**1. First-player advantage.** There is a real first-player edge. With equal Lifebuoys the first seat wins about 52-55%. The rule that gives seat 2 two Lifebuoys over-corrects. Seat 1 wins only 41-44%.

**2. Lifebuoy count is the biggest lever in the design.** First-seat win % in the strategic mirror by (first, second) Lifebuoy count:

| Lifebuoys | First seat wins |
|---|---|
| (0,0) | 55 |
| (1,1) | 55 |
| (2,2) | 55 |
| (3,3) | 55 |
| (1,2) as written | 43 |
| (2,3) | 46 |
| (1,3) | 35 |
| (0,2) | 31 |

- Each extra Lifebuoy is worth roughly 11-12 points of win rate, so the rule gap is huge compared with the real first-move edge of 5.
- Equal counts are fair for 0-3 each. A 1-point difference is far more than the first-move edge it is meant to offset.
- Nobody has an incentive to hoard them: see item 4.

**3. Species bonus.** The bonus is nearly irrelevant.
- Over 10-point-value cards, the bonus (5) flips the outcome in only about 4% of games. At 3 it flips 2.5%, at 7 it flips 4.8%, and at 0 it flips 0.1%.
- Players typically win about 2-3 species each, and about 0.7 are tied.
- Collector, the species-chasing bot, averages 61% in the round robin, but that is mainly because it is a 2-flip banker that flips more than random. The species leave heuristic is not the reason.
- The advertised "species majority" strategy (c) is not a meaningful strategy as designed.

**4. Unused-Lifebuoy value is dead.**
- Winners finish with 0.03 unused Lifebuoys on average; losers finish with 0. Bots with the same threshold use all of them (seat 1 uses 1.00, seat 2 uses 1.97 per game).
- Changing the end value from 0 to 5 changes strategic vs greedy by under 1 point.
- Never spending a Lifebuoy (hoarding for the 2 points) loses to the default 84% of the time (15.7% win). Spending always dominates hoarding.
- The "hold or cash out" decision in the design notes does not exist.

**5. Does always-bank-early dominate? No, but it exposes a design hole.**
- bank_early (flip exactly 1) wins only 2% vs strategic, 9% vs greedy, 9.7% vs collector, 47% vs pusher-20 and 68% vs random.
- A pusher with target 8-12 beats it 91%. Target sweep vs strategic: 4->5%, 8->18%, 12->36%, 16->34%, 20->23%, 30->4%. The sweet spot is about 12 points of pile.
- A bank_early mirror has 0 busts and no clashes. Each turn it flips 1 into an empty river and takes it, so the river is always empty and "leave one behind" never triggers. Both players get 30 random cards. This is a pure coin-flip line the rules allow, and a pair of cautious players would play it.
- Bank-early only fails because pushers exploit it. It is not dominant, but two timid players produce a degenerate, interaction-free game.

## Problems, ranked

1. **(High) Seat balance is wrong.** The second player wins about 57%, a 7-point error, and it grows with skill (pusher mirror: 37% for first seat). A single Lifebuoy is worth more than the first-move edge.
   - Fix: give both players 1 Lifebuoy. If seat 1 still wins 52-55%, give the second player +2 or +3 score points. Tested: (1,1) with +3 pts for second gives strategic 52.1%, greedy 49.1%, collector 50.7% for the first seat. Another option is 1 Lifebuoy each plus the existing second-player tiebreaker.
2. **(High) Bait mechanic collapses.** "Leave the lowest card" is nearly always right.
   - Test: greedy leaving the highest card wins only 17.6% vs leaving the lowest. Leaving a random card wins 30.1%. The "most copies remaining" bait rule wins 46.0%, which is about equal. Players have one sensible choice.
   - In narrated game 1 the same U1 stayed in the river for 24 turns. It is a permanent trap that makes every 1 a dead flip for both players.
   - Fix options: make the leftover count (e.g. leave exactly two cards when the river has 5 or more), let the leftover be taken by the next player for a cost, or score the leftover for whoever leaves it. Another option is to discard the leftover whenever a bust happens, so the river does not become a permanent 1-lock.
3. **(Medium) Dead turns and late-game dud turns.** 8-12% of turns are bust-on-first-flip with no effect. Late in the game players flip the one remaining card values into the lock and nothing happens for several turns in a row (game 1, turns 19-24).
   - Fix: a first flip should never clash. For example, let the first flip be discarded and replaced if it matches, or make the leftover not count on the first flip.
4. **(Medium) Species bonus is irrelevant.** About 4% of games are decided by it.
   - Fix: raise it to +10 or make it per-card-in-majority, and test again. At 7 it is still only 4.8%.
5. **(Low-Med) Unused-Lifebuoy points are irrelevant** because everyone spends them. Fix: remove the rule, or make Lifebuoys bank-able (recoverable) so holding one is a real choice.
6. **(Low) Bank-early mirror is a no-interaction coin flip** with 2.6% ties. Fix: force a minimum of 2 flips, or require the river to keep 2 cards after banking.
7. **(Low) Mild snowball.** The leader after one third of the game wins 67-75%. Acceptable, but watch it once seat balance is fixed.

## Rule ambiguities found (and my interpretation)

- Ambiguous "pile" after a Lifebuoy clash: the clash card goes to discard and the pile stays in the river. I keep it in the river for banking.
- Tiebreaker "second player wins" applied when score and haul count are both tied.
- First flip of a turn clashes with a leftover and the player has a Lifebuoy: I allowed the Lifebuoy to be spent (turn then banks the leftover). It seems wasteful but is legal.
- Deck empties mid-flip: I treat it as a no-clash stop and bank.
- When the river has exactly 1 card after a Lifebuoy, it is simply taken (river becomes empty).
- Bust with an empty pile hands over nothing. A zero-gain turn is allowed and, as above, common.
- Rules never state whether hauls' unused Lifebuoys count in the haul-count tiebreaker. I assumed not.
- Whether a player may choose to bust with a Lifebuoy available is stated (yes). Bots do it only when the pile is small.

## How it felt (narrated play)

**Game 1 (strategic, seat 1, vs greedy, seed 7).**
- Turn 1 I flipped five cards, banked 22 and left a U1. Fun: pushing past three cards felt like a real gamble.
- Turns 2-5 were fun. The opponent used both Lifebuoys early to survive clashes I would have dodged.
- Then the U1 sat there for 24 turns. Every 1 I flipped was an auto-bust, and by turn 19 I was flipping a single card and losing nothing, then watching the opponent do the same. Boring and frustrating.
- Seat 1 won 213-104. I felt no tension after turn 15 because nothing at stake was left.
- There was no real choice about what to leave. I left the 1 every time.

**Game 2 (strategic mirror, seed 21).**
- Turn 1 I pushed to four cards and a Lifebuoy saved me. Turn 2 the opponent's Lifebuoy at nine points felt like a fair trade. That is the best moment of the design.
- By turn 3 both Lifebuoys were gone and every later push was a coin flip on losing a pile.
- From turn 5, both players banked two cards every turn and left the S1 or L2 forever. The game was safe, slow and symmetrical, and I made the same move 15 turns in a row.
- Lead swapped 4-5 times. The score ended close (about 133 vs 115 at turn 23), so the species bonus mattered little.
- Downtime was minimal (turns are short), but there was no table talk because there were no decisions.

## Recommended fix list

1. Equalise Lifebuoys at 1 each. Optionally add +2 or +3 points for the second player. Re-test seat balance.
2. Rework the leave-one rule so the leftover stops being a permanent "1" lock.
3. Remove dead first-flip busts.
4. Remove or rework unused-Lifebuoy points and raise the species bonus.
5. Re-run the simulation after changes (`python3 run.py 2000`, `python3 fair.py`).
