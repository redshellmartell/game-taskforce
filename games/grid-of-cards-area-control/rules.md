# Nine Fields - Rules (v1)

## 1. Overview

- **Title:** Nine Fields
- **Hook:** Nine drifting islands, a handful of explorers. Crowd an island to its limit and the tide pushes its whole row or column, shoving one island off the edge of the world and into somebody's pocket.
- **Players:** 2-4
- **Play time:** about 20 minutes
- **Age:** 10+
- **Complexity:** 2.5 / 5

## 2. Components

- **30 Island cards.** Each card shows:
  - **Value** (1-4 pearls): points scored by whoever claims it.
  - **Capacity** (2-4 pawn circles): how many pawns the island can hold.
  - **Current arrow:** a double-headed arrow printed either along the card's long side or its short side. Cards always enter the grid upright (portrait), so a long-side arrow means the island pushes its **Column** and a short-side arrow means it pushes its **Row**. Giving the card a quarter turn swaps its axis.
- **16 pawns:** 4 each in 4 colours. Every player always uses exactly 4 pawns.

Nothing else is needed. Scores are kept as claimed Island cards.

### Island card list

Axis = axis when the card enters the grid upright (R = Row, C = Column).

| ID | Name | Value | Capacity | Axis |
|---|---|---|---|---|
| I01 | Gull Rock | 1 | 2 | R |
| I02 | Driftwood Key | 1 | 2 | C |
| I03 | Salt Flat | 1 | 2 | R |
| I04 | Kelp Bank | 1 | 2 | C |
| I05 | Tern Spit | 1 | 2 | R |
| I06 | Crab Shoal | 1 | 2 | C |
| I07 | Foam Isle | 1 | 2 | R |
| I08 | Seal Ledge | 1 | 2 | C |
| I09 | Amber Cay | 2 | 2 | R |
| I10 | Coral Knot | 2 | 2 | C |
| I11 | Lantern Rock | 2 | 2 | R |
| I12 | Reed Marsh | 2 | 3 | C |
| I13 | Pine Holm | 2 | 3 | R |
| I14 | Shell Beach | 2 | 3 | C |
| I15 | Mist Atoll | 2 | 3 | R |
| I16 | Otter Bay | 2 | 3 | C |
| I17 | Heron Isle | 2 | 3 | R |
| I18 | Cliff Mouth | 2 | 3 | C |
| I19 | Blue Lagoon | 2 | 3 | R |
| I20 | Pearl Reef | 3 | 3 | C |
| I21 | Whale Rest | 3 | 3 | R |
| I22 | Sunken Bell | 3 | 3 | C |
| I23 | Old Harbour | 3 | 4 | R |
| I24 | Fire Peak | 3 | 4 | C |
| I25 | Tide Temple | 3 | 4 | R |
| I26 | Long Strand | 3 | 4 | C |
| I27 | Orchard Isle | 3 | 4 | R |
| I28 | Storm Tower | 3 | 4 | C |
| I29 | Crown Island | 4 | 4 | R |
| I30 | Moon Atoll | 4 | 4 | C |

Totals: 30 cards, 65 points; 15 Row, 15 Column.

## 3. Setup

1. Each player takes the 4 pawns of one colour. Return unused colours to the box.
2. Choose a first player at random. Play goes clockwise.
3. Shuffle all 30 Island cards. Deal 9 face up, upright, into a 3x3 grid in reading order (top-left, top-middle, top-right, middle-left, ... bottom-right).
4. Place the remaining 21 cards face down as the **island deck**. Turn its top card face up beside the deck: this is the **next island**, visible to everyone.
5. **Opening pawns:** starting with the **last** player in turn order and going counter-clockwise (ending with the first player), each player places 1 pawn on any island that has no pawn yet. Opening pawns never cause a flood.
6. The first player takes the first turn.

## 4. Turn structure

On your turn, do exactly **one** action, then resolve a flood if one was caused.

### Phase 1: Action (choose one)

- **A. Land:** place 1 pawn from your supply onto any island that is not full.
- **B. Sail:** move 1 of your pawns from the island it is on to an orthogonally adjacent island that is not full. Adjacency is checked in the current grid.

An island is **full** when the number of pawns on it (all colours) is equal to or greater than its capacity. You may Sail a pawn *out of* a full island.

If your supply is empty you must Sail. If you have no legal action, you pass.

### Phase 2: Flood (only if triggered)

An island **floods** when a pawn arrives on it (by Land or Sail) and its pawn count becomes equal to its capacity. The player who moved that pawn is the **trigger player** and resolves these steps in order:

