# Critique: Fifty-Two Workshop (revision 1)

**Verdict: REVISE-MINOR**

Average 3.67 (pitch KPI 3.5). Up from 3.17. Multiplayer now passes nearly every KPI. Solo is still a free win. The engine suit (Spades) still does not pay in the data. Originality was not re-searched: the core mechanic did not change (Retool is a variant of build-over), so the revision 0 judgement stands (low similarity to Sprawlopolis and the other comparables).

## Scores (1-5)

| Area | Score | Why |
|---|---|---|
| Originality | 3 | Unchanged. Suit as function, rank as cost and adjacency as power on one standard deck is a fresh combination of familiar parts (rummy runs, market row, pay-to-discard). Retool adds some identity. |
| Clarity | 3 | Up from 2. Eleven ambiguities closed, Apprentice cut, exactly three special rules, full legal-action table. Four minor ambiguities remain (Retool of a Spade, hand-limit scrap hitting Gear cards, solo "24th turn" wording, deck-empty after a trim). The Retool and Bench-trim rules still need a worked example. One rule card is tight. |
| Fun | 3 | Panel predicted fun 3.93 (Family 2.96). The narrated game is weaker: Spades and Clubs were spent as payment at once, no train beyond 3, no Retool happened, flat finish at 18/18/17/18. The designed arc (engine, ride, cash out) was not seen in bot play. Retool is used only 0.4 times per game, and 85% of 4p games end on an empty deck at 6-8 cards, so the printed clock target of 10 is vestigial. Bots cannot judge whether humans find the arc fun. |
| Balance | 4 | Multiplayer passes: seat gap 1.2/0.6/1.2, strategic beats random by 67.8, runaway 55/41/34%, no stalls, no dead cards, 4p length within 12%. Misses are narrow: strategic vs greedy 59.0% (target 60%), 4p lead changes 2.32 (2.5). Not fixed: Spade win correlation -0.035, and the Story/Hearts bot still wins most. Solo fails outright (98.8% strategic, 97.4% greedy), so solo is held back from 5. |
| Market fit | 4 | Still matches the gap (one deck, a rule card, 1-4 players, about 20 minutes). Drift: solo was a first-class goal in the brief and is currently no game. Interaction is real in multiplayer (public payments, shared Bench). |
| Production | 5 | One standard deck and one rule card. |

## Biggest strength
A zero-cost physical product with a clear hook and multiplayer numbers that now pass: seats, skill gap, runaway, length, no stalls.

## Biggest weakness
The promised engine arc does not show up in the data. Spades lose, Retool is rare, and most games end on the empty deck before trains get long. Solo is also trivially won (98.8%).

## Specific changes required (small tuning pass, no new rules)

1. **Adopt the already-tested config: Spade discount 3 and Spades worth 2 points.** It gave strategic vs greedy 61.2% (lookahead 63.5%) and 4p lead changes 2.61, so it clears both near-misses. Spade correlation only improves to -0.015. Moves: Balance (skill gap, lead changes).
2. **Solo win line 31 to about 40, ladder rescaled** (strategic about 52%, greedy about 40%, random about 0%). It was sized from score medians and not re-run. It must be checked by a quick sim before it goes on the rule card. Moves: Balance (solo).
3. **State the 4p end honestly.** Say in the rules and design notes that at 3-4p the game normally ends when the deck runs out, with the 10-card target as the early finish. Do not add deck pressure. Moves: Clarity.
4. **Close the 4 minor ambiguities** with one sentence each, and add a Retool worked example. Moves: Clarity (target zero).
5. **Drop the claim "engine first is the strongest line"** from the design notes. The data does not support it, and bots do not plan trains. Keep it as a hypothesis for the first human playtest.

## Pitch, revise or park?

**Recommend: pitch as a multiplayer game (2-4 players), with solo flagged as unproven.** Do not run a full revision loop. Changes 1 to 5 are edits the Director or designer can make in one short pass. Change 2 needs one cheap sim re-run (a handful of games, not a full playtest). Remaining risks to list in the pitch:
- the engine and Retool arc is untested with humans;
- Spades are mostly spent as currency;
- solo is unbalanced and its length is unmeasured (7.5 min by formula);
- 4p ties run 10-13%;
- Family persona predicts fun of only 2.96.

The right next step is a physical test: it costs one deck and a printed card, and it answers the open question better than bots can.

## Is another revision worth it?
No: the remaining issues are small or cannot be tested by simulation. The Spade correlation stayed negative in every configuration tried. A further loop is a guess, and the real answer is a human playtest. Apply the tested config and the solo line as a tuning edit, then pitch.
