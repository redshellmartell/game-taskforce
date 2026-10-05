AMBIGUITIES = [
 "Retool spade cost: 'the replaced card is ignored' simulated as the replaced rank not counting its suit, only the new card does (a 6S replacing a 6D gets the new card's Spade discount, nothing from the old card). The text does not say this outright for the case where the replaced card is itself a Spade.",
 "Hand-limit scrap happens after Gears and payment, so cards taken by Gears this turn can be scrapped; stated, but a player may think Gears cards are protected.",
 "Solo: the Rival pile counts only the higher card each turn, so it reaches 24 only after 24 Rival actions; if the Bench ever held fewer than 2 cards the pile and the turn count would drift apart (never happened in 12,000 solo games, all ended on turn 22-25 by the pile, but the card-count and turn wording are both used: 'end of your 24th turn' versus 'pile holds 24').",
 "Deck-empty clock: a Bench card slid under an empty deck in step 3 makes the deck non-empty, so the deck-empty clock only strikes when the deck is empty after the trim and refill. Stated in rules; simulated as written. Passes still occur 0.04% of 4p games after the strike.",
]

VERDICT = "NEEDS-FIXES"
REVISION = 1
PROBLEMS = [
 {"severity": "high", "problem": "Solo is still far too easy and no longer separates skill. Win line 31 is met by 98.8% (strategic), 99.1% (lookahead), 97.4% (greedy); random 0.6%. A greedy bot is as good as the best bot (median 38 vs 40-41), so the solo ladder (Journeyman to Grandmaster) is meaningless.",
  "evidence": "2,000 solo games per bot, Rival takes 2 highest. Score quartiles (strategic) 36/40/44; greedy 35/38/42. Making the Rival take 3 per turn changes nothing (strategic >=36 82.8% vs 83.0% estimate). Win line at 40 gives strategic about 52%, greedy about 40%, random about 0%; strategic win rate by line 31:99 33:95 35:87.",
  "fix": "Move the win line to 40 and rescale the ladder (about 32 Tinkerer, 40 Journeyman, 44 Master, 48 Grandmaster); and because greedy is only about 12 points below strategic, add a real solo pressure (for example the Rival also takes a Diamond or Heart from the Bench before the player's next turn, or a hand limit of 5 in solo). Re-test; solo is currently a puzzle with a free win."},
 {"severity": "medium", "problem": "Spades still have a negative win correlation, so the engine is not the strongest line. Neither discount 4 nor 2-point Spades fixes it.",
  "evidence": "Spades: -0.035 (v2 as written), -0.015 (discount 3, 2 points), -0.020 (adding the 3-card Gear Gather); Clubs +0.049 / +0.056 / +0.072; Hearts +0.098 throughout. Spades are built in 14% of workshops vs 22% for Diamonds. In the log Spades are mostly paid away as money. Fix is not just a number: a Spade only helps when it sits in a train next to two other engine cards, which one card per turn rarely gets.",
  "fix": "Try 2-point Spades with discount 3 together with Gear Gather (the best of the three configs, lead changes 2.46-2.71) and re-measure Spade correlation; if still negative, give Spades the 'pay' role in the design (they are the best currency) and accept it, but then drop the claim that engine-first is the strongest line. A human test of the engine line is needed because the bots do not plan trains."},
 {"severity": "medium", "problem": "Strategic beats greedy only 59.0% (KPI 60%), and a lookahead bot beats strategic 54.5% (so there is skill depth), but greedy is nearly as good as strategic everywhere except Retool.",
  "evidence": "2p: strategic v greedy 59.0, lookahead v greedy 61.3, strategic v random 99.9 (gap 67.8 points). Retool off: strategic v greedy 51.1 (so Retool provides about 8 points of the skill gap and +0.06 lead changes). 4p mixed table: lookahead 37.8, strategic 33.5, greedy 28.6.",
  "fix": "Keep Retool (the main source of skill). Spade discount 3 with 2-point Spades gave 61.2% for strategic and 63.5% for lookahead v greedy, so both reference bots pass 60%; adopt that if the Spade fix in problem 2 is wanted anyway (judged on both bots, not tuned to one)."},
 {"severity": "medium", "problem": "In 4-player games the printed clock target (10 workshop cards) almost never ends the game: 85% of games end because the deck empties; Retool is used only 0.4 times per game, so it rarely matters.",
  "evidence": "4p strategic mirror: deck-empty ends 85% (3p 2%, 2p 0%); retools 0.4/game (2p 0.6). With Retool on, lead changes 2.32 at 4p (KPI 2.5, miss) vs 2.29 with it off. Estimated 4p length 17.7 min vs 20 (-11.5%, inside the 20% band).",
  "fix": "Either state the 4p end plainly as 'the deck runs out' (and drop the 4p card target from the rule card) or raise the deck pressure so Retool pays off; add a human check on 4p length. The 2.5 lead-change floor is met at 3p (2.49 as written, 2.71 with Spade 2 points)."},
 {"severity": "low", "problem": "Exact score ties are common at 3-4 players (10.5% and 12.9% of games have a tied top score); tiebreakers resolve them, shared wins under 1%.",
  "evidence": "Strategic mirror, 2,000 games per table size.", "fix": "None needed; keep the tiebreak chain."},
 {"severity": "low", "problem": "Solo length is 24 turns, about 7.5 estimated minutes (25 s build, 10 s gather) against the designer's 10-minute figure.",
  "evidence": "Real turn count 23.8 (strategic), 24.0 (greedy), 23.8 (random); 12 builds and 12 gathers per game.",
  "fix": "Accept with a human timing check; solo turns have thinking time the formula omits."},
]
ESTIMATED_MINUTES = 17.7
TARGET_MINUTES = 20
