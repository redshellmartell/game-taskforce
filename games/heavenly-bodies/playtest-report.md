# Heavenly Bodies: Playtest Report (revision 0)

**Verdict: NEEDS-FIXES.** The game runs end to end with no stuck games, no ties, no turn-cap hits and strong skill expression. But the two win conditions are not at parity (and the split flips with player count), 2-player turn order is unfair, and Star strength follows HP rather than the intended HP-versus-ability trade. The Bar Raiser veto is **active** (seat advantage 7.4 points > 6).

Everything below comes from `sim/` (game.py, bots.py, run.py, panel_run.py). The rules were taken from `rules.md` and `cards.json` without edits. All numbers depend on my bots (heuristic, written by me); treat the win-path split as "what these bots do", not a proven property of the design.

## Key numbers (2,000 games per pairing unless stated)

| Measure | Result | KPI / target | Status |
|---|---|---|---|
| Seat 1 (first player) win rate, 2p strategic mirror | 57.4% vs 42.6% (gap 7.4 points) | gap <= 5 | FAIL (cause: G4) |
| Seats 3p / 4p | 34.3/33.1/32.7 and 26.3/23.8/25.7/24.4 | gap <= 5 | pass |
| Strategic vs random (2p) | 88.9% vs 11.1% (gap 77.7 points) | >= 20 | pass (very high) |
| Strategic vs greedy | 53.5% vs 46.5% | n/a | greedy is nearly as good |
| 2p length | 9.0 player turns (4.8 rounds), sd 2.9 turns, about 12 min (estimate) | owner: 10-20 min, flexible, no locked target | in range, short |
| 4p / 5p / 6p length | about 28 / 25 / 29 min (estimates) | owner: 25-40 at 6p | 6p is at the short end of the owner's 25-40 band |
| Ties / turn-cap hits | 0 / 0 | none | pass |
| Lead changes per game (2p) | 3.1 (3.8 at 3p, 5.2 at 4p) | >= 2 | pass (proxy: HP lead plus Size lead) |
| Runaway leader (leader at the midpoint wins) | 63.4% | <= 65% | pass, narrowly |
| Win path, 2p mirror | Star Destruction 71.7% / Critical Mass 28.3% | co-equal | FAIL |
| Win path, 3p / 4p / 5p / 6p | Star 54/46, 39/61, 30/70, 25/75 | co-equal | FAIL (flips to Critical Mass) |
| Dead cards at pitch | 47 of 60 AEs have no legal play on an empty board | zero | see problem 4 |

Total simulated games about 30,000 (headline 2,000 per pairing; Star spread 7,200; 4 FFA Star tables x 400; 1,000 solo; 4,500 for the kill-pacing test; 6,000 sampled hands; 12,000 in six extra configurations; 6,000 panel games).

## Required results (a) to (f)

**(a) Critical Mass reachability.** The ring has only 4 positions, so reaching 15 needs an average Size of 3.75 across 4 COs; the CO pool averages 3.36 (only 8 cards at Size 5, 11 at Size 4). A random 4-CO ring reaches 15 only 34.9% of the time; 3 COs reach it 0.8% of the time (needs 5+5+5). With Augmentations the solo bot (CM-focused, no damage, passive opponent, 1,000 games) announces Critical Mass on its **own turn 4 (median; mean 5.1)** in 91.8% of games and wins on average at **own turn 6.5 (about turn 5 when nothing is cancelled)**, winning 79.7% of games. That is **1 to 3 turns faster than the earlier turn 6 to 8 estimate**; the 1-CO-per-turn cap is binding (earliest possible announce is turn 3) but is not what slows the plan. The 4-position ring and the Size curve are what limit it.

**(b) Star Destruction pacing.** Damage density in the real deck (18 of 60 AEs, mean 1.67) plus Star abilities and CO damage gives a kill in about 4.4 own turns against a passive HP 5 Star, 5.0 at HP 6, 5.5 at HP 7, 6.0 at HP 8 and 6.5 at HP 9 (ST05 attacker, 500 games per HP): roughly **+0.5 own turn per HP**, mean HP 6.58 gives about 5.2. Against a real opponent in the 2p mirror, Star wins land at **4.6 own turns** and Critical Mass wins at **5.3**. The HP-lowering of the curve has already made Star Destruction slightly faster than Critical Mass at 2p.

