# Whiskerdark - Playtest report, revision 1 (rules v2)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** No human has played it. Simulation cannot test fun, teaching time (about two pages of rules), whether the memory load of free Glow is bearable, table feel, or where a competent human sits between the two bots.

## Key numbers (every layout of 362,880 for outline, random, greedy; 3,632 layouts for lookahead)

| KPI | Target | Now | Previous (v1) |
|---|---|---|---|
| Outline bot first-run win | 25-60% (designer band) | **57.1%** | 19.1% |
| Lookahead bot win | <= 90% | **96.1%** (fail) | 80.8% |
| Greedy / random | random >= 20 pts below outline | 11.2% / 0.0% | 4.9% / 0.0% |
| Bot spread (lookahead - outline) | smaller is better | 39 pts | 62 pts |
| Skill gap (best bot - random) | >= 20 | 96.1 / 57.1 | 80.8 / 19.1 |
| Median turns / minutes | 7-12; 10 min +-20% | 8 / 8.3 (outline), 10 / 9.2 (lookahead) | 6 / 6.4, 9 / 8.3 |
| Turn cap (20) hits | 0 | 0 in about 1.1M runs | 0 |
| Opening shove share | 20-60% | 35.7% outline ok, 89.6% lookahead fail | 35.7 / 90.9 |
| Wins using Feint / Hypnotise / neither | >=10 / >=10 / >=25 | outline 2.4 / 9.9 / 87.7; lookahead 9.9 / 19.6 / 70.5 | 2.1 / 15.0 / 82.9; 15.7 / 21.1 / 63.2 |
| Killer spread | Hound 40-75%, 4+ cards >=5% | outline Hound 64.9, Fox 30.9, rest <3.4 (2 cards); lookahead Hound 9.9, 8 cards >=5% | outline Hound 54.5, Fox 32.8 |
| Single-Ghost lift (outline) | +5 to +25 each | Moth +4.1, Mouse +4.4, Spider +1.9, Rat -3.7, Crow +14.8, Owl +20.7, Snake +13.9, Fox +13.0, Hound +39.0 | 0.0, 0.1, 1.4, 21, 38, 44, 29, 43, 19 |
| Sessions (outline) | max score share <= 40%, 3-4 runs | 54% on score 8; 2.8 runs | 38.5% on 7; 4.1 runs |

Single-Ghost lift for the lookahead bot is not measurable: it wins 96.1% with no Ghost (ceiling, max +4).

Persona bots (free panel run): casual 18.6%, family 22.2%, story 31.3%, strategist 57.4%, competitor 93.0%, barraiser 97.0%. Panel: average fun 2.78, best fit competitor (3.72), worst fit family (1.75); no Bar Raiser veto flagged by the numbers. Written to `panel.json`.

## Ablations (full bot minus ablated bot, in win points; needs >= +5 and use >= 15% when Ready)

| Trick | Outline | Lookahead | Use when Ready (outline / lookahead) | Result |
|---|---|---|---|---|
| Glow | +2.8 | 0.0 | 72% / 56% | fail (used but inert) |
| Dart | +11.9 | not run | 36% / 80% | pass |
| Silk | **-3.8** | -0.5 | 16.7% / 7.5% | fail (better without it) |
| Scavenge | +24.5 | not run | 62% / 91% | pass |
| Carry | 0.0 | 0.0 | 0.7% / 0.07% | **dead** |
| Carry, never swap | 0.0 | 0.0 | swap fires in 0.5% / 0% of runs | swap dead |
| Hypnotise | +3.6 | not run | 24% / 94% | fail on points |
| Feint | +0.9 | not run | 13.0% / 100% | fail on points |
| Owl-first spend | +0.9 | not run | - | inert choice |
| Drift (Ghosts 1,2,3 set) | +13.0 | not run | - | pass |
| Never Shove | +27.9 | not run | - | pass (core) |
| Anger off | -19.8 (wins more) | not run | - | Anger is a real cost, as designed |

Wise changes the wounds in 92% of Owl runs (target 15%): fine.

## Problems, ranked

