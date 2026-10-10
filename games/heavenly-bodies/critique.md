# Heavenly Bodies: Critique (revision 1)

**Verdict: REVISE-MAJOR.** Average **3.17** (was 2.83). Real progress on balance, but the headline mechanic is inert and the game is heavy. Cycle 2 should simplify, not add.

Basis: `playtest.json` and report (bots only, unvalidated), `panel.json` (bot-predicted fun 4.16, veto inactive; bots, not people). No `panel-report.md` exists (no AI persona reviews). The fix-before-critic pass (F1-F11: six AE rewordings, 6p threshold 16, ambiguity rulings) was **not re-simulated**; I judge it on the text only. Originality was not re-searched (core mechanic unchanged except direction choice; previous result stands: low similarity, nearest Orbita 2025 and CCG duels).

## Scores (1-5), previous in brackets

| Area | Score | Why |
|---|---|---|
| Originality | 4 (4) | Per-player rotating ring plus dual win path is still fresh. No copying found. |
| Rules clarity | 3 (2) | All 40 gaps answered, 8 minor remain, fix pass reads clean. But about 300 lines, a 5-step Critical Mass cancel check, a LIFO stack, Collisions, anchors, retrograde: a heavy teach (L7). Never timed with a human. |
| Fun | 3 (3) | Skill gap 88.7, lead changes 3.78, no stalls. But the designer's own annotated play says direction "did not register as a decision", and 3.3 dead cards in a 7-card hand. Unproven with people. |
| Balance | 3 (2) | Seat gap 0.1, 2p/3p/4p path split 50/48/51, runaway 60.7. Still fails: 2 Stars outside 40-60, 4p HP 5 Stars win 3-8% (fair 25), 6p path split unverified at 16. |
| Market fit | 3 (3) | Owner-supplied, no brief. A 12-minute duel with a free-for-all mode suits the owner's card focus, but 108 unique-text cards is heavy against the "few small components" focus. |
| Production | 3 (3) | 108 unique cards, 12 Stars, HP dials, countdown markers. Unchanged; proofing 108 unique texts is the cost. |
| **Average** | **3.17** | Below the 3.5 pitch KPI. |

## Required changes from revision 0: met or not

1. Re-cost AE28 and AE25 (winning link under 0.2): **not met.** Link went up (+0.43 / +0.51). The causal ablation says only 4.6 points at 2p and about 0 at 4p, so this is mostly selection bias, and the link KPI is the wrong test. Partly met by judgement: stop chasing the link, use the ablation (under 5 points).
2. Cheap CM answers, one Denial card (cancel share 45-55%): **met at 2p** (46.6%); above band at 4p+ (58-68%). Overshoot at big tables.
3. Rotation-trick cards played 5%+: **met** (all eight 6-18%). But see below: playing them did not make rotation matter.
4. Rule rulings, re-run on locked readings, seat gap 5 or less: **met** (0.1; G29 shown not to move results).
5. Fewer dead cards (under 3 per hand): **not met** (3.31; F11 predicts about 2.85, unverified).

New problem it created: Star balance is still HP-driven, now with a new tail (ST11 29.7%).

## The things you asked about

**Rotation direction is inert (headline mechanic).** Always-clockwise bot loses by 0.9 (2p) and 2.4 (4p); ignore-North loses by 0.3. Fails L1 and design rule 2 outright. The twist was the pitch ("a clock you steer") and a bad choice costs nothing measurable. The playtester's own read of the logs agrees. Bot blindness is possible, but the designer asked for more rotation, got +8 cards played, and still no effect. This is **structural**: adding payoffs is the old fix (cycle 1 did that and it did not work). The honest options are (a) raise stakes sharply (damage or a Size penalty for what sits in North, so the choice swings games) or (b) cut direction choice and fix clockwise, saving rule weight. I recommend (b) as default, because the game is already too heavy; do (a) only if the owner wants the clock identity at any cost.

**HP-driven Stars (ST11, HP 5).** At 4p the HP 5 Stars win 3-8% against a fair 25. The playtester notes the strategic bot focus-fires lowest HP, so part of this is a bot rule (L2: one targeting bot). ST11's ability is inert (reclaim loop 30.3 vs 29.1; ability off +2.4 at 2p). The fix-before-critic pass deliberately left it. Fixable by cycle 2: HP 5 to 6 for ST11, or a real ST11 ability, plus a second targeting bot at 4p before touching other Stars. Note a flatter HP curve may be needed for free-for-all anyway.

