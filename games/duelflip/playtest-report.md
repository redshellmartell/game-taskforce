# Duel Flip - Playtest Report (v2 rules re-test)

**Verdict: NEEDS-FIXES (minor, one more loop at most).** v2 fixed the three things that were truly broken in v1: seat balance, dead first-flip busts, and the permanent "1 lock". The game is fair, always ends, and skill clearly matters. But three of the pitched twists are still close to inert: "leave lowest" is still the right answer about 3 turns in 4, the species bonus (even at 8) decides only about 5% of games, and the Lifebuoy refund changes nothing measurable. None of these makes the game unplayable. They make it a solid, simple push-your-luck game rather than the "bait and majority" game the rules advertise.

Code: `/home/user/game-taskforce/games/duelflip/sim/` (`game.py` v2 rules, `bots.py` 8 bots, `run.py` round robin and mirrors, `experiments.py` / `experiments2.py` knob and strategy tests, `trace.py` move logs). v1 code is archived in `sim/v1/`. Fixed seeds. Run `python3 run.py 2000`.

## Key numbers (v2 as written: 1 Lifebuoy each, seat 2 +3, safe scout, mandatory 2nd flip, refund at 4, take all leftovers, species bonus 8)

| Metric | v1 | v2 |
|---|---|---|
| First-seat win rate, mirrors | strategic 42-43% (rules as written), 51-55% with equal buoys | random 48.0, greedy 51.8, bank_early 51.4, pusher 50.6, strategic 51.9. Within 5 of fair for every bot. |
| Same, no +3 compensation | n/a | greedy 53.4, bank_early 54.0, strategic 53.9. So +3 is about right; +4 gives 50.5-51.2. |
| Strategic vs random | 95% | 82.5% (84.5% in the second run) |
| Strategic vs greedy / pusher / bank_early / collector | 61 / 64 / 98 (bank_early) / 80 | 62 / 63 / 63 / 63 |
| Strategic average over all 7 opponents | 84% | 66.9% (next best: greedy 54.9, bank_early 54.2, refund_pusher 54.1) |
| Game length (turns) | strategic 27.7 (19-39), random 34, bank_early 60 | strategic 23.5 (17-29), greedy 23.4 (20-26), random 22.3 (17-27), pusher 17.6 (15-21), bank_early 29 (25-30) |
| Ties | 0.5-0.8% | 0.1-0.8% |
| Games hitting the 500-turn cap | 0 | 0 |
| Dead turns (no effect) | 9-12% of turns | 0.0% exactly zero; 4.3% of turns move the haul balance by 3 points or less |
| Busts per game | 5.6-8.6 | 4.4-5.9 (bust turns are 19-33% of turns, by bot) |
| Lead changes per game | 3-5 | 2.4-3.9 (bank_early 6.9) |
| Leader after the first third wins | 67-75% | 66-70% |

Round robin, win% of row vs column, n=1000 per pair, seats alternate:

| | random | greedy | bank_early | pusher | refund_pusher | hoarder | collector | strategic | avg |
|---|---|---|---|---|---|---|---|---|---|
| random | - | 26.8 | 18.2 | 40.5 | 30.6 | 36.9 | 30.9 | 16.3 | 28.6 |
| greedy | 73.9 | - | 54.2 | 53.0 | 49.7 | 65.3 | 51.1 | 37.4 | 54.9 |
| bank_early | 79.1 | 48.3 | - | 52.6 | 45.5 | 63.9 | 53.9 | 36.2 | 54.2 |
| pusher | 63.5 | 47.0 | 49.2 | - | 45.8 | 55.4 | 48.0 | 37.5 | 49.5 |
| refund_pusher | 66.6 | 49.6 | 52.6 | 54.1 | - | 59.3 | 53.4 | 42.9 | 54.1 |
| hoarder | 59.5 | 36.0 | 37.2 | 41.5 | 39.0 | - | 37.6 | 24.9 | 39.4 |
| collector | 68.4 | 47.2 | 47.5 | 50.9 | 48.3 | 58.8 | - | 34.5 | 50.8 |
| strategic | 82.5 | 62.0 | 63.0 | 63.0 | 58.5 | 76.1 | 62.9 | - | 66.9 |