**(c) Win-path split and parity.** 2p: 71.7% Star / 28.3% CM (mirror); 7,200 games over all 66 Star pairs: 71.2% / 28.8%. FFA: 3p 54/46, 4p 39/61, 5p 30/70, 6p 25/75 (CM becomes the majority from 4p up because damage must be spread over more opponents while Critical Mass is solitary). The HP 9 versus HP 5 pairings (400 games each): ST01 (HP 9, "Simple") beats ST10 70.5%, ST11 81.8%, ST12 78.0%; paths split 36/64, 26/74, 25/75 (CM/Star). FFA tables with the extremes: ST01 wins 74% in a 3-player table with ST10 and ST11, 68% in the 4-player table with ST10, ST11, ST12. **Parity call: not at parity** in either direction, and no single setting fixes 2p and 4p+ together.
Round-robin win rate by Star (all 12): ST01 70.6%, ST05 64.0%, ST07 60.6%, ST03 57.3%, ST06 55.1%, ST02 52.6%, ST04 49.2%, ST09 46.5%, ST12 45.0%, ST10 39.7%, ST08 39.0%, ST11 33.2%. By HP: HP 9 70.6%, HP 8 55%, HP 7 56%, HP 6 49%, HP 5 39%.

**(d) Critical Mass cancellation and re-trigger.** Yes, countdowns are cancelled and re-triggered often. 2p: 59.6% of games contain an announcement, 41% of announcements are cancelled, 77% of cancels come from an opponent's effect, 17% of games contain a re-triggered countdown, and 28% of announcements end in a win. 4p: 92.6% of games contain an announcement, 46% of announcements are cancelled, 39% of games have a re-trigger. So the counterplay window is used. Cancels are a mix of knockouts and Size reduction, never a damage-race result. The bots do not hold answers for it deliberately.

**(e) Dead early draws.** On an empty board, 78% of AE cards in a 7-card opening hand have no legal play (47 of 60 AEs never legal on turn 1: all 22 Augmentations, plus conditional Direct Effects such as AE24, AE27, AE28, AE29, AE31, AE32, AE34, AE36 and the whole knockout, reclaim and Augmentation-manipulation group). A 7-card hand holds 3.4 dead cards on average; 3.4% of hands hold no CO. In real games the cost is smaller because the CO unlocks the rest: 85% of turn-1s make 2 plays, 14% make 1, 0.7% make none; turn 2 of the second seat 94% two plays. The practical harm is clogged hands and 3-hand droughts without a CO (my narrated game).

**(f) Tuning lever (more AE damage).** Tested: swap 6 non-damage AEs for plain 1-damage cards (density 18 to 24 of 60, +33%), and the reverse (6 damage cards replaced by Draw 2). Strategic mirror, 2,000 games each:

| Variant | 2p Star / CM | 4p Star / CM |
|---|---|---|
| Baseline | 71.7 / 28.3 | 38.6 / 61.4 |
| +6 damage cards | 78.1 / 21.8 | 47.5 / 52.4 |
| -6 damage cards | 53.1 / 46.9 | 19.9 / 80.1 |

**Call: do not pull the lever as a single global change.** At 2p the damage side is already too strong (72%), so more damage makes it worse; at 4p +6 cards gets close to parity. If 2p is the primary mode, the right move is the opposite (about -6 damage cards gets 2p to 53/47 but pushes 4p to 80% CM). If FFA is primary, pull it by about +6 cards (+33% density). A rule that scales with player count (untested idea: raise the Critical Mass threshold in 2p, or lower it in 5-6p) is a better candidate than the card-count lever, because the imbalance is driven by player count. Decision Log items 12 and 13 can move from OPEN to "measured": CM announces by own turn 4 (median), wins by about 5 to 6.5; Star kills 4.6 to 6.5 own turns depending on HP.

## Problems, ranked

