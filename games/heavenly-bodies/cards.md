# Heavenly Bodies: Card List (base set, 108 cards) - cycle 2

> **Cycle 2 changes (14 cards, marked "C2"; reasons in `rules.md` section 8):** Stars ST05 (HP 7 to 6), ST11 (HP 5 to 6, new ability); COs CO21, CO27 (rotation exceptions replaced by North effects); Augmentation AE16 (anchor removed); **AE04, AE07, AE08, AE14, AE15, AE17 are now Direct Effects** (same IDs; they were the least-played Augmentations); AE41, AE57, AE60 (one opponent / clockwise only). Split now **16 Augmentations / 44 Direct Effects**. Rotation is always clockwise and never causes a Collision. Card count unchanged (108). Sections below that say "cycle 1" are kept as history.

> Built to Part 4 of `source-design-doc.md` (Build & Test Brief) against the rules in `rules.md`. **12 Stars** + **96-card draw pile: 36 Celestial Objects + 60 Astronomical Events**, all unique, no duplicates. All names are placeholders. Machine-readable copy: `cards.json` (same format as before; reworked cards carry `"changed": "cycle1"` and `"previous_text"`).
>
> **Cycle 1 changes (18 cards, marked "C1" below; reasons in `rules.md` section 8):** Stars ST01 (HP 9 to 8), ST08, ST10, ST11, ST12; COs CO14, CO24; AEs AE16, AE23, AE25, AE28, AE41, AE43, AE45, AE49, AE55, AE57, AE60. Card count unchanged (108).

**Contents:** 1. Star roster (unchanged) - 2. Card-text conventions - 3. Celestial Objects (36) - 4. Astronomical Events (60) - 5. Tallies and cross-checks - 6. Notes for the simulation

---

## 1. Star roster (owner's working list, cycle 1 rebalance)

Not part of the draw deck. Names not assigned (open item). Cycle 1 rebalanced five Stars (C1) because HP outweighed ability (HP 9 won 70.6%, HP 5 Stars 33-45%); the owner may veto any of them.

| ID | HP | Archetype | Ability |
|---|---|---|---|
| ST01 (C1) | **8** (was 9) | Simple | Once per turn, you may discard a card to draw a different card. |
| ST02 | 8 | Augmentation-stacking | Once per turn, you may move an Augmentation from one of your COs to another. |
| ST03 | 8 | Out of Orbit | Whenever one of your COs is knocked into the Out of Orbit zone, you may draw a card. |
| ST04 | 7 | Critical Mass | While your total Size in orbit is 10 or greater, your COs gain +1 Stability. |
| ST05 (C2) | **6** (was 7) | Aggression | Once per turn, if you have 3 or more COs in orbit, you may deal 1 damage to an opponent's Star. |
| ST06 | 7 | Aggression | Once per turn, when an opponent's effect knocks one of your COs out of orbit, you may deal 1 damage to that opponent's Star. |
| ST07 | 6 | Aggression | Once per turn, if this Star took damage since your last turn, you may deal 1 damage to an opponent's Star. |
| ST08 (C1) | 6 | Augmentation-stacking | Each of your COs with 1 or more Augmentations attached has +1 Size. |
| ST09 | 6 | Out of Orbit | Once per turn, you may reclaim a CO from the Out of Orbit zone into your orbit, even if a CO has already entered your orbit this turn. |
| ST10 (C1) | 5 | Critical Mass | Your Critical Mass threshold is 2 lower than the table's. While your Critical Mass countdown is running, your COs have +1 Stability. |
| ST11 (C2) | **6** (was 5) | Out of Orbit | Once per turn, when an opponent's CO is knocked out of orbit, you may put it into your hand instead of the Out of Orbit zone. *(Still counts as knocked out; its Augmentations are discarded.)* |
| ST12 (C1) | 5 | Denial/control | Active, once per turn: choose an opponent's CO. It gets -1 Stability this turn. |

Old texts: ST08 "While a CO in your orbit has 2 or more Augmentations, it also has +1 Size." ST10 "Your Critical Mass threshold is 13 instead of 15." ST11 "Whenever you reclaim a CO, it deals 1 damage to an opponent's Star." ST12 "Once per turn, when one of your COs is knocked out of orbit for any reason, you may deal 1 damage to an opponent's Star."

Cycle 1 ST11 text: "Active, once per turn: reclaim a CO with Size 3 or less from the Out of Orbit zone into your orbit (it still counts as your 1 CO this turn). Whenever you reclaim a CO, deal 1 damage to an opponent's Star."

HP curve (cycle 2): 8/8/8/7/7/6/6/6/6/6/5/5 = 3/2/5/2 over HP 8/7/6/5, mean 6.5 (cycle 1: 3/3/3/3, mean 6.5). Archetypes: Aggression 3, Out of Orbit 3, Critical Mass 2, Augmentation-stacking 2, Simple 1, Denial/control 1 (ST12 is now a real denial ability).

