# Playtest report: Ladder Pairs (rules v1, cycle 0)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** The game runs cleanly (no stalls, 0 turn-cap hits, seats balanced, runaway OK) but the headline twist, hidden changing partners, does not change best play in simulation.

## Key numbers (2,000 games per configuration, fixed seeds; sim/results.json)
| KPI | Result | Target | Met |
|---|---|---|---|
| Seat gap (Reader mirror / Greedy mirror) | 0.9 / 0.45 pts | <= 5 | yes |
| Strategic vs random | Reader minus Random 74.8 (1 v 3), 36.7 (2 v 2) | >= 20 | yes, but see below |
| Strategic vs Greedy (L2 spread) | -2.5 (1 v 3), -1.5 (2 v 2); ReaderBest 0.0 | n/a | **no skill over a simple bot** |
| Length | 54 turns/hand, 324/game; 27.3 min at 6 s per decision, 2 s per quick turn, 0.5 min/hand overhead (about 37 min at 8 s/3 s/0.7) | 20-30 | yes at central assumption, unsettled |
| Runaway leader (after hand 4 / hand 3) | 0.403 / 0.324 (Greedy mirror 0.418) | <= 0.65 | yes |
| Lead changes per game | 1.13 (Greedy 1.12) | >= 2 | **no** |
| Ties (shared win after tie-breaks) / cap hits | 0.2% / 0 | | yes |
| First-lead team scores 3+ | 61.0% (left 62.0, across 62.2, right 58.6; Greedy 56.9) | 50-60%, spread <= 5 | spread yes, level +1 over band |
| First Rope played (trick no.) | median 3, IQR 2-4 (Greedy median 4, IQR 3-5); every hand sees a Rope; 3.5 of 4 Ropes played per hand | median 3-6 | yes (low edge) |
| Forced-pass rate | 42% of follow turns (Greedy 56%); 1.9 runs of 3+ per hand | (L11 watch) | flag |
| Dead cards | none: Triple is the rarest (used in 9.6% of player-hands) | 0 | yes |
| Ambiguities | 9 listed in playtest.json | 0 | no |

## Ablations (2 Reader + 2 ablated, seats rotated; margin = per-bot win-rate points, Reader minus ablated; needs >= +5)
| Bot | Reader | Ablated | Margin | Result |
|---|---|---|---|---|
| A1 partner-blind | 21.5% | 28.5% | **-7.0** | FAIL (ablated wins) |
| A2 reveal-blind | 24.4% | 25.6% | -1.2 | FAIL |
| A3 Uphill-blind | 24.8% | 25.2% | -0.4 | FAIL |
| A4 Relay-blind | 23.4% | 26.6% | -3.2 | FAIL |
| Code attack (two Readers with parity code) | | | gain -0.1 pts (limit 3) | PASS, weak test |

Rule variants (Reader mirror): **Uphill off**: runaway 0.663 (+26.0 pts, passes the >= 5 test) and lead changes 0.53, so the Uphill *rule* matters even though an Uphill-aware *bot* does not. **Relay off**: 4-point sweeps 36.1% vs 42.3%, first-lead 3+ unchanged; Relay is a mild effect.

## Problems, ranked
1. **HIGH: hidden partners are inert (L1).** The belief Reader loses to Greedy and A1 partner-blind beats it by 7 points: trying to help a likely partner costs more than it earns. Cause: points come only from finishing order, so letting a partner win a trick earns nothing directly and gives up tempo. Debugging budget used (3 attempts, experiments/e1.py, 9 Reader variants): the best never passes for a partner unless certain and still only ties Greedy (+0 to +1.7, inside noise at 600-2,000 games). Fix: give partner help a payoff (team credit for tricks won, or a bigger Relay), then re-run all ablations at once (L10).
2. **HIGH: skill gap is only "sensible vs random" (L6).** 75 pts against random but about 0 against Greedy. Same lever as 1; second source of scoring or decisions where "shed lowest" is wrong.
3. **MEDIUM: lead changes 1.13 vs 2.** Uphill (threshold 4) is the only comeback source. Knob: threshold 3.
4. **MEDIUM: dead turns.** 42% forced passes, long pass runs (sample hand: seat 0 passed 11 times in a row). L11 pattern; needs a human check.
5. **LOW:** first-lead 3+ at 61% (about 1 point over band); length depends on the pace assumption (needs a timed human hand); the code-attack test says little while partner knowledge is worthless.

## Rule ambiguities hit (9, all in playtest.json)
Relay shows a Rope that may already be known; turn-cap fallback unreachable; four of a kind only splits; "second out ends hand mid-trick" scoring; Uphill measured at hand start with >=4; final tie-break step 3 and shared wins; "cannot go out without Rope" is a consequence not a rule; leader must lead after Relay; pass-then-play within a trick.

## How it felt (narrated, read from one logged Reader hand, seat 0's view; 48 turns)
Tricks 1 to 3 I held low singles and passed twice then a third time while seats 1 to 3 climbed singles 6, 8, 9, 10, 13, then a Sun 15: boring (waiting with no legal play, 22 of 41 follow turns forced). Moment of fun: trick 4 I played my Sun 14 on a 13 and could be read by seat 3 (Sun 15 earlier), so I knew my partner and was glad to pass later; but in the hand nothing I did for the partner mattered, the finish order was decided by who emptied fastest (seat 1 out first with a Moon 14 after I led a worthless 2). Confusing: nothing, rules are short. Frustrating: seeing no payoff for the deduction.

## What simulation cannot test
Fun of guessing partners, human bluffing and table talk, whether private signals appear, teaching time (51 rules lines is a proxy), real pace per turn (assumed), theme, and card counting limits (Reader has perfect memory of discards, a human does not).

## Untested suggestions / BUDGET REQUEST
Untested: team credit per trick won; Uphill threshold 3; leader rotates with dealer; 9-card deal. Re-run all four ablations plus code attack after any of them. BUDGET REQUEST: none now; after the designer's fix, one pass (about 5 min, 2,000 games per config) to re-run everything.
