# Playtest report: Split the Take (rules v1, revision 0)

**Verdict: NEEDS-FIXES.** The game runs and is fair between seats, but its central twist (hit the exact Target) almost never happens, so the intended strategy is not the winning one.

| Metric | Result | KPI |
|---|---|---|
| Seat win rates (strategic x3, 2,000 games) | 34.9 / 34.5 / 30.6, gap 4.3 pts (std. error ~1.1 per seat) | <= 5, borderline |
| Strategic vs random (1 strategic vs 2 random) | 68.7% vs 15.6% each, gap 53 pts | >= 20, pass |
| Mixed table random/greedy/strategic (2,004 games) | 5% / 68% / 27% | greedy beats the intended strategy |
| Length | fixed 6 rounds x 7 tricks, est. 18 min | 20 +/-20%, pass |
| Ties / turn-cap hits | 3.6% (broken by tiebreakers or shared) / 0 | ok |
| Lead changes per game | 1.27 | >= 2, FAIL |
| Sole leader after round 3 wins | 64.4% | <= 65%, borderline |
| Contract success rate | 19.7% (random 17%, greedy 19%) | design aim 40-60%, FAIL |
| Points per round by role | Double-Crosser 4.8, Planner 3.7, Safecracker 2.7 | |

## Problems (ranked)
1. **High: exact contract almost never succeeds.** Crew hits the Target about 1 round in 5 whatever the bots do, so the Double-Crosser takes +4 in 80% of rounds. Fix: make success reachable (band of +/-1 for a reduced bonus, or lower the DC bonus to +2 and raise the crew bonus).
2. **High: intended strategy loses to trick-grabbing.** Greedy (grab every trick cheaply) beats my strategic bot (aims for exact count, ducks) 68% to 27%. Four variants of strategic (greedy swap, greedy plan, no ducking by crew, no ducking by DC) still reached only 13-17% against two greedy bots. Caveat: the strategic heuristic is simple; a smarter bot might do better, but the exactness rate suggests not much.
3. **Medium: role imbalance.** Safecracker is the weakest role (2.7 pts/round), Double-Crosser the strongest. Seats are still fair because roles rotate. The Swap is mandatory and gives little.
4. **Medium: lead changes (1.27) below KPI; Heat is nearly irrelevant.** Heat is held in 73% of rounds and costs about 0.45 pts. Removing it moves lead changes to 1.15 and early-leader wins to 68%. Make it bite harder or cut it.
5. **Low: No Trump never chosen** by the strategic planner (a trump suit always scores at least as many winners), so one of the Plan options is dead for the bot. Likely true for humans too.
6. **Low: Target 3 is chosen 34% of the time but hits only 10%**; best hit rate is Target 6 (35%). A fixed Target 5 is not dominant (wins 37% vs two adaptive bots, which is a small edge, within noise of fair).

Extra configurations run (5): no Heat, fixed Target 5, planner offset -1, planner offset +1, Double-Crosser always wins. None changed the picture (success stayed 19-22%). Untested suggestions: a +/-1 tolerance band on the Target; DC bonus 2; Heat of -2; Safecracker draws 3.

## Rule ambiguities
- Heat on a player who earns no bonus has no effect (rules do not say).
- Revoke text contradicts itself ("0 tricks" vs "tricks as played"); impossible in sim.
- Role-pass direction written as "pass left" but the description (Planner becomes Safecracker) can be read either way; sim uses P -> S -> D -> P by seat order, symmetric.
- Dealing "starting with the Planner" is irrelevant; Plan before Swap gives the crew an information edge over the Double-Crosser by design.
- Tiebreaker 1 counts double-crosses even when Heat reduced the bonus.

## How it felt (one narrated game, from a logged bot game; bot decisions read as a human would)
- R1 as Double-Crosser (led first): I led Ke9, then Co9, cashing two top cards. Easy decision, felt good. Crew needed 4, got 3, my +4 landed. No tension at all: I had not really tried.
- R2 as Planner with Target 3: crew finished with 4 tricks and the Double-Crosser pocketed +4 again. Frustrating: the Target felt like a guess no one could steer.
- Fun moment: R3 with Target 7 (all seven tricks for the crew); the Double-Crosser only needed one trick, and took it on trick 2. Tension in the first two tricks, then dead.
- Boring/confusing: the duck-or-win question for crew was rarely live. Downtime is low (3 players, every trick has all three acting). Plan and Swap are quick and clear.

## Panel rotation (free)
10 tables x 6 seatings x 200 games. Average predicted fun 3.58 (competitor 4.08 best fit, story 3.20 worst fit). The family persona's cautious bot wins 55% by playing greedy, again showing trick-grabbing beats contract play.