---

## 2. Card-text conventions (wording only, not new rules)

- **"Your COs"** = the COs currently in your orbit. **"An opponent's CO"** = a CO in an opponent's orbit.
- **"Must enter X"** = a printed placement restriction (§5): the CO may only be placed or reclaimed into position X.
- **"Next to"** (rules 5.9): North is next to East and West; East is next to North and South; South is next to East and West; West is next to South and North.
- **"Wins a Collision"** (rules 5.9): the CO that stays in its position while the other CO in the Collision is knocked out.
- **"Move a CO to another position"** (not rotation, not placement; rules 5.2): if the position is occupied, a Collision occurs and the moved CO is the incoming CO.
- **"Rotate an orbit one step"** on a card = every CO in that orbit moves one step clockwise at once (cycle 2: no direction choice). Never causes a Collision.
- **North is the exposed position.** Several cards hit only the CO in an opponent's North (AE22, AE41, AE55, AE60) or reward your own North (AE07, AE16, AE20, AE28, CO21, CO25, CO27). Where you place a CO decides when the clock brings it into North.
- No card anchors or reverses a CO in rotation any more (cycle 2), so rotation never causes a Collision.
- **"Play only if ..."** = a soft prerequisite; if unmet, the card is illegal exactly like a card with no legal target (rules 4.3).
- **"Cost: ..."** = a hard cost, paid in full before the effect (rules 4.3).
- **"This turn"** / **"until the start of your next turn"** = temporary effects (rules 5.8).
- **"Attach to ..."** on an Augmentation names its legal hosts; with no host spec the default is "one of your COs" (rules 4.3).
- **"Choose one: ...; or ..."** = pick one option as you play the card; the card is legal if at least one option is legal.
- No card uses the retired term "Overtake", "removed from game", or the unintegrated "secondary orbit".
- No card can be played on another player's turn. Only abilities already in play (passives and triggers) act outside your turn.

**Cost tiers (AEs):** **Free** = no condition. **Soft** = a board-state or targeting condition. **Hard** = self-damage, discarding from hand, or sacrificing a CO; used only on the strongest effects.

---

## 3. Celestial Objects (36)

**Grid (locked, followed cell for cell).** Rows = Stability, columns = Size, cells = card IDs.

| Stability \ Size | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| **1** | - (0) | CO01 (1) | CO02 (1) | CO03-CO08 (6) | CO09-CO13 (5) |
| **2** | CO14 (1) | CO15 (1) | CO16-CO18 (3) | CO19-CO21 (3) | CO22-CO23 (2) |
| **3** | CO24 (1) | CO25-CO26 (2) | CO27-CO28 (2) | CO29 (1) | CO30 (1) |
| **4** | CO31 (1) | CO32-CO33 (2) | CO34 (1) | CO35 (1) | - (0) |
| **5** | CO36 (1) | - (0) | - (0) | - (0) | - (0) |

Totals: 36 cards. Size sum 121, **average 3.36**. Stability sum 79, **average 2.19**. Buckets by Size+Stability: 4 or less = 5, 5-6 = 25, 7 or more = 6 (the locked 15/70/15). **27 core / 9 unique.**

Tags: **V** vanilla, **R** placement restriction, **A** wants an Augmentation, **P** position-based, **E** enters-orbit trigger, **Rot** changes rotation, **D** deals damage to a Star, **Def** defensive.

