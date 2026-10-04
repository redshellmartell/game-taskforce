# Critique: Split the Take (rules v3, revision 2)

**Verdict: REVISE-MINOR**

Average 3.67 (rev 1: 3.5, rev 0: 3.0). That clears the 3.5 bar for a pitch. No panel-report.md exists because the AI persona reviews were not approved, so Fun and Market fit are scored from the free predicted panel in panel.json (average predicted fun 3.54, Bar Raiser 3.95, no veto) and the playtest notes. No human playtest has happened. Originality was not re-searched: the core mechanic is unchanged since revision 0 (only payout rules moved), so the earlier finding stands.

| Area | Rev 0 | Rev 1 | Rev 2 |
|---|---|---|---|
| Originality | 3 | 3 | 3 |
| Rules clarity | 3 | 4 | 4 |
| Fun | 2 | 3 | 3 |
| Balance | 2 | 3 | 4 |
| Market fit | 3 | 3 | 3 |
| Production | 5 | 5 | 5 |

Average: (3+4+3+4+3+5)/6 = 3.67.

## What improved since revision 1
- The blocking problem is fixed. Mixed table: strategic 42.0%, greedy 41.8%, random 16.2% (was greedy 63.5% vs strategic 28.5%). The "loot only counts if the job comes off" rule did what the diagnosis said it would. The dominant-strategy flag is gone (panel metric dominant_strategy_absent 1.0).
- Seat gap 1.7 (was 3.5). Runaway 50.3%. Contract success 50.0%. Role points 2.93 / 2.48 / 2.59 (spread 0.45). Length 18.2 min. Ties 0.5%. Skill gap vs random 46.1.
- Lead changes 1.49 to 1.61.
- Double-Crosser payout is now one line, which helps teaching.

## Originality (3)
Closest existing game: **Oh Hell / Wizard** (similarity: medium), with Skull King nearby. The shared crew contract against a spoiler, with rotating roles, is a real twist on exact-target trick-taking. It is not a copy of any game's rules or text. Not re-searched.

## Rules clarity (4)
One page, a clear phase order, an action table, edge cases and tiebreakers. The playtester reports zero unresolved ambiguities. Remaining weight: three payout columns, three tiers (clean, messy, blown), the "loot only if the job comes off" rule and Heat on top of trick-taking. Every persona has rules_simplicity 0.0, and the casual, family and story personas hit rulebook-weight peeves. Also, the Planner must guess a two-hand total with a hidden, swapped partner hand, and the rules give new players no help with that. The "no talk about your hand" rule between partners who are also rivals is hard to enforce. The design note's scoring forecast (18-28 final scores) is stale; sim shows 16.0.

## Fun (3)
The new tension is real: a crew member on the Target with tricks left must dump winners, and a blown job zeroes both crew members at once. The weaknesses:
- Strategic only ties greedy, so a bot cannot show that steering is clearly better than grabbing. Greedy alone beats two randoms at 69.9%, against 64.1% for strategic. Whether humans find the contract-steering depth is unknown, and only a human playtest can say.
- Lead changes 1.61. Heat (-3) is doing almost all the work (1.07 without it) and applies in 74% of rounds. A penalty applied that often is a permanent tax on leading, not a surprise.
- Predicted fun by persona: competitor 4.35, Bar Raiser 3.95, strategist 3.78, story 3.18, casual 3.14, family 2.86 (would not buy). This is a game for competitive, strategy-minded groups, not for family tables, which the brief names as part of its audience (adults and families).

## Balance (4)
| KPI | Target | Result |
|---|---|---|
| Seat gap | 5 or less | 1.7, pass |
| Strategic vs random | 20 or more | 46.1, pass |
| Length | 16-24 min | 18.2, pass |
| Runaway leader | 65% or less | 50.3%, pass |
| Lead changes | 2 or more | 1.61, **fail (soft)** |
| Contract success | 40-65% | 50.0%, pass |
| Mixed table | strategic at or above greedy | 42.0 vs 41.8, pass (noise +-1.1) |
| Dominant strategy | none | none found |
| Role points | within about 1 | 0.45 spread, pass |

One KPI misses, by 0.39. The playtester ran three fallbacks (double-scored final round 1.84, clean-only crew loot 1.64, flat half-value 1.71) and none reached 2, so further tuning is a guess, not a diagnosis. A double-scored finale cut strategic to 38.5% against greedy 41.8%, which is a trade I would not take. Target 3 is the most-chosen bot Target (34%) and the least reliable (28% success), which is a minor oddity, not a dead option. The seat results (1.7 gap) are on 2,000-game mirrors, below the 4,000+ I asked for; the gap is far inside the limit, so I do not require a re-run.

## Market fit (3)
Still matches the brief: exactly 3 players, about 18 minutes, 40 cards, three special rules. It targets the gap (a trick-taker built for 3). The drift risk is audience: the family persona predicts 2.86 and a no-buy, and casual is 3.14, so this is a niche game for experienced trick-taking groups, which fits "demand is real but not exceptional". Bar Raiser would buy at a predicted $44; the competitor $36.

## Production (5)
40 standard-size cards and a score pad. Prototype cost about $10-15. The cards are plain, and the only real thing to make is a one-page rules sheet and a score pad with a result row.

## Biggest strength
The central idea now works: crew loot is lost on a blown job, so steering the shared contract competes with trick-grabbing, and every structural KPI (seat gap 1.7, role points, runaway, contract success, length) is inside target.

## Biggest weakness
Soft, unproven depth and a narrow audience. Strategic only ties greedy in sim, lead changes are 1.61 (below 2) and are propped up by a Heat penalty on the leader in 74% of rounds, and family and casual players are predicted to find the rules heavy and the game not fun.

## Required changes (small, for REVISE-MINOR; none needs a new simulation loop)
1. Correct the design notes to the measured values (mean final score about 16, not 18-28; Heat in 74% of rounds). KPI: zero rule ambiguities and no stale numbers in the rulebook.
2. Add a short teaching aid to rules.md: one worked example round and a one-line Planner hint (the Target is for two hands, so lean low). KPI: rules clarity 4 held, with rulebook weight less of a problem for the casual and family personas.
3. Describe the optional "double-scored final round" as a labelled variant, not a core rule, and say that it lowers strategic's mixed-table share (38.5%) in sim. KPI: lead changes 1.84 for tables that want more swings.
4. The pitch must state the risks below and must ask for a human playtest (record the player type) before any physical production. KPI: first human fun and clarity scores of 3 or higher, and steering felt as a decision.

## Risks the pitch must state
- Lead changes 1.61 against a target of 2 (a known soft miss; Heat does most of the work).
- Strategic only ties greedy in simulation. Skill expression of steering is unproven with humans.
- Audience: competitor and strategist players like it (4.35 and 3.78); casual 3.14 and family 2.86 (would not buy). It is not a family game.
- Rulebook weight: three-tier result plus conditional loot plus Heat. Teaching takes about 10 minutes.
- No panel-report.md (AI persona reviews not run); fun and market fit come from free predicted scores. No human playtest yet.
- Low scoring (mean final 16.0). Close to a 3.5 average, not above it by a margin.
- Originality: medium similarity to Oh Hell / Wizard.
- The crew partners cannot talk about their hands, and that is hard to enforce at a real table.

## Is another revision worth it?
**No: the single missed KPI is minor, three tested variants failed to fix it, and another bot-driven loop is unlikely to change the verdict; the next evidence should come from a human playtest.**
