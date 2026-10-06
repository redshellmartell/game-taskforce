# Critique: Silent Duo (rules v3, playtested at v3; revision 2 / cycle 2)

**Verdict: REVISE-MINOR.** Average 3.33/5 (was 3.67). The score fell, and it is below the 3.5 pitch bar. The verdict stays MINOR only because the one remaining mechanical fix (set Fog from the measured sweep) is cheap. After that, the next step is a human playtest, not another bot cycle.

Caveats. Everything is bots only and unvalidated; no human has played it. Human teams deduce worse than Honest, so real win rates will be lower than shown, which makes the high Standard win rates less worrying than they look and F10 possibly too easy to trust either way. Fun and Market fit lean on free bot-predicted panel scores (fun 3.99, worst fit family 3.11). No fix-before-critic pass ran this cycle. Activity lines are left to the Director.

## Scores

| Area | Score | Note |
|---|---|---|
| Originality | 3 | Unchanged core (Hanabi-like hidden own info, Crew-style silence, token-flip double-lamp Offer). Not re-checked, as instructed. |
| Rules clarity | 3 | Down from 4. Four new ambiguities from the Single Offer (listed in `playtest.json`) were not closed by a fix pass. rules.md is about 229 lines against a one-page promise (L7). Section 7.4 and 7.6 still carry guesses that the data has refuted. |
| Fun | 3 | Early turns are good puzzles and the Single Offer gives a nice moment. The middle game is still downtime: in the narrated game 5 of the last 12 turns were Trims and the loss was a forced 10 on a wide range. |
| Balance | 2 | Both bots out of band at the stated Standard at both counts, Greedy +10.8 / +11.0 over Honest, 3+ Trim runs 54% / 49% against under 10%. Strengths: code attack closed, ablations pass, skill gap 61.8, zero cap hits. |
| Market fit | 4 | Still cards-only, tuckbox, 2 players, about 20 minutes. Family fit 3.11 is a known drift, not new. |
| Production | 5 | 50 cards, 2 reference cards, 3 tokens. About 2 USD to print. |

## Originality
Closest: Hanabi (medium); also The Crew, Bomb Busters, Sky Team. Core mechanic unchanged this cycle; no copying; not a KILL.

## Rules clarity
A new player can learn the turn from the text, but the Single Offer adds a conditional ("legal only if all your fitting cards for that ship share one value, decided per target ship") that is harder to teach than what it replaced. Open ambiguities: two copies of one fitting value count as one value; Single on one ship while Pair is legal on another; skip during Last Watch advancing the counter; Single card equal to L or H. The playtester coded an interpretation for each, but humans need them written in the rules. Stale text: 7.4 says the Single Offer "turns that hand into a useful signal instead of a waiting turn" (it cut 4 points of Trim share); 7.6 Fog estimates (F6 and F2) are measured wrong; Known gaps still say values are "estimates".

## Fun
- Strength: the pair-Offer choice (which two lamps, knowing the token picks) is a real decision and the Single Offer is a clean fallback.
- Weakness: Trim stall. Trim share is 25% at 2p (borderline) but 3+ Trim runs are in 54% of 2p games and 49% of 3p games. Greedy, which Trims only when no Offer is legal, still Trims 18% of turns with runs in 40% of games, so many Trims are forced by hands with no fitting card, not by bad choices. Honest's Trims are 66% voluntary (an Offer exists but would cost a needed lamp), which is a decision but not an interesting one to sit through for three turns running.
- Comeback (L3, co-op reading): Trim selection works as repair (trim-blind -12.9 / -16.4) and round 1 decides nothing, but a repair that fires on a quarter of turns, in streaks, is a waiting action.

