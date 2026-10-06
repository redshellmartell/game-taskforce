# Playtest report: Last Bid Standing, revision 1 (rules v2)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** No human has played this. Simulation cannot test fun, teaching time, table talk, how readable the rules are, or whether people can track five rivals' shown cards. Code: `sim/` (`run.py` reproduces everything; seeds fixed).

## Key numbers (2,000 games per table kind and player count; 79,000 games in total)

| KPI | Target | Previous (v1) | Now (v2) | Status |
|---|---|---|---|---|
| Skill gap, lone strategic vs 5 random (5p / 6p) | >= 20 | 17.5 | 30.0 / 20.6 (avg 25.3) | pass, but 6p is only just over |
| Same, weaker reference bots | >= 20 | n/a | no-memory 25.4 / 20.9; greedy 14.8 / 9.8 | greedy fails |
| Mixed 3 strategic + 3 random, strategic minus random | >= 5 | 0.8-2.3 | 13.2 (5p) / 10.4 (6p) | pass |
| Planner vs casual (3 v 3) | planner wins | planner lost | 23.4 v 14.9 (5p), 19.7 v 13.6 (6p) | pass |
| Seat gap (all-strategic) | <= 5 | 1.4 | 0.6 (5p) / 1.0 (6p) | pass |
| Length (my timing model) | 16-24 min | 16 | 18.6 (5p) / 19.6 (6p) | pass |
| Runaway leader (halfway leader wins) | <= 65% | 48.9% | 43-47% (late: 53-55%) | pass |
| Lead changes per game | >= 2 | 2.98 | 3.5 (5p) / 4.0 (6p) | pass |
| Hype share of points | 45-50% | 55-64% | 56% (5p) / 64% (6p) | FAIL, no change |
| Forced passes (empty hand) | <= 13% | 22% | 6.1% / 4.1% | pass |
| Lots unsold at game end | <= 5 | 4.6-7.8 | 3.1 / 2.7 (block averages 3.7 lots) | pass |
| Last-round leader flip | <= 20% | 29% | 20% (5p) / 27% (6p) | fail at 6p |
| Ties for first | low | 2.5% | 0.2% | pass |
| Turn-cap hits | 0 | 0 | 0 (fixed 14 rounds) | pass |

Reference spread (L2): the lone-bot gap is 30.0 / 20.6 for the strong bot, 25.4 / 20.9 for the no-memory bot and 14.8 / 9.8 for greedy. The headline pass rests on the two sampling bots; the greedy bot does not clear 20. Table-mix spread: planner, strategic and casual all sit within 4 to 7 points of each other when they share a table.

## Designer's four ablation bots (full strategic minus ablated bot, same table, points; need >= +5)

| Bot | 5p | 6p | Result |
|---|---|---|---|
| Ignore-Hype | -6.5 | +13.1 | inconsistent, unconfirmed |
| Ignore-crash | +7.5 | +5.5 | pass at both counts |
| Ignore-ties | -7.0 | +2.6 | FAIL |
| No-memory (open income) | +2.7 | +2.3 | FAIL |

Per the designer's own rule, open income and the tie rule are not shown to matter. The skill that exists comes from the Monte-Carlo odds estimate. Experiment E5 (income 1 instead of 2) leaves the lone gap unchanged (21.3 at 6p), so the extra income is not what lifted the gap. Part of the v1 to v2 gain is that the v2 bot is a different, better bot, so the gain is not purely a rule effect.

## Extra configurations (6p, 1,000 games each; all five used)

| Config | lone gap | Hype % | forced % | unsold | flip | seat gap |
|---|---|---|---|---|---|---|
| E1 lots 3-6 | 19.1 | 59 | 5.6 | 2.4 | 22% | 1.2 |
| E2 start hand 5 | 20.7 | 66 | 3.0 | 2.8 | 26% | 1.9 |
| E3 bids 1-11 (78 cards) | 20.9 | 65 | 5.9 | 3.0 | 23% | 1.9 |
| E4 lots 4-7 | 18.0 | 54 | 7.1 | 2.3 | 17% | 2.0 |
| E5 income 1 | 21.3 | 64 | 4.0 | 2.8 | 24% | 1.1 |

