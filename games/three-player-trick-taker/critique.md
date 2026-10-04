# Critique: Split the Take (rules v2, revision 1)

**Verdict: REVISE-MAJOR**

Average 3.5 (previous 3.0 at revision 0; the KPI at pitch is 3.5 or higher). A pitch also needs zero dominant strategies, and that is still unmet. No panel-report.md exists because the AI persona reviews have not been approved. Fun and Market fit are therefore scored from the free predicted panel in panel.json, and from the narrated play notes. Originality was not re-checked: the core mechanic is unchanged (the bands only soften the exact-count contract), so the previous finding stands.

| Area | Rev 0 | Rev 1 |
|---|---|---|
| Originality | 3 | 3 |
| Rules clarity | 3 | 4 |
| Fun | 2 | 3 |
| Balance | 2 | 3 |
| Market fit | 3 | 3 |
| Production | 5 | 5 |

## What improved since revision 0
- Contract success rose from 19.7% to 56.6%, which is inside the 40-60% aim.
- Points per round by role are now 3.84 (Planner) / 3.53 (Safecracker) / 3.95 (Double-Crosser). Before, it was 3.5 / 2.7 / 4.8, and the Safecracker flag is gone.
- Runaway leader rate fell from 64.4% to 52.3%. Lead changes rose from 1.27 to 1.49.
- Seat gap is 3.5 points on 2,000 games.
- No Trump is removed, so there are no dead options. The ambiguities listed last time are resolved and the playtester reports none.
- Bar Raiser predicted fun is 3.90 with no veto. Average predicted fun is 3.54.

## Originality (3)
No change. Closest existing game: **Oh Hell / Wizard** (similarity: medium), with Skull King nearby. The shared crew contract with a spoiler is a real twist, but the idea that carries it (steering to a target) is not yet working. The panel's originality metric is 0.75 for every persona. No rules or text have been copied.

## Rules clarity (4)
It is a one-page game with a clear phase order, an action table and explicit edge cases. The earlier contradictions are fixed.
- The panel rules-simplicity metric is 0.0 for every persona, and every persona hits a rulebook-weight or ambiguity pet peeve. The reason is a three-tier job result, three role payout tables and Heat on top of trick-taking.
- The three-tier payout table is the hardest part for the casual and family audiences to learn. The family persona is the worst fit at 3.07.
- "No talk about your hand" between crew members who are partners and rivals is still hard to enforce.
- The playtester notes that the Planner has to estimate a tricks-total for two hands, one of which is hidden and will be changed by the Swap. Nothing in the rules helps a new player do that.

## Fun (3)
There is some real tension now. A crew on Target-1 with one trick left can take it (clean) or duck it (messy), and the Double-Crosser's push is visible. The weakness is the narrated-play note: cheap-win greedy play makes most rounds read as "take tricks" whatever the contract. A bot that grabs tricks beats the bot that plays the contract, so the contract isn't doing what the design says. Predicted fun from the panel is 3.54, ranging from competitor 4.31 to family 3.07. The game suits competitive players and is a poor fit for casual and family players, and 3.5 only means the average player is mildly positive.

## Balance (3)
| KPI | Target | Result |
|---|---|---|
| Seat gap | 5 or less | 3.5, pass |
| Strategic vs random | 20 or more | 51.6, pass |
| Length | 16-24 min | 18.2, pass |
| Runaway leader | 65% or less | 52.3%, pass |
| Lead changes | 2 or more | 1.49, **fail** |
| Contract success | 40-60% | 56.6%, pass |
| Mixed table (the intended strategy vs greedy) | strategic at or above greedy | greedy 63.5%, strategic 28.5%, **fail** |
| Dominant strategy | none | **greedy trick-grabbing, unfixed** |

Greedy dominance is the problem that matters. Doubling the bonuses took greedy to 50% and strategic only to 33%. Tripling gave 43% / 34%. Greedy fell and strategic did not rise, so more bonus alone cannot fix it. Contract success is about 50-55% whatever either bot does, so steering skill is not rewarded. The playtester also admits the strategic bot is simple, so some of the gap may be a bot weakness. That uncertainty is the reason a human playtest is worth more than another bot revision at this point, and the owner should know it.

## Market fit (3)
It still matches the brief: exactly 3 players, about 18 minutes, 40 cards, three roles and three special rules. The drift risk is that "a rotating role fixes the 2-vs-1 gang-up" is now partly true (the DC cannot kingmake, as the contract is shared), but the crew-versus-spoiler setup creates a different 2-vs-1 problem, and the crew members have to cooperate without table talk. The panel splits sharply, which fits a niche game and not a mass-market one.

## Production (5)
40 standard-size cards and a score pad. Prototype cost about $10-15. Nothing hard to make.

## Biggest strength
The cheap, 3-player-only shared-contract structure now works as a scoring structure. Roles, seats and contract success are all balanced inside target.

## Biggest weakness
The intended strategy (steering the contract) loses to plain trick-grabbing, 28.5% to 63.5%. Skill is in loot and not in the contract, which is the game's whole reason to exist.

## Required changes
1. **Make steering worth more than loot.** Cut loot to half value (1 point per 2 tricks) or make it count only for the Double-Crosser, and raise the clean bonus (about +5/+6). This was an untested experiment in the playtest. Aim: mixed table strategic win rate at least 40% and at or above greedy.
2. **Raise volatility.** Try Heat at -3 or a double-scored final round. Aim: lead changes 2 or more, with sole leader after round 3 still at 65% or less.
3. **Test with a stronger strategic bot, with card counting.** If the new bot still loses to greedy, the contract is not steerable and the game should be killed. Aim: a clear result either way.
4. **Hold the other KPIs.** Re-run the seat gap on 4,000+ games (5 points or less), contract success 40-60%, role points within about 1.
5. **Get at least one human playtest** before or alongside the next revision, since bot judgement of "steering" is the doubtful part.

## Is another revision worth it?
**Yes, as the last loop.** Six of the ten KPIs now pass, and the one remaining diagnosis (loot outweighs steering) comes with a specific untested fix. The kill condition set last time (contract success below 35%) was not triggered. If strategic still cannot reach greedy after loot is cut, kill the game and do not revise a third time.
