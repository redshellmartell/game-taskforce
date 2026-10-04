# Critique: Nine Fields (rules v1, revision 0)

**Verdict: REVISE-MINOR**

Fun and market fit are judged from `panel.json` only. The AI persona reviews were not approved, so there is no `panel-report.md`. Those two scores rest on bot-predicted numbers and are less certain than a written panel review.

## Scores (1-5)

| Area | Score | Note |
|---|---|---|
| Originality | 4 | See below |
| Rules clarity | 3 | One page, but several edge cases are unwritten |
| Fun | 3 | Strong core decision; 2p and the stall endings drag it down |
| Balance | 3 | 3-4p pass every KPI; 2p fails two |
| Market fit | 4 | Matches the brief's gap; a hard sell to casual and family players |
| Production | 5 | 30 cards and 16 pawns, nothing else |
| **Average** | **3.67** | Above the 3.5 pitch bar, but only just |

## Originality (4)

I ran one web search on top of the brief's comparables. It found Kahuna (12 islands joined by bridges, area control), Island of Gems (a 3x3 placement game with gems and patterns) and Contactics (static 3x3 area control). None of them uses overcrowding to push a row or column and drop an island off the edge. Shifting Stones is pattern scoring, as the brief says. Nothing here copies another game's rules or text.

- **Closest existing game: Contactics (similarity low).** It shares the 3x3 grid and area control, but its board is static.
- **Mild risk:** Kahuna gives the same "fight for island majorities with few pieces" feel. That is an acceptable overlap.
- The flood-trigger choice (which end falls) and the quarter-turn axis swap are genuinely new.

## Rules clarity (3)

A new player could learn the loop from `rules.md`, because the turn is one action and a clear flood procedure. The weak spot is the flood step: finding the line from the card's axis and then choosing which end falls. The playtester flagged this as the likely stumbling block. The playtester's own ambiguity list shows the rules are not yet at "zero ambiguities", which is a pitch KPI. Gaps to close:

1. State that a flooded island that itself falls off is not turned.
2. State whether the stall limit ends the game before or after the 3 x players-th turn.
3. State the final tide's reading-order scoring, and that pile sizes update as each island is scored. This affects the tiebreak.
4. State what happens when two tied players have equal pile sizes at the final tide.
5. Add a worked flood example. Crown Island flooding three times in six turns is a good one.
6. Define "full" against "floods" in one line: full is count >= capacity, and a full island can never be Landed on.

Casual and family bots hit the "rules overhead" peeve, and `rules_simplicity` scores 0.43. That is a warning for the weakest audiences, not a blocker.

## Fun (3)

- **The best part.** The trigger player's binary choice is a good one: cash this island now, or push the far end off and keep a locked prize. The next island is visible, so play is tactical. The 2-ply bot beats the 1-ply bot 68% at 2p, so depth is rewarded.
- **The weak part.** The narrated game was not fun in the middle. Turns 12 to 19 were Sail-shuffling because nobody wanted to trigger a flood. The game then ended on the stall limit with scores 8-7-9, and the final tide gave the winner about half their points. That is a poor ending: the middle game barely mattered and the end was a surprise only because values are hidden.
- **Ties.** 11.4% of 3p games and 17.4% of 4p games tie on points before the tiebreaks, and average margins are 2-3 pearls. Outcomes feel close, but many games are decided on tiebreaks that favour later seats.
- **Panel predictions** (from `panel.json`):
  - Average fun is 3.82. Competitor is highest at 4.52, then Bar Raiser 4.17 and strategist 4.09.
  - Family is lowest at 3.11, story 3.43, casual 3.61.
  - Casual, family and story bots win only 6-15% of games, so mixed tables are hard on casual players.
  - The Bar Raiser veto is not active.
- This is a game for planners. It will not suit a family table.

## Balance (3)

Against the KPI targets in `CLAUDE.md`:

| KPI (target) | 2p | 3p | 4p |
|---|---|---|---|
| Seat gap (<= 5) | 1.3 pass | 1.9 pass | 3.2 pass |
| Strategic vs random (>= 20) | 97.3 pass | 59.6 pass | 37.9 pass |
| Length within +/-20% of 20 min | 16.8, -16% pass | 22.2, +11% pass | 22.6, +13% pass |
| Runaway leader (<= 65%) | 68.7% **fail** | 53.6% pass | 43.2% pass |
| Lead changes (>= 2) | 1.77 **fail** | 3.37 pass | 3.69 pass |

