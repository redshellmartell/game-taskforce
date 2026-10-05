# Nine Fields - Rules (v2, revision 1)

## 1. Overview

- **Title:** Nine Fields
- **Hook:** Nine drifting islands, a handful of explorers. Crowd an island to its limit and the tide pushes its whole row or column, shoving one island off the edge of the world and into somebody's pocket. Wait too long and a storm does it for you.
- **Players:** 2-4
- **Play time:** about 20 minutes
- **Age:** 10+
- **Complexity:** 2.5 / 5

## 2. Components

- **30 Island cards.** Each card shows:
  - **Value** (1-4 pearls): points scored by whoever claims it.
  - **Capacity** (2-4 pawn circles): how many pawns the island can hold.
  - **Current arrow:** a double-headed arrow printed either along the card's long side or its short side. Cards always enter the grid upright (portrait), so a long-side arrow means the island pushes its **Column** and a short-side arrow means it pushes its **Row**. Giving the card a quarter turn swaps its axis. (Production: print the word "ROW" or "COLUMN" along the arrow so it reads correctly in both orientations.)
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
3. Shuffle all 30 Island cards. Deal 9 face up, upright, into a 3x3 grid in reading order (top-left, top-middle, top-right, middle-left, ... bottom-right). Grid spaces are numbered 1-9 in this reading order.
4. **3-4 players only:** take the top 3 cards of the remaining stack and return them to the box face down, unseen. Nobody may look at them. (2 players use every card.)
5. Place the remaining cards (21 at 2 players, 18 at 3-4 players) face down as the **island deck**. Turn its top card face up beside the deck: this is the **next island**, visible to everyone.
6. **Opening pawns:** starting with the **last** player in turn order and going counter-clockwise (ending with the first player), each player places 1 pawn on any island that has no pawn yet. Opening pawns never cause a flood and are not turns.
7. Set the **calm count** to 0 (keep it in your head or with a spare pawn of an unused colour; it is never more than 11).
8. The first player takes the first turn.

## 4. Turn structure

On your turn, do exactly **one** action, then resolve a flood if one was caused, then check for a storm.

### Phase 1: Action (choose one)

- **A. Land:** place 1 pawn from your supply onto any island that is not full.
- **B. Sail:** move 1 of your pawns from the island it is on to an orthogonally adjacent island that is not full. Adjacency is checked in the grid as it is now.

**Full** means the island's pawn count (all colours) is equal to or greater than its capacity. A full island can never be Landed or Sailed onto. You may Sail a pawn *out of* a full island; it then stops being full.

If your supply is empty you must Sail. If you have no legal Land and no legal Sail, you **pass** (this still counts as a turn).

### Phase 2: Flood (only if triggered)

An island **floods** when a pawn arrives on it (by Land or Sail) and its pawn count becomes equal to its capacity. The player who moved that pawn is the **trigger player** and resolves these steps in order:

1. **Choose a direction.** Look at the flooded island's current axis. For a Row axis, choose left or right; for a Column axis, choose up or down. The **line** is the row or column containing the flooded island.
2. **Fall off.** The island at the end of the line in the chosen direction (the far right for "right", the top for "up", and so on) falls off the grid. This may be the flooded island itself. It is claimed (Section 5, "Claiming"). All pawns on it return to their owners' supplies.
3. **Slide.** The other two islands in the line move one space in the chosen direction, carrying their pawns with them and keeping their orientation.
4. **Refill.** Place the next island, upright and empty, in the space left open at the opposite end of the line. Then turn the top card of the deck face up as the new next island (if the deck is empty, there is now no next island). If there was no next island to place, leave the space empty; the game ends after this flood (Section 6).
5. **Turn.** If the flooded island is still in the grid, give it a quarter turn: its axis swaps (Row becomes Column, Column becomes Row). It keeps all its pawns and stays full. If the flooded island fell off in step 2, nothing turns.

After any flood, set the calm count to 0.

### Phase 3: Storm check

If no flood happened this turn (including a pass), add 1 to the calm count. If the calm count is now **3 x the number of players** (6, 9 or 12), a **storm** strikes immediately:

