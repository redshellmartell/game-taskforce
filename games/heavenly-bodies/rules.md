# Heavenly Bodies: Rules (cycle 2)

> **Owner-supplied game, studio revision 2.** Built from the owner's **Rules v2** (Part 1 of `source-design-doc.md`). Cycle 2 is a **simplifying** revision: it cuts rules the simulation showed to be inert and fixes the Star outliers. **Every change is listed in section 8 (Change log) with its reason and KPI so the owner can veto it.** Answers that move results stay marked **PROVISIONAL**. Card list: `cards.md` (machine-readable: `cards.json`). Gap rulings: Appendix A (reference, not part of the teach).

---

## 1. Overview

- **Title:** Heavenly Bodies (working title).
- **Hook:** each player is a **Star** with a ring of four orbital positions. At the start of every turn your planets and moons (**Celestial Objects**, COs) **turn one step clockwise**, like a clock. Where you place a CO decides where it will be next round, and the CO in your **North** position is exposed to your opponents. Win by destroying an opposing Star, or by building enough Size in orbit and holding it for a full round (**Critical Mass**).
- **Players:** 2 to 6. 1v1 and free-for-all (3+ players, last Star standing) use the same rules.
- **Play time:** about 10-15 minutes at 2 players, 25-35 minutes at 6.
- **Age:** 12+ (studio proposal).

## 2. Components

| Component | Count | Notes |
|---|---|---|
| Star cards | 12 | HP 8 (x3), 7 (x2), 6 (x5), 5 (x2). Not in the deck. List in `cards.md` section 1. |
| Celestial Object (CO) cards | 36 | Size 1-5, Stability 1-5, all unique. |
| Astronomical Event (AE) cards | 60 | 16 Augmentations, 44 Direct Effects, all unique. |
| **Total cards** | **108** | 12 Stars + 96-card draw deck. |
| HP trackers | 6 | A d10 or 0-9 dial per player. |
| Countdown markers | 6 | Put on your Star when you announce Critical Mass. |
| First-player marker | 1 | |

No board. Your four positions are the spaces directly above (**North**), right (**East**), below (**South**) and left (**West**) of your Star card.

**Zones.** *Draw deck* (shared, face down). *Discard pile* (shared, face up, public). *Out of Orbit zone* (shared, face up, public, no owners). *Orbit* (your 4 positions, at most 1 CO each). *Hand* (hidden; the number of cards is public).

## 3. Setup

1. Choose the first player at random. Play passes clockwise (to the left).
2. **Choose Stars** (the table picks one variant). *Draft:* lay out all 12 Stars face up; players pick one each in **reverse turn order**. *Deal 2, keep 1:* deal 2 random Stars to each player; each keeps 1 secretly, then all reveal; the rest go back to the box.
3. Set your HP tracker to your Star's printed HP. This is also your maximum HP.
4. **Critical Mass threshold** by the number of players at setup: **2p 14, 3p 15, 4p 16, 5p 17, 6p 16.** It never changes during the game.
5. Shuffle the 96 COs and AEs into the draw deck. Deal 5 cards to each player.
6. **Mulligan:** in turn order, a player whose 5 cards include **no CO** may reveal them, shuffle them into the deck and draw 5 new cards, once. The new hand is kept.

## 4. Turn structure

### 4.1 Start of Turn
1. Your "at the start of your turn" triggers resolve.
2. Draw 2 cards. **The first player skips this draw on the first turn of the game only.**

### 4.2 Rotation Phase
Every CO in your orbit moves one step **clockwise** (North to East, East to South, South to West, West to North) at the same time. Rotation never causes a Collision. Other players' orbits do not move. Then your "at the end of your Rotation Phase" triggers resolve (CO27).

### 4.3 Play Phase
Make **up to 2 plays** in any order (0 or 1 is allowed). Each play is one of:

**A. Place a CO** from your hand into **your own** orbit, on any position its printed restriction allows ("Must enter North"). An occupied position is legal: a Collision follows (5.2) and the placed CO is incoming. Its enters-orbit trigger resolves first, even if it then loses the Collision.
- **CO cap (PROVISIONAL):** at most **1 CO may enter each orbit per turn**, from any source (placing, reclaiming, a card that places). A CO that enters and loses its Collision still used it. Moving and rotating are not entering. Only ST09 and AE46 ignore the cap.