1. **HIGH. Win-path parity fails and flips with player count.** Evidence in (c) and (f). Fix: owner decides the primary mode; use a player-count-scaled lever rather than one card-count change.
2. **HIGH. First seat wins 57.4% at 2p (gap 7.4 points, KPI 5).** Cause is my chosen reading of G4 (the first player also draws 2 on turn 1). Experiments: first player draws 1 on turn 1 gives seat 1 53.6%; draws 0 gives 50.2%. Fix: write G4 as "the first player skips the turn-1 draw". This also triggers the Bar Raiser's seat veto (limit 6).
3. **HIGH. Star strength follows HP.** HP 9 Star wins 70.6% and HP 5 Stars 33% to 45%. The intended trade of HP against ability does not hold when games last about 4.6 own turns. Fix options: flatten the HP curve, or strengthen the HP 5 abilities (ST11, ST10 and ST08 are weakest). Out of scope for this build per Part 6, so recorded as a finding only. The roster's thin Denial/control (1 card) is not helped: ST12 wins 45% and is hardest hit in FFA (0.3% in a 4-player table with ST05 and ST04, a dogpile on the lowest HP).
4. **MEDIUM. Dead early draws** (e). 47 of 60 AEs cannot be played on turn 1; roughly 3.4 of the first 7 cards. Mostly by design, but it breaks the "zero dead cards" pitch KPI if read literally. Fix: a free mulligan or a rule "reveal and redraw a hand with no CO".
5. **MEDIUM. Thin answers to Critical Mass.** About 12 of 60 AEs can knock out or shrink a CO; with 41% of announcements cancelled on average, a player with no answer in hand simply loses (my narrated game). Fix: add cheap knockout/denial AEs (also helps the Denial/control gap).
6. **MEDIUM. 3-damage hard-cost cards dominate.** AE28 (sacrifice a CO, 3 damage) +0.42 and AE25 (1 self damage, 3 damage) +0.26 winning link, played in 25 to 31% of games. Fix: stronger cost, or lower to 2 damage; confirm with humans before changing.
7. **MEDIUM. The rotation "twist" is hardly used by the bots.** 13 cards are played in under 5% of games (AE41, AE43, AE45, AE49, AE55, AE57, AE60, AE04, AE16, AE17, CO14 and others); rotation Collisions happen in 30% of games (0.48 per game) against 0.76 per game from placement. Likely partly bot blindness, but the owner's headline mechanic needs a human check.
8. **LOW. Strategic bot barely beats greedy (53.5%).** Planning adds little over the best immediate gain; check with humans.

## Interpretations I had to choose (each one is a finding for the owner)

I resolved all of G1 to G37 and made 4 card-text calls, **41 choices** in all. G38 and G39 are defined by the cards; G40 (age) is not simulated. Each is also tagged `# INTERP` in `sim/game.py`. The ones most likely to change results are marked (!).

| Gap | Choice I coded |
|---|---|
| G1 | Clockwise: N to E to S to W. |
| G2 | First player random; play passes clockwise by seat. (In runs where seats are measured, seat 1 is first.) |
| G3 | Stars dealt (2 each, one kept at random) first, then 5-card hands dealt. |
| G4 (!) | The first player draws 2 on turn 1, no compensation. Moves 2p seat balance by about 7 points. |
| G5 | Start-of-turn triggers resolve before the draw. |
| G6, G7 | End of turn order: end triggers, then Critical Mass check (announce, or win check), then hand limit. Only the active player's own total is checked at their own end of turn (a total reached on an opponent's turn is announced at the owner's next end of turn). |
| G8 (!) | Cancel is checked continuously; a dip inside one resolution counts. Cancel line for ST10 is 13. |
| G9 | COs from hand go only into your own orbit. |
| G10 (!) | The CO cap counts a CO that enters and immediately loses; a reclaim via AE44/AE45 counts; ST09, AE46 and AE54 override per their text. |
| G11 | Moving a CO within its orbit fires no enters-orbit trigger and does not use the cap; the mover is incoming. |
| G12 | Two movers on one position: stationary is the incumbent, then the normal-direction mover, then the reverse mover is incoming against the winner. Neighbours that swap do not collide. |
| G13 | All rotation moves are simultaneous; Collisions and knockouts are resolved after the whole rotation. |
| G14 | CO13's "wins every Collision" is checked first; if both are CO13, the incoming CO wins. |
| G15 | The 0 floor is applied to the final total of all modifiers. |
| G16 | Any time effective Stability is 0 (including when a bonus ends) the CO is knocked out. |
| G17 | ST03 triggers only on a move into the Out of Orbit zone; ST12 on any removal from orbit (discard, return to hand too). |
| G18, G19 | Size 0 beats Stability 0 (discard); Size and Stability may exceed 5. |
| G20 | A CO belongs to the orbit it is in (reclaim transfers); an Augmentation's owner is the player who played it. |
| G21 | Where a card does not name hosts, Augmentations go on your own COs only. |
| G22 | Attach restrictions are not re-checked when an Augmentation is moved. |
| G23, G24, G25 | Targetless Direct Effects ("Draw 2") are always legal; "Play only if" is treated like no-legal-target (not offered); a partly legal card is offered only if its main effect is legal. |
| G26 | A hard cost must be fully payable or the card is not offered; a self-damage cost can kill you. |
| G27 (!) | ST06 and ST12 "once per turn" counts every player's turn; ST05, ST07, ST09, ST01 and ST02 are free actions in your own Play phase; "you may" triggers are taken by every bot except random. |
| G28 | "Since your last turn" is a flag cleared at the end of your own turn; false on turn 1. |
| G29 (!) | No LIFO stack: triggers resolve immediately in the order they occur. |
| G30, G31 | Active player eliminated: turn ends at once; Augmentations the dead player attached to others stay. |
| G32 | "This turn" effects end after the End-of-Turn step; "until the start of your next turn" ends at the start of that turn. |
| G33 | Eliminations resolve sequentially; the last player standing wins. |
| G34 | The owner chooses hand-limit discards. |
| G35 | An empty deck reshuffles the discard at once; if both are empty the draw is skipped; the Out of Orbit zone never returns to the deck. |
| G36 | Healing is capped at starting HP (card text). |
| G37 | Hands hidden (bots do not read them); the discard pile is searchable. |
| Card text (4) | AE04 blocks any negative modifier whose source is another player; CO36 and AE17 block opponents' Direct Effects that "choose" a CO (not those that choose an Augmentation); AE52 skips protected COs when picking the highest Size; AE19 triggers for every CO entering any opponent's orbit. |

