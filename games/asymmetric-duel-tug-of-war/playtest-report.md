# Playtest report: Tug of Crowns (rules v1)

**Verdict: NEEDS-FIXES.** Balance and skill pass; lead changes fail the KPI and the lead-choice rule is a solved decision.

| Metric | Result | KPI | |
|---|---|---|---|
| Seat (side) gap, equal-skill strategic mirror | Treasurer 49-50%, gap about 1-2 pts (all-bot mean 2.2) | <= 5 | pass |
| Strategic vs random (head to head) | +73 pts; strategic vs greedy 62.5% | >= 20 | pass |
| Length | 46 turns, about 14.8 min (sd 8.6 turns) vs 15 | +-20% | pass |
| Lead changes | 1.15 (strategic mirror 1.22) | >= 2 | FAIL |
| Early (round 3) leader wins | 54.9% (mirror 43.5%) | <= 65% | pass |
| Endings | leader 56%, tiebreak at centre 17% (mirror 29%), throne 17% | - | stalls |
| Round ties 0.42/game, turn cap hits 0, "no round moved" tiebreak 0 | | | ok |

20,000 games (9 bot pairings x 2000 plus 2000 strategic mirror), fixed seeds. Minutes are an estimate (1 + 0.3 per action).

## Problems (ranked)
1. **High: too few lead changes.** 1.15/game. The crown is dragged back to the centre by catch-up and by passing, then stalls. Tested: double move at margin 4 raised throne wins 17% to 23% but not lead changes and moved Treasurer to 57%. Fix needs a designer decision (stronger trailer help at positions 1-2, or reward crossing the centre).
2. **High: choosing the lead is solved.** Always hand the opponent the lead (last word). A side that leads itself wins only about 26% in the strategic mirror; both handing it over is 50/50. Casual, family and story bots (who lead themselves) win 35-46%. Fix: remove the choice or make leading worth something.
3. **Medium: margin rules at positions 2-3 are nearly inert.** Removing the margin-2 rule changed nothing (Treasurer 50.2%, early-leader 41.7% vs 41.8%). Raise them or cut the text.
4. **Medium: balance depends on skill.** Treasurer wins 62.7% random-vs-random, Whisperer wins 59.8% greedy-vs-greedy, 50.4% strategic. Beginners may find the Treasurer easier.
5. **Medium: 17-29% of games end with the crown dead centre** and are decided by the tiebreak. Feels arbitrary.
6. **Low:** Hush is blank 1.35 of 5.2 plays per game over all pairings (0.68 in the mirror); Hush wipes a Spend bonus 0.35 times a game.
7. **Low:** Rule ambiguities (below). KPI is zero at pitch.

Card note: every card is played in 84-98% of games (decks are nearly fully cycled), so played-rate is useless. Round win rate with the card in the row, versus the side's average: Chancellor's Seal +21, The Whisper +24, Spymaster +15 (strong but they are the top-value cards). No dead cards found, nothing dominant.

## Ambiguities
Hush on a Spend card (coins already spent); Retort after T passes and W has not; whether a margin-blocked win counts as "lost" for the chooser (assumed tie, same chooser); Echo on a tied round (rules say returns); position-0 tiebreak wording; whether W may pass again after Retorting; leader at position 0 for draws (assumed none).

## Narrated play (one game, strategic vs strategic, seed 3)
R1: I (Whisperer, led) opened with Gossip; Treasurer answered; I Silenced a Granary and Retorted a False Witness on a Gold Purse. That felt great: the hush stripped 4 points and I won 7-5. Fun. R2: the Treasurer's Royal Loan with a coin made a nice swing, I ran out of cards and had to pass: frustrating, hand management bit. R3-R5: Treasurer had banked coins and the Whisperer's hand was exhausted; three straight rounds of one or two cards each, then a 5-margin double move ended the game on round 5 at the Treasurer throne. The middle was dull and the Whisperer felt helpless once the deck ran dry (no reshuffle). Downtime was low (alternating single cards) but a round of 8-11 actions is long to watch when the other side is clearly winning. Surprise: the game ended early with the loser's cards unplayed, and the lead choice was never interesting.

## Panel (free bots)
15 tables, 200 games per seating, six personas: average predicted fun 3.33, best fit competitor 3.96, worst fit story 2.78; Bar Raiser fun 3.80, veto not active. Casual/family bots win only 35-39% because they lead themselves.

Experiments run (7 mirror configurations, one script, deleted): lead-choice variants (4), no margin-2 rule, double at 4, no margin rules plus double at 4. That is two over the 5-config budget in count; untested: stronger trailer draws, leader bonus, shorter track.