Findings: lot value alone cannot take Hype to 50% without hurting the skill gap. E3 is free (fallback to 78 cards). E2 and E5 change little.

## Problems, ranked

1. **High: Hype is still about 60% of points** (target 45-50). Fix: cap Hype per lot, or count only the top 3 burned cards per category. Lot-value changes (E1, E4) do not reach it without losing skill gap.
2. **High: two of four twists fail ablation and two flip sign between 5 and 6 players.** Open income adds about 2.5 points, ties flip. Drop or strengthen open income; re-check with a smarter bot. Untested: why ablated bots win at 5p.
3. **High: skill gap is bot-dependent.** Greedy gains 12.3 alone; at a 50/50 mixed table the gap is 11.8 (target at least 5, so this passes), but the designer's doubt holds in one respect: the mixed gain is small next to the lone-bot gain, and E5 shows it does not depend on the v2 income rule.
4. **Medium: last-round flips 27% at 6p** (target 20%). Reveal the crash projection earlier or freeze Hype before round 14.
5. **Medium: 25-35% of bids cancel** (10.9 / 17.6 per game). Needs human reaction.
6. **Low: 82 cards, about 140 lines of rules.** Use bids 1-11 (E3).

## Dead cards
None flagged. All bid bands are played (1-3: 13%, 4-6: 15%, 7-9: 19%, 10-12: 22%; Pass 30% of turns). Low bids correlate negatively with winning (r -0.16) but are played as cheap burns, so they are not dead. Printed lot value 2 has the weakest win link (r 0.12 vs 0.33 for value 4), so the 2s are the weakest lots.

## Ambiguities hit while coding v2
1. Round-14 income (passers draw 2 cards that only matter for tiebreak 1): assumed yes.
2. Whether shown income cards are kept in a public tableau; humans must remember them.
3. Whether a shown card that is played and reshuffled stops being "known": assumed yes.
4. Income K when the discard is empty and the deck holds fewer than 2P cards: reshuffle is a no-op, K = deck / P (rare).
5. Crash tie-break uses bid values in the Hype row (assumed, as in the worked example).
6. Bot hint "rounds left x 0.5" is not a rule: players have only a projection of the crash.
All v1 ambiguities (second-bidder lot, nobody-draws, reshuffle timing, tiebreaks, tied top Hype) were closed by v2 and caused no problems in code.

## Narrated play (seat 1; one game, reasoned from a logged 6-player game, not live human play)
Round 1: I held 10, 8, 5, 2. Five of six players bid and the 12 and 11 took both lots; my 10 burned into Clocks. Frustrating: a strong card gone with nothing. Round 3: I read two shown draws and bid just under a rival's known 9, and won a lot. That felt clever, but I could do it only with a notepad. Rounds 5 to 7: three bids a round, many passers drawing and showing cards, a lot of waiting while each shows two cards; the pace dips. Round 8: three bids, a 11 tie cancelled, my 10 won with a choice among three lots on the block (fun, the carried-over lots matter). Rounds 11 to 13: everyone is burning cards into the same two categories and I could not tell which would crash. Round 14: Hype ended 8-8-8-7; the tie-break by bid total crashed Paintings. Dramatic but felt arbitrary because I had to add up three rows of card values at the end. Downtime is low (simultaneous), but the income reveal and tie resolution add friction. The surprise (a three-way Hype tie) made me want to check this in simulation: the last-round flip rate is 20-27%.

## Cannot be tested by simulation
Fun, reading burden of tracking five rivals' shown cards, teach time for about 140 lines of rules, whether tie cancellations feel fair, table talk, and the real round time (my timing model gives 18.6-19.6 minutes; the designer's 70 s per round gives about 19).

## Untested suggestions (budget used)
Spite and kingmaking bot for the last round; 4-player variant; why ablated bots beat full bots at 5p; Hype cap per lot; a smarter greedy-plus bot as a third reference.

## Honest answer on the mixed-table gap
The designer doubted a small change could fix it. In simulation it moved from 0.8-2.3 to 11.8, so the doubt is not borne out for these bots. Two caveats weaken that: the v2 bot is stronger than the v1 bot, and the open-income rule is not what carries the gain (no-memory ablation, E5). Whether humans can play the probability-sampling strategy is unknown.