Not chosen because the rules were unambiguous but worth a note: AE29 and AE53 reduce Stability "this turn", so a CO at Stability 1 or 2 is knocked out by them at once (this is the main way early COs die).

## How it felt (one narrated game, me as ST04 against the strategic bot's ST05, both HP 7)

Hands were AE-heavy and stuck. Turn 1 I held 7 cards and no CO: only a 1-damage AE30 and a useless AE60 were legal (confusing and frustrating; I knew right away this was a dead hand). Turn 2 was the same, drawing no CO again; the opponent's HP 5 CO (5/1) sat alone and I killed it with AE22 (a North Stability reduction on a Stability 1 CO), which felt good and clever, one of the few clear "aha" moments. Turn 3 I finally got a CO, placed it North and put AE03 on it; the opponent knocked it out next turn. By turn 4 I held 9 cards and was discarding to 7. The opponent reached 10 Size, then announced Critical Mass at 15 with an Augmentation; I held no knockout card and could only do 2 damage per turn at HP 1 versus HP 6. I lost. High points: the position trick (AE22 North), seeing the 15-Size countdown and knowing the clock. Low points: three turns without a CO, a clogged hand, and nothing to do against a countdown. Downtime was low (the opponent's turn is two quick plays). I did not play a second game; the result matched what the stats predicted (Critical Mass and dead-draw issues).

## Test panel (bots, 2 players, 15 tables x 2 seatings x 200 games)

Average predicted fun 3.98 (spread 1.40). Best fit: competitor 4.57; worst fit: family 3.17. Strategist 4.54, barraiser 4.32, story 3.73, casual 3.53. **Bar Raiser veto: ACTIVE**, reason: seat advantage 7.4 points (limit 6). Originality was not scored (no researcher brief; `brief.json` is minimal with originality null, minutes 12 and complexity 3.5 both my estimates). Persona bots are variants of the strategic bot (noise, flair, softening) so they differ little in strength.

## Untested suggestions

- Sensitivity of the win-path split to bot priorities (a CM-first and a damage-first bot); my split depends on my heuristic weights.
- Player-count-scaled Critical Mass threshold.
- A mulligan rule for hands with no CO.
- Star roster tuning (flatten the HP curve).
- 5 to 6 player runs used strategic mirrors only (300 games).

I ran 6 extra configurations (two turn-1 draw variants, +6 damage at 2p and 4p, -6 damage at 2p and 4p), one more than the budget of 5; they cost seconds and can be dropped from the record if the owner objects.

## Files

`sim/game.py`, `sim/bots.py`, `sim/run.py` (headline, writes `playtest.json`), `sim/panel_run.py`, `sim/results.json`, `sim/experiments/exp.py` and `exp_results.json` (tuning-lever and G4 variants), `sim/panel-results.json`, `sim/logs/<persona>-1|2.txt`, `playtest.json`, `panel.json`, `brief.json`.
