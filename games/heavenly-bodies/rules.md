# Heavenly Bodies: Rules (Owner-supplied, studio format)

> **Owner-supplied.** This is a faithful restatement of the owner's **Rules v2** (Part 1 of `source-design-doc.md`) in studio format. No locked rule has been changed, reinterpreted or "fixed". Tags are carried over from the source: `[LOCKED]`, `[PROVISIONAL]`, `[OPEN]`. Anything the source does not state is either marked **[GAP Gn]** (listed under "Rule gaps", section 7.3) or labelled *studio proposal (not a rule)*. References such as "§5" point to Rules v2. If this file and Rules v2 ever disagree, Rules v2 wins.
>
> The card list is in `cards.md` (machine-readable copy: `cards.json`).

---

## 1. Overview

- **Title:** Heavenly Bodies (working title).
- **Hook:** a strategy card game of orbital mechanics. Each player is a **Star** with a ring of four orbital positions. The planets and moons around you (**Celestial Objects**, COs) **rotate one step every turn**, so your board is a clock: where you place a card now decides what it will hit later. Win by destroying an opposing Star, or by building 15+ Size in orbit and holding it for a full round (Critical Mass).
- **Players:** 2 to 6. 1v1 and free-for-all (3+ players, last Star standing) are both first-class modes with the same rules `[LOCKED]` (§1). The 2-6 range comes from §8 ("2p through 6p") and §11 (12 Stars = 2x the 6-player maximum).
- **Play time:** the source gives 10-20 minutes at 2 players and 25-40 minutes at 6 players, but the owner has said these figures are **flexible, not binding** (Audit Part A). No target is locked.
- **Age:** not specified by the owner. **[GAP G40]**

---

## 2. Components