**B. Play an AE.**
- **Augmentation:** attach it to a CO in orbit its text allows (no host named = one of your COs). It stays until that CO leaves orbit, then is discarded. No legal host = cannot be played. Its condition is checked only when played.
- **Direct Effect:** resolve it, then discard it.
- **Legality:** a card is legal only if every "Choose" in it (in the option you pick, for "Choose one" cards) has a legal choice and every "Play only if" is true. An option without "Choose" (such as "or draw 1 card") is always legal. Other parts do as much as they can. An illegal card played by mistake returns to hand and uses no play.
- **Costs** ("Cost: ...") must be paid in full, before the effect. A self-damage cost can eliminate you; then the effect does not happen.
- **Targets:** "an opponent" is the acting player's choice. Any Star may be targeted.

**Active abilities (not a play).** A sentence marked "Active", or a "Once per turn, you may ..." sentence with no "when", "whenever" or "at the start/end of", may be used in your own Play Phase between plays, **once per turn per source**. A reclaim this way uses the CO cap unless the text says otherwise.

No card is ever played on another player's turn. Reclaims happen only through cards that say "reclaim".

### 4.4 End of Turn
1. Your "at the end of your turn" triggers resolve.
2. **Critical Mass (your own total only; PROVISIONAL):** (a) if your countdown is running and this is its deadline turn, and your total Size is at or above your threshold, **you win**; (b) otherwise, if no countdown of yours is running and your total is at or above your threshold, **announce**: put your countdown marker on your Star. Its deadline is the end of your **next** turn.
3. **Hand limit:** discard down to 7 (your choice).
4. "This turn" effects end.

Play passes to the next player still in the game.

## 5. Special rules and timing

### 5.1 Size and Stability
- **Effective value** = printed value plus all modifiers, floored at 0 (sum first, then floor). It may exceed 5. Every check uses effective values.
- **Stability 0:** the CO is **knocked out** (to the Out of Orbit zone) at once, including when a bonus ends.
- **Size 0:** the CO is **discarded** at once. If Size and Stability are both 0, it is discarded.
- COs outside orbit have no modifiers: checks on them use printed values (AE45 "Size 3 or less").
- A CO leaving orbit as a cost or effect is judged by its effective values just before it left (AE28).

### 5.2 Collisions and movement
A **Collision** happens whenever two COs would occupy one position (placing, reclaiming or moving; never rotating). The CO with **lower effective Stability** is knocked out; if tied, the **smaller effective Size**; if still tied, the CO already there (the incoming CO wins). A card changes this only if it says so; if both COs say they win, ignore both. Collisions happen only inside one orbit.

**Moving a CO** within an orbit (by a card or ability) is not entering: no enters-orbit trigger, no CO cap. If the destination is occupied, a Collision follows and the moved CO is incoming.

**"Rotate an orbit one step"** on a card: every CO in that orbit moves one step clockwise at once, as in 4.2 (no Collision, no "end of Rotation Phase" triggers).

### 5.3 Out of Orbit zone and ownership
- Knocked-out COs go here and stay until reclaimed or removed. Their Augmentations are discarded. **Knocked out** always means leaving an orbit this way; discarding (Size 0, AE40) and returning to hand are not knockouts. If a card sends a knocked-out CO elsewhere (ST11), it still counts as knocked out.
- Any player may **reclaim** any CO from here into their own orbit, through a card or ability that says "reclaim". It follows placement rules (restriction, Collision, CO cap) and fires its enters-orbit trigger.
- A CO's **owner** is the player whose orbit it is in. An Augmentation's "you" is the player who played it.

### 5.4 Triggers (PROVISIONAL)
- "When", "whenever" and "at the start/end of" abilities are **triggers**; they work on any player's turn. A "you may" choice is made when the trigger resolves. A trigger marked "once per turn" can fire once in **each player's turn**.
- If several fire at once, the active player stacks theirs in any order, then each other player in turn order; the **last stacked resolves first**, and a new trigger goes on top. Each item fully resolves (Collisions and knockouts included) before the next.

### 5.5 Deck, hand and information
- Empty deck: when a card must be drawn or looked at, shuffle the discard pile into a new deck. If both are empty, skip the rest. The Out of Orbit zone is never shuffled in.
- "Look at the top N": if the deck holds fewer than N, look at what is there.
- A Star never goes above its printed HP.