**AE25/AE28.** Causal effect 4.6 points at 2p, about 0 at 4p. Under the 5-point ablation bar, so acceptable. Optional: AE25 to 2 damage. Not a priority; stop using the winning-link KPI.

**Hand clog from 22 Augmentations.** The designer admits F11 reduces the count but the felt clog comes from Augmentations needing a host, and bots do not feel clog. Never-Recycle bot wins 54.9% (Recycle is not helping, even hurts). Never-mulligan costs 1.3. Both of the clog patches are inert in the sim. Not provable by bots; this one is a human-test question. A cheap structural cut: remove 6 to 8 weakest Augmentations (AE14, AE17, AE04 are 1.5-4% played) and replace them with Direct Effects or COs.

**Is a 100+ card, ~300-line game simple enough to be fun for humans?** Unproven, and I doubt it. Playable rules are about 160 lines with a 5-moment cancel check, LIFO stack, Collisions, anchors, retrograde, Out of Orbit zone, plus 108 unique-text cards that must be read. Each turn is only two plays, which helps. Drivers of weight that bots say do nothing: direction choice, Recycle, mulligan, anchor/retrograde exceptions, ST11 loop. Cutting inert rules is both a clarity and a balance win. A human teach test would settle this faster than more simulation.

## Strength and weakness

**Strength:** a fresh, skill-rich duel (strategic beats random by 88.7, greedy by 58.2%), now balanced at 2-4p on seat and win path, and runs cleanly.

**Weakness:** the advertised twist does nothing (L1), and the rules carry weight for rules the sim says are inert (L7); HP still decides Star strength (L8, repeating the "mechanical fixes move scores, structural do not" pattern of L9).

## Structural or fixable?

Mixed. Star balance, 6p threshold, dead cards, AE25 are fixable in cycle 2. Rotation inertness is a structural design question; cycle 1's card-payoff approach already failed once, so a third patch of the same kind would hit the "same failure two cycles running" stop rule. Cycle 2 must take a decisive step (cut or sharply raise stakes), not another tweak.

## Required changes for cycle 2

1. Rotation: either cut direction choice (clockwise fixed) and move North exposure onto a few cards, or make North exposure carry real damage. KPI: always-clockwise ablation loses by 5 or more at 2p and 4p, OR the rule is removed and total rule lines drop by 15 or more with seat/path KPIs unchanged.
2. ST11: HP 6 or a reworked ability; test ST05 down if needed. KPI: every Star 40-60 at 2p (1,100 games each); at 4p HP 5 Stars at 15% or more with two targeting bots (focus-lowest and leader-targeting).
3. Re-run F1-F11 (not yet simulated): 6p path split at 16 (40-60), dead cards per hand under 3, the six edited AEs played 5%+.
4. Cut 6 to 8 low-use Augmentations (AE14, AE17, AE49, AE04, AE08 first) for hosts-free cards. KPI: dead cards under 3.0, Augmentation count about 15.
5. Rule weight: remove or merge at least two inert rules (Recycle, mulligan, ST11 loop, anchor exceptions). KPI: playable rules under 130 lines; ambiguities zero.
6. Big-table cancel share: trim cheap answers so 4p+ falls to 45-55% (now 58-68%).
7. Add an ablation run at 3p/6p (not yet run) and a minimax rotation bot to rule out bot blindness.

## Rule changes for the owner to confirm or veto

R1 first player skips turn-1 draw; R2 free mulligan of a no-CO hand; R3 active player chooses rotation direction (recommend veto or cut: inert); R4/R12 threshold 12 + players, max 17, 6p 16; R5/F6 cancel checked at five listed moments only; R6 Recycle as a play (inert, recommend cut); R7 ST01 HP 9 to 8; R8 buffed ST08/10/11/12; R10 eliminated player's Augmentations discarded; R11 draft in reverse turn order; F2 anchors act only in the Rotation Phase; F11 "draw 1" option on six Direct Effects. PROVISIONAL readings: G1, G7, G8, G10, G12/13, G27, G29.

## Is another revision worth it?

**Yes, one more cycle, but only a simplifying one, then a human playtest.** Balance fixes are cheap and clear; the rotation decision needs the owner's choice (cut or raise stakes). If cycle 2 does not move the rotation ablation or rule weight, stop and park for a human test: more bot cycles cannot judge fun or teachability.