Bots: random; greedy (flip to 12 pile points, buoy on clash, leave lowest); bank_early (exactly the 2 mandatory flips); pusher (flip to a pile target); refund_pusher (flip to 4 cards); hoarder (never spends its Lifebuoy); collector (3 flips, species-aware leave); strategic (EV flip rule that knows about clash odds, Lifebuoy and refund, plus a bait/species-aware leave).

## Questions asked, v1 vs v2

**1. Seat balance: FIXED.** Seat 1 wins 50.6-51.9% for every non-random bot with +3, against 53-54% without it. The 1-point rule in v1 (second player with a Lifebuoy extra) is gone. Random bots give 48% to seat 1, a small over-correction from +3 that a human will not notice. Residual: no bot is further than 2 points from fair.

**2. Does "leave the lowest card" still dominate? Mostly yes, and it is the main remaining problem.** Win% of each bot when it uses another leave rule against the same bot leaving lowest (n=2000):

| Bot | leave highest | leave random | leave "most copies left" | leave species-aware | leave smart (bait + species) |
|---|---|---|---|---|---|
| greedy | 23.8 | 35.8 | 49.5 | 46.5 | 52.2 |
| strategic | 16.7 | 31.3 | 47.9 | 45.0 | 52.6 |
| bank_early | 7.6 | 24.1 | 39.3 | 42.3 | 46.5 |

- v1 reference: highest 17.6%, random 30.1%, bait rule 46.0%. So no real change. Leaving a high card is still a clear mistake, and the best clever rule I could build is worth only +2 to +3 points over "lowest".
- The smart rule picks the non-lowest card in 24% of choices, and 98% of banks have a real choice of 2 or more cards. So there is a decision every turn, but the answer is "lowest" three times in four.
- What did improve: the leftover can no longer sit in the river for 24 turns. Bait is claimed back by a bust about 1.4-2.6 times per game (roughly 8-10% of turns), so bait is visible and exciting. It just is not worth leaving a bigger card for.
- Dropping "must take leftovers" (take_leftovers=False, a leftover may stay) lets "leave lowest" beat "leave highest" 78%, so the forced-take rule is not what made leaving high bad. Leaving high is bad simply because you gift the card.

**3. Dead-turn rate: FIXED.** 0.0% of turns have exactly zero effect (v1: 9-12%). 4.3% of turns move the haul balance by 3 points or less. Safe scout works: 0.5-1 flips per game are scout discards. A new minor issue: 1-card busts (a clash on the mandatory second flip, so you lose only your first card) are 2-4 per game, about 10-17% of turns. They hurt little (average bust pile is 5.6 points, 49% are 5 or less, none reach 15), so they feel like small tax turns, not dead turns.

**4. Does bank-early dominate? No, but the landscape is flat.**
- bank_early (exactly 2 flips) wins 36% vs strategic, 48% vs greedy, 53% vs pusher. It is on par with greedy as the second-best simple bot (54% average). It is not dominant, but it is a viable "do the minimum" line.
- The mandatory 2nd flip did end the v1 degenerate mirror: bank_early now has 2.9 busts per game (v1: 0) and ties are 0.8%, not 2.6%. With the second flip made optional the mirror goes back to 0 busts, 60 turns, no interaction. So the rule is doing its job.
- Pusher target sweep vs strategic (win% of pusher): 4 -> 35.0, 8 -> 35.2, 12 -> 37.5, 16 -> 39.5, 20 -> 37.3, 30 -> 20.6. Pushing deep is not rewarded: anything from 4 to 20 scores about the same. v1 had a clear sweet spot at about 12. The reason is that the first-flip scout gives a free safe card, the second flip is forced, and then each extra flip faces about 25-35% clash risk against a river that is growing.
- Average bank pile is 2.4-3.2 cards, so reaching 4 cards is uncommon.