| ID | Name | Size | Stab | Cell | Core/Unique | Tags | Ability text |
|---|---|---|---|---|---|---|---|
| CO01 | Ice Moonlet | 2 | 1 | Sz2/St1 | Core | A | This CO has +1 Stability for each Augmentation attached to it. |
| CO02 | Debris Clump | 3 | 1 | Sz3/St1 | Core | R | Must enter South. |
| CO03 | Gas Dwarf | 4 | 1 | Sz4/St1 | Core | V | No ability. |
| CO04 | Puffy Planet | 4 | 1 | Sz4/St1 | Core | A | While this CO has an Augmentation attached, it has +1 Size. |
| CO05 | Polar World | 4 | 1 | Sz4/St1 | Core | R | Must enter North. |
| CO06 | Drifting Giant | 4 | 1 | Sz4/St1 | Core | E | When this CO enters orbit, you may move one of your other COs to an empty position in your orbit. |
| CO07 | Equatorial World | 4 | 1 | Sz4/St1 | Core | P | While this CO is in your East position, it has +2 Stability. |
| CO08 | Crumbling Giant | 4 | 1 | Sz4/St1 | Core | E | When this CO enters orbit, discard 1 card from your hand (if you have any). |
| CO09 | Bloated Giant | 5 | 1 | Sz5/St1 | Core | V | No ability. |
| CO10 | Ice Giant | 5 | 1 | Sz5/St1 | Core | R | Must enter West. |
| CO11 | Shedding Giant | 5 | 1 | Sz5/St1 | Core | E | When this CO enters orbit, each opponent draws 1 card. |
| CO12 | Hydrogen Giant | 5 | 1 | Sz5/St1 | Core | A | While this CO has an Augmentation attached, it has +2 Stability. |
| CO13 | Ringed Titan | 5 | 1 | Sz5/St1 | **Unique** | A | While this CO has 2 or more Augmentations attached, it wins every Collision it is part of. |
| CO14 (C1) | Shepherd Moon | 1 | 2 | Sz1/St2 | **Unique** | A, E | When this CO enters orbit, draw 1 card. Then you may attach an Augmentation from your hand to one of your COs; it does not count as one of your 2 plays. |
| CO15 | Scout Moon | 2 | 2 | Sz2/St2 | Core | E | When this CO enters orbit, draw 1 card. |
| CO16 | Twilight World | 3 | 2 | Sz3/St2 | Core | P | While this CO is in your West position, it has +2 Stability. |
| CO17 | Water World | 3 | 2 | Sz3/St2 | Core | A | While this CO has an Augmentation attached, it has +1 Size and +1 Stability. |
| CO18 | Tumbling Moon | 3 | 2 | Sz3/St2 | Core | E | When this CO enters orbit, you may rotate one opponent's orbit one step. |
| CO19 | Mini-Neptune | 4 | 2 | Sz4/St2 | Core | V | No ability. |
| CO20 | Salvager World | 4 | 2 | Sz4/St2 | Core | A, E | When this CO enters orbit, you may take an Augmentation from the discard pile into your hand. |
| CO21 (C2) | Eccentric Wanderer | 4 | 2 | Sz4/St2 | **Unique** | P | While this CO is in your North position, it has +2 Size. |
| CO22 | Overheated Giant | 5 | 2 | Sz5/St2 | Core | E | When this CO enters orbit, deal 1 damage to your own Star. |
| CO23 | Brown Dwarf Companion | 5 | 2 | Sz5/St2 | **Unique** | A, D | At the end of your turn, if this CO has an Augmentation attached, deal 1 damage to an opponent's Star. |
| CO24 (C1) | Trojan Asteroid | 1 | 3 | Sz1/St3 | Core | P, Def | Your other COs in the positions next to this CO have +1 Size and +1 Stability. |
| CO25 | Polar Sentinel | 2 | 3 | Sz2/St3 | Core | P, Def | While this CO is in your North position, your other COs have +1 Stability. |
| CO26 | Thieving Moon | 2 | 3 | Sz2/St3 | Core | A, E | When this CO enters orbit, you may move one Augmentation from any CO in orbit onto this CO. |
| CO27 (C2) | Tidally Locked World | 3 | 3 | Sz3/St3 | **Unique** | P | At the end of your Rotation Phase, if this CO is in your North position, draw 1 card. |
| CO28 | Terrestrial World | 3 | 3 | Sz3/St3 | Core | R | Must enter East. |
| CO29 | Super-Mercury | 4 | 3 | Sz4/St3 | Core | V | No ability. |
| CO30 | Hot Jupiter | 5 | 3 | Sz5/St3 | **Unique** | D | When this CO wins a Collision, deal 1 damage to an opponent's Star. |
| CO31 | Guardian Moon | 1 | 4 | Sz1/St4 | **Unique** | Def | Damage dealt to your Star by each AE is reduced by 1, to a minimum of 1. |
| CO32 | Rocky Moon | 2 | 4 | Sz2/St4 | Core | R | Must enter North or South. |
| CO33 | Survey Moon | 2 | 4 | Sz2/St4 | Core | E | When this CO enters orbit, look at the top 2 cards of the draw deck. Put 1 into your hand and the other on the bottom of the deck. |
| CO34 | Spin Moon | 3 | 4 | Sz3/St4 | Core | E | When this CO enters orbit, you may rotate your orbit one step. |
| CO35 | Super-Earth | 4 | 4 | Sz4/St4 | **Unique** | A, Def | While this CO has an Augmentation attached, your other COs have +1 Stability. |
| CO36 | Iron Remnant | 1 | 5 | Sz1/St5 | **Unique** | Def | Opponents' Direct Effects cannot choose your other COs. |

