# Critique: Last Bid Standing (revision 1, rules v2.1, playtested at v2)

**Verdict: REVISE-MINOR** (bots only, unvalidated; no human has played it)

| Area | Score | Previous |
|---|---|---|
| Originality | 3 | 3 |
| Rules clarity | 3 | 3 |
| Fun | 3 | 2 |
| Balance | 3 | 2 |
| Market fit | 3 | 3 |
| Production | 5 | 5 |
| **Average** | **3.33** (target 3.5 at pitch) | 3.0 |

## What changed since revision 0
Skill gap 17.5 to 25.3 (lone bot; no-memory bot 23.1; greedy 12.3). Mixed 3+3 table gap 0.8-2.3 to 11.8. The planner now beats casual (23.4 v 14.9 at 5p). Forced passes 22% to 5%. Unsold lots 4.6-7.8 to 2.9. Lead changes 3.4, runaway 48%, seat gap 1.0. Ambiguities from v1 closed; v2.1 fixes the 6 new ones. The structural worry from the first critique (the planner loses to the casual bot) is gone in simulation. That is real progress.

## Originality (3)
Core mechanic unchanged, so no new search. Closest remains Burnout/Pairs (tied bids cancel, loser's bid goes to a reserve). The "losing bids become category value, hottest category crashes" hook still has no direct precedent I found. Similarity low to medium, no copying.

## Rules clarity (3)
v2.1 is tidy: income procedure, tie-breaks and edge cases are all defined, and the example is good. Remaining problems:
- About 140 lines against a "one page" promise (L7); the teach is untimed.
- Open income depends on players remembering 5 rivals' shown cards with no public record. Bots remember perfectly. This is the largest unproven human burden, and the ablation says it earns only about 2.5 points.
- The crash tie-break needs adding three rows of printed bid values at the end. The narrated game found this arbitrary. Rows should be tracked live.
- The 5-player 78-card configuration is untested, and E3 (bids 1-11) was measured only at 6p. The full KPI table was measured at 1-12.

## Fun (3)
Good moments exist: a carried-over rich block with a three-lot choice, bidding just under a known card, a close crash. Weak points: a quarter to a third of bids cancel (10.9 / 17.6 per game), and the mid-game pace dips while passers show two cards each. Last-round flips are 24% overall (27% at 6p, 20% at 5p) and end on an arbitrary tie-break sum. Hype is about 60% of points, so what you burn matters more than what you win, and the printed lots feel secondary. Table talk and bluffing cannot be tested by bots.

## Balance (3)
Seat balance, lead changes, runaway, length, forced passes and unsold lots all pass. Failures against the KPI targets and the playbook:
- **Hype share 56% (5p) / 64% (6p) vs 45-50% target: FAIL, unchanged from v1.** The designer's own knob (lots 3-6, E1) does not fix it. The designer said the knob fails, so a different lever is required.
- **L1, twist ablation: 2 of 4 fail.** Open income +2.7 / +2.3 (needs +5). Ignore-ties -7.0 / +2.6 (fails, sign flips). Ignore-hype -6.5 / +13.1 (inconsistent), so the central twist is not confirmed either. Only ignore-crash passes (+7.5 / +5.5). The full bot beating its ablations by pooled values (2.5, 3.3, 6.5, -2.2) means the skill comes from the Monte-Carlo odds estimate, not from the twists.
- **L2, bot spread:** the 20-point headline rests on the two sampling bots; greedy 14.8 / 9.8 fails. Part of the gain is that v2's bot is a different, better bot (E5 income 1 gives the same gap), so the improvement is not purely a rule effect.
- **L3, comeback:** the stated mechanism (pass for 2 cards, buy the rich block, push the leader's category into the crash) is plausible, and lead changes 3.4 and runaway 48% support it. No test isolates the pass-comeback effect. A 27% last-round flip at 6p shows the end is partly luck of the tie-break.
- **L8, player count:** 6p fails the flip KPI and has the thinner skill margin (20.6 gap, just over target). 5p ablations flip sign. 5p at 78 cards is untested.

## Market fit (3)
Still matches the brief (5-6 players, simultaneous, low downtime, cheap). No drift. Appeal depends on humans enjoying a probability-estimation strategy that only bots have been shown to use. The "strategist" audience may find the game noisy (cancels, tie-break end).

## Production (5)
78 cards, no board, no tokens, roughly $15. Fits the owner's card focus. Nothing hard to make.

## Biggest strength
The skill problem moved: gap 25.3 lone and 11.8 mixed (from 0.8-2.3), planner beats casual, with the other KPIs healthy, from a cheap and distinctive hook.

## Biggest weakness
The twists are not shown to matter and Hype swamps the printed lots. Repeats L1 (two of four ablations fail; ignore-hype inconsistent), L2 (greedy bot misses 20, and the gain is partly a better bot) and L6 (skill is concentrated in the odds estimate, not the designed rules). Hype share is the same 60% it was in v1.

## Required changes (one more revision, mechanical in nature)
1. **Fix Hype dominance.** Cap Hype added per lot (for example at most +3) or count only the top 3 burned cards per category. KPI: Hype share of points 45-50% (now 56 / 64%), with the lone gap staying at least 20 and mixed gap at least 5.
2. **Cut or strengthen open income.** It fails the ablation and is a human memory burden. Either drop shown income (draw face down; simpler, saves rules text) or make it matter. KPI: no-memory ablation at least +5, or the rule removed and the lone gap re-measured at both counts. Re-check ignore-ties and ignore-hype with a smarter full bot to settle the sign flips (L1).
3. **Calm the end.** Keep a running crash-tie-break total on the Hype rows, or freeze Hype changes before round 14. KPI: last-round flip at most 20% at 6p (now 27%).
4. **Re-run at the final 78-card 1-11 config at both 5p and 6p** with at least three reference bots (greedy, no-memory, strategic) plus a spite bot. KPI: gaps and seat gap at both counts (L2, L8).
5. **Trim rules text.** KPI: rules about 100 lines or less, and the teach time stated (L7).

## Is another revision worth it?
**Yes, one more cycle: the issues are mechanical (a Hype cap, dropping or fixing open income, a visible tie-break) and the skill gap has already moved, so the next revision should target Hype share of points (now 56 / 64%, target 45-50%) and the two failed ablations.** If Hype share and the ablations do not move, stop and put the game in front of humans or park it, because the remaining problems would then be about the design itself.
