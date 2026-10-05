# Playtest report: Tug of Crowns, revision 1

**Verdict: NEEDS-FIXES.** 20,000 headline games (2,000 per pairing of random/greedy/strategic, 3x3) plus 2,000-game lead-policy tests, plus 5 extra experiments of 1,000-game batches each. Code: `sim/game.py` (rules v2), `sim/bots.py`, `sim/run.py`, `sim/panel_run.py`.

## Key numbers vs KPI
| Metric | Result | Target | |
|---|---|---|---|
| Seat/side gap (equal-skill Treasurer win: random 57.8, greedy 38.1, strategic 37.9) | 10.9 pts (strategic mirror 36.6% Treasurer) | <= 5 | FAIL |
| Strategic vs random | 56 pts | >= 20 | pass |
| Lead changes per game | 1.83 (mirror 1.70) | >= 2 | just below |
| Early leader (after round 2) wins | 49% | <= 65% | pass |
| Centre/tiebreak endings | 0% (throne 68%, round-7 leader 22%) | < 10% | pass |
| Length | 39 actions, about 12.7 min, avg 4.4 rounds | 15 min +/-20% | pass (-15%) but see problem 3 |
| Dead cards | none; The Whisper is strong (+17.6 pts) | 0 | pass |
| Ambiguities | 0 blocking | 0 | pass |
| Fixed lead policy vs evaluating bot | always-lead-self 63%, always-give 43% | each 40-60 | FAIL |
| Lead's round-win rate | 54% (random 56%, greedy 44%, strat mirror 50%) | rules ask: report | ok |
| Reshuffles per game | Treasurer 0.48, Whisperer 0.47 | report | equal, rare |

Ties 1% of rounds (0-0 only), no capped games. Panel: average fun 3.30, best fit competitor (4.03), worst fit family (2.67).

## Problems (ranked)
1. **High: the lead is solved again, now towards leading.** The extra card is too strong: always-lead-self beats always-give 63/43 against the evaluating bot, and 80/35 in fixed-policy mirrors. A greedy bot (always leads) beats the strategic bot overall (59% vs 57%). Experiments (all 1,000 games per cell): E1 no tie-win, self 65%; E2 no extra card, policies 47/50 (balanced but the choice barely matters; Treasurer then wins 62%); E3 second player draws, give dominates (60%, Treasurer 85%); E4 ties to the second player, self 59%; E5 lead draws only if its hand is not larger, self 63%. Fix idea (untested): make the lead pay a price that is not a card (reveal a hand card, or play first card face down), or give half a bonus (the lead draws 1 only in rounds 2, 4, 6).
2. **High: side gap 10.9 points and it flips with skill and lead habits.** Treasurer wins 58% random, 38% greedy and strategic. The Whisperer's Hush/Retort rewards skill. Retune after problem 1 (Spend bonus or Treasury cap, one lever at a time).
3. **Medium: games end early.** 31% end by round 3 (15% in round 2); only 29% reach round 7. A 5-plus margin from position 1 wins on the spot. Fix: double-move margin 6 or a 4-step track.
4. **Medium: lead changes 1.83.** Probably fixed by the same change as problem 3.
5. **Medium: strategic only beats greedy 43%** (mostly via lead choice). May be bot weakness; recheck after problem 1.
6. **Low:** The Whisper is outlier (played 79% of games). No dead cards. Possibly drop it to 4.

Bug note: my first sim run put spent coins into the draw pile as blank cards; fixed (the five experiments ran before that fix; conclusions are expected to hold).

## Interpretations (not ambiguities)
All 8 earlier ambiguities are resolved in v2. Remaining small notes: the lead's extra card comes after Phase 1 draws; Retort only follows a Treasurer card.

## Narrated play (one bot-assisted game, seed 5, strategic Treasurer vs greedy Whisperer)
Round 1 was a long, even grind: both sides played the whole hand (Treasurer 22, Whisperer 18) and the crown only moved one step, a fun slow start. Round 2 was boring: the Treasurer passed with 0, the Whisperer played one Echo and took the lead for 2 points. Round 3 had the best moment: three Hushes stripped three Treasurer cards, yet the Treasurer won 12-11 through a Spend. Then round 4 ended with a 7-point pass and a lead swing. Downtime is low (alternating single cards), but the passes feel flat when the leader gives up round 2 for nothing. 15% of games, as in an earlier seed, end in round 2 on a double move, which would feel abrupt.

## What simulation can't test
Whether bluffing with Retort feels clever, whether the lead choice is fun or a chore, how readable the keyword text is, hand-size memory for real players, and whether short 2-3 round games feel exciting or unsatisfying. The bots do not bluff or read the opponent's discard pile. A human playtest is needed.
