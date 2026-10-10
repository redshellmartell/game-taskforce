# Heavenly Bodies v2: Rules (cycle 1, revision 1, fix-before-critic pass)

Working title: **Heavenly Bodies: Gearbox**. Card list: `cards.md` (machine copy `cards.json`). Playtest switches for single-change tests: section 7.7.

---

## 1. Overview

- **Hook:** Every player has a little 4-card orbit, and each orbit touches the orbits of the players next to them. On your turn you **spin any orbit on the table**: yours to line up your planets, or an opponent's to drag their weak moon into your path. Where two touching orbits meet, the bodies **crash**: the bigger one captures the smaller one into its owner's hand. Finish your turn with a full orbit that makes one of three patterns and you win, so everyone can see who is one card away and gang up to break them.
- **Players:** 2-4 (2 and 3 are the core counts; 4 is provisional, see 7.5).
- **Play time:** target 10-15 minutes (brief). **Measured in cycle 1 (bots): 4.4 / 7.2 / 8.0 turns at 2 / 3 / 4 players, about 2-3 minutes: far under band, to be fixed in cycle 2** (see 7.3).
- **Age:** 8+. **Complexity:** 1.5/5. **Teach:** about 5 minutes (script in 7.4).
- **Core loop:** Wake, Draw, Launch a card into your orbit, Spin an orbit, Crash, End (check for a win).
- **Three ways to win** (all need 4 bodies in your orbit at the **end of your own turn**):
  - **Critical Mass:** total Size at least 16 / 15 / 14 (2 / 3 / 4 players).
  - **Constellation:** all four the same colour, or one of each colour.
  - **Grand Alignment:** four Sizes in a run: 1-2-3-4 or 2-3-4-5.

---

## 2. Components

56 cards, nothing else.

| Component | Count | Contents |
|---|---|---|
| Body cards | 52 | 4 colours (Ember red, Frost blue, Verdant green, Solar gold) x 13 cards. Each colour has Sizes 1,1, 2,2,2, 3,3,3, 4,4,4, 5,5. |
| Star cards | 4 | One per player. The centre of your orbit. Printed: slot names, turn summary, the three patterns and the Critical Mass table. |

| Size | Kind | Per colour | Total | Card text |
|---|---|---|---|---|
| 1 | Comet | 2 | 8 | "Captures a Giant." |
| 2 | Moon | 3 | 12 | none |
| 3 | World | 3 | 12 | none |
| 4 | Ringed World | 3 | 12 | none |
| 5 | Giant | 2 | 8 | "Captured by a Comet." |

Zones: **Deck** (face down), **Deep Space** (face-up discard pile; cards there are out of the game), **hands** (hidden; hand sizes are public), **orbits** (face up).

---

## 3. Setup

1. Each player puts a Star card in front of them. The four spaces around it are that player's **orbit slots**, named from the owner's seat: **North** (toward the table centre), **East** (owner's right), **South** (toward the owner), **West** (owner's left).
2. Shuffle the 52 Body cards. Deal 5 to each player.
3. Each player secretly chooses 2 of their 5 cards and places them face down in any two different slots of their own orbit. When everyone has placed, turn them all face up at once (upright, not shielded). Nothing crashes at setup. Each player keeps the other 3 cards as their hand.
4. The rest of the Body cards form the Deck (42 / 37 / 32 cards at 2 / 3 / 4 players).
5. Choose the first player at random. Play passes to the left.
6. The first player skips the Draw step of their first turn only.

**Contacts.** Your **West** slot touches the **East** slot of the player on your left; your **East** slot touches the **West** slot of the player on your right. Each touching pair is one **contact**. With 2 players the opponent is on both sides, so you have 2 contacts with them. North and South never touch anything.

---

## 4. Turn structure

**1. Wake.** If you have a sideways (shielded) body, turn it upright in whatever slot it now occupies (spins may have moved it since you launched it). Standing a body up never causes a crash; it can crash only when an orbit with that contact is spun later.