1. **Storm island.** The storm island is the island with the fewest open spaces (capacity minus pawns). Ties: the one with the most pawns; then the first in reading order.
2. **Storm player.** The storm player is the player with the fewest trophy cards. Ties: the first tied player in clockwise order starting from the player whose turn is next.
3. **Resolve.** The storm island floods: the storm player is its trigger player and resolves Phase 2 steps 1-5 exactly as for a normal flood (including salvage and the quarter turn). The storm island need not be full.
4. Set the calm count to 0. Then play passes to the next player clockwise, who takes a normal turn.

Otherwise, play passes to the next player clockwise.

## 5. Special rules and timing

- **Claiming.** When an island falls off, or is scored in the final tide, the player with the most pawns on it claims it and puts it face down in their **trophy pile**.
  - **Tie for most pawns:** among the tied players, the one with the **fewest trophy cards at that moment** claims it. If two or more tied players also have equal pile sizes, nobody claims it; remove it from the game face up. This applies during play and during the final tide.
  - **No pawns at all:** during a flood or storm, the trigger player claims it (salvage). In the final tide, an empty island is not claimed by anyone; remove it from the game.
- **Trophy piles.** You may look at your own trophies at any time. The **number** of cards in each pile is public; their values are not. You may not look at, or ask about, other players' trophies.
- **Only one flood per turn.** A flood or storm cannot cause another flood: sliding and refilling never add pawns. A storm happens only in Phase 3, never in the same turn as a normal flood.
- **Turning cards.** Only the flooded (or storm) island turns, and only if it is still in the grid. Islands that slide keep their orientation. Every card entering the grid enters upright with its printed axis.
- **Re-flooding.** A flooded island that stays in the grid is full. If a pawn Sails out and a pawn then arrives (by Land or Sail) to bring it back to capacity, it floods again. The same island may flood many times (see the worked example).
- **Empty deck.** When the deck is empty, the face-up next island is still placed normally at the next refill. Only when a refill is needed and no next island exists does the game end.
- **Calm count.** Opening pawns do not count. Every turn without a flood (Land, Sail or pass) adds exactly 1. Floods and storms reset it to 0.

### Worked example (2 players: Red first, Blue second)

Grid (spaces 1-9), each card upright unless noted. Pawns in brackets. Next island: Tern Spit (1 / cap 2 / Row).

| | Left | Middle | Right |
|---|---|---|---|
| Top | Gull Rock 1/2 R [ ] | Pearl Reef 3/3 C [ ] | Kelp Bank 1/2 C [ ] |
| Middle | Reed Marsh 2/3 C [ ] | Crown Island 4/4 R [Red, Red, Blue] | Amber Cay 2/2 R [Blue] |
| Bottom | Salt Flat 1/2 R [ ] | Whale Rest 3/3 R [ ] | Fire Peak 3/4 C [ ] |

Red has 2 pawns in supply, Blue has 2. Neither has trophies.

**Flood 1.** Red Lands on Crown Island: 4 pawns = capacity 4, so it floods and Red is the trigger player. Its axis is Row, so the line is the middle row and Red chooses left or right.
- *Right:* Amber Cay falls off. Blue has the only pawn, so Blue claims it (2 points) and that pawn returns to Blue. Reed Marsh and Crown slide right; Tern Spit enters at middle-left.
- *Left:* Reed Marsh falls off. It is empty, so Red salvages it (2 points). Crown and Amber Cay slide left; Tern Spit enters at middle-right.

Red chooses **left**. Crown Island is now in middle-left with [Red x3, Blue] and gets a quarter turn: its axis is now **Column**. It is full. The new next island is turned up: Shell Beach (2 / cap 3 / Column). Calm count is 0.

**Blue's turn.** Crown is full, so nobody can Land there. Blue Sails his pawn from Crown down to Salt Flat (adjacent, not full). Crown is now [Red x3] with capacity 4, so it is no longer full. Salt Flat has 1 of 2 pawns: no flood. Calm count 1.

**Flood 2.** Red Lands her last pawn on Crown: 4 = capacity, it floods again. Its axis is now Column, so the line is the left column: Gull Rock (top), Crown (middle), Salt Flat (bottom).
- *Up:* Gull Rock falls off; empty, so Red salvages it (1 point).
- *Down:* Salt Flat falls off; Blue claims it (1 point) and his pawn returns.

