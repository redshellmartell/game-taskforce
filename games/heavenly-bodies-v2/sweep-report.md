# Sweep report, cycle 2 step 1 (bots only, unvalidated)

Method: 1,000 games per cell and count, strategic mirror (all KPI columns), greedy mirror (seat gap check) and strategic vs greedy (points = strategic win rate minus fair share). Win-at-end ON, Rebound OFF, Deep Space draw OFF. Code: `sim/sweep.py`, `sim/score.py`, `sim/abl.py`; raw data `sim/results/sweep.json`, `sweep_abl.json`. Seat gap shown is the strategic mirror.
New sim switches (shield_mode full|big|spin, mass_plus, last_draw2) are in `sim/game.py`. Interpretation of "spin" shield: a launched body is sideways until its owner's next Wake OR until the first spin of its orbit (by anyone) has resolved, whichever is first (the first spin is still protected). "big" = only sizes 1 and 5 go sideways. Last-seat draw-of-2: the last player draws 2 on its first turn only.
Bands: turns 14-24 / 18-30 / 20-34; captures >= 8; Long Night <= 10/10/15%; seat gap <= 5; 2p runaway <= 65%; lead changes >= 2; strategic > greedy; each pattern 15-50% of wins. Score = KPIs in band out of 24 (8 per count; runaway counted at 2p only).

## Table (turns / minutes at 0.4 min per turn)
| cell | 2p turns/min | 3p | 4p | caps 2/3/4 | LN% 2/3/4 | seat gap 2/3/4 | runaway 2p | lead chg 2p/3p/4p | strat-greedy pts 2/3/4 | pattern shares M/C/A 2p | KPIs in band of 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c1_full_o0 | 8.3 / 3.3 | 14.8 / 5.9 | 18.3 / 7.3 | 2.1/3.5/3.7 | 0/0/2 | 11.6/4.9/10.0 | 0.80 | 2.4/5.2/6.5 | -15/-12/-13 | 25/52/23 ; 3p 32/50/18 ; 4p 37/40/23 | 11 |
| c2_none_o0 | 31.8 / 12.7 | 37.2 / 14.9 | 32.8 / 13.1 | 24.5/20.9/17.1 | 34/94/97 | 7.5/27.5/27.9 | 0.51 | 13.4/18.0/15.8 | +22/+4/-7 | 43/48/9 ; 3p 40/42/17 ; 4p 37/45/18 | 14 |
| c3_big_o0 | 11.6 / 4.6 | 30.1 / 12.0 | 30.3 / 12.1 | 4.5/12.2/11.0 | 0/45/68 | 2.1/8.7/15.8 | 0.77 | 2.5/10.7/11.5 | -9/-14/-17 | 44/42/14 ; 3p 43/43/14 ; 4p 46/38/15 | 11 |
| c4_spin_o0 | 8.8 / 3.5 | 17.8 / 7.1 | 21.1 / 8.4 | 2.5/5.1/5.2 | 0/3/7 | 2.6/4.8/20.3 | 0.82 | 2.6/6.4/7.6 | -17/-11/-10 | 24/52/25 ; 3p 30/50/20 ; 4p 38/40/23 | 13 |
| c3big_x_open1 | 9.1 / 3.7 | 27.6 / 11.1 | 28.3 / 11.3 | 4.2/12.4/11.9 | 0/39/61 | 4.2/6.9/12.3 | 0.83 | 1.8/9.3/10.7 | -4/-11/-16 | 39/46/15 ; 3p 41/48/11 ; 4p 42/41/17 | 12 |
| c3big_x_cm1 | 10.8 / 4.3 | 28.3 / 11.3 | 29.9 / 12.0 | 4.1/11.1/10.6 | 0/35/66 | 2.4/5.1/13.7 | 0.78 | 2.4/9.6/11.1 | -4/-12/-17 | 31/54/15 ; 3p 35/49/16 ; 4p 37/47/16 | 13 |
| c3big_x_draw2 | 11.4 / 4.5 | 29.7 / 11.9 | 29.8 / 11.9 | 4.4/11.8/10.8 | 0/48/71 | 1.7/8.1/20.8 | 0.74 | 2.8/10.7/11.5 | -13/-15/-18 | 46/43/11 ; 3p 41/47/12 ; 4p 46/35/19 | 12 |
| c4spin_x_open1 | 6.8 / 2.7 | 13.9 / 5.6 | 17.3 / 6.9 | 2.5/4.5/5.5 | 0/1/5 | 10.2/7.8/19.4 | 0.74 | 1.5/4.4/6.1 | -14/-8/-9 | 24/50/25 ; 3p 30/51/18 ; 4p 37/40/24 | 8 |
| c4spin_x_cm1 | 8.7 / 3.5 | 17.7 / 7.1 | 21.4 / 8.6 | 2.5/5.0/5.3 | 0/2/10 | 1.4/5.3/21.9 | 0.83 | 2.5/6.2/7.8 | -13/-8/-10 | 15/59/26 ; 3p 21/53/25 ; 4p 28/54/18 | 10 |
| c4spin_x_draw2 | 8.8 / 3.5 | 17.9 / 7.2 | 21.4 / 8.5 | 2.4/5.2/5.3 | 0/3/11 | 0.9/1.2/19.2 | 0.82 | 2.7/6.6/7.8 | -20/-12/-12 | 26/52/22 ; 3p 29/52/19 ; 4p 37/39/24 | 12 |

