# Nine Fields - Playtest report (revision 1)

**Verdict: NEEDS-FIXES (minor).** 3-4 players pass every KPI. The 2-player game misses one KPI by about 1.4 points (early-leader wins) and sits at the top of the length band. Everything below is bot simulation; no human has played it.

## Key numbers (2,000 games per bot pairing; strategic mirror unless stated)

| Metric | 2p | 3p | 4p | Target |
|---|---|---|---|---|
| Seat gap (points from fair) | 0.1 (1.7 at 10k) | 2.6 | 2.7 | <= 5 PASS |
| Strategic vs random | 100 | 57.4 | 37.7 | >= 20 PASS |
| Mean turns / est. minutes | 60.7 / 24 | 48.5 / 20 | 48.4 / 19.9 | ~20 +-20% (2p at the edge) |
| Lead changes | 2.77 | 3.15 | 3.28 | >= 2 PASS |
| Early-leader wins | 64.9% (66.4% at 10,000) | 55.5% | 48.9% | <= 65% (2p FAIL by 1.4) |
| Storms per game | 0.99 | 0.05 | 0.00 | - |
| Score ties before tiebreaks / shared wins | 5.9% / 1.2% | 12.7% / ~2% | 19.2% / ~2.5% | - |
| Turn-cap hits | 0 | 0 | 0 | 0 PASS |

Length uses an assumed pace (15 s/turn, 20 s/flood, 90 s setup). Games now always run the full deck (22 floods at 2p, 19 at 3-4p); sd of turns 8.1 / 6.6 / 5.0 (v1 2p sd was 17.6).

## Problems, by severity

1. **Medium - 2p runaway leader just over the KPI, and 2p length at the top of the band.** Early leader wins 66.4% over 10,000 games (KPI 65); ~24 min vs 20 target (+20%, cap 25). The designer's expected 19-21 min for 2p was optimistic: 2p takes 2.76 turns per flood, not 2.3-2.6. Shortening makes runaway worse (experiment: remove 3 cards at 2p -> 52.7 turns, early leader 69.8%; remove 6 -> 44.9 turns, 74.9%). Fix options (untested): 2p storm threshold 2 x players; or accept as noise and check in a human 2p game. Do not cut cards at 2p.
2. **Low - storm exploit does not work.** A sandbag bot (avoids trophies in the first half to hold the storm direction and plays calm) wins 48.2% vs a strategic bot at 2p, 33.3% vs two at 3p, 23.3% vs three at 4p (all at or under fair). The designer's flagged risk is not borne out. Caveat: a bot only tests one way of sandbagging; and the storm hardly fires at 3-4p (0.05 and 0.00 per game), so the rule is effectively a 2p rule.
3. **Low - late 2p game is a flood engine.** In sample games the same island floods 5+ times by Sailing the same pawns (only 33% of 2p actions are Lands). Fair, but it may read as pawn shuffling. Watch in human play.
4. **Low - shared wins and score ties.** Ties on score are common at 4p (19%); the new tiebreaks resolve nearly all (shared wins 1-2.5%) without seat bias.
5. **Info - skill depth.** A 2-ply bot beats the 1-ply strategic bot 84% at 2p, but at 3p it ties (33.4% vs 33.3% each). Smarter 2p play also increases runaway (2-ply vs 1-ply: early leader wins 82%, lead changes 1.62), so the 2p runaway KPI will probably be worse with expert humans than the 1-ply number.

Dead cards: none. Island classes claimed 1.7-6.4 times per game at 3p; the weakest (value 1, cap 2) shows -3.3 points win correlation, the strongest (value 4) +11.6. No class flagged. Score of v3 cap 4 cards (+6.8) is fine.

## Rule ambiguities (all minor)
- Phase 2 step 5 says the turned island "stays full", but a storm island need not be full.
- A storm flood can end the game (deck empty); rules imply it but do not say it.
- A shared win is still possible after all tiebreaks; one line should say so.
- Tie breaks for the storm island and storm player are clear as written (implemented as stated). The six v1 gaps are closed; I hit none of them.

## How it felt (one 2p game, strategic bots, seed 4242, 58 turns, final 28-29)
- Turns 3-9 are quick and clear: each Land is a pressure decision. Fun: the first flood and the choice of direction.
- Turns 13-33: the same two islands (Crown-type cards) flood again and again via Sails. Scores swing 14-9 to 14-14 to 14-17; lead changed several times, so it felt tense but slightly samey.
- Turn 42: a storm after six quiet turns handed seat 2 (fewest trophies) the direction; it felt like a natural "someone must break the standoff" moment, better than v1's abrupt stall ending. Downtime is low (one action per turn).
- Confusing: working out which island is the storm target (fewest open spaces) needs a scan of all nine cards; players may forget to track the calm count.

## What simulation cannot test
Whether stalling humans bluff or table-talk, the kingmaking feel of direction choice at 3-4p (bots pick by score, not by spite), whether the card-turning/axis reading is clear in real hands (rotation by quarter turn, the "ROW/COLUMN" print), real pace (minutes are an assumption), and whether the flood engine feels boring. A human 2p and a human 3p test are the next real checks.

## Panel (free bots)
Average predicted fun 3.60 (spread 1.93). Best fit: competitor 4.52 (strategist 4.08, barraiser 4.09, no veto). Worst fit: family 2.59 (would not buy). Casual 3.10, story 3.22.

## Experiments used (3 of 5)
1. 2p mirror at 10,000 games (runaway within 2 points of KPI). 2. Sandbag exploit probe at 2/3/4p. 3. Remove 3 / 6 cards at 2p. Plus a 2-ply check at 2p and 3p. Not run: 2p storm threshold 2 x players; "just-flooded island cannot be Sailed onto next turn".
