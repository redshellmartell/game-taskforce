# Heavenly Bodies: Playtest Report (revision 1)

**Verdict: NEEDS-FIXES** (bots only, unvalidated). Revision 1 fixed most of what revision 0 flagged: 2p seat gap, path split at 2p to 4p, cancel share, rotation-trick card use, ambiguities in the sim. Four KPIs still fail: the Star balance, the 6-player path split, rotation direction mattering at all, and the AE25/AE28 winning link. Dead cards per hand is 3.3 (target under 3). The Bar Raiser veto is no longer active.

Sim: `sim/game.py`, `bots.py`, `run.py` (parts head/abl/exp), `summarize.py` (writes `playtest.json`), `panel_run.py`, `experiments/e5_burst.py`, `e6_rotdecision.py`. About 109,000 games (2,000 per pairing for the headline; Star round-robin 100 per pair). All rules and the 18 changed cards were recoded; card-count integrity is checked in smoke runs. Fixed seeds.

## Before and after

| Measure | Revision 0 | Revision 1 | Target | Status |
|---|---|---|---|---|
| 2p seat gap (seat 1 vs 2) | 7.4 (57.4/42.6) | **0.1** (50.2/49.8) | <= 5 | pass |
| Critical Mass share 2p / 3p / 4p / 5p / 6p | 28 / 46 / 61 / 70 / 75 | **50 / 48 / 51 / 42 / 38** | 40-60 each | 6p FAIL (38.0%, CI 35.8-40.1); 5p passes narrowly |
| Strategic vs random gap | 77.7 | 88.7 | >= 20 | pass |
| Strategic vs greedy / bot spread | 53.5% / n.a. | 58.2% / 69.5 pts | report | strategic clearly above greedy |
| Runaway leader (2p) | 63.4% | 60.7% (3p 58, 4p 51, 6p 35) | <= 65% | pass |
| Lead changes (2p) | 3.1 | 3.78 | >= 2 | pass |
| Length 2p | 9.0 turns, ~12 min | 9.8 turns, ~12.8 min (3-6p: 15/21/26/31 turns) | ~12 min | pass |
| Ties / cap hits | 0 / 0 | 0 / 0 | 0 | pass |
| CM cancel share (2p) | 41% | 46.6% (3p 54, 4p 58, 5p 64, 6p 68) | 45-55% | pass at 2p; above band at 4p+ |
| Each Star 40-60 (2p, 1,100 games each) | 33-71 | 29.7 (ST11) to 65.4 (ST05); ten of twelve inside | all | FAIL (2 outside) |
| Each Star at 4p (fair 25) | n.a. | HP8 37-48, HP7 31-40, HP6 17-20, HP5 3-8 | n.a. | FAIL (bot-dependent, see 2) |
| AE28 / AE25 winning link | +0.42 / +0.26 | **+0.43 / +0.51** | < 0.2 | FAIL (causal effect 4.6 pts at 2p) |
| Rotation-trick cards played (2p games) | all under 5% mostly | AE41 16.5, AE43 17.5, AE45 11.9, AE55 8.9, AE57 14.5, AE60 10.2, CO14 6.2, CO24 7.7 | each 5%+ | pass |
| Always-clockwise bot loses by | n.a. | 0.9 (2p) / 2.4 (4p) | >= 5 | FAIL |
| Dead cards per 7-card hand | 3.43 | 3.31 | < 3 | FAIL (small move) |
| Ambiguities hit | 41 | 8 minor (list below) | 0 | not zero |

## Ablations (2,000 games each; ablated bot vs full strategic; margin = points below fair)

| Test | 2p | 4p | Passes (>=5)? |
|---|---|---|---|
| Always-clockwise bot | 49.1% (0.9) | 22.6% (2.4) | no |
| Ignore-North bot (direction and placement) | 49.7% (0.3) | 25.1% (-0.1) | no |
| Never-Recycle bot | 54.9% (-4.9, better) | 25.1% (-0.1) | no, Recycle is not helping |
| Never-mulligan bot | 51.3% (-1.3) | 24.2% (0.8) | no (expected small; 18% of 2p games use one) |
| ST08 ability off (Star with ability vs same Star off) | +6.5 | +1.6 | 2p only |
| ST10 ability off | +12.7 | +6.9 | yes |
| ST11 ability off | +2.4 | +0.6 | no, inert |
| ST12 ability off | +13.8 | +2.8 | 2p only |
| Flat threshold 15 vs scaled (CM share 2/3/4/6p) | 39 / 49 / 62 / 64 (scaled 50 / 48 / 51 / 38) | | scaling works |

The rotation decision exists (the two directions differ in value in 60% of Rotation Phases, by over 1 point in 33%, and the North term flips the choice in 26%) but a bad choice costs too little to change results. Possible bot blindness; a human check is needed.

## Single-change tests of the riskiest pieces (extra configurations: 5 of 5 used)

1. **ST12 free -1 Stability (switch off):** ST12 wins 41.7% at 2p with it, 29.8% without; it moves 2p games toward Star Destruction (CM 31.7% vs 40.9%). At 4p 4.2% vs 3.7%. Not too strong; the Star is still below fair.
2. **ST11 reclaim loop (switch off):** 30.3% with, 29.1% without at 2p; 4.4% vs 4.2% at 4p. The loop is inert, and ST11 is the weakest Star.
3. **Threshold at 5p/6p:** 5p: 17 gives 43.7% CM, 16 gives 56.4%. 6p: 17 gives 36.3% (38.0% in the headline), 16 gives 50.2%. So 17 at 5p is right and 6p should be 16.
4. **NEW test, bot priorities:** CM-first and damage-first strategic mirrors. 2p CM share 54.3% (CM-first) vs 39.9% (damage-first); 4p 52.6% vs 41.4%. Head to head, CM-first beats damage-first 50.4% at 2p and 25.2% at 4p (fair 25). So neither style dominates and the path split is fairly stable (+-7) under extreme priorities, which supports the split numbers.
5. **NEW test, causal check of AE25/AE28 (bot that never plays them):** loses by 4.6 points at 2p, about 0 at 4p. Most of the +0.43/+0.51 link is selection (they are played when a kill is near).
(Also a diagnostic count of rotation decisions, no extra games to speak of: `experiments/e6_rotdecision.py`.)