**5. Do decisions matter? Yes.** Strategic beats random 82-85% and every other bot 58-63%. The gap is mainly the flip-or-stop rule (strategic with a plain "leave lowest" still beats greedy 60.8%, while strategic's leave rule alone, put on a greedy bot, is worth 48%, i.e. nothing). Buoy spending threshold: spending at a pile of 0-9 is identical (49-50%); thresholds of 14 and 20 lose (43%, 29%), and never spending loses 22%. So "spend it, don't hoard it" is still correct. Hoarder vs greedy: 36.8%.

**6. Lifebuoy refund: inert.** Strategic mirror with refund at 3 / 4 / 5 / never gives seat-1 win rates of 55.5 / 51.7 / 50.2 / 51.5%. Refunds happen only 0.56 times per game. Players use 2.04 Lifebuoys per game and finish with 0.5 ready on average. Refund at 3 shortens the game (21.0 turns) and re-tilts the seats toward seat 1 (55.5%), so do not lower it. Holding a Lifebuoy is still not an interesting decision, because spending always wins. The refund neither hurts nor helps; it is almost unused.

**7. Species bonus at 8: still weak.** It flips the winner in 4.8% of games (v1: about 4% at bonus 5, 4.8% at 7). Each player takes about 2.5-2.8 species per game. It is a tiebreaker-sized effect. The species-aware leave rule scores 45-47% against plain "lowest", so chasing species costs more than it gains.

## Problems, ranked

1. **(Medium) Bait/leave decision is solved by "leave your lowest card".** Evidence: table in question 2. Suggested fixes (untested, in order of how cheap they are):
   - Make bait pay: when a bust hits your bait, the bait returns to you and the opponent's pile is worth double for you (or you also take one random card from the opponent's haul). A larger payoff changes the maths for a mid card.
   - Make the opponent's second flip riskier for a high bait: after scouting the first flip, the bait stays live. It already is; instead raise the bait payoff as above.
   - Alternatively, make the species bonus bigger (problem 2) so that cards of a species the opponent is chasing are never safe to leave.
2. **(Medium) Species bonus decides only about 5% of games** and species strategy is a net cost. Suggested fix: score the bonus per card of margin (for example +3 per card ahead in a species) or raise it to 12-15, then re-test. Also consider scoring bonus at 2+ cards ahead only if you want a clearer swing.
3. **(Low-Med) Pushing deep is not rewarded and Lifebuoy refund is unused.** The first-flip scout plus mandatory second flip made 2-3 card turns the norm, and the 4-card refund goal is rarely reached (0.56 per game). Fix options: refund at 3 and re-balance seats with +4 (seat 1 55.5% at refund 3 with +3, so +4 would be needed), or keep 4 but make the refund more valuable. Or drop the refund and accept a simple one-shot Lifebuoy.
4. **(Low) 1-card busts (10-17% of turns) feel like small taxes.** The mandatory second flip can bust you on a 2-card pile after one flip. Acceptable, but consider letting the Lifebuoy be free when the pile is one card.
5. **(Low) Mild snowball.** The leader after one third of the game wins 66-70%. Unchanged from v1 and fine.
6. **(Low) Random-bot seat bias: seat 1 wins 48%** at +3. Likely not felt in human play, but +2 is an alternative (+2: random 48.5%, strategic 52.6%, bank_early 52.1%). Keep +3.

## Rule ambiguities found