1. **Choose a direction.** Look at the flooded island's current axis. For a Row axis, choose left or right; for a Column axis, choose up or down. The **line** is the row or column containing the flooded island.
2. **Fall off.** The island at the end of the line in the chosen direction falls off the grid (this may be the flooded island itself). It is claimed (see Section 5, "Claiming"). All pawns on it return to their owners' supplies.
3. **Slide.** The other two islands in the line move one space in the chosen direction, carrying their pawns with them.
4. **Refill.** Place the next island, upright and empty, in the space left open at the opposite end of the line. Then turn the top card of the deck face up as the new next island. If there was no next island to place, leave the space empty; the game ends after this flood (Section 6).
5. **Turn.** If the flooded island is still in the grid, give it a quarter turn: its axis swaps (Row becomes Column, Column becomes Row). It stays full with its pawns on it.

Then play passes to the next player clockwise.

## 5. Special rules and timing

- **Claiming.** When an island falls off (or is scored at game end), the player with the most pawns on it claims it and puts it face down in their **trophy pile**.
  - **Tie:** among the tied players, the one with the **fewest trophy cards** right now claims it. If still tied, nobody claims it; remove it from the game face up.
  - **No pawns at all:** during a flood, the trigger player claims it (salvage). At game end, an empty island is not claimed by anyone.
- **Trophy piles.** You may look at your own trophies at any time. The **number** of cards in each pile is public; their values are not. You may not look at or ask about other players' trophies.
- **Only one flood per action.** A flood cannot cause another flood: sliding and refilling never add pawns.
- **Sail adjacency** uses the grid as it is at the moment of the action.
- **Turning cards.** Only the flooded island turns. Islands that slide keep their orientation. Every card entering the grid enters upright with its printed axis.
- **Empty deck.** When the deck is empty, the face-up next island is still placed normally. Only when a refill is needed and no next island exists does the game end.
- **Stall limit.** If 3 x (number of players) consecutive turns pass without a flood, the game ends immediately (proceed to final scoring).

## 6. End of game and scoring

1. **Trigger:** the game ends at the end of a flood in which an empty space could not be refilled, or when the stall limit is reached.
2. **Final tide:** score each island still in the grid in reading order (top-left to bottom-right) using the Claiming rules. The fewest-trophies tiebreak uses pile sizes at the moment each island is scored. Empty islands are not claimed.
3. **Score:** everyone reveals their trophy pile. Your score is the total value of your trophies.
4. **Tiebreakers:** (a) the most trophy cards; (b) the player later in turn order (the player who acted later in the first round) wins.

## 7. Design notes

**Core tension.** Every Land pushes an island toward its flood. Filling an island gives you, the trigger player, a binary choice: let the full island fall off now (scoring it to its majority holder), or push the far end of the line off instead and keep the full island in place, turned to its new axis, as a locked prize for later. Players fight over majorities but must also watch which lines are dangerous: an island two columns away can be shoved off by a flood you never touched. Sailing lets you rescue pawns or contest a neighbour but adds no new presence.

**The twist (originality).** The trigger is crowding: islands move because players fill them, and the overcrowded island decides which line moves while the trigger player decides which end falls. Then the island turns a quarter, so the same island next pushes the other axis. Everything is visible (capacity, axis, next island), so it is fully tactical. This differs from the close comparables:
- *Shifting Stones* manipulates tiles by playing cards for secret pattern goals; Nine Fields has no hands and no patterns, and grid movement is the scoring trigger for open majority control.
- *Contactics* is static-board 3x3 area control; *Collapsi* shifts rows and columns as movement. In Nine Fields, falling off the edge is the only way an island scores mid-game, so a shift means "cash in this island now," and the grid is a conveyor feeding new islands from the deck.

**Kingmaking at 3-4 players.** Three rules keep the trigger choice self-serving rather than "pick which opponent wins":
1. **Salvage:** an empty island that falls goes to the trigger player, and new islands always enter empty at a line's end, so most floods offer at least one option that pays you.
2. **Hidden values:** only pile sizes are public, so near the end nobody can be sure who is leading, and deliberate kingmaking is a guess.
3. **Fewest-trophies tiebreak:** tied majorities go to whoever has claimed least, so piling onto the leader's island often hands it to a trailing player rather than the leader.

**Catch-up and closeness.** The fewest-trophies tiebreak is the main brake on a runaway leader. Pawns return only when their island falls, so a player who wins many islands keeps re-deploying while a player with pawns locked on a full island is temporarily short. Final tide scoring keeps the last few floods tense, and the next-island card lets players plan the endgame.

**Seat balance.** Opening pawns are placed in reverse turn order, so later seats pick the best opening islands. The final tiebreak also favours later seats.

**Expected length (for the playtester to verify).** 21 refills plus the final flood = 22 floods, at roughly 2-3 turns per flood, giving about 50-70 turns. Levers if the length is off: deck size (deal fewer cards), or capacities.

**Bot notes.** All randomness is in the initial shuffle. Decisions per turn: action (Land on up to 9 islands, or Sail up to 4 x 4 targets) and, on a flood, 1 of 2 directions. A greedy bot can value a direction by the claimed island's value to itself minus its value to the current points leader.

## 8. Changelog

- v1 (2026-10-04): first version from the brief.
