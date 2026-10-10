# Heavenly Bodies: Rules (cycle 1)

> **Owner-supplied game, studio revision 1.** Built from the owner's **Rules v2** (Part 1 of `source-design-doc.md`). The owner opened all rules for this cycle; **every change to a previously locked, open or provisional rule is listed in section 8 (Change log) with its reason and the KPI it should move, so the owner can veto it.** All 40 rule gaps (G1-G40) from revision 0 are now answered (table in 5.10). Answers that move results are marked **PROVISIONAL**. Card list: `cards.md` (machine-readable: `cards.json`).

---

## 1. Overview

- **Title:** Heavenly Bodies (working title).
- **Hook:** each player is a **Star** with a ring of four orbital positions. Your planets and moons (**Celestial Objects**, COs) **rotate one step every turn, and you choose which way**, so your board is a clock you steer: what sits in your exposed North position, and what lands on a bonus position, is decided every turn. Win by destroying an opposing Star, or by building enough Size in orbit and holding it for a full round (**Critical Mass**).
- **Players:** 2 to 6. 1v1 and free-for-all (3+ players, last Star standing) use the same rules.
- **Play time:** about 10-15 minutes at 2 players, 25-35 minutes at 6 (owner's targets are flexible).
- **Age:** 12+ (studio proposal).

---

## 2. Components

| Component | Count | Notes |
|---|---|---|
| Star cards | 12 | HP 8/7/6/5, three of each (cycle 1; was 9/8/8/7/7/7/6/6/6/5/5/5). Not shuffled into the deck. Full list in `cards.md` section 1. |
| Celestial Object (CO) cards | 36 | Size 1-5, Stability 1-5, all unique. |
| Astronomical Event (AE) cards | 60 | 22 Augmentations, 38 Direct Effects, all unique. |
| **Total cards** | **108** | 12 Stars + 96-card draw pile. |
| HP trackers | 6 | A d10 or 0-9 dial per player. |
| Countdown markers | 6 | Placed on your Star card when you announce Critical Mass. |
| First-player marker | 1 | |

No board. Your Star card sits in front of you; your four positions are the spaces directly above (**North**), right (**East**), below (**South**) and left (**West**) of it.

**Zones.** *Draw deck* (shared, face down). *Discard pile* (shared, face up; anyone may look through it at any time). *Out of Orbit zone* (shared, face up, no size limit, no owners). *Orbit* (each player's 4 positions; at most 1 CO per position once any Collision has resolved). *Hand* (hidden; the number of cards is public).

---

## 3. Setup

1. Choose the first player at random (any fair method). Play passes **clockwise** (to the left).
2. **Choose Stars**, using one of two variants (the table picks):
   - *Draft:* lay out all 12 Stars face up. Players pick one each in **reverse turn order** (the last player picks first).
   - *Deal 2, keep 1:* deal 2 random Stars to each player; each keeps 1 secretly, then all reveal. Unkept Stars go back to the box.
   No two players have the same Star.
3. Set your HP tracker to your Star's printed HP. This is also your **maximum HP**.
4. Note the table's **Critical Mass threshold**: **12 + the number of players**, to a maximum of 17 (2p: 14, 3p: 15, 4p: 16, 5p-6p: 17). It does not change when players are eliminated.
5. Shuffle the 96 COs and AEs into the draw deck. Deal 5 cards to each player.
6. **Mulligan:** in turn order, each player whose 5-card hand contains **no CO** may reveal it, shuffle it into the draw deck and draw 5 new cards. Each player may do this once; the new hand is kept even if it has no CO.
7. All orbits, the discard pile and the Out of Orbit zone start empty.

---

## 4. Turn structure

Each turn has four phases in this order.

### 4.1 Start of Turn
1. Your "at the start of your turn" triggers resolve (see 5.5).
2. Draw 2 cards. **The first player skips this draw on the first turn of the game only.**

### 4.2 Rotation Phase
1. **Choose a direction: clockwise (North to East to South to West to North) or counter-clockwise.** Every CO in your orbit moves one step that way at the same time, including into empty positions. **PROVISIONAL (G1).**
2. Exceptions printed on cards: a CO that "does not move during your Rotation Phase" stays put; a CO that "moves one step in the opposite direction" moves one step against your chosen direction.
3. Plain rotation is a permutation and never causes a Collision. A Collision happens only when an exception puts two COs on one position; resolve it as in 5.2 (rotation Collisions).
4. Other players' orbits do not rotate in your Rotation Phase.

### 4.3 Play Phase
Make **up to 2 plays**, in any order. Playing 0 or 1 is allowed. Each play is one of:

**A. Place a CO** from your hand into **your own** orbit (G9).
- Choose any position that meets the CO's printed restriction (for example "Must enter North"). Placing on an occupied position is legal and causes a Collision (5.2); the placed CO is incoming.
- **CO cap:** at most **1 CO may enter each player's orbit per turn**, from any source (placement, reclaim, or a card that places). A CO that enters and then loses its Collision still used the cap. Moving a CO within an orbit and rotation are not "entering" and do not use the cap. Only ST09 and AE46 ignore the cap. **PROVISIONAL (G10).**
- The placed CO has **entered orbit** even if it loses its Collision: its enters-orbit trigger resolves first, then it is knocked out.

**B. Play an AE.**
- **Augmentation:** attach it to a CO in orbit that its text allows ("Attach to ..."; with no host named, the default is "one of your COs"). It stays until that CO leaves orbit, then is discarded. A CO may carry any number of Augmentations. An Augmentation with no legal host is illegal. Its attach condition is checked only when it is played, not when it is later moved (G21, G22).
- **Direct Effect:** resolve it, then discard it.
- **Legality.** A Direct Effect with no "Choose" in it is always legal. Otherwise it is legal only if **every "Choose" in it** (in the option you picked, for "Choose one" cards) has at least one legal choice. "Play only if ..." conditions must be true. Other parts do as much as they can. An illegal card cannot be played; if played by mistake it returns to hand and uses no play (G23-G25).
- **Hard costs** ("Cost: ...") must be payable in full, and are paid **before** the effect. A self-damage cost can eliminate you; if it does, the effect does not resolve (G26).
- **Targeting:** "an opponent" means the acting player's choice of opponent. Any Star may be targeted, including one with a running countdown.

**C. Recycle:** discard 1 card from your hand, then draw 1 card. You may Recycle twice in a turn (using both plays).

**Not a play: Active abilities.** A sentence marked "Active", or a "Once per turn, you may ..." sentence with no "when", "whenever" or "at the start/end of" condition (those are triggers, 5.5; for example ST06), on your Star or on your COs/Augmentations may be used during your own Play Phase, between plays, **once per turn per source**. It does not use a play. Reclaiming through such an ability does use the CO cap unless the ability says otherwise.

There is no instant-speed play: you never play cards on another player's turn. There is no generic reclaim action; reclaims only happen through a card or ability that says "reclaim".

### 4.4 End of Turn
In this order (G6):
1. Your "at the end of your turn" triggers resolve.
2. **Critical Mass check (your own total only, at your own End of Turn; PROVISIONAL, G7):**
   a. If your countdown is running and this is its deadline turn, and your total Size is still at or above your threshold, **you win**.
   b. Otherwise, if no countdown of yours is running and your total Size is at or above your threshold, **announce Critical Mass**: put your countdown marker on your Star. Its deadline is the end of **your next turn**.
3. **Hand limit:** if you hold more than 7 cards, discard down to 7 (you choose which).
4. "This turn" effects end (5.8).

Play passes clockwise to the next player still in the game.

---

## 5. Special rules and timing

### 5.1 Size, Stability and effective values
- **Effective** value = printed value plus all active modifiers, then floored at 0. Add all modifiers first, then apply the floor once (G15). Effective values may exceed 5 (G19). Every check uses effective values.
- **Stability 0:** the CO is **knocked out** (moved to the Out of Orbit zone) whenever its effective Stability is 0 after any change, including when a bonus ends (G16).
- **Size 0:** the CO is **discarded** (not knocked out) whenever its effective Size is 0. If Size and Stability reach 0 together, it is discarded (G18).

### 5.2 Collisions and movement
A **Collision** happens whenever two COs would occupy one position. Resolve it:
1. The CO with **lower effective Stability** is knocked out.
2. If tied, the CO with **smaller effective Size** is knocked out.
3. If still tied, the **incoming** CO wins and the CO already there is knocked out.
4. A card may change this only if its text says so. If both COs have an effect saying they win, ignore both and use steps 1-3 (G14).

Collisions only happen inside one orbit; there are no cross-player Collisions.

**Rotation Collisions (PROVISIONAL, G12, G13).** In a Rotation Phase all COs move at once; two COs that swap positions pass each other without colliding. Then, for each position holding 2 or more COs, using effective values in the new positions:
- the CO that did not move (if any) is the occupant; the CO that moved in your chosen direction collides with it first (and is incoming); a CO that moved in the opposite direction then collides with the winner (and is incoming);
- if no CO stayed, the CO that moved in your chosen direction is the occupant and the opposite mover is incoming.
After all Collisions, check every CO for Stability 0 and Size 0.

**Moving a CO within an orbit** (by a card or ability) is not entering orbit: no enters-orbit trigger, no CO cap. If the destination is occupied, a Collision occurs and the moved CO is incoming (G11).

**"Rotate an orbit one step"** on a card: the acting player chooses the direction and every CO in that orbit moves one step at once, ignoring "does not move" and "opposite direction" effects (those apply only in a Rotation Phase). It never causes a Collision.

### 5.3 Out of Orbit zone and ownership
- Knocked-out COs go here and stay until reclaimed or removed. Their Augmentations are discarded.
- Any player may **reclaim** any CO from here into **their own** orbit (by a card or ability that says "reclaim"). It follows placement rules (restriction, Collision if occupied, CO cap). It can never fail for lack of a position. Its enters-orbit trigger fires.
- A CO's **owner** is always the player whose orbit it is in (G20). An Augmentation's "you" is the player who played it. "Your COs" are the COs in your orbit.
- "**Knocked out**" always means moved from an orbit to the Out of Orbit zone. Discarding a CO (Size 0, AE40) and returning it to hand remove it from orbit but are **not** knockouts (G17).

### 5.4 Enters-orbit triggers
A CO's enters-orbit trigger fires whenever it enters an orbit from hand, by a card that places it, or by reclaim, even if it then loses its Collision (trigger first, then knockout).

### 5.5 Triggers and the stack (PROVISIONAL, G27, G29)
- Only triggered and passive abilities already in play act outside the Play Phase or on other players' turns.
- "Whenever ...", "When ...", "At the start/end of ..." abilities are **triggers**. A "you may" choice is made when the trigger resolves.
- A trigger marked "once per turn" can fire once during **each player's turn**.
- **LIFO stack:** when one or more triggers fire at the same moment, the **active player** puts all of theirs on the stack in any order they choose, then each other player in turn order does the same. Resolve the stack **top first** (the last one put on resolves first). A trigger that fires while the stack is resolving goes on top and resolves next.
- A card or ability fully resolves (including any Collision and knockouts it causes) before the next stack item.

### 5.6 Hand, deck and information
- Starting hand 5; draw 2 per turn; up to 2 plays per turn; hand limit 7, checked only at End of Turn. Same at every player count.
- **Empty deck:** the moment the draw deck is empty and a card must be drawn or looked at, shuffle the discard pile to form a new deck and continue. If both are empty, the remaining draws are skipped. The Out of Orbit zone never returns to the deck (G35).
- Hands are hidden; hand sizes, the discard pile and the Out of Orbit zone are public (G37).
- A Star never goes above its maximum (printed) HP (G36).

### 5.7 Elimination
- A Star at 0 HP is eliminated at once, whatever the source (including its own cost).
- The eliminated player's orbit and hand are discarded, and so are all Augmentations they played onto other players' COs (G31). Their countdown ends. The Out of Orbit zone is untouched.
- If the **active** player is eliminated, their turn ends at once; stack items they control are removed (G30). Stack items that would affect only an eliminated player are removed.
- If one effect brings several Stars to 0, they are eliminated together. If that would leave no player, the active player wins (G33).

### 5.8 Durations and timing words
- "**This turn**" effects end in step 4 of End of Turn (after the hand limit) (G32).
- "**Until the start of your next turn**" effects end in step 1 of that player's Start of Turn, before triggers. If that player is eliminated first, the effect ends then.
- "**Since your last turn**" / "since the end of your last turn" means since the end of your previous turn; on your first turn, since the start of the game (G28).
- Order inside Start of Turn: triggers, then draw (G5).

### 5.9 Glossary
- **Next to:** North is next to East and West; East to North and South; South to East and West; West to South and North (G38).
- **Wins a Collision:** stays in its position while the other CO is knocked out (G39).
- **Entered orbit:** placed from hand, placed by a card, or reclaimed (not moved or rotated).
- **North (the exposed position):** several cards hit only an opponent's North CO (AE22, AE41, AE55, AE60); others reward your own North (AE20, AE28, CO25).

### 5.10 Gap rulings (all 40 answered)
P = PROVISIONAL (moves results; owner may change).

| Gap | Ruling | Where |
|---|---|---|
| G1 (P) | Active player chooses rotation direction each Rotation Phase; card rotations: acting player chooses | 4.2, 5.2 |
| G2 | Random first player; play passes clockwise; draft in reverse turn order | 3 |
| G3 | Stars chosen first, then hands dealt; unkept Stars go to the box | 3 |
| G4 | First player skips the turn-1 draw (owner ruling) | 4.1 |
| G5 | Start triggers, then draw | 5.8 |
| G6 | End triggers, Critical Mass win check, announce, hand limit, "this turn" ends | 4.4 |
| G7 (P) | Only the active player's own total, only at their own End of Turn | 4.4 |
| G8 (P) | Cancel checked after each card, ability, trigger or Rotation Phase finishes resolving, on any turn; a dip inside one resolution does not count; cancel line = your threshold | 6.2 |
| G9 | COs from hand go only into your own orbit | 4.3 |
| G10 (P) | 1 CO enters each orbit per turn from any source; losing its Collision still uses it; moves do not | 4.3 |
| G11 | Moving within an orbit: no trigger, no cap, mover is incoming | 5.2 |
| G12, G13 (P) | Simultaneous move; swaps pass; occupant, then same-direction mover, then opposite mover; stat-0 checks after all Collisions | 5.2 |
| G14 | Two "wins every Collision" effects cancel out | 5.2 |
| G15, G16 | Floor after summing; knocked out whenever Stability is 0, including when a bonus ends | 5.1 |
| G17 | "Knocked out" = to the Out of Orbit zone only | 5.3 |
| G18, G19 | Size 0 wins (discard); effective values may exceed 5 | 5.1 |
| G20 | Owner = orbit holder; Augmentation's "you" = who played it | 5.3 |
| G21, G22 | Default host "one of your COs"; no host = illegal; attach condition checked only when played | 4.3 |
| G23-G25 | No "Choose" = always legal; every "Choose" needs a legal choice; "Play only if" is legality | 4.3 |
| G26 | Costs fully payable, paid first; self-damage can eliminate you | 4.3 |
| G27 (P) | "Once per turn" triggers: once per each player's turn; Active abilities only in your Play Phase | 4.3, 5.5 |
| G28 | First turn counts from the start of the game | 5.8 |
| G29 (P) | LIFO stack; active player stacks first, then others in turn order; top resolves first | 5.5 |
| G30, G31 | Active player eliminated: turn ends; their Augmentations on others' COs are discarded | 5.7 |
| G32 | "This turn" ends after the hand limit; "until your next turn" ends at its start or on elimination | 5.8 |
| G33 | Simultaneous zero: eliminated together; if none remain, active player wins | 5.7 |
| G34 | You choose your hand-limit discards | 4.4 |
| G35 | Reshuffle mid-draw; skip if both empty; Out of Orbit never reshuffled | 5.6 |
| G36 | HP never above printed HP | 5.6 |
| G37 | Hands hidden, sizes public; discard and Out of Orbit public | 2, 5.6 |
| G38, G39 | Defined | 5.9 |
| G40 | Age 12+ | 1 |

---

## 6. End of game and scoring

No points. The game ends the instant a player wins.

### 6.1 Star Destruction
- Checked immediately whenever a Star reaches 0 HP, at any moment of any turn.
- **1v1:** the other player wins. **Free-for-all:** the eliminated player leaves (5.7); the **last player remaining wins**.

### 6.2 Critical Mass
- **Total Size** = the sum of the effective Size of the COs in your orbit. The Out of Orbit zone never counts.
- **Threshold** = 12 + number of players at setup, maximum 17 (2p 14, 3p 15, 4p 16, 5-6p 17). ST10's threshold is 2 lower.
- **Announce** and **win** only at your own End of Turn (4.4). Earliest announcement: your 3rd turn (CO cap); earliest win: your 4th.
- **Cancel (PROVISIONAL, G8):** after each card, ability, trigger or Rotation Phase finishes resolving, on any player's turn, if your total is below your threshold your countdown is cancelled (remove the marker). You must reach the threshold again at an End of Turn to announce a new one, whose deadline is always your **next** turn, never the current one.
- A countdown gives no protection; a player with a running countdown can be targeted and eliminated.
- **Ties cannot happen:** turns are sequential and both win checks happen as soon as they are true, so the first true check ends the game.

### 6.3 Turn cap
None in play. The simulation uses a cap of 30 rounds (a draw) and must report any hits; none occurred in revision 0.

---

## 7. Design notes

### 7.1 Intent
- **The twist: a clock you steer.** Every turn your whole orbit turns one step and you choose the direction. North is the exposed position (AE22, AE41, AE55, AE60 hit it), East, South and West carry bonuses for some cards (CO07, AE05, CO16), and anchors and retrograde movers (CO21, CO27, AE14, AE15, AE16) create Collisions you can predict. "Where do I put this, and which way do I turn" is the decision every turn.
- **Two co-equal win paths:** Star Destruction (immediate) and Critical Mass (a held state with a one-round window for counterplay). The threshold scales with player count because damage is split across more opponents in big games, while Critical Mass is a solo race (owner's own precedent: "scale deck composition or thresholds instead", Rules v2 §8).
- **No mana.** Throttles are 2 plays, 1 CO entering per turn, and per-card costs.
- **Free-for-all dogpiles** on a Critical Mass leader are intended.

### 7.2 Comeback
Catch-up damage (AE30 if the target has more COs, AE35 if you have less HP, AE31 and ST07 after taking damage); five cheap answers to a countdown (AE23, AE41, AE43, AE55, AE60) plus AE32, AE52, AE53 and ST12; and AE32's 2 damage against a 12+ Size orbit. KPI: runaway leader at most 65% (was 63.4%), lead changes at least 2 (was 3.1). Round 1 cannot decide the game: no Critical Mass win before your 4th turn, and the fastest kill took 4.4 own turns.

### 7.3 Target bands and knobs
| Measure | Band | Knob |
|---|---|---|
| Win path split, each player count | each path 40-60% (2p was 72/28 Star; 6p 25/75) | Critical Mass threshold per player count (±1) |
| Seat gap, 2p | at most 5 points (was 7.4) | first-player draw (now skipped) |
| Star round-robin | every Star 40-60% (was 33-71%) | that Star's HP (±1) |
| Critical Mass cancel share | 45-55% of announcements (was 41%) | number of cheap answers |
| Rotation-trick cards | each played in 5%+ of games | North-hitting card count |

### 7.4 Skill
Good play shows in the rotation choice (what is in North when the opponent acts, which CO lands on its bonus position, whether an anchor collides), in holding an answer for a countdown, and in choosing when to switch from building to damage. Revision 0 gap: 77.7 points (strategic vs random); target at least 20.

---

## 8. Change log

### Cycle 1 (revision 1)
Responds to `critique.md` (REVISE-MAJOR, 2.83) and `playtest-report.md` (NEEDS-FIXES). Rules changes first (the owner may veto any), then cards.

| # | Change | Was | Status before | Reason (feedback) | KPI it should move |
|---|---|---|---|---|---|
| R1 | First player skips the turn-1 draw | gap G4 | gap | Owner ruling; critic decision 1 | 2p seat gap 7.4 to about 0 (playtest: 50.2%); clears Bar Raiser veto |
| R2 | Free mulligan of a no-CO opening hand, once | none | none | Owner ruling; playtest (e) 3.4% CO-less hands | Turns with no CO in hand; dead-start rate |
| R3 | **Rotation direction is the active player's choice** each Rotation Phase | clockwise in original notes | `[OPEN]` | Critic change 3 and owner's ask "rotation should matter more": rotation Collisions 0.48/game, 8 rotation cards under 5% | Ablation: always-clockwise bot loses by 5+ points; rotation-trick cards 5%+; strategic beats greedy by more than 53.5% |
| R4 | **Critical Mass threshold = 12 + players, max 17** (was 15 at every count); ST10 = 2 lower | 15 | `[LOCKED]` | Critic weakness: path split flips with count (2p 72/28, 4p 39/61, 6p 25/75); one card-count change cannot fix both ends (playtest f) | Path split within 40-60 at 2p, 4p and 6p |
| R5 | Cancel is checked after each resolution, not mid-resolution | "drops below at any point" | `[LOCKED]` wording, gap G8 | G8 flagged result-moving; humans cannot track mid-card dips | Rule ambiguity count; small rise in Critical Mass share |
| R6 | **Recycle** play: discard 1, draw 1, costs a play | optional End-of-Turn swap | `[OPEN, deferred]` | Playtest (e): 3.4 dead cards per 7-card hand, clogged hands; deferred item said "revisit if playtesting shows a need" | Turns with no legal play to 0; hand clog |
| R7 | ST01 HP 9 to 8 (curve now 3/3/3/3 over HP 8-5, mean 6.5) | 9 | `[LOCKED]` curve | Critic decision 3: HP 9 wins 70.6% | ST01 round-robin into 40-60% |
| R8 | ST08, ST10, ST11, ST12 abilities buffed (see `cards.md`) | roster | working list | Critic: buff abilities first; HP 5 Stars 33-45%; ST12 had no denial | Each into 40-60% |
| R9 | All gaps G1-G40 answered (5.10); LIFO stack ordering defined | gaps | gaps | Critic decision 5; target zero ambiguities | Ambiguity count 40 to 0 |
| R10 | Eliminated player's Augmentations on others' COs are discarded | gap G31 | gap | Cleaner exit (no dangling AE11 owner) | Ambiguities |
| R11 | Draft picks in reverse turn order | "in turn order" | `[LOCKED]` | Gives later seats the better Star, a second seat-balance lever | Seat gap at 3p+ |

**Cards (all 108 kept, same IDs, `cards.json` format unchanged plus a `changed` flag):**
| Card | Change | Feedback | KPI |
|---|---|---|---|
| AE28 | Sacrifice must be your **North** CO; 2 damage, 3 only if it had Size 4+ | Critic change 1 (winning link +0.42) | Winning link under 0.2 |
| AE25 | Self-damage cost 1 to 2 | Critic change 1 (+0.26) | Winning link under 0.2 |
| AE23 | Modal: 1 damage **or** -1 Stability to an opponent's CO | Change 2 (cheap answers) | Cancel share 45-55% |
| AE41 | Hits only opponents' North COs, draws 1 | Change 2, 3, 5 (0.4% played, self-harming) | Played 5%+; legal on empty board |
| AE43 | Any opponent's CO: strip Augmentations, -1 Size | Change 2, 3 (2.2%) | Played 5%+; cancels |
| AE55 | **Denial card:** bounce an opponent's North CO to hand | Change 2, 3 (0%) | Played 5%+; cancels |
| AE60 | Forced Collision at an opponent's North | Change 2, 3 (0.65%) | Played 5%+; cancels |
| AE57 | Draw 1, then rotate your orbit either way | Change 3, 5 (0.1%) | Played 5%+; legal on empty board |
| AE45 | Draw 1 first, then optional small reclaim | Change 3, 5 (2.4%) | Played 5%+; legal on empty board |
| AE49 | Look at top 4, take a CO | Change 5 (4.5%, dead early) | Legal on empty board; fewer CO droughts |
| CO14 | Draws 1 on entering, then the free Augmentation | Change 3 (4.75%) | Played 5%+ |
| CO24 | Neighbours also get +1 Size | Change 3 (5.05%, negative link) | Played 5%+ |
| AE16 | Anchor also gives +1 Size | Playtest: under 5% | Played 5%+ |

---

## 9. Design notes, cycle 1

**Biggest problem:** the win path flips with player count (Star Destruction 72% at 2p, Critical Mass 75% at 6p). Three candidate fixes:
1. **Threshold scales with player count (12 + players, max 17).** One number per count, a natural knob, matches the owner's own note that thresholds (not hand economy) should scale. Each count is tuned without touching the others.
2. **Bold: "kill shot" free-for-all.** The first Star destroyed ends the game and the player who dealt the final damage wins. Removes player elimination and makes damage worth as much at 6p as at 2p. **Lost** because it concentrates fire on the HP 5 Stars (HP already dominates ability), invites sniping a softened Star, and replaces the owner's last-Star-standing pillar.
3. **Bold: "impact damage."** Whenever an opponent's effect knocks out your CO, your Star takes 1 damage, tying the two paths together. **Lost** because it adds damage at 2p, where Star Destruction is already 72%, and blurs the two paths the owner wants distinct.

**Picked: 1**, with the 2p threshold lowered to 14 and two of the strongest damage cards weakened, so 2p moves toward Critical Mass while 4-6p move toward Star Destruction. The cheap answers pull 2p back toward Star Destruction, so the 2p number is the one to watch.

**Rotation (second problem), three candidates:** (a) cards only: give the 8 named cards payoffs; (b) **bold: choose the direction each turn** (picked; it adds a real decision every turn and makes every position card reachable, and it settles the open G1); (c) "North flare": the CO rotating into North deals damage (lost: adds damage at 2p). I did (a) and (b) together, with North as the shared target, so the twist has one readable focus.

**What I would try next if this works:** cut rule weight. Fold CO21, CO27, AE14 and AE15 into fewer rotation exceptions, and turn the North theme into a printed icon so the teach shrinks. Then tune the threshold per count from the playtest numbers.

**What I suspect is still wrong:** (1) ST12's free -1 Stability every turn may be too strong against the 11 Stability-1 Size 4-5 COs and could choke Critical Mass at 2p, undoing R4. (2) The ST11 loop (knock out a small CO, reclaim it for 1 damage) may be too strong. (3) 17 at 5-6p may overshoot into a Star Destruction majority. (4) This cycle bundles many changes (lesson L10); only single-change experiments can show which one moved what. (5) The rules are about 300 lines, too long to teach in one sitting (L7).

---

## 10. Playbook check
1. **Family:** `studio/mechanics.md` "Asymmetric roles" (12 asymmetric Stars) plus "All families". Its trap: a side gap that depends on the bot, and keyword abilities that do not change best play. Hence the per-Star ability ablations below.
2. **Comeback:** catch-up damage (AE30, AE35, AE31, ST07), five new cheap countdown answers, AE32 against big orbits, free-for-all dogpiles. KPI: runaway at most 65% (was 63.4), lead changes at least 2 (was 3.1).
3. **Ablations (each at 2p and 4p, must lose by 5+ points):** (a) always-clockwise bot against the direction-choosing bot; (b) a bot that ignores North exposure when choosing direction and placing; (c) never-Recycle bot; (d) never-mulligan bot (expected small, report it); (e) ability-off versions of ST08, ST10, ST11, ST12; (f) lever check: flat threshold 15 vs scaled, path split at 2p, 3p, 4p, 6p.
4. **Self-check:** fixed 40 gaps (5.10). Dead or near-dead cards reworked: AE41, AE43, AE45, AE49, AE55, AE57, AE60, CO14, CO24, AE16. AE41 no longer hurts its player. AE60 no longer needs a "table-wide" reading. Undefined cases now covered: empty deck (5.6), ties (6.2), simultaneous triggers (5.5), simultaneous zero (5.7), elimination mid-turn (5.7). Still to watch: AE04 and AE17 (rarely played, high winning link; possibly bot blindness).
5. **Band and knob:** see 7.3. Win path 40-60 at each count (knob: threshold); Stars 40-60 (knob: HP); seat gap at most 5 (knob: turn-1 draw).
6. **Ends:** Star Destruction or Critical Mass; each player turn adds cards to orbits or deals damage, and the reshuffle prevents deck stalls. Simulation cap 30 rounds (0 hits in revision 0). Expected 2p about 9-10 player turns, about 12 minutes; 6p 25-35 minutes; the owner's targets are flexible.
7. **Budget:** about 300 lines including notes and the gap table; about 160 lines of playable rules (sections 1-6). Special rules: rotation with direction choice, Collisions, CO cap, Out of Orbit zone, Critical Mass countdown, stack (6). No brief promise exists (owner-supplied); over a one-page teach (L7, known gap).
8. **Re-run list:** the threshold (a ceiling) and the legality, cap and stack rulings changed, so re-run **all** ablations above at 2p, 3p, 4p and 6p, plus the revision-0 headline set (seat, path split, Star round-robin, card play rates, winning links for AE25 and AE28, cancel share).