- **River with only 1 card at banking.** Section 4 says the river has at least 2 cards, but it can have 1: if the deck runs out after your first flip, or you spend the Lifebuoy on a second-flip clash with an empty river (pile of 1, clash against it). Interpretation: you take that single card (nothing is left). Needs a sentence in the rules.
- **Safe scout when the deck runs dry.** If every remaining card matches the river, the scout redraws until the deck is empty with the pile empty: the game ends (consistent with section 5). Counted 0-1 times per 1,000 games.
- **Refund.** "Pile of 4 or more at banking" counts the card you leave (it is in your pile). Interpretation: yes, all cards you flipped that stayed in the river count. Also the refund applies only if the Lifebuoy is spent.
- **Bust against bait plus own pile.** The clash card is matched against any river card; if it matches both a leftover and a pile card, that cannot happen because river values are unique. Fine.
- **Multiple leftovers.** In practice only 0 or 1 leftover exists at any time (a bust removes the pile, a bank leaves exactly one), so the "other leftovers stay" wording in section 4 is dead text.
- **Lifebuoy on a bait clash.** Spending it keeps your pile and the bait stays in the river, and you must bank taking the bait. Allowed, and good for you if the bait is high.
- **Tiebreaker.** Equal score, then more cards, then second player. Assumed.

## How it felt (narrated play)

**Game 1 (strategic mirror, seed 11, 26 turns, 160 to 132 for seat 1).**
- Turn 1: I flipped Ur9, then Ke6, then risked a third and hit An6, spending my Lifebuoy. I banked the 9 and left Ke6. It felt right to save my pile at once. The tension came from the third flip.
- Turn 2: the opponent also clashed (Ur10) and spent theirs, but they took my Ke6 and a Sn10. Both Lifebuoys were gone by turn 2, so every later push was a plain gamble. Same flat feel as v1 turn 3 onward, but arrived faster.
- Turn 4: the opponent's bait An3 got hit by an unlucky St3 on their own turn 3: they lost An8 and An3 to me. Fun: a clear "I left it, they hit it" moment, but it was the opponent's flip that decided it, not my bait choice (I had no better choice than An3).
- Turns 12-19 were the best stretch: three bait hits in 8 turns. The river had one card, we both had to flip two, and each flip carried real risk (about 20-25% per flip). Short turns, no downtime.
- Turns 22-25: low cards left in the river (Ke1, Ke2, Sn5, An2). I always left the lowest. No tension; I made the same move 4 turns in a row.
- Bot quirk: it left a 10 (An10) on turn 5 for 2 cards. That was fine for it (the bait had a 2-flip hit chance), but a human would call that a gift.

**Game 2 (strategic vs greedy, seed 5).**
- Turn 1: I banked three cards (An10 St7 Sn8) after the third flip, leaving Ur3. Turn 2 the greedy bot took the 3 plus three of its own, for 4 cards, refunding nothing (it had its Lifebuoy). Then my own turn 3 (Cr2 clash on 2 flips) lost Sn2 and An4 at once: a bust after a cautious 2-flip turn still hurt, but mildly.
- Turns 4-5: both of us reached 4-card banks, and the species race started: Cr, St, Ke, Ur all split. It felt like the species bonus might matter, but the final gap came from card values. Honestly it was a pile of numbers, not a majority fight.
- Turn 7: opponent spent a Lifebuoy to save a 1-point pile (Sn1 vs Cr1), then banked only the Cr7 bait I had left. Frustrating for me: my Cr7 bait was safely collected because they used a Lifebuoy on a worthless pile.
- Overall: fast (about 12 minutes for a human), clear turns, no hand management. The single decision each turn is "one more flip?" and it is a good one. The leave decision is mostly automatic.

## Recommended fix list for v3

1. Make the bait decision matter: increase the payoff of a bait hit (see problem 1) and re-run `python3 experiments.py` section A. Target: "leave lowest" below 60% against a smart leaver.
2. Raise species bonus (12) or score it per card of margin, and re-run section E. Target: flips 10%+ of games.
3. Either move the refund to 3 cards with seat bonus +4, or drop the refund (the Lifebuoy is then a pure one-shot and the rule text gets shorter).
4. Add the single-card river sentence to section 4 and delete the "other leftovers" wording.
5. Keep: 1 Lifebuoy each, seat 2 +3, safe scout, mandatory second flip, forced leftover take. All four tested well.