## Problems, ranked

1. **HIGH. Rotation choice is inert** (see ablations). The headline twist of the revision does not change best play in the sim. Fix: raise the stakes of position (bigger North payoff or penalty, more cards that score on E/S/W) or retire the direction choice to save rule weight. Needs human check for bot blindness.
2. **HIGH. Star balance follows HP, HP 5 Stars lose at 4p.** 2p: ST05 65.4%, ST11 29.7% outside 40-60. 4p random tables: HP8 43/37/48%, HP7 31/40/33%, HP6 17/19/20%, HP5 8/3/4%. The strategic bot focus-fires the lowest HP, so the 4p gap is partly a bot rule; the same pattern was in revision 0 (HP followed win rate). ST11's ability is inert. Fix: lift HP 5 Stars (ST11 especially); retest with a second targeting bot.
3. **MEDIUM. 6p CM share 38.0%.** Fix: threshold 16 at 6p (50.2% in test); keep 17 at 5p.
4. **MEDIUM. AE25/AE28 link above 0.2**, but the causal effect is only 4.6 points at 2p and zero at 4p. Judge by the ablation; optional: AE25 to 2 damage.
5. **MEDIUM. Dead cards 3.3 per hand** (22 Augmentations need a host); Recycle and mulligan do not help the bots (no-Recycle bot wins 54.9%). Recycle is used 1.5 times per game.
6. **LOW. Rarely played cards at 2p:** AE14 1.5%, AE17 3.3%, AE49 3.5%, AE04 4.2%, AE08 4.9% (4p: AE14 1.8%). Dead-ish; AE49 is still low after the rewrite (the bot values it at a flat 0.8 draw).
7. **LOW. AE58 and CO18** (rotate an opponent's orbit) lost their teeth under plain card rotation: mostly a cantrip or ping.
8. **LOW. CM cancel share above 55% at 4p+** (58, 64, 68%): cheap answers are plentiful in big games; the 6p CM win per announce is 14%.

## Rule ambiguities I hit (8, all minor; the sim chooses as stated)

AE60 moving an anchored CO (coded: yes); AE49 with under 4 cards in the deck; "Size 3 or less" of a CO in the Out of Orbit zone (printed Size); ST11 damage when the reclaimed CO loses its Collision (still deals damage); Critical Mass cancel check per card/trigger vs per play (coded per play, Rotation Phase and End of Turn); AE28 "Size 4 or more" (effective at cost); Recycle with deck and discard both empty (not offered); order choice among the active player's own simultaneous triggers (arbitrary, no effect). PROVISIONAL readings coded as written: G1 (direction choice), G7, G8 (cancel after each resolution), G10 (cap), G12/13 (rotation Collisions), G27, G29 (LIFO). G29 effect on results is nil: the start/end triggers (AE09, AE11, CO23, AE20) are all the active player's own and do not interact.

## How it felt (two annotated sim games, bot decisions, no interactive play)

I replayed two logged games from their logs and read them as a player.
**Game 1 (seed 3, ST08 vs ST11, CM win for ST11 on turn 14).** Opening turns were quick: one CO, one Augmentation, done. The nice moment was turn 6: opponent bounced my North CO with AE55 (Free-Return) right after I built; I felt the North exposure, which is the intended story. Turn 10 felt like a combo (ST11 reclaim, AE53, AE43 in one turn) and was fun for the active player, a lot of damage for me to sit through. Rotation direction did not register at all for me as a decision: I only noticed it when a CO landed in North. No downtime issue (turns are two plays).
**Game 2 (seed 8, ST11 vs ST08, Star win turn 10).** A damage race: AE29, AE38, AE31, AE27 and the finisher AE28 (2 damage from a North sacrifice, 3 with Size 4+). Nobody built Critical Mass. Felt short and a bit swingy: the HP 5 Star lost the damage race by turn 5. Both games had a turn where a hand held cards with no legal play (Recycle was available and useful).

## Test panel (bots, 2p, 15 tables x 2 seatings x 200 games)

Average predicted fun 4.16 (was 3.98), spread 1.49. Best fit competitor 4.82, worst fit family 3.33; strategist 4.68, barraiser 4.54, story 3.95, casual 3.62. Bar Raiser veto: inactive. The panel rotation covers 2 players only (main count); 3-5 player tables not run.

## What to try next

Rotation: add position stakes (e.g. AE22-type North effects to every damage Star hit) or cut direction choice. Stars: ST11 HP 6 or a stronger reclaim; test a second targeting bot at 4p before touching HP. Threshold 6p to 16. A human playtest is now worth more than another bot cycle on the Star balance, since the 4p Star gap depends on a bot rule.
Untested suggestions: Recycle once per turn free; a leader-targeting bot at 4p; 5p/6p ablations; a second bot family for rotation (a minimax rotation bot) to rule out bot blindness.

## Sim-kit improvement

`sim-kit` would benefit from (1) a multi-seat `vs(n, A, B, N)` helper (one tested bot against n-1 copies, seats rotated, fair share 1/n) and (2) an `ability_off` mirror helper. I wrote both inline in `run.py`; they are generic.