Other points on balance:
- **2p root cause.** 58% of 2-player games end on the stall limit, with only 14.5 of 22 floods played. Length has a standard deviation of 17.6 turns, so the game is erratic.
- **3p stall.** The narrated 3p game showed the same stalling at the table, even though the sim says only 5% of 3p games end that way. Human players may stall more than the bots do.
- **Fix untested.** The playtester's "storm" fix has not been run. Experiment 2 showed that only lengthening the limit does not fix the runaway rate (69.4%).
- **Pace is an assumption.** The minutes estimates rest on an assumed pace. 3-4p sit near the 25 minute cap.
- **Cards.** No dead or dominant card class. Value-1 cap-2 islands are weakest and value-4 are strongest, which is acceptable.
- **Tiebreaks.** The final tiebreak favours later seats. It is within KPI but the rule is not neutral.
- **Direction choice at 3p.** The 2-ply bot barely beats greedy at 3p. This may be a bot limit, but it could be kingmaking noise in the direction choice. Human play is the only way to check.

**Which player counts it is good for:**
- **3-4 players:** good. All KPIs pass.
- **2 players:** not good as written, until the stall problem is fixed.
- If the revision is declined, the safe fallback is to pitch it as a 3-4 player game, or drop 2p from the box.

## Market fit (4)

The game still matches the brief: a micro area-control game on a 3x3 grid of cards, shifting islands, under 40 cards and 16 pawns, about 20 minutes. It has not drifted. Demand was always "moderate, not proven" in the brief. The panel numbers (average fun 3.82, would-buy "yes" for competitor, strategist and Bar Raiser, "maybe" for the other three) support a niche abstract-leaning audience, not a family one. The brief targeted hobby-light players, so a 3.1 family score is a real gap against that target. The 2p-fail makes the "2-4 players" box claim weak.

## Production (5)

30 island cards and 16 pawns in 4 colours. Nothing else, and no hidden-information components beyond face-down trophy piles. Cheap and easy to prototype: the sheet can be cut from standard card stock and the pawns can be any cubes. The only awkward part is the quarter-turn mechanic, which needs cards that read clearly when turned. Axis arrows must be unambiguous on both orientations. Estimated prototype cost is low (about $10-15).

## Biggest strength

The flood-trigger decision. One simple action, and every Land creates a real dilemma over which end of the line falls, plus a visible next island to plan around. The quarter-turn axis swap adds foresight without adding rules. It is original and deep at 3-4 players (lead changes 3.4-3.7, strong skill expression).

## Biggest weakness

The stall limit. When nobody wants to trigger a flood, the game stalls into pointless Sail-shuffling and then ends early. At 2 players this is the main cause of the two failed KPIs. The narrated 3p game shows it can also happen at the table with three players.

## Required changes (REVISE-MINOR)

1. **Replace the stall-limit ending with a storm.** After 3 x players turns without a flood, the fullest island floods and the next player picks the direction. The deck then always completes. Targets: 2p stall-end rate down from 58% toward 0%, 2p lead changes from 1.77 to 2 or more, 2p runaway from 68.7% to 65% or below, 2p length standard deviation down from 17.6. Re-check 3p stall-ends and length, which are near the 25 minute cap.
2. **Test a neutral last tiebreak.** Use most islands, then fewest pawns left on the board, in place of the "later seat wins" rule. Target: keep the seat gap at or below 5 at all counts, and reduce wins decided on the seat tiebreak.
3. **Fix the six rules gaps listed above and add a worked flood example.** Target: zero rule ambiguities at pitch, and a better clarity score.
4. **Shorten 3-4p play if it stays near 22 minutes.** Options are dealing 18 islands, or a stall limit of 2 x players. Target: 3-4p length at or under 22 minutes, further from the 25 minute cap. Only do this if the storm change does not already lengthen the game.
5. **Recommended, not required:** a human test at 3p, for the direction-choice kingmaking concern and the mid-game stall.

## Is another revision worth it?

**Yes.** The problem is clearly diagnosed (stall endings), the fix is small and testable, and 3-4p already pass every KPI. One loop should move the 2p KPIs, and the average of 3.67 only has to rise a little to stay above 3.5. If a revision is declined, pitch it as a 3-4 player game only.