Red chooses **up**. Crown and Salt Flat slide up; Shell Beach enters at bottom-left. Crown turns back to **Row**. Red now has all 4 pawns on Crown and an empty supply, so on her next turn she must Sail. If she Sails one off, Blue can Land on Crown to flood it a third time; then Blue picks the direction along the top row, and pushing **left** drops Crown off the grid for Red to claim (4 points, Red has 3 pawns to Blue's 1), while pushing **right** drops Kelp Bank instead.

**Storm (illustration).** If 6 turns passed in a 2-player game with no flood, a storm strikes. The island with the fewest open spaces floods (for example a capacity-3 island holding 2 pawns, 1 open space, beats any island with 2 open spaces). The player with fewer trophy cards picks its direction, then the next player takes a normal turn.

## 6. End of game and scoring

1. **Trigger:** the game ends at the end of a flood (normal or storm) in which an empty space could not be refilled because there was no next island. There is no other way for the game to end.
2. **Final tide:** score each island still in the grid one at a time in reading order (space 1 to space 9, skipping the empty space) using the Claiming rules. Each claimed island goes into its claimer's pile at once, so the pile sizes used for the fewest-trophies tiebreak change as the final tide goes on. Empty islands are not claimed.
3. **Score:** everyone reveals their trophy pile. Your score is the total value of your trophies.
4. **Tiebreakers:** (a) the most trophy cards; (b) the fewest of your pawns that were on the grid when the game ended (counted before the final tide); (c) if still tied, the tied players share the win.

## 7. Design notes

**Core tension.** Every Land pushes an island toward its flood. Filling an island gives you, the trigger player, a binary choice: let the full island fall off now (scoring it to its majority holder), or push the far end of the line off instead and keep the full island in place, turned to its new axis, as a locked prize for later. Players fight over majorities but must also watch which lines are dangerous: an island two columns away can be shoved off by a flood you never touched. Sailing lets you rescue pawns or contest a neighbour but adds no new presence.

**The twist (originality).** The trigger is crowding: islands move because players fill them, and the overcrowded island decides which line moves while the trigger player decides which end falls. Then the island turns a quarter, so the same island next pushes the other axis. Everything is visible (capacity, axis, next island), so it is fully tactical. This differs from the close comparables:
- *Shifting Stones* manipulates tiles by playing cards for secret pattern goals; Nine Fields has no hands and no patterns, and grid movement is the scoring trigger for open majority control.
- *Contactics* is static-board 3x3 area control; *Collapsi* shifts rows and columns as movement. In Nine Fields, falling off the edge is the only way an island scores mid-game, so a shift means "cash in this island now," and the grid is a conveyor feeding new islands from the deck.
- *Kahuna* shares the "few pieces fighting over island majorities" feel, but its islands never move.

**The storm (revision 1).** In v1 a leader could refuse to trigger floods until the stall limit ended the game early. Now stalling only hands a free flood to whoever has the fewest trophies: the trailing player gets the direction choice (and any salvage) on the most crowded island. Stalling is no longer a way to protect a lead, so players should keep flooding on their own terms, and the deck always runs out, so every game has the same number of floods.

**Kingmaking at 3-4 players.** Three rules keep the trigger choice self-serving rather than "pick which opponent wins":
1. **Salvage:** an empty island that falls goes to the trigger player, and new islands always enter empty at a line's end, so most floods offer at least one option that pays you.
2. **Hidden values:** only pile sizes are public, so near the end nobody can be sure who is leading, and deliberate kingmaking is a guess. Three unseen cards removed at setup (3-4 players) add to this uncertainty.
3. **Fewest-trophies tiebreak:** tied majorities go to whoever has claimed least, so piling onto the leader's island often hands it to a trailing player rather than the leader.

**Catch-up and closeness.** The fewest-trophies tiebreak and the storm player rule are the brakes on a runaway leader. Pawns return only when their island falls, so a player who wins many islands keeps re-deploying while a player with pawns locked on a full island is temporarily short. Final tide scoring keeps the last few floods tense, and the next-island card lets players plan the endgame.

**Seat balance.** Opening pawns are placed in reverse turn order, so later seats pick the best opening islands to offset the first player's tempo. The final tiebreakers are now seat-neutral.

**Expected length (for the playtester to verify).** 2 players: 21 refills plus the final flood = 22 floods every game (v1 averaged 14.5), at roughly 2.3-2.6 turns per flood, so about 50-57 turns and 19-21 minutes. 3-4 players: 18 refills plus the final flood = 19 floods (v1: 21.4-22.0), so about 47-48 turns and about 19.5-20 minutes. Levers if the length is off: number of cards removed at setup, or the storm threshold (3 x players).

**Bot notes.** All randomness is in the initial shuffle (and the 3 cards removed at 3-4 players, which come from that shuffle). Decisions per turn: action (Land on up to 9 islands, or Sail up to 4 x 4 targets) and, on a flood or storm, 1 of 2 directions. The storm island and storm player are fully determined by Phase 3 steps 1-2. A greedy bot can value a direction by the claimed island's value to itself minus its value to the current points leader.

## 8. Changelog

- v1 (2026-10-04): first version from the brief.
- v2 (revision 1): storm replaces the stall-limit ending; neutral final tiebreak; 3 cards removed at 3-4 players; six rules gaps closed; worked example added.

### Revision notes (revision 1)

| # | Change | Feedback it answers | KPI target |
|---|---|---|---|
| 1 | **Storm replaces the stall limit** (Phase 3). After 3 x players calm turns, the island with the fewest open spaces floods and the player with the fewest trophies resolves it. The game now ends only when the deck runs out. | Critique required change 1; playtest problem 1 (58% of 2p games ended on stall; narrated 3p game stalled turns 12-19). | 2p stall-ends 58% to 0%; 2p lead changes 1.77 to 2 or more; 2p early-leader wins 68.7% to 65% or less; 2p length sd below 17.6 turns; seat gap stays 5 or less at all counts. Giving the storm to the fewest-trophies player (not simply the next player, as the critique suggested) is aimed directly at the runaway rate, because experiment 2 showed that merely prolonging 2p play leaves it at 69.4%. |
| 2 | **Neutral final tiebreak:** most trophies, then fewest pawns on the grid at the end, then a shared win. "Later seat wins" removed. | Critique required change 2; playtest problem 2. | Seat gap 5 or less at every count; no game decided by seat order. |
| 3 | **Six rules gaps closed:** (1) a flooded island that falls off does not turn (Phase 2 step 5, Section 5); (2) the calm count is defined exactly and the storm strikes at the end of the turn that reaches 3 x players (Phase 3, Section 5); (3) final tide scores in reading order with piles updating as it goes (Section 6 step 2); (4) tied players with equal pile sizes: nobody claims, during play and in the final tide (Section 5); (5) worked example with Crown Island flooding twice, plus a storm illustration (Section 5); (6) one-line definition of full against flood, and a full island can never be Landed or Sailed onto (Phase 1). Also: fall-off end defined, passes count as turns, re-flooding explained, opening pawns are not turns. | Critique required change 3; playtest "Rule ambiguities found" list. | Zero rule ambiguities at pitch; clarity score up from 3. |
| 4 | **3-4 players remove 3 unseen cards at setup** (19 floods instead of 22). 2 players keep the full deck. | Critique required change 4; playtest problem 3 (3p 22.2, 4p 22.6 minutes; the storm adds about 5% more full-length games at 3p). | 3-4p length 22 minutes or less, ideally about 20. 3-4p lead changes stay 2 or more (v1: 3.37-3.69) and early-leader wins stay 65% or less (v1: 43-54%). If the playtest shows the full deck already under 22 minutes at 3-4p with the storm, drop this step. |
| 5 | Combined effect of 1-4: the 2p game passes its failed KPIs, the endings no longer feel arbitrary, and the rules are complete. The 3-4p core (actions, flood, claiming, opening) is unchanged. | Critique average 3.67, just above the bar. | Critic average 3.5 or more (aim: Balance 4, Rules clarity 4, Fun 3-4). |

Still recommended (not a rules change): a human test at 3 players to check the direction-choice kingmaking concern and whether people still stall when stalling hands the storm to the trailing player.