**2. Draw.** If the Deck is empty, the game ends now (Long Night, section 6). Otherwise draw the top card of the Deck. (First player, first turn: skip this step, including the check.)

**3. Launch.** You may play 1 card from your hand into any slot of your own orbit, placed **sideways**: it is **shielded** until the start of your next turn (see Crash). If the slot already holds a body, that body returns to your hand (**Recall**). A recalled body is always upright (your Wake has already stood up last turn's launch), so it goes to your hand like any card. Launching never causes a crash.

**4. Spin.** Choose one orbit on the table that holds at least one body (yours or any other player's) and turn it one step, **clockwise** (North to East to South to West) or **counter-clockwise**, as seen from above. Every body in it moves one slot at once; sideways bodies stay sideways. You must spin if any orbit holds a body. A spin is legal even if it causes no crash or changes nothing that matters (for example spinning an orbit whose only body is sideways); that is allowed and works as a pass. You may spin even with an empty hand.

**5. Crash.** Check the spun orbit's West contact, then its East contact. At each contact where both slots hold a body and **neither is sideways**, they collide:
- The **larger Size wins**, except that a **Comet (1) beats a Giant (5)**.
- The loser is **captured**: the owner of the winning body takes it into their hand. The winner stays where it is.
- **Equal Size:** both go to Deep Space.

**6. End.** If you have more than 5 cards in hand, discard down to 5 (to Deep Space). Then (discarding never touches an orbit, so this order cannot change the result), if your orbit holds 4 bodies that form a pattern (section 6), **you win**. Otherwise play passes left.

**Legal options in one line:** Wake -> Draw 1 -> Launch 0 or 1 card sideways (Recall allowed) -> Spin exactly one non-empty orbit one step either way -> Crash -> discard to 5, check your win.

---

## 5. Special rules and timing

Three special rules: **Comet beats Giant**, **Recall**, **Shield** (sideways bodies do not crash).

- **Shield.** A sideways body never collides: it cannot capture or be captured, and a contact where either body is sideways does nothing. It still counts for patterns and for Long Night. You have at most one sideways body: the one you launched on your most recent turn. It moves with the spin like any body and stays sideways until your next Wake. Because sideways bodies never collide, a sideways body and an upright body of the same Size (or two bodies of any Sizes) may sit in a contact together; nothing happens until a later spin brings them into a contact with both bodies upright.
- **Contact with a sideways body.** The whole contact does nothing: neither body is captured, whichever one would have won.
- **Only your own win.** Only the active player's orbit is checked, only in step 6. Patterns formed in other orbits during your turn do nothing. If your orbit meets two or three patterns at once, you win; patterns are not ranked and each is checked on its own.
- **Hand limit timing.** The 5-card limit applies only in your own End step. Captures on other turns may take you above 5 until then.
- **Empty hand:** skip Launch. **No body anywhere:** skip Spin and Crash.
- **Spin targets.** At 4 players you may spin the orbit of the player opposite you. Its contacts with its own neighbours crash; you can neither win nor lose cards there.
- **Two players.** Either orbit's spin checks both contacts, and both are with the other player, so up to two crashes happen.
- **Captured bodies** go to the hand of the winning body's owner, whoever's turn it is.
- **One body per slot.** Spinning keeps this true.

---

## 6. End of game and scoring

**A. Pattern win (the usual ending).** At the end of your own turn (step 6), your orbit holds 4 bodies and at least one is true:

| Name | Pattern | Example |
|---|---|---|
| **Critical Mass** | Total Size at least **16** (2 players), **15** (3 players), **14** (4 players) | 5, 4, 4, 3 |
| **Constellation** | All four the same colour, **or** one of each of the four colours | E2, F5, V1, S3 |
| **Grand Alignment** | Sizes exactly 1,2,3,4 or exactly 2,3,4,5, any slots, any colours | 2, 5, 3, 4 |

You win immediately. Slot order and sideways cards do not matter.

**B. Long Night (fallback).** If the Deck is empty at the start of a Draw step, the game ends at once. The player with the highest total Size in their orbit wins. Ties: more bodies in orbit; then the largest single body; then the tied player who would have taken the next turn soonest, counting from and **including** the player whose Draw found the Deck empty (so if that player is among the tied players, they win).

**Turn cap.** Every turn but the first draws exactly 1 card, so Long Night comes after exactly **43 / 38 / 33** completed turns at 2 / 3 / 4 players. That is the hard cap; no backstop is needed.

**Earliest win.** You start with 2 bodies and gain at most 1 per turn, so nobody can win in round 1; the earliest win is at the end of your second turn (3 completed turns at 2 players). **Measured in cycle 1:** 52% of 2p games end at that minimum of 3 turns; mean 4.4 / 7.2 / 8.0 turns at 2 / 3 / 4 players; the Long Night cap is reached in 0 / 0 / 0.1% of games.

---

## 7. Design notes

### 7.1 Intended strategies and tensions
- **The visible threat.** Orbits are face up and the patterns are simple, so every player can see who is one Launch from winning ("she has 5-4-4 out and 3 cards in hand"). The rest of the table spins to capture that player's bodies. Being close makes you the target; the swing when a Comet knocks out the Giant that was about to finish someone's Critical Mass is the moment the game is built for.
- **Build vs fight.** Big bodies win crashes and make Critical Mass but Comets take Giants; Moons and Comets are weak in a crash but finish Alignments and Constellations.
- **The forced spin.** You must spin every turn, and at 2 players every spin touches your own contacts. Completing your orbit and then choosing a spin that does not wreck it is the last puzzle of a winning turn.
- **Where to launch.** The new body is shielded for a round. Put it in a contact to block that crash, or in North/South to keep it out of contact after the shield drops. Opponents can still spin your orbit to move the shielded body out of the contact.
- **The twist:** the table is a gearbox. You can turn anyone's orbit, and the turn of one ring is an attack on its neighbours.

### 7.2 Comeback and pacing
- **Comeback:** (1) the player closest to winning is visible and anyone can spin their orbit; (2) captured cards go to the attacker's hand, so the players breaking the leader gain cards to rebuild; (3) Comet beats Giant lets a weak hand topple the biggest body; (4) the shield protects a rebuilding player's newest body. KPI: runaway leader at most 65%, lead changes at least 2.
- **Round 1 cannot decide the game:** nobody can hold 4 bodies before their second turn.
- **Lead metric for the sim:** keep orbit total Size (continuity with cycle 0). I expected lead changes to fall from 21 to roughly 3-8 per game. **Measured in cycle 1: 0.64 / 1.76 / 2.06 (out of band at 2-3p); midpoint leader wins 74.7 / 63.5 / 41.0% (out of band at 2p).** Captures per game 1.8 / 2.3 / 2.5 against 15-25, so comebacks (1)-(3) barely fire in games this short.

### 7.3 Expected length
Target 14-24 / 18-30 / 20-34 total turns at 2 / 3 / 4 players (about 10-14 minutes at 0.4 min per turn). **Measured in cycle 1 (1,000 games per count, strategic mirror): 4.4 / 7.2 / 8.0 turns, about 1.8 / 2.9 / 3.2 minutes: out of band by a factor of 3-4.** Seat 1 wins 66.9% at 2p and 62.4% at 3p (seat gap 16.9 / 29.1 / 18.4 points, band 5). The playtester's switch test isolates the shield as the cause (SHIELD off: 22.6 / 33.7 / 30.4 turns). Left for cycle 2 after the critique; this fix pass changes no mechanics.

### 7.4 Five-minute teach script
1. "Your orbit is 4 slots round your Star. West and East touch your neighbours."
2. "Each turn: draw, put a card in your orbit sideways, then spin any one orbit one step."
3. "Where spun cards touch, they crash: bigger takes smaller into its owner's hand. Same size, both are lost. A Comet takes a Giant. Sideways cards are new and do not crash; stand yours up at the start of your turn."
4. "Finish your turn with 4 cards that total 16 or more (15 with 3 players, 14 with 4), one colour or all four colours, or a run, and you win. Watch whoever is close."
5. "Over 5 cards in hand at your end? Discard."

### 7.5 Bands and knobs
| Players | Seat gap | Total turns | Long Night | Pattern share | Captures per game |
|---|---|---|---|---|---|
| 2 | <= 5 pts | 14-24 | <= 10% | each pattern 15-50% of pattern wins | 15-25 |
| 3 | <= 5 pts | 18-30 | <= 10% | same | 15-25 |
| 4 | <= 5 pts | 20-34 | <= 15% | same | 15-25 |

- **Main knob: Critical Mass threshold per count** (16 / 15 / 14). Raise by 1 at a count where Critical Mass takes over 50% of pattern wins or games are under band; lower by 1 where it is under 15% or Long Night is over band.
- **2p length knob:** if 2p is still under 14 turns with threshold 17, open with 1 body at 2p. (Measured in cycle 1: threshold 17 gives 4.6 turns, 1 opening body 6.5, both 6.5; the knob does not reach band. CM 15 at every count is inert.)
- **Constellation knob:** if Constellation is over 50%, return to "one colour only"; if under 15% with the rainbow, keep it and lower nothing else.
- **4 players:** if Long Night stays over 15% or the seat gap over 5 after one threshold step (14 to 13), **drop 4 players** and print the game as 2-3.

### 7.6 Three candidate fixes for the main problem (win timing and churn)
1. **Win at the end of your own turn, Rebound cut, a one-turn shield (picked).** The win needs one completed turn of your own instead of surviving everyone else's, so the threat is visible and breakable but not impossible (cycle 0 variant: 3p 20 turns, Long Night 12.5%, patterns 42 / 39 / 5). The 2p collapse to 4.9 turns came mostly from Rebound: the second player faced a 3-body orbit on turn 1, launched twice to 4 bodies and could win at once. Cutting Rebound removes that and the rule. The shield is the critic's one-turn protection; it slows churn and adds a placement decision without tokens (the card is turned sideways).
2. **Bold: Supernova countdown.** At the end of your turn, if you form a pattern, turn your Star sideways (a public warning); you win at the end of your next turn if your orbit still makes any pattern, and you may repair it in between. **Lost:** it keeps "survive every opponent's turn", which the oracle probe found impossible in over 99% of positions, so repair becomes the same churn and Long Night returns; it also stretches each game by a full round per threat, the wrong direction for length.
3. **Bold: captures that do not always happen ("graze").** A body captures only if it is bigger by 2 or more; otherwise the bodies bounce. Captures would roughly halve (79% to 44% of meetings) and the equal-size rule disappears. **Lost:** nothing is Size 6, so Ringed Worlds could never be captured and Giants only by Comets; a wall of 4s makes Critical Mass a fortress (dominant strategy), and fixing that needs card changes.
- **Not taken from the critic's list:** 3 opening bodies (lets the first player win at the end of turn 1, a decided round 1, L3) and a 32-36 card Deck (Long Night was the 4p failure, 58%; a smaller Deck makes it worse). The smaller Deck is a switch (DECK40) to try after the win-timing result.
- **Deep Space draw cut:** its ablation was inert (-5.2 / +8.0 / -2.9) and it made the turn cap false. Without it the Deck is an exact clock and the equal-size "choose the top card" ruling is gone.

### 7.7 Playtest switches (one change each; defaults are the rules above)
| Switch | Default | Off / alt value = | KPI it tests |
|---|---|---|---|
| `WIN_AT_END` | on | win checked at the start of your turn (cycle 0) | Long Night rate, pattern wins, length |
| `REBOUND` | off | on: fewest bodies (strict) launches twice (cycle 0); with `SHIELD` on, both launched bodies are sideways until that player's next Wake | 2p length, runaway, lead changes |
| `SHIELD` | on | off: launched bodies are upright at once | captures per game, runaway, length |
| `CM_BY_COUNT` | 16/15/14 | 15 at every count | Critical Mass share per count, 2p length, 4p Long Night |
| `RAINBOW` | on | off: Constellation is one colour only | Constellation share (cycle 0: 5%) |
| `DEEPSPACE_DRAW` | off | on: Draw may take the Deep Space top card; equal-size crash, active player picks the top card | deck-only ablation, length |
| `DECK40` | off | on: remove copy c of Sizes 2, 3 and 4 in every colour (12 cards; 40 bodies) | length, Long Night at 4p |
| `CAPTURE_TO_DS` | off | on: captured bodies go to Deep Space, not a hand (alternative arm; weakens "cards change owners") | captures, runaway, length |
| `OPENING_2P` | 2 | 1 opening body at 2p: each player places 1 of their 5 cards and keeps 4 in hand (the first player still skips their first Draw) | 2p length only |

Suggested order: headline at defaults (2, 3, 4p); then `REBOUND` on, `SHIELD` off, `CM_BY_COUNT` off, `RAINBOW` off, one at a time; `DECK40` and `CAPTURE_TO_DS` only if length or captures miss band.

### 7.8 Ablation bots (each must lose to the full strategic bot by at least 5 points at 2, 3 and 4 players)
- **Self-spin only:** never spins another orbit (the twist).
- **Comet-blind:** treats a Comet as a plain Size 1.
- **No Recall:** never Launches onto an occupied slot.
- **Shield-blind:** chooses the Launch slot ignoring the shield (best pattern slot only).
- **Threat-blind:** spins only for its own captures and never targets the player closest to a pattern (tests the visible-threat comeback).
- **Defence check (critic):** a bot that keeps its biggest body in each contact; compare with the strategic bot to see whether the cycle 0 oracle result was a bot artefact.
- Reference bots: random, greedy (best immediate capture and total), strategic (pattern-aware with threat targeting). Report the spread (L2).

### 7.9 Known gaps
- Teach time and fun are untested by humans.
- **Cycle 1 measurements out of band (bots only, unvalidated), held for cycle 2:** length 4.4 / 7.2 / 8.0 turns; seat gap 16.9 / 29.1 / 18.4; captures 1.8 / 2.3 / 2.5; lead changes 0.64 / 1.76 / 2.06; 2p runaway 74.7%; strategic bot loses to greedy by 14.0 / 8.0 / 13.1 points. In band: Long Night 0 / 0 / 0.1%, pattern shares 21-46%, strategic vs random +92 to +98.
- **Inert twists (ablation under 5 points):** Recall (no-recall -1.8 / -1.9 / 0.0) and Comet beats Giant (comet-blind 3.4 / 0.1 / 0.9; Giants captured 0.1 times per game); shield-blind and threat-blind at 3-4p. Re-test after the length fix; cut Recall if still inert.
- The per-count Critical Mass thresholds are measured as inert (CM 15 everywhere gives the same length and seat gap).
- The 4p count is provisional (7.5).
- Player-facing rules (sections 2-6) are about 80 lines with 3 special rules, inside the brief's limit of 3; the page count with design notes is over one page.

### 7.10 Next and suspicions
- **What I would try next if this works:** time a human teach with the 5-line script and check whether the sideways shield reads clearly; if 4p holds, try `DECK40` to bring the box under 50 cards.
- **What I suspected (cycle 1 result):** 2p too fast: confirmed, at every count (4.4 / 7.2 / 8.0 turns). Critical Mass crowding out the others: false for the strategic bot (27-40% of pattern wins), true for the greedy bot (81-93%).

---

## 8. Changelog

### Cycle 1 fix pass (before the critic), from `playtest-report.md` / `playtest.json` cycle 1 (11 ambiguities)
Wording and stale numbers only; no mechanic, threshold, shield, opening-body or win-timing change. Each ruling matches what the sim already does.
| # | Ambiguity (playtest.json) | Ruling, where |
|---|---|---|
| F1 | Long Night last tie-break: does the empty-Deck player count? | "counting from and **including**" that player; they win a full tie (6B) |
| F2 | Sideways body spun into another slot before Wake | Wake stands it up wherever it now is; standing up never causes a crash (step 1) |
| F3 | Rebound plus Shield | Switch-only: both launched bodies are sideways (7.7 `REBOUND`) |
| F4 | Discard vs win-check order | Discard first; it never touches an orbit, so order cannot matter (step 6) |
| F5 | Can Recall return a sideways card? | No: the recalled body is always upright after Wake (step 3) |
| F6 | Shielded body in a contact, either side would win | Whole contact does nothing (section 5, new bullet) |
| F7 | Equal Sizes resting in contact with a shield up | Allowed; nothing happens until a later spin with both upright (section 5, Shield) |
| F8 | Spin with an empty hand / all orbits empty | Spin is allowed with an empty hand; skip only if no orbit holds a body (step 4; section 5 already) |
| F9 | `OPENING_2P` = 1 hand size | Place 1 of 5, keep 4; first player still skips first Draw (7.7) |
| F10 | Spinning an orbit whose only body is sideways | Legal, acts as a pass (step 4). Flagged: makes "must spin" soft; for the critic, not changed here |
| F11 | Hand limit only in your End step | Already written (section 5); no change |
- **Wrong number fixed:** teach script line 4 said "15 or more"; now 16 / 15 / 14 by player count (7.4), matching section 6.
- **Stale text corrected to the cycle 1 measurements (flagged out of band):** play time (1), earliest win (6), lead changes and captures (7.2), expected length (7.3), 2p knob result (7.5), known gaps (7.9), suspicions (7.10), Playbook check line 6. The cycle 1 "Kept" line below predicted Recall would matter more; measured no-recall -1.8 / -1.9 / 0.0, so it is still inert (7.9).
- `cards.json`: Long Night tie-break text updated to "including"; version note added. Still parses (no structural change).

### Cycle 1 (revision 1), from `critique.md` cycle 0 (REVISE-MAJOR, 3.17) and `playtest-report.md`
| # | Change | Was | Feedback | KPI it should move |
|---|---|---|---|---|
| C1-1 | **Win checked at the end of your own turn** (step 6), not the start | start of turn, after surviving a round | Critic change 1; L14: patterns survived 0-0.2%, Long Night 95-100% | Long Night to <= 10/10/15%; pattern wins to most games; turns into 14-24 / 18-30 / 20-34 |
| C1-2 | **Critical Mass by count: 16 / 15 / 14** | 15 everywhere | Critic changes 1 and 6 (2p 4.9 turns, 4p 58% Long Night) | Critical Mass share 15-50% at each count; 2p length; 4p Long Night |
| C1-3 | **Rebound cut** | fewest bodies launch twice | Critic change 3: inert as comeback, fired on 70% of turns, caused 2p turn-1 wins | 2p length up; captures down; runaway <= 65% held |
| C1-4 | **Shield:** a launched body is placed sideways and does not crash until its owner's next Wake | none | Critic change 3 | captures per game to 15-25; runaway <= 65% |
| C1-5 | **Constellation also counts one of each colour** | one colour only | Constellation 5% of 3p pattern wins in the variant (target 15-50%) | Constellation share to 15%+ |
| C1-6 | **Deep Space draw cut**; equal-size crash just sends both to Deep Space | Draw could take the Deep Space top; active player chose the top card | Critic change 5 (deck-only ablation -5.2 / +8.0 / -2.9); false turn cap | turn cap exact (43/38/33), backstop deleted; rule lines down |
| C1-7 | **Long Night tie-break** extended (largest body, then next in turn order) | shared win | Critic change 5 (5-8% shared wins at 3-4p) | shared wins 0% |
| - | **Kept:** spin any orbit either way, Comet beats Giant, Recall (expected to matter more now that a full orbit must be fixed in one turn; no-recall measured +10.3 at 4p in the variant), 56 cards, first-player skip draw, 5-card hand limit, 2 opening bodies | | | |

Captured-to-Deep-Space is offered only as the `CAPTURE_TO_DS` switch (critic change 4). Why the other candidates lost: 7.6.

### Cycle 0
First draft and fix-before-critic pass (12 rulings). Rulings 1, 2, 6 are obsolete with C1-6 (exact Deck clock, no top-card choice); rulings 3-4 are obsolete with C1-3; the others stand in sections 3-5.

---

## Playbook check

1. **Family:** `studio/mechanics.md` "Race to a finite pile" and "All families" (the Deck is the clock). Trap: the early leader keeps the lead, and Long Night can still swallow the win patterns (L14); hence an exact Deck clock and an ending-share measurement.
2. **Comeback:** visible threat that anyone can spin at, captures feed the attackers' hands, Comet beats Giant, shield for the newest body. KPI: runaway leader <= 65%, lead changes >= 2.
3. **Ablations (each must lose by >= 5 points at 2, 3 and 4 players):** self-spin-only, comet-blind, no-Recall, shield-blind, threat-blind; plus a defence-check bot; rule switches in 7.7 one at a time.
4. **Self-check:** fixed: (a) a false turn cap (Deep Space draw cut, cap now exact 43/38/33); (b) the equal-size top-card choice (gone); (c) Rebound's recall/relaunch timing (gone); (d) Long Night shared wins (tie-break to a single winner); (e) shield cases written out: sideways vs upright, sideways vs sideways, sideways during your own spin, sideways counts for patterns and Long Night, sideways moves with the spin, at most one per player; (f) win check only for the active player, only in step 6, after discarding; (g) setup reveal is upright, not shielded; (h) 3 opening bodies rejected because it allows a turn-1 win; (i) cycle 1 fix pass: 11 playtest ambiguities ruled (F1-F11, changelog), the main one the Long Night tie-break "including" the empty-Deck player. Inert rules measured, not yet cut: Recall, Comet beats Giant (7.9). Dead cards: none (every Size serves a pattern; Comets now also fill a rainbow). Undefined cases covered: empty Deck, empty hand, no body anywhere, crash ties, simultaneous patterns, Long Night ties.
5. **Band and knob:** 7.5. Seat gap <= 5; turns 14-24 / 18-30 / 20-34; Long Night <= 10/10/15%; each pattern 15-50%; captures 15-25. Knob: Critical Mass per count; 2p fallback 1 opening body; drop 4p if it misses.
6. **Ends:** a pattern at the end of your own turn, or Long Night after exactly 43 / 38 / 33 turns (hard cap). Target 10-14 minutes against the brief's 10-15; **measured in cycle 1: 4.4 / 7.2 / 8.0 turns (about 2-3 minutes), out of band, held for cycle 2.**
7. **Budget:** player-facing rules about 80 lines; 3 special rules (Comet beats Giant, Recall, Shield), on the brief's limit of 3; card text on 16 cards, at most 3 words.
8. **Re-run list:** the win timing, a legality change (shield), a ceiling (thresholds) and a tie-break all changed, so re-run **all** ablations at every count, the seat gap, ending shares and pattern shares, captures per game, runaway and lead changes, with two or more reference bots.