**Design notes on the COs**
- **Augmentation bias (Part 4 content goal):** 10 of 36 COs (28%) want an Augmentation: CO01, CO04, CO12, CO13, CO14, CO17, CO20, CO23, CO26, CO35. Four of them (CO14, CO20, CO26 and, indirectly, CO23) also help find or move Augmentations, easing the early "dead Augmentation" problem (Audit item 38).
- **Size 4 / Stability 1 peak (6 cards) is deliberately not the power peak:** 1 vanilla, 1 restriction, 1 drawback (discard), 1 small Augmentation bonus, 1 position bonus, 1 repositioning trigger. No unique CO sits in that cell.
- **Placement restrictions:** 5 of 36 (CO02, CO05, CO10, CO28, CO32), about 14%, "a flavourful minority".
- **The rotation hook (cycle 2):** 6 position-based COs (CO07, CO16, CO24, CO25, and North payoffs CO21, CO27) and 3 that rotate or reposition (CO06, CO18, CO34). Old CO21 "During your Rotation Phase, this CO moves one step in the opposite direction to your other COs." Old CO27 "This CO does not move during your Rotation Phase."
- **Unique (build-around) designs, 9:** CO13 Augmentation tank, CO14 Augmentation tempo, CO21 North Size spike (C2; was retrograde), CO23 Augmentation damage engine, CO27 North draw (C2; was anchor), CO30 Collision damage (sacrifice-into-damage), CO31 and CO36 defensive anchors, CO35 Augmentation-powered shield.
- **Small Size / high Stability COs** (Size 1-2, Stability 3-5) are mostly defensive or utility, so they earn their slot without adding much Critical Mass.

---

## 4. Astronomical Events (60)

**Split (cycle 2): 16 Augmentations (27%) / 44 Direct Effects (73%)**, close to the source's old 30/70 guideline; cycle 2 turned the six least-played Augmentations into host-free Direct Effects to cut dead cards. No split is locked. Cycle 1 note: The source mentions an old 30/70 guideline; this build leans slightly more to Augmentations because 10 COs and 2 Stars (ST02, ST08) need Augmentations to function, and because 6 Augmentations attach to opponents' COs, which gives early Augmentation draws a target.

**Cost tiers: 33 Free / 21 Soft / 6 Hard (10%)** (cycle 1: AE43, AE45, AE49, AE57 Soft to Free; AE60 Free to Soft).

**Damage column** = damage to an opposing Star each time the card resolves (or each time an attached Augmentation triggers). "1-3" = scales with the board.

### 4.1 Augmentations (16 in cycle 2)

Cycle 2: AE04, AE07, AE08, AE14, AE15 and AE17 moved to 4.2 as Direct Effects (rows removed here; old texts in 4.2 and `cards.json`).

| ID | Name | Cost tier | Damage | Ability text |
|---|---|---|---|---|
| AE01 | Orbital Stabilizer | Free | - | Attach to one of your COs. It has +2 Stability. |
| AE02 | Accretion Disk | Free | - | Attach to one of your COs. It has +1 Size. |
| AE03 | Planetary Ring | Soft | - | Attach to one of your COs that has no other Augmentation attached. It has +1 Size and +1 Stability. |
| AE05 | Thick Atmosphere | Free | - | Attach to one of your COs. It has +1 Stability, or +2 Stability instead while it is in your South position. |
| AE06 | Captured Satellite | Soft | - | Attach to one of your COs with Size 3 or less. It has +2 Size. |
| AE09 | Ion Cannon | Soft | 1 per turn | Attach to one of your COs with Stability 2 or less. At the start of your turn, deal 1 damage to an opponent's Star. |
| AE10 | Impact Lance | Free | 1 per trigger | Attach to one of your COs. When it wins a Collision, deal 1 damage to an opponent's Star. |
| AE11 | Siphon Tap | **Hard** | 1 per turn | Cost: discard 1 card from your hand. Attach to an opponent's CO. At the start of your turn, deal 1 damage to the Star of the player whose orbit that CO is in. |
| AE12 | Erosion | Free | - | Attach to any CO in orbit. It has -1 Stability. |
| AE13 | Mass Loss | Free | - | Attach to any CO in orbit. It has -1 Size. |
| AE16 (C2) | Polar Accretion | Free | - | Attach to one of your COs. It has +1 Size, or +2 Size instead while it is in your North position. |
| AE18 | Booster Engine | Free | - | Attach to one of your COs. Active, once per turn: move that CO to an empty position in your orbit. |
| AE19 | Deep Space Network | Free | - | Attach to one of your COs. Whenever any CO enters an opponent's orbit, you may draw 1 card. *(The set's one table-wide "any CO enters orbit" trigger.)* |
| AE20 | Tidal Heating | Free | - | Attach to one of your COs. At the end of your turn, if it is in your North position, draw 1 card. |
| AE21 | Volatile Core | **Hard** | - | Cost: discard 1 card from your hand. Attach to one of your COs. It has +2 Size and +1 Stability. |
| AE22 | Roche Tether | Free | - | Attach to an opponent's CO. While it is in its owner's North position, it has -2 Stability. |

### 4.2 Direct Effects (44 in cycle 2)