1. **High: strong play is nearly free.** Lookahead wins 96.1% (sanity cap 90%); lookahead sessions end on score 9 96% of the time. v2 made everything easier (Thief cut, Ghosts softer, free Glow and Silk). Outline sits at 57.1%, the top of its band. Suggested fix: the designer's own knob, **Hunt lethal**. Tested as extra config 1: lookahead 96.1 to 77.0, outline 57.1 to 56.4, spread 39 to 21 points. Adopt and re-measure both bots.
2. **High: dead or inert tricks.** Carry is dead and its swap never fires (0.0 ablation, 0.7% use); Silk is worse than not using it; Glow, Hypnotise, Feint and Owl-first fail the +5 bar. Cut Carry (or make the swap its only effect), rework or cut Silk, and decide whether Glow is flavour. (Caveat: a stronger Carry bot may find a use; the lookahead bot's Carry options only swap a known Hound away.)
3. **Medium: Ghost lift uneven.** Four of nine in band (Crow, Owl, Snake, Fox). Moth, Mouse, Spider just under +5. Rat is negative (-3.7; cause not established; guess: a Danger 2 Rat is fought early). Ghost Hound is +39 because Danger 7 plus no Hunt. Fix: Ghost Hound Danger 8 or keep Hunt for it; let the Rat Drift.
4. **Medium: variety targets missed** (killer spread, Feint share 2.4%/9.9%, session shape). Re-measure after fix 1.
5. **Medium: grind and the Angry Hound trap.** First Fight is on turn 3 or later in 24% of outline layouts. A normal Shove of the Hound makes it Danger 11; the rules do not say so plainly.
6. **Low:** length fine (8.3 / 9.2 minutes vs 10).

## What worked in v2

- Win band moved the right way for the outline bot (19.1 to 57.1) and the bot spread fell (62 to 39 points; 21 with Hunt lethal).
- Shove loop fixed: 0 turn-cap hits; no stalls.
- Drift is a real effect (+13 with all three small Ghosts); Ghost lifts for Crow, Owl, Snake, Fox are now in band (were +29 to +44).
- Glow free: used 72% / 56% (was 17.6% / 0.5%) but changes outcomes by under 3 points.
- Median length now 8 (outline) vs 6.
## What did not work
- Carry (dead), Silk (negative), Thief removal plus easier Ghosts pushed the strong bot to ceiling.

## Rule ambiguities hit while coding (7)
1. Silk then a normal Shove of the same card X: unstated (implemented legal).
2. Carry swapping two Dark cards: legal but pointless (implemented legal).
3. A Ghost turned Lit by Lighting after Phase 1 waits a turn to Drift (as written).
4. Drift of an Angry Ghost: unstated (implemented: legal, Anger vanishes).
5. Hide-by-Shove makes the Hound Angry (Danger 11); rules do not warn.
6. Whether Scavenge can re-ready a trick used this turn: closed in v2.
7. Hound Hunt on a Hound lit by Drift or Silk: closed in v2.

## Dead cards (v2)
Crow (Carry): dead. Spider (Silk): below the 15% bar for the lookahead bot and negative. Moth (Glow), Snake (Hypnotise), Fox (Feint) used but weak on points. No card fails "beaten or Shoved in 25% of runs".

## Narrated play (seed 2, layout Rat Snake Crow / Owl Fox Spider... Hound bottom-left)
Doorway Rat 4, Snake 7, Crow 5 against Claws 2 with no trophies: every Fight costs more wounds than I have trophies, so Shove. Turn 1 I Shove Rat and Owl comes up (Danger 6, worse). Turns 2 to 4 are more Shoves; I deduce from elimination where the Hound is and it comes up on turn 4. Hiding it by Shove felt clever until I noticed it is now Angry, Danger 11: I had just made the win nearly impossible. Turn 5 a Moth finally appears; turns 6 to 10 are a pleasant snowball (Moth, Spider, Rat, Owl at 3 wounds, Mouse) and I felt strong. Then the Hunt drained a trophy, I had 1 left and the Angry Hound needed 6 wounds: dead. Fun: the deduction and the snowball. Frustrating: five turns with no Fight, and the Hound trap that the rules never warn about. No downtime (solo); each turn took a few decisions only.

## Configurations used (budget 5 extra)
1: Hunt lethal (both bots). 2: Anger off (outline). The ablation battery (12 outline variants + 3 lookahead + Drift) is the designer's required tests. Untested suggestions: Hunt lethal with Ghost Hound Danger 8; lookahead ablations for Dart, Scavenge, Hypnotise, Feint; lookahead single-Ghost lifts under Hunt lethal; a Carry-aware bot that swaps known low cards into the doorway.
