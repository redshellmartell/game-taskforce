# Heavenly Bodies v2: Rules (cycle 0, first design pass)

Working title: **Heavenly Bodies: Close Orbit**. Card list: `cards.md` (machine copy `cards.json`).

---

## 1. Overview

- **Hook:** Every player has a little 4-card orbit, and each orbit touches the orbits of the players next to them. On your turn you **spin any orbit on the table**: yours to line up your big planets, or an opponent's to drag their weak moon into your path. Where two touching orbits meet, the bodies **crash**: the bigger one captures the smaller one and it flies into the winner's hand. Build a full orbit that survives a whole round with one of three winning patterns.
- **Players:** 2-4 (2 and 3 are the core counts).
- **Play time:** 10-15 minutes.
- **Age:** 8+. **Complexity:** 1.5/5. **Teach:** about 5 minutes (script in section 7.4).
- **Core loop:** Draw, Launch a card into your orbit, Spin an orbit, Crash, Cool down.
- **Three ways to win** (all need a full orbit of 4 bodies at the **start of your turn**):
  - **Critical Mass:** total Size 15 or more.
  - **Constellation:** all four the same colour.
  - **Grand Alignment:** four Sizes in a run: 1-2-3-4 or 2-3-4-5.

---

## 2. Components

56 cards, nothing else.

| Component | Count | Contents |
|---|---|---|
| Body cards | 52 | 4 colours (Ember red, Frost blue, Verdant green, Solar gold) x 13 cards. Each colour has Sizes 1,1, 2,2,2, 3,3,3, 4,4,4, 5,5. |
| Star cards | 4 | One per player. The centre of your orbit. Printed: the four slot names, the turn summary, the three win patterns. |

Body kinds by Size (name and icon only; the only printed rule text is on Size 1 and Size 5):

| Size | Kind | Per colour | Total | Card text |
|---|---|---|---|---|
| 1 | Comet | 2 | 8 | "Captures a Giant." |
| 2 | Moon | 3 | 12 | none |
| 3 | World | 3 | 12 | none |
| 4 | Ringed World | 3 | 12 | none |
| 5 | Giant | 2 | 8 | "Captured by a Comet." |

Zones: **Deck** (face down), **Deep Space** (one shared face-up discard pile; only its top card is available), **hands** (hidden; hand sizes are public), **orbits** (face up).

---

## 3. Setup

1. Each player puts a Star card in front of them. The four spaces around it are that player's **orbit slots**, named from the owner's seat: **North** (beyond the Star, toward the table centre), **East** (owner's right), **South** (between the Star and the owner), **West** (owner's left).
2. Shuffle the 52 Body cards. Deal 5 to each player.
3. Each player secretly chooses 2 of their 5 cards and places them face down in two different slots of their own orbit. When everyone has placed, turn them all face up at once. Each player keeps the other 3 cards as their hand.
4. The rest of the Body cards form the Deck. Deep Space starts empty.
5. Choose the first player at random. Play passes to the left (clockwise around the table).
6. The first player skips the Draw step of their first turn only.

**Contacts.** Your **West** slot touches the **East** slot of the player on your left. Your **East** slot touches the **West** slot of the player on your right. Each touching pair is one **contact**. With 2 players the opponent is on both sides: your West touches their East and your East touches their West (2 contacts). With 3 players there are 3 contacts, with 4 players 4. North and South never touch anything.

---

## 4. Turn structure

**0. Check for a win.** If your orbit holds 4 bodies that form Critical Mass, Constellation or Grand Alignment (section 6), you win now. Otherwise continue.

**1. Draw.** If the Deck is empty, the game ends now (Long Night, section 6). Otherwise take either the top card of the Deck or the top card of Deep Space into your hand. (First player, first turn: skip this step.)

**2. Launch.** You may play 1 card from your hand into any slot of your own orbit.
- **Recall:** if that slot already holds a body, take that body back into your hand. (You can use this to swap a card or rescue one from a contact.)
- **Rebound:** if, at the start of this step, your orbit holds **fewer** bodies than every other player's orbit, you may Launch twice, into two different slots.
- Launching never causes a crash by itself.