| ID | Name | Cost tier | Damage | Ability text |
|---|---|---|---|---|
| AE04 (C2) | Magnetosphere | Free | - | Choose one of your COs. Until the start of your next turn, it has +2 Stability and opponents' cards cannot choose it. |
| AE07 (C2) | Solar Harvest | Free | - | Draw 1 card. If the CO in your North position has Size 4 or more, draw 2 cards instead. |
| AE08 (C2) | Interstellar Dust | Free | - | Draw 1 card. If an opponent has more COs in orbit than you, draw 2 cards instead. |
| AE14 (C2) | Orbital Exchange | Free | - | Draw 1 card. Then you may swap the positions of two of your COs (both move at once; no Collision). |
| AE15 (C2) | Heliosphere | Free | - | Until the start of your next turn, prevent the first 2 damage that opponents' cards and abilities would deal to your Star. Draw 1 card. |
| AE17 (C2) | Spectral Analysis | Free | - | Draw 2 cards, then discard 1 card from your hand. |
| AE23 (C1) | Solar Flare | Free | 1 | Choose one: deal 1 damage to an opponent's Star; or choose an opponent's CO, it gets -1 Stability this turn. |
| AE24 | Coronal Mass Ejection | Soft | 2 | Play only if you have 2 or more COs in orbit. Deal 2 damage to an opponent's Star. |
| AE25 (C1) | Gamma-Ray Burst | **Hard** | 3 | Cost: deal **2** damage to your own Star. Deal 3 damage to an opponent's Star. |
| AE26 | Supernova Shockwave | Free | 1 (each opponent) | Deal 1 damage to each opponent's Star. |
| AE27 | Meteor Shower | Soft | 1-3 | Play only if you have a CO with Size 4 or more in orbit. Deal 1 damage to an opponent's Star for each of your COs with Size 4 or more (maximum 3). |
| AE28 (C1) | Gravitational Slingshot | **Hard** | 2-3 | Cost: put the CO in your **North** position into the Out of Orbit zone (it is knocked out of orbit). Deal 2 damage to an opponent's Star, or 3 if that CO had Size 4 or more. |
| AE29 | Impact Event | Soft | 1 | Choose an opponent's CO with Size 4 or more. It gets -1 Stability this turn, and deal 1 damage to its owner's Star. |
| AE30 | Stellar Wind | Free | 1-2 | Deal 1 damage to an opponent's Star. If that opponent has more COs in orbit than you, deal 2 instead. |
| AE31 | Retaliation Pulse | Soft | 2 | Play only if your Star has taken damage since the end of your last turn. Deal 2 damage to an opponent's Star. |
| AE32 (C1F) | Tidal Disruption | Soft | 2 | Choose one: choose an opponent whose total Size in orbit is 12 or more and deal 2 damage to their Star; or draw 1 card. |
| AE33 | Pulsar Beam | Free | 1 | Deal 1 damage to an opponent's Star. Draw 1 card. |
| AE34 | Kessler Cascade | Soft | 1-3 | Play only if the Out of Orbit zone has at least 1 CO. Deal 1 damage to an opponent's Star for each CO in the Out of Orbit zone (maximum 3). |
| AE35 | Flare Star | Free | 1-2 | Deal 1 damage to an opponent's Star. If your Star has less HP than that Star, deal 2 instead. |
| AE36 | X-Ray Binary | Soft | 1-3 | Play only if at least 1 Augmentation is attached to your COs. Deal 1 damage to an opponent's Star for each Augmentation attached to your COs (maximum 3). |
| AE37 | Starquake | Free | 2 | Deal 2 damage to an opponent's Star. That opponent draws 2 cards. |
| AE38 | Gravitational Perturbation | Free | - | Choose an opponent's CO and move it to another position in their orbit. If that position is occupied, a Collision occurs; the moved CO is the incoming CO. |
| AE39 | Asteroid Impact | Soft | - | Choose an opponent's CO with Stability 1. Knock it Out of Orbit. |
| AE40 | Black Hole | **Hard** | - | Cost: discard 2 cards from your hand. Choose any CO in orbit and discard it (it does not go to the Out of Orbit zone). |
| AE41 (C2) | Solar Wind Sweep | Free | - | Choose an opponent. The CO in their North position (if any) gets -1 Stability this turn. Draw 1 card. |
| AE42 (C1F) | Strip Atmosphere | Soft | - | Choose one: choose an Augmentation attached to any CO and discard it; or draw 1 card. |
| AE43 (C1) | Solar Storm | Free | - | Choose an opponent's CO. Discard all Augmentations attached to it. It gets -1 Size this turn. |
| AE44 (C1F) | Recapture | Soft | - | Choose one: choose a CO in the Out of Orbit zone and reclaim it into your orbit; or draw 1 card. |
| AE45 (C1) | Comet Return | Free | - | Draw 1 card. Then you may reclaim a CO with Size 3 or less from the Out of Orbit zone into your orbit. |
| AE46 | Lagrange Rescue | **Hard** | - | Cost: discard 1 card from your hand. Reclaim a CO from the Out of Orbit zone into your orbit, even if a CO has already entered your orbit this turn. |
| AE47 | Stargazing | Free | - | Draw 2 cards. |
| AE48 | Deep Field Survey | Free | - | Look at the top 3 cards of the draw deck. Put 1 into your hand and the other 2 on the bottom of the deck in any order. |
| AE49 (C1) | Search the Skies | Free | - | Look at the top 4 cards of the draw deck. You may reveal a CO from among them and put it into your hand. Put the rest on the bottom of the deck in any order. |
| AE50 (C1F) | Mass Transfer | Soft | - | Choose one: choose an Augmentation attached to an opponent's CO and choose one of your COs, then move that Augmentation onto that CO; or draw 1 card. |
| AE51 | Dark Matter Halo | Free | - | Until the start of your next turn, COs in your orbit have +1 Stability. |
| AE52 (C1F) | Event Horizon | Soft | - | Choose one: choose an opponent with an active Critical Mass countdown and knock their CO with the highest Size Out of Orbit (if several are tied, you choose among them); or draw 1 card. |
| AE53 | Roche Limit | Soft | - | Choose an opponent's CO with Size 4 or more. It gets -2 Stability this turn. |
| AE54 | Orbital Insertion | Soft | - | Play only if no CO has entered your orbit this turn. Place a CO from your hand into your orbit, then you may attach an Augmentation from your hand to it. Neither of those cards counts as one of your 2 plays. |
| AE55 (C1) | Free-Return Trajectory | Soft | - | Choose an opponent's CO in their North position. Return it to its owner's hand; its Augmentations are discarded. |
| AE56 | Stellar Nursery | Soft | - | Play only if your Star has less HP than its starting HP. Your Star regains 2 HP, up to its starting HP. |
| AE57 (C2) | Gravity Assist | Free | - | Draw 1 card. Then you may rotate your orbit one step. |
| AE58 | Orbital Resonance | Free | - | Rotate one opponent's orbit one step. Draw 1 card. |
| AE59 (C1F) | Scavenge | Soft | - | Draw 1 card. Then you may discard a CO from the Out of Orbit zone. |
| AE60 (C2) | Gravitational Wave | Soft | - | Choose an opponent who has a CO in their North position. Every CO in their orbit except the one in North moves one step clockwise. The CO that moves into North (from West) causes a Collision there; it is the incoming CO. (This chooses a player, not a CO.) |

