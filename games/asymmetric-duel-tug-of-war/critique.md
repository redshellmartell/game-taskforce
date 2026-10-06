# Critique: Tug of Crowns, revision 2 (cycle 2, rules v3)

All numbers are bot simulation; no human has played this game.

**Verdict: REVISE-MAJOR (recommend PARK, no further auto cycle). Average 3.17 (was 3.33).**

## Bar Raiser veto (first)
Veto is ACTIVE: seat advantage of 9.3 points. It stays in any pitch's "Remaining risks". The game must not be pitched without an explicit owner decision. The 9.3 is also flattering. It is an average of absolute gaps of +20 (random mirror, Treasurer 60.2%), -29 (greedy, 35.3%) and -19 (strategic, 40.5%, or 44.0% on a second run). Which side is stronger depends on which bot you ask. The two better bots both say the Whisperer is stronger, and the weaker bot says the opposite (L2).

## Applying my own parking rule
Last critique: "if the side gap stays above 8 or fun below 3.3 after revision 2, park the game." The side gap is 9.3 on the headline and 10-19 in the strategic mirror, which is above 8. Panel fun is 3.51, above 3.3. The gap condition fires, so the rule says park.

## Scores (1-5)
| Area | Score | Why |
|---|---|---|
| Originality | 3 | Core mechanic unchanged, so not re-searched. Closest is Tug of Roar (medium). Asymmetric decks plus a tug track is a known space; Hush, Retort and Echo are the only distinctive part, and bots cannot show that they matter. |
| Clarity | 3 | Zero ambiguities and the wording is tidy. But the file is about 250 lines with 6 keywords plus Retort timing against the brief's "one page, 3 special rules" (L7). The panel's rules_simplicity metric is 0.0 for every persona and every persona hit the heavy-rulebook peeve. Retort timing (4.4) is hard to teach. |
| Fun | 3 | Panel average 3.51, but casual 3.05, story 3.09 and family 3.25 sit below the 3.5 line. The playtester's narrated game says round 1 is a 6-card dump, rounds 2-4 are flat, decisions are mostly "play or pass", and Retort never came up. |
| Balance | 2 | Side gap fails in all three mirrors, in opposite directions. The Treasury cap knob is inert (cap 2 vs 3 differs by 1-2 points). All five keyword ablations fail (L1). Whisper (+20) and Seal (+23) are outliers. |
| Market fit | 3 | Still a 2-player, 15-minute, cheap card game as briefed. But the "asymmetric" promise rests on keywords that do not change best play, so the asymmetry is mostly a difference in card totals (58 vs 42). |
| Production | 5 | 47 cards, no other parts, trivial cost. |

Average (3+3+3+2+3+5)/6 = 3.17, below the 3.5 pitch bar.

## Playbook check
- **Comeback (L3): met.** Lead changes 2.22, runaway 44%, games over by round 3 18.5%, length 13.1 min (target 15 +-20%). Pacing is genuinely fixed. The playtester notes that the comeback comes from the track shape and not from the advertised court draws (draws off: +0.09 lead changes for strategic, needs +0.3).
- **Twist ablation (L1): failed on every keyword.** never-Spend -0.1, ignore-Steady -0.9, no-Echo-throw -3.1, random Hush +3.1, never-Retort +1.9; each needs 5 or more. The designer wrote the ablation tests, which is good, and they ran, but they show the twists do nothing for these bots. This is the same failure as duelflip and the other games named in L1.
- **Two or more bots (L2): done, and it shows the problem.** The side gap flips sign with bot strength.
- **Target band and knob (L5, L8): knob inert.** The one declared knob moves nothing.
- **Rule budget (L7): over.**
- **Skill gap (L6): ok.** Strategic beats random by 45 points. Strategic beats greedy by only 62%.

## Biggest strength
Pacing and structure now meet the KPIs: lead changes 2.22, runaway 44%, early finishes 18.5%, length 13.1 minutes, no dead cards and no ambiguities, for a 47-card box. Cycle 2 did what it was meant to on those targets.

## Biggest weakness
The two decks are not balanced against each other, and the "asymmetric" keywords have no effect on best play. Revision 2 removed the lead dial (L9 mechanical part) and the gap just moved to a different place. Treasurer wins 60/35/40-44% by bot strength, no tuning lever (cap, Whisper 5 to 4, Gold Purse) moves the strategic mirror by more than about 4 points, and none of the five keywords passes ablation. This repeats L1 (inert twist), L2 (verdict depends on the bot) and L9 (mechanical fixes move scores, structural ones do not).

## Is the problem structural? Yes.
Two cycles on the lead mechanic and two levers on the decks have left the gap at 9-19 points. Pacing improved, balance did not. The balance gap comes from two asymmetric decks whose power depends on how well each bot uses keywords, and the keywords are inert, so there is nothing to tune. Fixing it means redesigning the keyword layer (for example giving Hush and Spend real, testable stakes), and that is a new game, not a third cycle.

## Required changes (only if the owner overrides the park)
1. Rework the keyword layer so each of the five passes ablation by at least 5 points. KPI: all five ablations at 5 or more.
2. Then rebalance with Whisper 5 to 4 and Seal 6 to 5 together, checked against three bots (random, greedy, strategic plus the plus bot). KPI: strategic mirror 45-55% and no mirror outside 40-60%.
3. Cut the rules to six lines of keywords. KPI: rules file about 100 lines or less (L7); clarity score up.
4. Cheap play-pattern fix to consider on its own: a two-game side-swap format (each player plays both sides, winner takes the better total margin). It would hide the side gap without fixing it, so it is a workaround and not a balance fix.

## Is another revision worth it?
No. The remaining problems are structural: the keywords are inert and the side gap flips with bot strength. The last two cycles fixed pacing but not balance, and my park condition (side gap above 8) is met. Recommend park; kill only if the owner wants the idea-bank entry closed.