**3. Spin.** You must choose one orbit on the table that holds at least one body (yours or any other player's) and turn it one step, **clockwise** (North to East to South to West to North) or **counter-clockwise** (North to West to South to East to North). Every body in that orbit moves one slot at once. "Clockwise" is as seen from above the table. If no orbit holds a body, skip steps 3 and 4.

**4. Crash.** Check the two contacts of the orbit that was spun: its West contact first, then its East contact. At each contact where **both** touching slots hold a body, those two bodies collide:
- The **larger Size wins**, except that a **Comet (Size 1) beats a Giant (Size 5)**.
- The winner stays where it is. The loser is **captured**: the owner of the winning body takes the losing body into their hand. (It does not matter whose turn it is.)
- **Equal Size:** both bodies are knocked out to Deep Space. The active player chooses which of the two goes on top.

**5. Cool down.** If you have more than 5 cards in hand, discard down to 5. Discards go face up onto Deep Space one at a time, in the order you choose (the last one is the new top card). Play passes left.

**Legal options in one line:** Draw (Deck or Deep Space top) -> Launch 0 or 1 card (2 with Rebound), Recall allowed -> Spin exactly one non-empty orbit one step either way -> Crash resolves automatically -> discard to 5.

---

## 5. Special rules and timing

There are three special rules: **Comet beats Giant**, **Recall**, **Rebound**. Everything else is the core loop.

- **When orbits change.** Your orbit gains bodies only during your own Launch. It loses bodies only in a Crash or by your own Recall. Spinning never changes which bodies are in an orbit, only where they sit. So a winning orbit at the start of your turn is one that survived every opponent's turn since you built it.
- **Hand limit timing.** The 5-card limit applies only in your own Cool down step. Captures on other players' turns may take you above 5 until then.
- **Empty Deep Space.** If Deep Space is empty you must draw from the Deck.
- **Empty hand.** If your hand is empty, skip Launch.
- **Spin targets.** You may spin an orbit belonging to a player who is not next to you (only possible with 4 players). Its contacts with that player's own neighbours then crash; you can neither win nor lose cards in those crashes.
- **Two-player contacts.** When either orbit spins, both of its contacts are with the other player, so up to two crashes happen between the same two orbits.
- **One body per slot.** A slot holds at most one body. Spinning keeps this true, since every body moves together.
- **Simultaneous win patterns.** Only the active player's orbit is checked, only in step 0, so two players can never win at the same moment.
- **Ties in Rebound.** "Fewer than every other player" is strict: if you are tied for the fewest, no Rebound.
- **Setup reveal.** Players choose their 2 opening bodies without seeing anyone else's.

---

## 6. End of game and scoring

The game ends in one of two ways.

**A. A win pattern (the usual ending).** At step 0 of your turn, your orbit holds 4 bodies and at least one of these is true:

| Name | Pattern | Example |
|---|---|---|
| **Critical Mass** | Total Size of the four bodies is 15 or more | 5, 4, 3, 3 |
| **Constellation** | All four bodies are the same colour | four Frost cards of any Sizes |
| **Grand Alignment** | The four Sizes are exactly 1,2,3,4 or exactly 2,3,4,5, in any slots and any colours | 2, 5, 3, 4 |

You win immediately. Slot order does not matter for any pattern.

**B. Long Night (fallback and turn cap).** If the Deck is empty at the start of any player's Draw step, the game ends at once. The player with the highest total Size in their orbit wins; if tied, the tied player with more bodies in orbit; if still tied, those players share the win.

Turn cap: the Deck is the cap. It holds 42 / 37 / 32 cards at 2 / 3 / 4 players, so the game lasts at most 43 / 38 / 33 turns.

---

## 7. Design notes

### 7.1 Three directions considered
1. **Gearbox (chosen).** Personal 4-slot orbits that touch their neighbours at East and West; spin *any* orbit and the touching bodies crash; the bigger captures the smaller into its owner's hand; win with a full orbit pattern that survives a round. *Risk:* the active player picks the best of several spins every turn, so orbits may churn and nobody completes a pattern (stall into Long Night).
2. **Carousel (brief direction B).** Each player has a 3-slot arc. Launching a card into your first slot pushes the arc along, and the card pushed off the end flies into your left neighbour's arc and pushes theirs (a chain round the table that stops before returning to you). *Risk:* chains are deterministic and hard to read, and the only decision is which card to push in; few real choices per turn.
3. **Shared Sky (bold, brief direction A taken to the limit).** No personal ownership at all: every body sits in one ring that runs round the whole table, a 3-slot arc in front of each player, and the whole sky turns one step each round. You own whatever is in front of you when a win is checked. *Risk:* moving 9-12 cards each round is fiddly, ownership feels weightless, and planning more than one turn ahead is nearly impossible.

**Why Gearbox:** it keeps rotation as the main verb with a real choice every turn (which orbit, which way), makes ownership change visibly through captures, moves at most 4 cards per spin, and works at 2 to 4 players because contacts are defined by neighbours. Carousel lost on decisions per turn; Shared Sky lost on fiddliness and on the owner's "simple".

### 7.2 Intended strategies and tensions
- **The clock.** Spinning your own orbit always brings your North and South bodies into the contacts, so you choose only which side each one faces. Spinning an opponent instead keeps your current contacts and changes what they face. Every turn is a choice between "improve my line-up" and "break theirs".
- **Build vs fight.** Giants win fights and make Critical Mass, but a Comet takes them. Moons are weak in a crash but complete Alignments and Constellations. A strong orbit is also a target.
- **The round of exposure.** A completed orbit must survive one turn of every opponent. Players will hold their fourth card until the contacts facing them are safe (small opposing bodies, empty neighbouring slots), or keep a Comet ready for the opponent's Giant.
- **Deep Space** tempts you: the top card may complete your pattern, but everyone sees what you take.
- **The twist:** the table is a gearbox. Rotation is not just your own clock (as in v1); you can turn anyone's orbit, and contacts make the turn of one ring an attack on its neighbours.

### 7.3 Comeback and pacing
- **Comeback:** (1) every win needs a full orbit that survives a round, so the leader is the obvious target and anyone, even a non-neighbour, can spin the leader's orbit; (2) **Rebound** gives the player with the fewest bodies two Launches, a catch-up tied to the gap in orbit size; (3) Comets let a weak hand topple a Giant. KPI: runaway leader at most 65%, at least 2 lead changes per game.
- **Round 1 cannot decide the game:** nobody can win during round 1. Normally the earliest win is at the start of your third turn (2 opening bodies + 1 Launch per turn). A player who gets Rebound on turn 1 (for example the second player in a 2-player game, facing a 3-body orbit) can reach 4 bodies at once, but must still survive every opponent's turn and can win no earlier than the start of their second turn.
- **Lead metric for the sim:** the leader after each turn is the player with the highest orbit total Size (ties: no leader change).

### 7.4 Five-minute teach script
1. "Your orbit is 4 slots round your Star. West and East touch your neighbours."
2. "Each turn: draw, put a card in your orbit, then spin any one orbit one step."
3. "Where spun cards touch, they crash: bigger takes smaller into its owner's hand. Same size, both fly off. A Comet takes a Giant."
4. "Win at the start of your turn with 4 cards: 15 total, one colour, or a run."
5. "Fewest cards in orbit? Launch two. Over 5 cards in hand at your end? Discard."

### 7.5 Bands and tuning knobs
| Players | Seat gap | Length (total turns) | Minutes | Pattern share target | Long Night |
|---|---|---|---|---|---|
| 2 | <= 5 pts | 14-24 | 9-14 | each pattern 15-50% of wins | <= 10% of games |
| 3 | <= 5 pts | 18-30 | 10-15 | same | <= 10% |
| 4 | <= 5 pts | 20-34 | 11-15 | same | <= 15% |

- **Main knob: the Critical Mass threshold** (15). Raise to 16 if Critical Mass takes over 50% of wins; lower to 14 if under 15%.
- **Length knob: opening bodies** (2). Use 1 if games are under band, 3 if Long Night exceeds its band.
- **Comeback knob: Rebound** (two Launches). Ablate it; if runaway stays above 65% with it, extend Rebound to "fewest or tied for fewest".
- Drop 4 players if its seat gap or Long Night rate cannot be brought into band with these knobs.

### 7.6 Ablation bots (for the playtester)
Each must lose to the full strategic bot by at least 5 points at 2, 3 and 4 players:
- **Self-spin only:** never spins another player's orbit (tests the twist).
- **Comet-blind:** values a Comet as a plain Size 1 and never plans Comet-vs-Giant (tests the special crash rule).
- **No Recall:** never Launches onto an occupied slot.
- **Deck only:** never takes the Deep Space top card.
- **Rule ablation, not a bot:** play with Rebound removed and compare runaway leader and lead changes.

### 7.7 What I suspect is weakest
1. **Churn:** the active player picks the best of 4 to 8 spin options, so they may capture almost every turn; full orbits may rarely survive a round, pushing games into Long Night or past 15 minutes.
2. **Grand Alignment may be too easy** (Sizes 2-4 are 36 of 52 cards) and could crowd out Constellation.
3. **4-player turns:** 8 spin options and a non-neighbour across the table may slow turns (analysis paralysis) and weaken that player's interaction.

### 7.8 Test these first
1. At 2 and 3 players: game length, Long Night rate, and the share of wins from each pattern (is the churn real?).
2. The self-spin-only ablation at every count: does spinning other orbits change best play?
3. Runaway leader and lead changes with and without Rebound, plus the seat gap with the first-player skip-draw.

What I would try next if this works: give each colour a one-icon Launch effect only if the sim shows turns feel samey. What I suspect is still wrong: see 7.7, item 1.

### 7.9 Known gaps
- Teach time and fun are untested by humans (simulation cannot measure them).
- The rules file is longer than one page because of these design notes; the player-facing rules (sections 2-6) are about 75 lines with 3 special rules, inside the brief's limit of 3.

---

## 8. Changelog

- **Cycle 0:** first draft. No feedback yet.

---

## Playbook check

1. **Family:** read "Race to a finite pile" and "All families" in `studio/mechanics.md` (the Deck is a finite pile with a Long Night fallback). Named trap: an early leader keeps the lead; the brief also warns against an inert twist (L1).
2. **Comeback:** a winning orbit must survive one turn of every opponent, anyone can spin the leader's orbit, Rebound (fewest bodies Launches twice, tied to the gap), Comet beats Giant. KPI: runaway leader <= 65%, lead changes >= 2.
3. **Ablations:** self-spin-only, Comet-blind, no-Recall, Deck-only bots must each lose by >= 5 points at 2, 3 and 4 players; Rebound removed as a rule ablation on runaway and lead changes.
4. **Self-check:** fixes made while drafting: (a) all three patterns now need a full orbit (three Giants would otherwise make Critical Mass with 3 cards); (b) the spin must target a non-empty orbit (spinning an empty orbit was a free pass); (c) tie order on Deep Space is chosen by the active player (top card matters); (d) Rebound is strict to make 2-player ties unambiguous; (e) Long Night triggers only at a Draw step, the only place cards are drawn; (f) captures on other players' turns may exceed the hand limit until your own Cool down; (g) 2-player contacts defined explicitly (two contacts with the same opponent); (h) Launch never crashes, only Spin does. Dead cards: none; every Size serves at least one pattern and Sizes 1 and 5 have the crash exception. Undefined cases covered: empty Deck, empty Deep Space, empty hand, no non-empty orbit, ties in crashes, Rebound ties, Long Night ties, simultaneous patterns.
5. **Band and knob:** seat gap <= 5 at 2/3/4p; each pattern 15-50% of wins; Long Night <= 10% (2-3p) and <= 15% (4p). Knob: Critical Mass threshold (15); length knob: opening bodies (2).
6. **Ends:** a win pattern checked at the start of a turn, or Long Night when the Deck runs out; cap 43/38/33 turns; expected 14-24 / 18-30 / 20-34 turns, about 9-15 minutes vs the brief's 10-15.
7. **Budget:** player-facing rules (sections 2-6) about 75 lines; 3 special rules (Comet beats Giant, Recall, Rebound) vs the brief's limit of 3; card text at most 3 words on 16 cards, none on the rest.
8. **Re-run list:** first pass, so run all ablations at every count. Any change to the Critical Mass threshold, the hand limit, Rebound or the Spin targets means re-running all of them.