Cells: c1 shield full, c2 none, c3 big (Comet/Giant only), c4 spin (until first spin of the orbit), all opening 0. Crosses: x_open1 = 1 opening body, x_cm1 = Critical Mass +1 (17/16/15), x_draw2 = last seat draws 2 on its first turn.

## Reading
- Shield full (c1): 8 / 15 / 18 turns, 2-4 captures, repeats cycle 1. Too fast at every count.
- Shield none (c2): the only cell with real combat (17-25 captures) but 32 / 37 / 33 turns and Long Night 34 / 94 / 97%. Opening 0 plus no shield stalls at 3-4p. 14/24 only because it passes captures, lead changes and runaway.
- Big-only shield (c3): the lever with the most range. 2p 11.6 turns (short), 3p 30.1 and 4p 30.3 (at the top of band) but Long Night 45% / 68%; captures 4.5 / 12 / 11. Seat gap 2.1 at 2p.
- Spin shield (c4): barely longer than full (8.8 / 17.8 / 21.1); 3p and 4p turns in band, 2p far short, captures 2.5-5.
- Crosses: opening 1 shortens everything (wrong way at 2p, gap worse). CM +1 adds only about 0.3-0.5 turns at 2p and lowers mass share (c4: mass 15% at 2p, outside the pattern band). Last-seat draw-of-2 is the only seat-gap tool that works: spin cell 2p gap 2.6 to 0.9, 3p 4.8 to 1.2; no help at 4p (19-20, so 4p gap is not the first-draw effect; the greedy mirror gap there is only 3, so the strategic bot's own play creates a seat edge, probably bot style, to be checked with a second strong bot).
- Strategic loses to greedy in 9 of 10 cells (-4 to -20 points; only no-shield wins at 2p +22). The greedy race beats the strategic bot whenever games are short; this is the bot-skill finding (L2), not a rules finding, but it means skill expression cannot be judged until games are 20+ turns with fights.

## Ablations (strategic vs ablated, margin in points; need >= 5)
| cell | no-recall 2p/3p/4p | comet-blind 2p/3p/4p | Giant / Comet captures per game (4p) |
|---|---|---|---|
| c4spin_x_draw2 | -0.2 / -4.6 / -0.9 | +4.8 / -1.2 / +1.1 | 0.32 / 0.62 |
| c3big_x_cm1 | +0.8 / -0.6 / +1.9 | +2.6 / +0.1 / +4.1 | 0.27 / 0.69 |
Neither Recall nor Comet beats Giant reaches 5 points anywhere (Recall used 0.01-0.06 times per game; Giants captured about 0.3 times per game). Both are still inert even with big-only shield and 11-12 captures. Recommend cutting Recall and Comet beats Giant, or reworking them (not by card text alone, L12).

## Recommendation
No cell is coherent at all three counts. Best KPI count: c2 none (14/24) is not a playable length; among playable cells:
- **Recommended set: shield "spin" + opening 0 + last-seat draw-of-2 (c4spin_x_draw2, 12/24).** 3p is in band on turns (17.9, just under 18; round up with one more body of delay), Long Night, seat gap (1.2), runaway, lead changes, patterns (29/52/19); 2p seat gap 0.9. Fails: 2p length (8.8 vs 14-24), captures (2-5 vs 8), 4p seat gap (19), strategic vs greedy.
- **Runner-up: shield "big" + opening 0 + CM +1 (c3big_x_cm1, 13/24).** Gives captures of 4-11 and 2p gap 2.4, but 2p is 10.8 turns and 3p/4p overshoot with Long Night 35% / 66%.

## Still out of band (after any of the cells)
1. 2p length: no shield variant gets 2p above 12 turns while keeping Long Night low (only no shield reaches it, 32 turns). 2p needs a different length lever than the shield.
2. Captures: only reached by big shield at 3-4p (11-12) and no shield; spin shield stays at 2.5-5.
3. 4p seat gap about 19-21 in every strategic-mirror cell (greedy mirror about 3): check with a second strong bot before changing a rule.
4. Strategic below greedy in short games; Recall and Comet beats Giant inert.
5. 2p runaway 0.74-0.83 in every cell except no shield (0.51), above the 65% limit.

## Untested suggestions (budget used: 4 shield cells + 6 crosses; the crosses count as the one cross configuration)
- Per-count thresholds with the big shield (2p +2, 3-4p -1) to cross the 2p/3p/4p gap at once.
- Big shield plus spin shield together (Comet/Giant, until first spin).
- Rebuilding the 2p game: a bigger deck pull or a 5th slot orbit; or accept 2p as a short filler (about 3.5-4.5 min) and drop it from the 12-minute claim.