## Balance (playbook check)
- Two bots (L2): yes (Honest, Greedy, Random). The Greedy-over-Honest gap of +10.8/+11.0 appears at every Fog setting, which is the L2 signature of a bot artefact (Honest too cautious), but it is also the exact symptom the design said it would not accept. It is unresolved, not disproven. The Honest variant with Greedy's Light threshold was not run (budget request not approved).
- Win band (L5, L8): Standard F6 / F2 is out of band for both bots (63.0/73.8 and 61.9/72.9). The measured sweep gives in-band values only at 2p F10 (48.6/56.2) and 3p F8 (40.6/51.9). This is the same L5 lesson as before: Fog set by estimate rather than sweep. It is mechanical: change the table.
- Length: 2p F10 gives 21.0 turns, under the 22-26 target (about -9% against 23.1 midpoint; inside the +-20% of the 20-minute brief if minutes track turns, so tolerable). F9 gives 52.1/62.1 and 21.7 turns; F8 gives 57.4/65.8 and 22.2 turns. Choose F9 or F10; do not rerun to find a third.
- Ablations (L1): pair-blind -6.9/-6.0, trim-blind -12.9/-16.4, no counting -9.4/-8.3, all at or above 5. Pass.
- Code attack: +2.8 at F6, +2.3 at F10 (limit 10). Pass.
- Skill gap 61.8 (target 20). Pass. Turn-cap hits 0.
- Single Offer (L10): the single-change check shows it is used and valuable (single-blind -12.9 win points) but explains only about 4 points of the Trim drop (Trim 29% to 25%, 3+ runs 60% to 54%). The cycle bundled the Single Offer, the Beacon cut and new Fog values, so the Trim drop from 30% to 25% cannot be attributed beyond that single-blind check. The Beacon cut removed a time gift, so the Fog sweep is the only place it shows.
- 3p: unbalanced at Standard F2, Greedy +11.0; labelled variant, which is the right call (L8). In band at F8 only.

## Market fit and production
No drift. Cards only, tiny cost. The panel's lowest fit is family (3.11), unchanged and unaddressed.

## Biggest strength
The core Offer puzzle with the pair-versus-single choice, now protected by an anti-code design that holds (code attack +2.3 to +2.8) with all three twist ablations passing and a 62-point skill gap, in a 52-card tuckbox.

## Biggest weakness
Trim as a forced or low-value waiting action: 3+ Trim runs in about half of all games (target under 10%), unmoved by two cycles (61% to 54%). This repeats L11 (a rule that blocks cheating forces dead turns), L5 (win band tuned by estimate; Standard is out of band), L10 (bundled changes), L2 (Greedy/Honest gap that may be a bot artefact) and L9 (the Trim fix was mechanical in intent but did not move the number).

## Required changes
1. **Reset the Fog table from the sweep** (balance: both bots in 40-60): 2p Standard F9 or F10 (Honest 52.1 or 48.6, Greedy 62.1 or 56.2; pick F10 for band, accepting 21.0 turns); 3p Standard F8; recalibrate Calm and Storm around those. No new run needed beyond a confirmation of the chosen cells.
2. **Write the four Single Offer rulings into the rules text**, update stale lines in 7.4, 7.6 and Known gaps to the measured numbers, and keep the line count from growing (clarity, L7).
3. **Do not iterate the Trim stall on bots again.** List it in Known gaps as an open risk with the numbers (54% / 49%), and make it the first question of the human test: do real players find consecutive Trim turns boring? (fun).
4. Optional, and only after a human says the stall hurts: try a no-discard draw action or hand size 6 in place of forced Trim. These are guesses, not diagnoses.

## Mechanical or structural?
- Mechanical: Fog values (a table edit backed by the sweep), the four ambiguities, stale text.
- Structural: the Trim stall. It comes from hands that fit no open range (the legality rule that closes the code channel) interacting with a shrinking range late in the game. Offer legality cannot be loosened without reopening the code channel, and the Single Offer, the one targeted fix, recovered about 4 points of 30. The Greedy-over-Honest gap is probably a bot artefact, but that is unconfirmed.

## Is another revision worth it?
No for bot cycles: the stall is structural, one cycle moved it about 4 to 7 points against a 15-45 point need, and humans are the only way to learn whether it matters. A single mechanical edit (Fog table plus wording, no playtest beyond a confirm of the chosen cells) is fine and cheap; the KPI to check is both bots in 40-60 at 2p Standard. Then take a human playtest. Yes, I now recommend the human playtest instead of more bot cycles, with the main KPI being Trim runs: if humans report the middle as dull, the next revision should be a structural rework, not a tweak.
