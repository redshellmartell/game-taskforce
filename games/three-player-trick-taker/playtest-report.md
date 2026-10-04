# Playtest report - Split the Take (revision 2, rules v3)

**Verdict: NEEDS-FIXES (minor).** Five of six headline KPIs now pass, including the one that failed for two revisions (strategic vs greedy). Lead changes are still 1.61 against a target of 2, and none of the three fallback variants reached 2.

Sim updated in place (`sim/game.py` scoring to v3; new card-counting `Counter`/`Strategic` bot in `sim/bots.py`; old heuristic kept as `Basic`, used by the casual/story/family persona bots). 2,000 games per pairing, fixed seeds.

| KPI | Target | Rev 1 | Rev 2 | Result |
|---|---|---|---|---|
| Mixed table strategic vs greedy | strategic >= greedy, >= 40% | 28.5% vs 63.5% | strategic 42.0%, greedy 41.8%, random 16.2% | pass (parity, noise +-1.1) |
| Skill: 1 strategic vs 2 random | >= 20 pts | 51.6 | 46.1 pts (64.1% vs 18.0%) | pass |
| Seat gap (strategic mirror) | <= 5 pts | 3.5 | 1.7 (34.4/32.7/32.9) | pass |
| Lead changes | >= 2 | 1.49 | 1.61 | FAIL |
| Runaway (sole leader after R3 wins) | <= 65% | 52.3% | 50.3% | pass |
| Contract success (clean or messy) | 40-65% | 56.6% | 50.0% | pass |
| Role pts/round P / S / DC | within ~1 | 3.84/3.53/3.95 | 2.93 / 2.48 / 2.59 | pass (spread 0.45) |
| Length | 20 min +/-20% | 18.2 | 18.2 min (42 tricks) | pass |
| Ties | low | 0.75% | 0.5% | pass |

## Problems
1. **Medium: lead changes 1.61 (target 2).** Fallbacks run on 2,000-game mirrors (3 of 5 allowed configs): double-scored final round 1.84 (early leader 43%, role points 3.4/2.9/3.0, but mixed-table strategic drops to 38.5% vs greedy 41.8%); crew loot on clean jobs only 1.64 (and Planner/Safecracker fall to 1.9/2.0 vs DC 2.7); critic's flat half-value version 1.71 (greedy 48%, strategic 36%; DC only 1.6). None reaches 2. Without Heat, lead changes are 1.07, so Heat -3 does most of the work. Fix options: accept as a known soft miss (runaway only 50%, so games are not decided early), or ship the double-scored final round as an optional finale. Untested: Heat also costing the leader 1 loot.
2. **Low: strategic only ties greedy.** Greedy alone beats two randoms at 69.9% (vs strategic 64.1%). The v3 rule (crew loot lost on a blown job) closed the v2 gap of 35 points, but a bot cannot show that steering is clearly better than grabbing. Tuning (Target offset -1/+1, greedy swap, an always-grab DC) all landed at 35-43% for strategic, so this is the ceiling of the heuristic. A human playtest should settle whether humans can do better.
3. **Low: Target 3 is the most common bot choice (34% of rounds) and the least reliable (28% success).** Targets 5-7 succeed 59/85/73%. Not a dead option.
4. **Low: scoring is low.** Mean final score 16.0 (rules.md predicted 18-28); Heat is active in 74% of rounds. Update the design-note expectation; no rule change.

## Rule ambiguities
None blocking. Interpretations: Heat -3 floors the bonus at 0; tiebreaker 2 counts all tricks, including those on blown jobs; the role-pass direction is equivalent to a fixed seat rotation; revokes are impossible in sim.

## Experiments run (5 of 5 allowed, plus bot tuning)
Mirror experiments from run.py: no Heat, fixed Target 5, offset -1, offset +1, DC always grabs (all inside the headline run). Fallbacks: double_final, cleanloot, flat (critic's variant). Throwaway scripts are in `sim/experiments/` (`variants.py`, `tune.py`, results in `variants.json`).

## How it felt
Narrated play skipped (the change is scoring and bot strength, not turn flow). From the logs, the new tension is real: a crew member at the Target with tricks left must dump winners, and the blown job now zeroes both crew members at once, which creates sharp swings in single rounds. The cost is that many rounds still end at a modest score, so standings shuffle less than the design hopes.

## Panel
Panel rotation re-run on v3; see `panel.json` and the summary below.