| Component | Count | Notes |
|---|---|---|
| Star cards | 12 | HP 9/8/7/6/5 in a 1/2/3/3/3 curve `[LOCKED]`. Not shuffled into the deck. Full list in `cards.md` section 1 (unchanged from the owner's roster; names not yet assigned). |
| Celestial Object (CO) cards | 36 | Size 1-5, Stability 1-5, all unique `[LOCKED]`. Stat grid locked (see `cards.md`). |
| Astronomical Event (AE) cards | 60 | Augmentations and Direct Effects, all unique `[LOCKED]`. |
| **Total cards** | **108** | 12 Stars + 96-card draw pile `[LOCKED]` (§11). |

**Simple tokens (studio proposal, not in Rules v2):** the rules require tracking values that are not printed on cards. Suggested minimum, all generic:
- 1 HP tracker per player (a d10, or a 0-9 dial or track), 6 total.
- 1 Critical Mass countdown marker per player, 6 total (placed on your Star card when Critical Mass is announced).
- 1 first-player marker. **[GAP G2]**
- About 10 small reminder tokens for temporary effects ("this turn", "until the start of your next turn"), optional.

No board is needed: each player's Star card sits in front of them, and the four orbital positions are the spaces directly above (North), right (East), below (South) and left (West) of it. Seasons (Winter/Spring/Summer/Fall) may appear as art on Star cards but are never used in rules text `[LOCKED]` (§4).

**Zones:**
- **Draw deck:** one shared, face-down deck of the 96 COs and AEs `[LOCKED]` (§11).
- **Discard pile:** one shared pile. **[GAP G37: public / searchable?]**
- **Out of Orbit zone:** one shared, persistent, open-access pool of knocked-out COs, no size limit `[LOCKED]` (§6).
- **Each player's orbit:** 4 positions: North, East, South, West `[LOCKED]` (§4). At most one CO per position once any Collision has resolved (§5).
- **Hands:** one per player. **[GAP G37: hidden information is not stated]**

---

## 3. Setup

Rules v2 has no numbered setup section. The steps below are assembled from the locked rules they cite; ordering points the source does not fix are marked.

1. **Choose Stars** (§10, `[LOCKED]`). The table picks one of two official variants:
   - *Full-visibility draft:* lay out all 12 Stars face up; players pick one each, freely, in turn order. **[GAP G2: how turn order is set before the game starts]**
   - *Random deal, then choose (Bang!-style):* deal 2 random Stars to each player; each keeps 1 and returns the other to the pool.
   - No two players may have the same Star `[LOCKED]`.
2. Each player sets their Star's HP to the HP printed on their Star card.
3. Shuffle the 96 CO/AE cards into one face-down draw deck `[LOCKED]` (§11).
4. Deal **5 cards** to each player as their starting hand `[PROVISIONAL]` (§8). **[GAP G3: before or after Star selection]**
5. The Out of Orbit zone and discard pile start empty; all orbits start empty.
6. Choose a first player. **[GAP G2: method and direction of play are not stated]**

---

## 4. Turn structure

Each turn has four phases, in this order `[LOCKED]` (§7).

### Phase 1: Start of Turn
1. "Start of turn" triggers resolve (§7).
2. Draw **2 cards** from the draw deck `[PROVISIONAL]` (§8).
   - **[GAP G5]** The order of steps 1 and 2 is not stated.
   - **[GAP G4]** Whether the first player draws on the first turn of the game is not stated.

### Phase 2: Rotation Phase
- The **active player's own COs** rotate one step. Other players' COs do not rotate `[LOCKED]` (§4). Cards may override this (for example, an effect that rotates an opponent's orbit).
- **Direction:** `[OPEN]` (§4). The original notes say clockwise. **[GAP G1]** *(If clockwise: North -> East -> South -> West -> North.)*
- Normal rotation moves all of the player's COs one step at the same time, including into empty positions. It is a pure permutation and **never causes a Collision by itself** `[LOCKED]` (§5).
- A rotation Collision happens only when a card effect keeps a CO in place, or moves a CO against the normal direction, so that a rotating CO lands on an occupied position. The rotating CO is the **incoming** CO for the tie-break (§5). **[GAP G12: two COs both moving into one position; G13: when knockouts are checked during rotation]**

### Phase 3: Play Phase
Play **up to 2 cards** from your hand, in any order `[PROVISIONAL]` (§7, §8). Playing 0 or 1 is allowed. The legal plays are:

**A. Place a CO from your hand into your orbit** (1 of your 2 plays) `[LOCKED]` (§5).
- Choose any of your 4 positions. Placement is **always legal**, including onto an occupied position, as long as the CO's own printed restriction (for example "Must enter North") is met `[LOCKED]`. **[GAP G9: placing into an opponent's orbit]**
- If the position is occupied, a **Collision** resolves immediately (section 5.2). The placed CO is the incoming CO.
- **CO-per-turn cap:** at most **1 CO may enter a player's orbit per turn, from any source** (from hand, by reclaim, or otherwise) `[LOCKED]` (§5). This is separate from, and stricter than, the 2-plays limit. Only cards that explicitly say so can override it. **[GAP G10]**
- A placed CO that loses its Collision still counts as a play, and still counts as having **entered orbit**: its enters-orbit trigger fires, then it is knocked out, in that order `[LOCKED]` (§5).

**B. Play an AE** (1 of your 2 plays) `[LOCKED]` (§10).
- **Augmentation:** attach it to a CO in orbit. It stays attached until that CO leaves orbit for any reason; then it is discarded. It never follows the CO to another zone `[LOCKED]`. One CO may carry any number of different Augmentations `[LOCKED]`. **[GAP G21: default for which COs may be chosen]**
- **Direct Effect:** resolve it once, then discard it.
- A Direct Effect with **no legal target** is illegal: it cannot be attempted, does not resolve and does not use a play `[LOCKED]` (§10). If attempted anyway, it returns to hand as if never played `[LOCKED]` (§5 enforcement note). **[GAP G23, G24, G25]**
- **Reclaiming** a CO from the Out of Orbit zone through an AE counts as 1 of your 2 plays `[LOCKED]` (§6).
- **Targeting an opponent:** unless the card says otherwise, the acting player chooses which opponent `[LOCKED]` (§10). Any Star may be targeted, including one in a Critical Mass countdown, unless the card says otherwise `[LOCKED]` (§2).

**Not a play: using an ability already in play.**
- **Active** abilities (on Stars, or on COs in orbit) may be activated **once per turn per source** unless the card says otherwise `[LOCKED]` (§5). Using one does not use one of your 2 plays (§5, §6). **[GAP G27: classifying Star abilities]**
- **Passive** abilities are always on and are not limited `[LOCKED]` (§5).
- **There is no generic reclaim action.** A CO can only be reclaimed through a CO or Star ability in play, or through an AE `[LOCKED]` (§6).

**No instant-speed play.** Players never play cards on another player's turn `[LOCKED]` (§9).

### Phase 4: End of Turn
1. End-of-turn triggers resolve (§7).
2. **Critical Mass** is checked and announced (section 6.2) `[LOCKED]` (§2, §7).
3. **Hand limit:** if you hold more than **7** cards, discard down to 7 `[LOCKED]` (§8). A hand may exceed 7 during the turn. **[GAP G34: who chooses]**
4. **Optional swap (discard 1, draw 1):** `[OPEN, deferred]` (§8). **Not a rule. Do not implement.**

**[GAP G6]** The order of steps 1 to 3 is not stated in Rules v2; the numbering above follows the order of §7's wording and is not confirmed.

Play then passes to the next player still in the game; eliminated seats are skipped `[LOCKED]` (§2). **[GAP G2: direction]**

---

## 5. Special rules and timing

### 5.1 Size, Stability and effective stats (§3)
- Size (1-5) counts toward Critical Mass. Stability (1-5) resists being knocked out.
- Size and Stability can never go below **0** `[LOCKED]`. **[GAP G15: floor arithmetic; G19: values above 5]**
- All checks use **effective** values (printed value adjusted by all active modifiers), never the printed value alone `[LOCKED]`.
- **Stability 0:** the CO is knocked into the Out of Orbit zone the moment its effective Stability becomes exactly 0 `[LOCKED]`.
- **Size 0:** the CO is removed from orbit and **discarded** the moment its effective Size becomes exactly 0; it skips the Out of Orbit zone `[LOCKED]`. **[GAP G17, G18]**
- A permanent or passive reduction knocks a CO out the moment its effective value reaches 0. A temporary effect also knocks it out the moment it brings the value to 0; this is checked when the effect applies, not retroactively `[LOCKED]`. **[GAP G16: when a temporary bonus ends]**

### 5.2 Collisions (§5)
A **Collision** happens whenever two COs would occupy the same position in an orbit, whatever the cause (rotation, placement from hand, reclaim, or any other placement effect). It is one unified event `[LOCKED]`. Resolve it in this order `[LOCKED]`:
1. The CO with **lower effective Stability** is knocked into the Out of Orbit zone.
2. If Stability is tied, the CO with **smaller effective Size** is knocked out.
3. If both are tied, the **incoming / moving** CO wins, and the CO already there is knocked out.
4. An AE, CO or Star ability may change this only when its text explicitly says so. **[GAP G14: conflicting overrides]**

Because rotation is per player, Collisions only happen inside one player's own orbit; there are no cross-player Collisions `[LOCKED]` (Audit item 20).

### 5.3 Out of Orbit zone (§6)
- Persistent, shared, open to every player. COs stay there until reclaimed or otherwise removed; it is never cleared at end of turn `[LOCKED]`. No size limit `[LOCKED]`.
- When a CO enters this zone, its Augmentations are discarded `[LOCKED]`.
- Any player may reclaim any CO from this zone into their own orbit, whoever owned it before `[LOCKED]`; **ownership transfers** to the reclaiming player `[LOCKED]`. **[GAP G20]**
- A reclaim follows the normal placement rules: into an empty or an occupied position (Collision), satisfying the CO's printed restriction `[LOCKED]`. A reclaim can never fail for lack of a destination `[LOCKED]`. It counts against the 1-CO-per-turn cap (§5).
- You may reclaim your own CO in the same turn it was knocked out; there is no limit on how often a CO moves between orbit and this zone `[LOCKED]`.

### 5.4 "Enters orbit" triggers (§10)
A CO's printed enters-orbit trigger fires whenever it is placed into orbit for any reason: from hand, a placement that wins its Collision, or a reclaim, **including one that immediately loses its Collision** (trigger first, then knockout) `[LOCKED]`. **[GAP G11: moving a CO within an orbit]**

### 5.5 Simultaneous triggers (§9)
Only automatic triggered and passive abilities already in play can respond to each other. When several triggers fire at the same time, they resolve on a **LIFO stack** (last triggered resolves first) `[LOCKED]`. **[GAP G29: the order triggers go on the stack]**

### 5.6 Hand economy (§8) `[PROVISIONAL]`
- Starting hand 5; draw 2 at Start of Turn; play up to 2 per turn; hand limit 7, enforced only at End of Turn.
- **Empty deck:** when the shared draw deck is empty, shuffle the discard pile to form a new deck `[LOCKED]`. **[GAP G35]**
- The same numbers at every player count, 2 to 6 `[LOCKED]`.

### 5.7 Illegal plays (§5, §10)
There is no engine to block illegal plays. A play that turns out to be illegal (for example, a Direct Effect with no legal target) does not resolve; the card returns to hand as if never played and does not use a play `[LOCKED]`.

### 5.8 Elimination (§2)
- A player whose Star reaches 0 HP is eliminated immediately, whether the damage came from an opponent or from themselves (for example a card's own cost) `[LOCKED]`.
- Their **orbit and hand** go to the discard pile (Augmentations on those COs go too). Their seat is skipped in turn order `[LOCKED]`.
- Cards they previously sent to the Out of Orbit zone **stay there**; the zone has no owners `[LOCKED]`.
- If a player is eliminated while a Critical Mass countdown is running, nothing special happens `[LOCKED]`.
- **[GAP G30, G31, G32, G33]**

---

## 6. End of game and scoring

There are no points. The game ends the instant a player wins.

### 6.1 Star Destruction (§2)
- Checked **immediately**, the instant any Star's HP reaches 0, at any point in any turn; it does not wait for End of Turn `[LOCKED]`.
- **1v1:** the other player wins. **Free-for-all:** the eliminated player leaves (section 5.8) and play continues; the **last player remaining wins** `[LOCKED]`.

### 6.2 Critical Mass (§2)
- **Total Size** = the sum of the effective Size of the COs **currently in your orbit**. COs in the Out of Orbit zone never count `[LOCKED]`.
- **Announcement:** checked **only at End of Turn**, never mid-phase `[LOCKED]`. If your total Size is **15 or more**, announce Critical Mass and start your countdown. **[GAP G7: whose End of Turn]** *(One Star sets its owner's threshold to 13; see `cards.md`.)*
- **Win:** if your total Size is **still 15 or more at the end of your very next turn**, you win immediately `[LOCKED]`. In free-for-all this ends the whole game.
- **Cancel:** if your total Size drops below 15 at **any point** before that deadline, the countdown is cancelled `[LOCKED]`. You must reach 15 again (announced at an End of Turn) to restart it. **[GAP G8]**
- **Re-trigger deadline:** a restarted countdown always ends at the end of your **next** turn, never the current one, even if it restarts during what would have been the deadline turn `[LOCKED]`.
- A countdown gives no protection: an AE may target a player mid-countdown, and that player can still be eliminated `[LOCKED]`.
- **No tie-break is needed.** Turns are sequential and both win conditions are checked as soon as they are true, so the first check in turn order resolves first and ends the game `[LOCKED]`. **[GAP G33: several Stars at 0 at the same moment]**

### 6.3 Tiebreakers
None defined or needed under the locked rules (see 6.2). GAP G33 is the one case the source does not cover.

---

## 7. Design notes

### 7.1 Intent (from the owner's Audit)
- **The twist:** the orbit is a clock. Your COs rotate one step every turn, so position-based effects, placement restrictions, and cards that stop or reverse rotation make "where do I put this" an ongoing puzzle. The owner names this as the thing most worth protecting.
- **Two co-equal win conditions:** Star Destruction (immediate) and Critical Mass (a held state with a one-round counterplay window). The owner wants them comparable in turns-to-win, not just in theme.
- **No mana or resource system.** The only throttles are 2 plays per turn, 1 CO entering per turn, and per-card costs. This is a pillar, not an omission.
- **Cost philosophy** `[LOCKED]`: most AEs are free or have only soft prerequisites (board or target conditions); hard costs (self-damage, discards, sacrificing a CO) are kept for the strongest effects.
- **Pacing levers:** the HP curve was lowered to a mean of 6.58 to speed up Star Destruction. If simulation shows that path still drags, the planned lever is more AE damage and/or more damage cards in the 96 (§10).
- **Free-for-all dogpiles** on a Critical Mass leader are intended table tension (Audit items 18, 41).
- **Phase 2 vision:** personal constructed decks later, with the same core rules; copy limits will be decided then.

### 7.2 Open and provisional items for the owner
Carried over unchanged; this build decided none of them.
1. **Rotation direction** `[OPEN]` (§4). Original notes say clockwise.
2. **Hand economy** `[PROVISIONAL]` (§8): start 5, draw 2, play 2, limit 7, pending playtest.
3. **Optional End of Turn swap** (discard 1, draw 1) `[OPEN, deferred]` (§8), together with Audit item 45 (its order against the hand-limit discard).
4. **Star roster** is a working list: names not assigned, abilities not power-checked, archetype balance off-plan (Denial/control has 1 card vs a planned 2). Not rebalanced here. The card pool adds denial/control tools (`cards.md` section 5), but that does not close the roster item.
5. **Critical Mass reachability** (Audit item 12) and **HP-race pacing** (item 13) stay OPEN until the simulation runs. The damage-density tally in `cards.md` is its input.
6. **Secondary orbit** (Audit item 25): never integrated, not used anywhere in this build.
7. **Zone glossary** (item 26): this build uses only "Out of Orbit zone", "discard pile" and "hand"; no card uses "removed from game".
8. **Placement-restriction percentages** (item 28, the source's ~20/40/40 split): no split is locked. This build gives 5 of 36 COs a restriction (about 14%), following Part 4's "flavourful minority" instruction.
9. **Card template, teaching pass, roster cleanups** (items 21-23, 29, 31): untouched.
10. **Age rating and play-time target:** not set by the owner.
11. **AE subtype split:** none is locked. The source mentions an old 30/70 AE type ratio; this build uses 22 Augmentations / 38 Direct Effects (37/63) and explains why in `cards.md`.

### 7.3 Rule gaps (for the owner)
Each point is a question a simulation programmer has to answer to code the game. **None is resolved here.** If the playtester must pick an answer to run a simulation, it should be treated as a temporary assumption and reported.

**Setup and turn order**
- **G1. Rotation direction.** `[OPEN]` in §4; needed for every Rotation Phase.
- **G2. Turn order.** How the first player is chosen, which way play passes, and what "in turn order" means for the Star draft before any turn exists.
- **G3. Setup order.** Are starting hands dealt before or after Stars are chosen? In the random-deal variant, does the returned pool matter after setup?
- **G4. First turn.** Does the first player draw 2 on turn 1? Any compensation for later seats?

**Phase ordering**
- **G5. Start of Turn order.** Draw 2 before or after start-of-turn triggers (for example an Augmentation that deals damage "at the start of your turn")?
- **G6. End of Turn order.** Order of end-of-turn triggers, the Critical Mass announcement, the Critical Mass deadline win check, and the hand-limit discard. (The Audit mentions an End-of-Turn ordering gap found during Star drafting but records no answer.)
- **G7. Whose End of Turn.** Is Critical Mass checked only at the active player's End of Turn, for that player only, or for every player at every End of Turn? Can a total that rises to 15 on an opponent's turn be announced then?
- **G8. Cancel monitoring.** "Drops below 15 at any point" implies a continuous check, including on opponents' turns. Does a dip inside a single resolution count (for example one CO knocked out and another placed by the same card)? For the Star whose threshold is 13, is the cancel line 13?

**Placement, movement and Collisions**
- **G9. Whose orbit.** May a CO from hand go into an opponent's orbit, or only your own? §7 says "add a CO to orbit".
- **G10. CO cap scope.** Does a CO entering your orbit during another player's turn count toward a cap? Does a CO that enters and is immediately knocked out use the cap (implied yes by §5, not stated)?
- **G11. Moving within an orbit.** Effects that move a CO to another position in the same orbit are neither rotation nor placement. Do enters-orbit triggers fire? Does it count toward the CO cap? (Cards in this build that move COs state that the moved CO is the incoming one in any Collision.)
- **G12. Two moving COs.** When a reverse-rotating CO and a normally rotating CO land on the same position, both are "rotating", so incoming-wins has no answer. Also: two neighbouring COs moving in opposite directions swap positions; is that a Collision?
- **G13. Knockout timing during rotation.** Position-based stat changes take effect as COs rotate. Are knockouts and Collisions checked after the whole simultaneous rotation, or per CO?
- **G14. Conflicting Collision overrides.** If two effects both claim to decide one Collision, which wins?

**Stats and removal**
- **G15. Floor arithmetic.** Is the 0 floor applied only to the final total, or after each modifier (printed 1, then -2, then +2: is it 1 or 2)? Is a CO knocked out if its Stability passes through 0 while several modifiers apply together?
- **G16. A temporary bonus ending.** If a temporary bonus ends and leaves effective Stability at 0, is the CO knocked out? §3 says checks happen "at the moment the effect applies, not retroactively".
- **G17. What counts as "knocked out of orbit".** Do Size-0 discards, "discard a CO" effects, or returning a CO to hand count for "knocked out of orbit for any reason" (HP 5 Denial Star) or "knocked into the Out of Orbit zone" (HP 8 Out of Orbit Star)?
- **G18. Size 0 and Stability 0 at the same moment.** Out of Orbit zone or discard?
- **G19. Values above 5.** Can effective Size or Stability exceed 5 (Augmentations add to them)? The 1-5 range in §3 may describe printed values only.

**Ownership, Augmentations and targeting**
- **G20. Owner vs orbit.** Is a CO's owner always the player whose orbit it is in? Who owns an Augmentation attached to another player's CO (matters for the HP 8 Star's "move an Augmentation from one of your COs")?
- **G21. Augmentation default target.** When a card doesn't say, may an Augmentation go on any player's CO or only your own? Is an Augmentation with nothing to attach to illegal, like a targetless Direct Effect? (Every Augmentation in this build names its legal hosts, but a default is still needed.)
- **G22. Restrictions after moving.** Do an Augmentation's attach restrictions ("attach to an opponent's CO", "a CO with Stability 2 or less") still apply when it is later moved by the HP 8 Star or by a card?
- **G23. Targetless Direct Effects.** Are Direct Effects that target nothing (for example "Draw 2 cards") always legal?
- **G24. Partly legal Direct Effects.** If one part of a card has a legal target and another part doesn't, is the card legal, and does it resolve partly?
- **G25. "Play only if" conditions.** This build prints conditions as "Play only if ...". Should an unmet condition be treated exactly like the no-legal-target rule (illegal, back to hand, no play used)?
- **G26. Hard costs.** Paid before or after the legality check? Is a card illegal if its cost can't be paid in full (for example "discard 2 cards" with 1 card in hand)? Can a self-damage cost be paid if it would eliminate you (§2 implies yes, and you lose)?
- **G27. Ability classes.** Is "once per turn" on triggered Star abilities (HP 7 retaliation, HP 5 Denial) counted per any player's turn or only per your own? Are "Whenever ..." Star abilities triggers that use the stack, and are "you may" triggers chosen at resolution?
- **G28. "Since your last turn"** on a player's first turn (HP 6 Aggression Star; one AE).

**Stack, elimination and end**
- **G29. Stack order.** When triggers controlled by different players fire together, whose go on the stack first? Can a player order their own simultaneous triggers?
- **G30. Elimination mid-turn.** If the active player eliminates themselves, does the turn end at once? What happens to triggers on the stack that come from, or target, the eliminated player?
- **G31. Eliminated player's attachments.** Augmentations the eliminated player attached to other players' COs: discarded or left in place?
- **G32. Durations.** When does a "this turn" effect end (start or end of End of Turn)? What happens to an "until the start of your next turn" effect if that player is eliminated?
- **G33. Simultaneous zero.** If several Stars reach 0 from one effect (for example "1 damage to each opponent's Star"), all are eliminated together; if that leaves no player, or the last players reach 0 together (for example through a self-damage cost), who wins?

**Economy and information**
- **G34. Hand-limit discard.** Does the player choose which cards (assumed, not stated)?
- **G35. Deck empty mid-draw.** Reshuffle immediately and keep drawing? If deck and discard are both empty, is the draw skipped? Do COs in the Out of Orbit zone ever return to the deck (implied no)?
- **G36. Healing.** Rules v2 has no rule for a Star regaining HP, and no maximum HP. The one card in this build that heals states its own cap ("up to its starting HP").
- **G37. Hidden information.** Are hands hidden? Is the discard pile public and searchable (one AE in this build searches it)?

**Terms and metadata**
- **G38. "Next to".** Not a rules term. Cards that use it define it: North is next to East and West, and so on round the ring.
- **G39. "Wins a Collision".** Not a rules term. Cards that use it define it: the CO that stays in the position while the other is knocked out.
- **G40. Age rating** not specified.

### 7.4 What this build adds (content, not rules)
`cards.md` / `cards.json` add the 96-card draw pile. The card-text conventions in `cards.md` section 2 are wording only, not new rules. The Star roster is reproduced unchanged.

---

## 8. Changelog

- **2026-10-04, studio restatement 1 (no rule changes).** Restated Rules v2 in studio sections at the owner's request (Part 4 of `source-design-doc.md`). Added: suggested generic tokens (marked as a studio proposal), an assembled setup sequence with gaps marked, and the Rule gaps list G1-G40. Nothing locked was altered; `[OPEN]` and `[PROVISIONAL]` tags are preserved.