**Cycle 2 rulings and old texts.** AE04: "cannot choose" covers Direct Effects and Augmentations that would name the CO; AE52 (chooses a player) and AE41 (hits a position) still apply. AE15: counts damage points in order across sources, after CO31's reduction; does not stop your own costs (AE25, CO22). AE14's swap is a move, not entering orbit. Old texts: AE04 (Augmentation) "Attach to one of your COs. Opponents' effects cannot reduce its Size or Stability." AE07 Binary Tether (Augmentation) "Attach to one of your COs. While it has another Augmentation attached, it has +2 Stability." AE08 Satellite Swarm (Augmentation) "... While it has 3 or more Augmentations attached (including this one), it has +2 Size." AE14 Rogue Gravity (Augmentation) "Attach to an opponent's CO. It does not move during its owner's Rotation Phase." AE15 Retrograde Kick (Augmentation) "Attach to any CO in orbit. During its owner's Rotation Phase, it moves one step in the opposite direction ..." AE16 Lagrange Anchor "... It has +1 Size and does not move during your Rotation Phase." AE17 Shield Lattice (Augmentation) "Attach to one of your COs. Opponents' Direct Effects cannot choose it." AE41 (cycle 1) "Each opponent's CO in a North position gets -1 Stability this turn. Draw 1 card." AE57 (cycle 1) "... rotate your orbit one step in either direction." AE60 (cycle 1) "... and a direction. Every CO ... moves one step in that direction ..."

Old texts of the cycle 1 reworks: AE16 "...It does not move during your Rotation Phase." AE23 "Deal 1 damage to an opponent's Star." AE25 cost was 1 self-damage. AE28 "Cost: put one of your COs from orbit into the Out of Orbit zone ... Deal 3 damage ..." AE41 "Every CO in a North position (in every orbit) gets -1 Stability this turn." AE43 "Choose a CO with 2 or more Augmentations attached. Discard all of them." AE45 "Reclaim a CO with Size 3 or less ... Draw 1 card." AE49 "Take a CO from the discard pile into your hand." AE55 "Return one of your COs from orbit to your hand ..." AE57 "Choose one of your COs and move it to another position ..." AE60 "Every player's orbit rotates one step."

---

## 5. Tallies and cross-checks

### 5.1 Damage density (required output, Part 4 §3)

**18 of the 60 AEs (30%) deal direct damage to an opposing Star:** 15 Direct Effects (AE23-AE37) and 3 Augmentations (AE09, AE10, AE11).