### 5.6 Elimination
- A Star at 0 HP is eliminated at once. Its orbit, hand and all Augmentations its player put on other COs are discarded; its countdown ends.
- If the active player is eliminated, their turn ends and their pending triggers are removed.
- Several Stars reaching 0 together are eliminated together; if none would remain, the active player wins.

### 5.7 Timing words
- "**This turn**" effects end at End of Turn step 4. "**Until the start of your next turn**" effects end at the start of that turn, before triggers, or when that player is eliminated.
- "**Since your last turn**" means since the end of your previous turn (on your first turn, since the game began).
- **Next to:** North and South are each next to East and West (not to each other).

## 6. End of game

The game ends the instant a player wins. No points.

**Star Destruction.** When a Star reaches 0 HP: at 2 players the other player wins; at 3+ the player is eliminated (5.6) and the **last player remaining wins**.

**Critical Mass.** **Total Size** = the sum of the effective Size of the COs in your orbit. **Threshold:** 2p 14, 3p 15, 4p 16, 5p 17, 6p 16 (ST10: 2 lower). Announce and win only at your own End of Turn (4.4); earliest win is your 4th turn.
- **Cancel (PROVISIONAL):** after each play, Active ability, Start of Turn and Rotation Phase has fully resolved (on any player's turn), and at End of Turn step 2, a running countdown whose owner's total is below their threshold is cancelled. To announce again you must reach the threshold at a later End of Turn.
- A countdown gives no protection. Ties cannot happen: the first win check that is true ends the game.

**Turn cap:** none in play. The simulation uses 30 rounds (a draw) and reports any hits.

---

## 7. Design notes

### 7.1 Intent
- **The twist: a clock you plan.** Your orbit turns one fixed step every turn, so every CO visits North once every four of your turns. North is exposed (AE22, AE41, AE55, AE60 hit only an opponent's North) and also pays (AE07, AE16, AE20, AE28, CO21, CO25, CO27 reward your own North). East, West and South carry bonuses for a few cards (CO07, CO16, AE05). The decision is **where to place** each CO, knowing what the clock will bring into North next round: a big CO in North pays you and is a target for everyone.
- **Two co-equal win paths:** Star Destruction (immediate) and Critical Mass (a held state with a one-round window for counterplay). The threshold scales with player count because damage spreads over more opponents in big games.
- **No mana.** Throttles: 2 plays, 1 CO entering per turn, per-card costs.

### 7.2 Comeback
Catch-up damage (AE30, AE35, AE31, ST07), catch-up draw (AE08), cheap countdown answers (AE23, AE41, AE43, AE55, AE60 plus AE32, AE52, AE53, ST12), and free-for-all dogpiles on a Critical Mass leader. KPI: runaway leader at most 65% (cycle 1: 60.7), lead changes at least 2 (3.78). No Critical Mass win before your 4th turn.

### 7.3 Target bands and knobs
| Measure | Band | Knob |
|---|---|---|
| Win path split, each count | each path 40-60% | threshold per count (±1) |
| Seat gap, 2p | at most 5 points | first-player turn-1 draw |
| Star round-robin, 2p | every Star 40-60% | that Star's HP (±1) |
| HP 5 Stars at 4p (two targeting bots) | each 15%+ (fair 25) | ST10/ST12 HP 5 to 6 |
| Cancel share | 45-55% at every count | AE23's Stability option (cut it if 4p+ stays above 55) |
| Dead cards per 7-card hand | under 3 | count of host-needing Augmentations |

### 7.4 Skill
Good play shows in placement (what the clock brings into North and when), holding an answer for a countdown, choosing when to switch from building to damage, and target choice at big tables. Cycle 1 gap: 88.7 points (strategic vs random); target at least 20.

---

## 8. Change log

### Cycle 2 (revision 2): simplify
Responds to `critique.md` revision 1 (REVISE-MAJOR, 3.17, required changes 1-7) and `playtest-report.md` revision 1. **The owner may veto any row.** Bundled changes (L10): each row names its single-change test.

| # | Change | Was | Reason (feedback) | KPI it should move |
|---|---|---|---|---|
| C2-R1 | **Rotation is always clockwise**; the direction choice is removed. Card rotations are clockwise too. (Restores the owner's original note.) | Active player chooses (R3, G1) | Critic change 1: always-clockwise bot lost by only 0.9 (2p) / 2.4 (4p); L12 | Rule lines down 15+ with seat and path KPIs held; placement-blind bot loses by 5+ (new test) |
| C2-R2 | **Anchors and retrograde removed**: CO21, CO27, AE16 lose them; AE14, AE15 replaced. Rotation can never cause a Collision, so the rotation-Collision rules and the anchor exception are deleted | G12, G13, F2 | Critic changes 1 and 5 (inert rule weight); AE14 1.5%, AE15 5.1% played | Rule lines; ambiguities to 0 |
| C2-R3 | **Recycle removed** | R6 | Never-Recycle bot won 54.9% (critic change 5) | Rule lines; win rates unchanged |
| C2-R4 | ST11: **HP 5 to 6**, new ability (capture: an opponent's knocked-out CO may go to your hand); the reclaim-damage loop is gone | HP 5, reclaim loop (R8) | Critic change 2: ST11 29.7%, ability-off +2.4 (inert) | ST11 40-60 at 2p; 15%+ at 4p |
| C2-R5 | ST05: **HP 7 to 6** (HP curve now 8x3, 7x2, 6x5, 5x2, mean still 6.5) | 7 | ST05 65.4% at 2p, above band | ST05 into 40-60 |
| C2-R6 | **Six low-use Augmentations become host-free Direct Effects** (same IDs): AE04, AE07, AE08, AE14, AE15, AE17. Augmentations 22 to 16 | Augmentations | Critic change 4 (AE14 1.5, AE17 3.3, AE04 4.2, AE08 4.9, AE07 5.0%); playtest problem 5 | Dead cards per hand under 3 (estimate 2.85 to about 2.5); each new card played 5%+ |
| C2-R7 | **AE41 hits one opponent's North**, not every opponent; **AE60 always moves clockwise** | each opponent; chosen direction | Critic change 6: cancel share 58-68% at 4p+; AE41 was the only answer that scaled with opponents | Cancel share at 4p+ toward 45-55 |
| C2-R8 | Rules text compressed; gap table moved to Appendix A; cancel moments in one sentence (same five moments) | about 160 playable lines | Critic change 5, L7 | Playable rules (sections 1-6): 121 lines with blanks, about 90 of text |
| - | **Kept on purpose:** mulligan (owner ruling R2; inert in the sim but costs 2 lines), first-player skip (G4), 6p threshold 16 and the F11 draw options (not yet re-simulated; critic said do not change) | | | |

**Cards changed in cycle 2 (14, details in `cards.md`):**
| Card | New text (short) | Why |
|---|---|---|
| ST05 | HP 6 | Above band |
| ST11 | HP 6; "Once per turn, when an opponent's CO is knocked out, you may put it into your hand instead." | Inert loop; weakest Star |
| CO21 | "While this CO is in your North position, it has +2 Size." | Retrograde removed; North pays and exposes |
| CO27 | "At the end of your Rotation Phase, if this CO is in your North position, draw 1 card." | Anchor removed; clock payoff |
| AE16 | Augmentation: +1 Size, or +2 Size while in your North | Anchor removed; kept its popular +Size |
| AE04 | Direct Effect: one of your COs gets +2 Stability and cannot be chosen by opponents until your next turn | Replaces AE04 + AE17 protection as a one-shot |
| AE07 | Draw 1; draw 2 instead if your North CO has Size 4+ | Host-free; North payoff |
| AE08 | Draw 1; draw 2 instead if an opponent has more COs than you | Host-free; catch-up |
| AE14 | Draw 1; then you may swap two of your COs | Host-free; position control without a direction rule |
| AE15 | Prevent the first 2 damage from opponents until your next turn; draw 1 | Host-free; helps low-HP Stars at big tables |
| AE17 | Draw 2, then discard 1 | Host-free; hand filter (replaces Recycle's job) |
| AE41 | One opponent's North CO -1 Stability; draw 1 | Cancel share at 4p+ |
| AE57 | "in either direction" removed | C2-R1 |
| AE60 | Moves clockwise (no direction choice) | C2-R1; trims a cheap answer |

### Cycle 2: three candidates for the main problem (rotation inert)
1. **Simplifying cut (picked):** fixed clockwise, remove anchors and retrograde. The clock stays as a planning layer (placement decides what reaches North) and the rules lose the direction choice, the rotation-Collision order and the anchor exception.
2. **Rotation central, "North burns":** keep the direction choice and give North an intrinsic stake: the CO that ends your Rotation Phase in North gets -1 Stability until your next turn. A wrong direction would cost a CO, so the ablation would surely pass. **Lost:** 11 of 36 COs have Stability 1 (locked grid), so it kills them on arrival in North and would gut Critical Mass (the 2p split took a cycle to reach 50/50, L13); it adds a rule while the critic asks for fewer; and choosing direction every turn for a penalty is bookkeeping, not fun.
3. **Cross-pollinated from v2, "Spin any orbit":** the Rotation Phase rotates any one orbit (yours or an opponent's), as in Gearbox. **Lost:** in v2 a spin is an attack because touching orbits crash; v1 orbits do not touch, so a spin only matters through position cards again, the same card-payoff fix that failed in cycle 1 (L12). It also adds a decision with up to 6 targets at 6p.

**Second problem (Stars):** ST11 options were (a) HP 6 only, (b) a damage ability, (c) HP 6 plus a capture ability. (b) lost because it pushes 2p toward Star Destruction; (a) alone leaves an inert ability on the card; (c) adds card value, not damage, and gets stronger at big tables, where HP 5 Stars are weakest.

**What I would try next if this works:** a human teach test of the shortened rules, timed; then cut the Out of Orbit "reclaim by anyone" breadth if humans find it fiddly.
**What I suspect is still wrong:** (1) rotation may now be pure flavour: if the placement-blind bot also loses by under 5, the owner should decide whether the clock is theme only; (2) ST10 and ST12 (HP 5) may still be under 15% at 4p; (3) AE04 and AE15 are defensive and could drop the 2p cancel share below 45 or slow 2p games; (4) the extra draw on five new cards may shorten games slightly; (5) ST11's capture could be strong at 6p (many knockouts per round).

### Cycle 1 (revision 1) and fix-before-critic pass, for reference
R1 first player skips turn-1 draw (owner ruling, kept); R2 mulligan (owner ruling, kept); R3 direction choice (**reverted by C2-R1**); R4/R12 threshold 12 + players, max 17, 6p 16 (kept); R5/F6 cancel checked after each resolution (kept, compressed); R6 Recycle (**cut by C2-R3**); R7 ST01 HP 9 to 8 (kept); R8 ST08/ST10/ST11/ST12 buffs (ST11 **replaced by C2-R4**); R9 gaps answered (Appendix A); R10 eliminated player's Augmentations discarded (kept); R11 reverse-order draft (kept); F2 anchors in Rotation Phase only (**obsolete**, anchors removed); F3-F5, F7, F9, F10 rulings (kept, F5 obsolete with ST11's new text); F8 Recycle legality (**obsolete**); F11 draw options on AE32, AE42, AE44, AE50, AE52, AE59 (kept). Cards reworked in cycle 1: AE16, AE23, AE25, AE28, AE41, AE43, AE45, AE49, AE55, AE57, AE60, CO14, CO24 (see `cards.json` `previous_text`).

---

## Appendix A. Gap rulings (reference for the playtester; not part of the teach)
P = PROVISIONAL (moves results; owner may change).

| Gap | Ruling | Where |
|---|---|---|
| G1 | Rotation always clockwise (cycle 2) | 4.2 |
| G2, G3 | Random first player, play clockwise, reverse-order draft; Stars before hands; unkept Stars to the box | 3 |
| G4 | First player skips turn-1 draw (owner ruling) | 4.1 |
| G5, G6 | Start triggers then draw; End: triggers, Critical Mass, hand limit, "this turn" ends | 4.1, 4.4 |
| G7 (P) | Only your own total, only at your own End of Turn | 4.4 |
| G8 (P) | Cancel after each play, Active ability, Start of Turn and Rotation Phase, and at End of Turn step 2; dips inside a play do not count | 6 |
| G9, G11 | COs from hand only into your own orbit; moves: no trigger, no cap, mover incoming | 4.3, 5.2 |
| G10 (P) | 1 CO enters each orbit per turn, any source; a loser still used it | 4.3 |
| G12, G13 | Retired: rotation never causes a Collision (cycle 2) | 4.2 |
| G14-G19 | Two "wins" effects cancel; floor after summing; Stability 0 knocks out (also when a bonus ends); Size 0 discards and wins ties; "knocked out" = to Out of Orbit; values may exceed 5 | 5.1-5.3 |
| G20-G26 | Owner = orbit holder; default host; legality of "Choose" and "Play only if"; costs paid first | 4.3, 5.3 |
| G27 (P), G29 (P) | "Once per turn" triggers once in each player's turn; stack: active player first, last stacked resolves first | 5.4 |
| G28, G32 | "Since your last turn"; "this turn" and "until your next turn" end points | 5.7 |
| G30, G31, G33 | Elimination of the active player; their Augmentations discarded; simultaneous zero | 5.6 |
| G34-G37 | Hand-limit discards chosen; reshuffle rules; HP cap; public zones | 4.4, 5.5, 2 |
| G38-G40 | "Next to", "wins a Collision", age 12+ | 5.7, 5.2, 1 |
| New (cycle 2) | ST11 capture still counts as a knockout (ST03 and ST06 trigger; AE34 does not count it, it is not in the zone). AE14 swap: both move at once, no Collision. AE15 prevention applies after CO31's reduction. AE04: "cannot be chosen" covers Direct Effects and Augmentations that name it; AE52 (which chooses a player) can still remove it | 5.3, `cards.md` |

---

## Playbook check
1. **Family:** `studio/mechanics.md` "Asymmetric roles" plus "All families". Trap: keyword abilities that do not change best play, and a side gap that depends on the bot; hence ability-off tests for the reworked Stars and a second targeting bot.
2. **Comeback:** catch-up damage (AE30, AE35, AE31, ST07), catch-up draw (AE08), cheap countdown answers, damage shield for low-HP Stars (AE15), dogpiles. KPI: runaway at most 65% (cycle 1: 60.7), lead changes at least 2 (3.78).
3. **Ablations (2p, 3p, 4p, 6p; each must lose by 5+):** (a) **placement-blind bot** (places COs on a random legal position, ignores where the clock moves them; tests the clock); (b) **rule ablation:** no Rotation Phase at all, report path split and position-card play rates (if nothing moves, rotation is theme only; owner's call); (c) ST11 ability off; (d) never-mulligan (expected small, owner ruling); (e) **two targeting bots at 4p and 6p** (focus-lowest-HP and leader-targeting) for the Star round-robin; (f) single-change tests: ST05 HP 7 vs 6, AE41 old vs new (cancel share 4p/6p).
4. **Self-check:** fixed in this pass: rotation Collision order (deleted), anchor/retrograde exceptions (deleted), Recycle legality (deleted), ST11 reclaim-damage ruling F5 (obsolete), AE60 direction (fixed), AE57 direction (fixed), "knocked out to hand" for ST11 (ruled in 5.3), AE14 swap (no Collision, on card), AE15 with CO31 (Appendix A), AE04 vs AE52 (Appendix A). New dead-card risk: AE04 needs one of your COs (5 of 6 new cards always legal). Undefined cases: empty deck (5.5), ties (6), simultaneous triggers (5.4), simultaneous zero (5.6).
5. **Band and knob:** section 7.3. Path split 40-60 each count (threshold); Stars 40-60 at 2p (HP); HP 5 Stars 15%+ at 4p (ST10/ST12 HP); cancel share 45-55 (AE23 option); seat gap at most 5 (turn-1 draw).
6. **Ends:** Star Destruction or Critical Mass; the reshuffle prevents deck stalls; sim cap 30 rounds (0 hits so far). Expected 2p about 9-10 player turns, about 12 minutes; 6p 25-35 minutes.
7. **Budget:** playable rules (sections 1-6) are 121 lines including blank lines, about 90 lines of text (was about 160; critic target under 130). Special rules: rotation (fixed), Collisions, CO cap, Out of Orbit zone, Critical Mass countdown, trigger stack (6, was 8 with direction choice and Recycle). No brief promise (owner-supplied); a one-page teach is still not met (L7, known gap). Never timed with a human.
8. **Re-run list:** legality (Recycle cut), rotation and card changes, so re-run **all** ablations at every count plus the headline set: seat gap, path split per count (including 6p at 16), Star round-robin (2p 1,100 games each; 4p with both targeting bots), dead cards per hand, cancel share per count, play rates of the 14 changed cards and of the six F11 cards, runaway, lead changes, length.