| Card | Min | Max | Notes |
|---|---|---|---|
| AE23 Solar Flare | 1 | 1 | modal: or -1 Stability to a CO |
| AE24 Coronal Mass Ejection | 2 | 2 | |
| AE25 Gamma-Ray Burst | 3 | 3 | hard cost: 2 to own Star (C1) |
| AE26 Supernova Shockwave | 1 | 1 | to each opponent |
| AE27 Meteor Shower | 1 | 3 | per Size-4+ CO |
| AE28 Gravitational Slingshot | 2 | 3 | hard cost: sacrifice your North CO; 3 only if it had Size 4+ (C1) |
| AE29 Impact Event | 1 | 1 | |
| AE30 Stellar Wind | 1 | 2 | 2 if behind on COs |
| AE31 Retaliation Pulse | 2 | 2 | |
| AE32 Tidal Disruption | 2 | 2 | anti-Critical-Mass |
| AE33 Pulsar Beam | 1 | 1 | |
| AE34 Kessler Cascade | 1 | 3 | per CO Out of Orbit |
| AE35 Flare Star | 1 | 2 | 2 if behind on HP |
| AE36 X-Ray Binary | 1 | 3 | per Augmentation |
| AE37 Starquake | 2 | 2 | |
| AE09 Ion Cannon (Aug) | 1 | 1 | every turn while attached |
| AE10 Impact Lance (Aug) | 1 | 1 | per Collision won |
| AE11 Siphon Tap (Aug) | 1 | 1 | every turn while attached |
| **Total (18 cards)** | **25** | **34** | |

- **Average damage per resolution: 1.39 minimum, 1.89 maximum, 1.64 midpoint.** Direct Effects alone: 22 / 15 = 1.47 min, 31 / 15 = 2.07 max. AE25's net swing fell from +2 to +1 and AE28 now costs real Critical Mass progress.
- Recurring sources (count per trigger above): the 3 Augmentations, plus 2 COs (CO23 Brown Dwarf Companion, 1 per turn with an Augmentation; CO30 Hot Jupiter, 1 per Collision won). COs are **not** in the 18/60 tally.
- Damage mitigation in the pool: CO31 Guardian Moon (-1 per AE, minimum 1), AE56 Stellar Nursery (heal 2). Self-damage: AE25 (cost), CO22 (enters orbit).
- Star-side damage (roster, unchanged): 5 of 12 Stars can deal 1 damage per turn under conditions (ST05, ST06, ST07, ST11, ST12).

### 5.2 Counts

| Check | Required | Built |
|---|---|---|
| Draw pile | 96 | 96 (36 CO + 60 AE) |
| Duplicates | 0 | 0 (all names and texts unique) |
| CO grid | locked, cell for cell | matched (section 3) |
| CO Size / Stability averages | 3.36 / 2.19 | 3.36 / 2.19 |
| Core / unique COs | 27 / 9 | 27 / 9 |
| COs wanting Augmentations | "visible" | 10 of 36 |
| Placement restrictions | minority | 5 of 36 |
| AE subtypes | both meaningful | 16 Augmentation / 44 Direct Effect (cycle 2; was 22 / 38) |
| Hard costs | small minority, strongest only | 6 of 60 (AE11, AE21, AE25, AE28, AE40, AE46) |
| Instant-speed cards | 0 | 0 |
| Table-wide "any CO enters orbit" triggers | at most a couple | 1 (AE19) |
| Jargon ("Overtake") | 0 | 0 |

### 5.3 Cross-check against the 12 Stars

No CO or AE copies a Star's exact effect. Closest neighbours, all deliberately complementary:

| Star | Nearest cards | Why it isn't a duplicate |
|---|---|---|
| ST01 discard to draw | AE47, AE48, CO33 | Card draw, not filtering; cost a play. |
| ST02 move an Augmentation | CO26, AE50 | One-time steal on entry / from an opponent, not a repeatable move between your own COs. |
| ST03 draw when your CO is knocked out | AE28, CO30, CO13 | Give it sacrifice and Collision outlets; no card draws on knockout. |
| ST04 +1 Stability at Size 10+ | CO25, CO35, AE51 | Conditional on position, an Augmentation, or one turn. |
| ST05 damage with 3+ COs | AE24 (2+ COs, 2 damage, one-shot) | One-shot AE. |
| ST06 retaliate when knocked out | none | |
| ST07 damage if you took damage | AE31 Retaliation Pulse | One-shot, 2 damage; same trigger condition (rules 5.8 defines "since your last turn"). |
| ST08 +1 Size per Augmented CO | AE02, AE16, CO04, CO17 | Single-CO bonuses; ST08 applies to every Augmented CO. They stack, an intended synergy to watch. |
| ST09 reclaim ignoring the cap | AE46 Lagrange Rescue | One-shot, hard cost; §5 explicitly allows AEs to override the cap. |
| ST10 threshold 2 lower, +1 Stability during countdown | AE51 (one-turn +1 Stability) | One-shot, not tied to the countdown. |
| ST11 reclaim small COs, damage on reclaim | AE44, AE45, AE46, ST09 | AEs are one-shot; ST09 ignores the CO cap but deals no damage. |
| ST12 -1 Stability to an opponent's CO each turn | AE23 (mode 2), AE41, AE12 | One-shot or position-bound; ST12 repeats every turn. |

**Cycle 2 update.** Denial/control: AE14 and AE15 left the denial list (17 cards remain); AE41 now hits one opponent. Defensive one-shots added: AE04 (one CO), AE15 (Star). **Playable on an empty board: 26 of 44 Direct Effects** (new: AE07, AE08, AE14, AE15, AE17; AE41 stays legal; AE04 needs one of your COs). Estimated dead cards on an empty board 34 of 96, about 2.5 per 7-card hand (was 39, about 2.85); unverified until simulated. ST11 (was in the Out of Orbit reclaim group) now captures instead.

**Denial/control support (cycle 1 text):** the pool carries 19 denial/control cards: AE12, AE13, AE14, AE15, AE22, AE23 (mode 2), AE32, AE38, AE39, AE40, AE41, AE42, AE43, AE52, AE53, AE55, AE59, AE60, CO36. **Cheap answers to Critical Mass (cycle 1):** five Free or Soft cards now knock out or shrink a CO without a hard cost and with an easy target: AE23 (-1 Stability), AE41 (-1 Stability in North, cantrip), AE43 (strip Augmentations and -1 Size), AE55 (bounce the North CO, the Denial card), AE60 (forced Collision at North). ST12 is now a true Denial Star.

**Playable on an empty board (cycle 1):** 15 of 38 Direct Effects are always legal (AE23, AE25, AE26, AE30, AE33, AE35, AE37, AE41, AE45, AE47, AE48, AE49, AE51, AE57, AE58); AE45, AE49 and AE57 are new to this list and AE41 is no longer self-harming. AE60 left the list (it now needs an opponent's North CO). **Fix-before-critic pass (C1F):** AE32, AE42, AE44, AE50, AE52 gained an "or draw 1 card" option (worth exactly a Recycle of that card) and AE59 draws first, so **21 of 38** Direct Effects are now always legal (dead on an empty board: 39 of 96 cards, about 2.85 per 7-card hand, was 45 / 3.3). Old texts: AE32 "Choose an opponent whose total Size in orbit is 12 or more. Deal 2 damage to their Star." AE42 "Choose an Augmentation attached to any CO and discard it." AE44 "Reclaim a CO from the Out of Orbit zone into your orbit." AE50 "Move one Augmentation attached to an opponent's CO onto one of your COs." AE52 "Choose an opponent with an active Critical Mass countdown. Knock their CO ..." AE59 "Choose a CO in the Out of Orbit zone and discard it. Draw 1 card."

---

## 6. Notes for the simulation (and the owner)

- **Cycle 2 re-coding list:** ST05 (HP 6), ST11 (HP 6, capture trigger), CO21, CO27, AE04, AE07, AE08, AE14, AE15 (now Direct Effects), AE16, AE17, AE41, AE57, AE60; rules: rotation always clockwise with no rotation Collisions, Recycle removed, CO27's end-of-Rotation-Phase trigger (cancel check after the Rotation Phase still applies; CO21 and AE16 change Size on rotation). Swingy pairs to watch: ST11 at 6p (knockouts on every turn), CO21 + AE16 in North (Size 7-8 exposed), AE04 on the deadline CO.
- **Early dead draws.** Cycle 2: 26 of 44 Direct Effects are always playable and the mulligan stays; Recycle was removed (the never-Recycle bot won 54.9%). Playing 0 cards is always legal. The simulation should record how often a hand has no legal play.
- **Cycle 1 re-coding list for `sim/game.py`:** ST01 HP, ST08, ST10, ST11, ST12, CO14, CO24, AE16, AE23, AE25, AE28, AE41, AE43, AE45, AE49, AE55, AE57, AE60, plus the rule changes in `rules.md` section 8 (rotation direction choice, threshold by player count, G4, mulligan, Recycle, G8 check timing, G29 stack, G31 discard). **Fix pass adds:** AE32, AE42, AE44, AE50, AE52, AE59; 6p threshold 16; G8 checks after Active abilities and Start of Turn triggers (`rules.md` change log F1-F11).
- **Swingy pairs to watch (cycle 1 list; AE08 and the ST11 loop no longer exist):** ST08 + CO13 (Augmentation stacking into a Collision-proof Size 6+ CO); AE54 Orbital Insertion + CO14 Shepherd Moon (several free Augmentations); AE28 + ST03 (sacrifice draws a card); ST08 + cheap Augmentations (+1 Size each, watch ST08's Critical Mass rate); ST12 + AE53 or AE23 (two Stability reductions in one turn knock out a Stability-3 CO); ST11 + AE60/AE41 (knock a small CO out, then reclaim it for 1 damage).
- **Anti-Critical-Mass counterplay present:** AE32, AE52, AE53, AE13, AE39, AE40, AE38 (Collision forcing), AE22 (North sabotage); AE14/AE15 rotation sabotage removed in cycle 2.
- **Rule gaps:** all of G1-G40 are now answered in `rules.md` (table in section 5.10); the result-moving ones are marked PROVISIONAL.
