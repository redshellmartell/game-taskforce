# Dead Reckoning - Rules (v1)

## 1. Overview

- **Title:** Dead Reckoning
- **Hook:** Two submarines hunt for salvage in a fog bank. Each round both captains secretly lay down three helm orders and the two courses run at the same moment, step by step. You always know where your rival is and exactly which orders they still hold. You never know which ones they will play, or in what order. Orders you play stay face up on the table for a round while your crew recovers, so every course you take tells your rival what you **can't** do next.
- **Players:** 2
- **Play time:** about 15 minutes (8-10 rounds)
- **Age:** 10+
- **Complexity:** 2 / 5

## 2. Components

- **25 grid cards:** 23 Sea cards (same back) and 2 Harbour cards (different back, always face up).
- **18 Helm cards:** 9 Blue (Player 1) and 9 Red (Player 2).
- **2 submarine tokens:** 1 Blue, 1 Red (coins work too).
- **Pencil and paper** to tally rounds (nothing else is written down).

### Grid cards

| ID | Card | Count | Effect when a sub enters it (see section 4, step D) |
|---|---|---|---|
| S01-S05 | Salvage 1 | 5 | Take the card into your score pile: worth 1 point. The square becomes open water. |
| S06-S10 | Salvage 2 | 5 | Same, worth 2 points. |
| S11-S13 | Salvage 3 | 3 | Same, worth 3 points. |
| S14-S17 | Mine | 4 | Remove the Mine from the game (the square becomes open water); your sub stays on the square. You lose your **lowest-value** Salvage card (it leaves the game; if you have none, you lose nothing). Your remaining steps this round are **cancelled**. |
| S18-S20 | Reef | 3 | Flip it face up and leave it on the grid for the rest of the game. Your sub **bounces**: it goes back to the square it started this step on. A face-up Reef can never be entered. |
| S21-S23 | Sonar | 3 | Take the card and keep it face up in front of you. Once, at the start of a later round, you may spend it to **ping** your rival (section 4, phase 1). Each unspent Sonar is worth 1 point at the end. The square becomes open water. |
| H1 | Blue Harbour | 1 | Player 1's start square. No effect when entered. While the **Blue** sub is on it, the Blue sub cannot be hit by torpedoes. |
| H2 | Red Harbour | 1 | Player 2's start square. Same, for the **Red** sub. |

Totals: 13 Salvage cards worth 24 points; 4 Mines; 3 Reefs; 3 Sonars; 2 Harbours.

**Open water** is any square whose card has been removed (an empty gap in the grid) or a Harbour. Subs may move through and stop on open water freely.

### Helm cards (each player has this identical set of 9 in their colour)

| Card | Count | Effect at its step |
|---|---|---|
| N (North) | 2 | Move 1 square north (towards row 5, Player 2's side) |
| E (East) | 2 | Move 1 square east (towards column E) |
| S (South) | 2 | Move 1 square south (towards row 1, Player 1's side) |
| W (West) | 2 | Move 1 square west (towards column A) |
| T (Torpedo) | 1 | Do not move; fire a torpedo (special rule 3) |

Directions are fixed to the grid, not to the players. Diagonal moves do not exist.

## 3. Setup

1. Name the squares: columns **A-E** from west to east, rows **1-5** from south to north. Player 1 (Blue) sits at the row-1 edge, Player 2 (Red) at the row-5 edge.
2. Place the Blue Harbour face up at **C1** and the Red Harbour face up at **C5**.
3. Shuffle the 23 Sea cards. Deal them face down, one per square, to the other 23 squares in this order: row 5 from A to E, then row 4, row 3, row 2, row 1 (skipping C5 and C1).
4. Put the Blue sub on C1 and the Red sub on C5.
5. Each player takes their 9 Helm cards into hand. Helm hands are open information (see special rule 1); you may keep them face up.
6. Write "Round 1" on the paper. Play 10 rounds at most.

## 4. Turn structure

The game is played in **rounds**. Both players act at once in every round. A round has four phases.

### Phase 1 - Ping (optional)
A player holding a Sonar may spend it now. The player with the **lower score** decides first (if scores are tied: Player 1 decides first in odd rounds, Player 2 in even rounds). If the first player pings, the second may not ping this round. If not, the second player may.
- **Ping:** remove the Sonar from the game. Your rival must do phase 2 first, alone: place their 3 Helm cards and then turn their **step-1** card face up. Only then do you place yours. The revealed card is locked in.

### Phase 2 - Plot
Each player chooses **exactly 3 Helm cards from their hand** and places them face down in a row in front of them: left card = step 1, middle = step 2, right = step 3. Without a ping, both players plot at the same time; when both have placed 3 cards, the plots are locked and cannot change.

### Phase 3 - Run the course
Resolve step 1, then step 2, then step 3. Each step runs A to E in order:

- **A. Reveal.** Both players turn their card for this step face up (if it is not already face up). A player whose steps were cancelled by a Mine still turns the card face up, but it has no effect.
- **B. Aim.** Work out each sub's **target** square:
  - Move card: the adjacent square in that direction. If that would be off the grid or is a face-up Reef, the target is the sub's **current** square (the sub is blocked and stays).
  - T card, or a cancelled step: the target is the current square.
- **C. Collision check (special rule 2).** If both targets are the same square, or each sub's target is the other sub's current square, the subs collide: **both** targets become their current squares. No card is entered.
- **D. Move and enter.** Each sub moves to its target. A sub that moved onto a new square **enters** it; apply that square's effect from the grid card table (face-down cards are flipped first; a face-up Salvage or Sonar card is simply taken). The two subs are always on different squares, so the two effects are independent; resolve Blue's first, then Red's, if it ever matters. Then:
  - **Reef bounce clash:** if a sub bounces off a Reef back onto the square the other sub has just moved onto, that other sub also goes back to the square it started this step on.
- **E. Fire (special rule 3).** Each player whose card this step is T (and not cancelled) fires a torpedo. If the rival sub is on any of the **8 squares surrounding** the firer's square (orthogonal or diagonal), and the rival is not on its own Harbour, it is **hit**: the firer takes the **highest-value** Salvage card from the rival's score pile into their own. If both fire and both hit, work out both stolen cards first, then swap them. A hit on a rival with no Salvage takes nothing.

### Phase 4 - Cooling and round end
1. Take back into your hand the Helm cards in your **Cooling row** (the ones you played last round).
2. Move the 3 cards you played this round, face up, into your Cooling row. They cannot be played next round.
3. Check the end of the game (section 6). If it has not ended, add 1 to the round tally and start the next round.

So in round 1 you choose from 9 cards; in every later round you choose from the 6 in your hand, and both players can see exactly which 6 those are.

### Every legal action, summarised
| Action | When legal | Choices |
|---|---|---|
| Ping | Phase 1, you hold a Sonar, your rival has not pinged this round | Ping or not |
| Plot | Phase 2, always | Any 3 cards from your hand, in any order (moves into edges or known Reefs are legal and simply leave you in place) |

There are no other actions. Players may not talk about their plots in a binding way; bluffing talk is allowed.

## 5. Special rules and timing

The game has exactly three special rules:
1. **Cooling helm.** Cards you play sit face up for one round and come back after it. Everyone can always see the full hand each player can plot from.
2. **Collisions.** Two subs never share a square. If they would end a step on the same square, or swap squares, neither moves that step.
3. **Torpedoes.** A T card fires after both subs move that step, hitting a rival on any of the 8 surrounding squares (unless it is on its own Harbour) and stealing its highest Salvage card.

Timing and edge cases:
- **Order inside a step** is fixed: reveal, aim, collision check, move and enter, Reef bounce clash, fire.
- **Collisions with hidden cards:** if both subs target the same face-down card, neither enters and it stays face down. A sub moving onto the square the rival is leaving is legal (it is not a collision unless the rival moves onto its square at the same time).
- **Blocked moves** (edge, face-up Reef, collision) still use up the Helm card.
- **Mines:** after a Mine, that player's later steps this round are cancelled; the rival's plan carries on as normal. A sub that hits a Mine can still be torpedoed in step E of that step or later steps.
- **Stealing and losing:** "highest" and "lowest" mean by value; between cards of equal value it does not matter which. Sonar cards can't be stolen or lost.
- **Public information:** sub positions, all face-up grid cards, score piles, Sonars held, both Helm hands and Cooling rows. The only hidden things are the face-down Sea cards (their remaining mix is always known by counting) and each player's plot until it is revealed.

## 6. End of game and scoring

**The game ends at the end of a round (phase 4, step 3) if either is true:**
- all 13 Salvage cards have left the grid (in score piles or lost to Mines); or
- round 10 has just been played.

Unentered cards left on the grid score nothing.

**Score:** the total value of the Salvage cards in your score pile, plus 1 for each unspent Sonar.

**Winner:** highest score. **Tiebreaker 1:** more Salvage cards in your score pile. **Tiebreaker 2:** more Salvage 3 cards. **Still tied:** a draw (count it as half a win for each player in simulations).

## 7. Design notes

**The twist: the cooling helm.** Plotting is simultaneous, but it is never blind. Both subs are always in plain sight, and the Cooling rows tell you exactly which six orders your rival can choose from. If they fired last round, they cannot fire now, so you can close in. If both their Norths are cooling, they can't come up the grid at you this round. The guessing is real (which three, in what order), but it is narrowed by facts on the table, so it rewards reading and planning two rounds ahead. Your own plot is always a trade-off: the orders you use now are the ones you won't have next round, and your rival sees them.

**Why each card matters.**
- *Salvage 1/2/3* is the score. The 3s are the target of every torpedo, so holding them makes you the hunted.
- *Mines* make entering fog risky, and they hurt most when you hold low cards you'd rather keep. Revealed squares are safe, so the explored part of the sea fills with predictable routes.
- *Reefs* waste a step when found and then shape the map for good, creating walls you can hide behind (you can't be followed through them) and corridors your rival must use.
- *Sonar* trades 1 point for forcing your rival to commit first and show step 1: the strongest reading tool, best used just before a hunt or a race for a revealed 3.
- *Harbours* are the only safe spot from torpedoes, so a leader can duck home. Doing so costs moves (on C1, only S into the edge or T keeps you still, and you hold just 3 such cards), and the cooling rule stops you doing it every round.
- *Torpedo* is the only attack. It costs a move, it must be aimed at where the rival **will** be, and once used it is off the table for a round, which tells your rival you can't fire.

**Catch-up and tension.** A hit steals the victim's best card, so it costs the leader the most and gives a trailer up to a 6-point swing in one step. The player behind decides first whether to ping. With 24 points on the grid and swings of 2-6 per hit, the lead should change hands, and the last rounds become a duel near the final Salvage.

**Strategies to expect.** (1) *Prospector:* explore fresh fog fast and accept Mine risk. (2) *Hunter:* stay one square from the rival with T in hand, ideally after they have just used their own T. (3) *Shadow:* take revealed Salvage behind your rival's exploration, keep T as a deterrent, and use Sonar to win races. No route is always right, because whatever you used last round is visible and missing.

**Distinct from Nine Fields.** Nine Fields is 2-4 players, alternating turns, area control with pawns and shifting rows. Dead Reckoning is a strict duel with simultaneous secret plots, no area control, and a grid that only gets revealed and emptied, never rearranged.

**Brief deviation:** plots are made with 9 Helm cards per player (within the 20-extra-card budget) instead of being written on paper. Cards make plots unambiguous and enforce the cooling rule without any writing. Paper is used only for the round tally.

**Length.** Plotting takes about 30-45 seconds and running the course about 30 seconds, so each round is about 75-90 seconds. Salvage usually runs out in rounds 8-10, so a game should take 12-15 minutes plus a 1-minute setup.

**Tuning knobs for the playtester** (change one at a time): torpedo range (8 surrounding squares vs. only the 4 orthogonal ones); what a hit steals (highest vs. lowest card); the Mine penalty (lose lowest card vs. only lose your steps); round cap (8-12); the number of Reefs (2-4) if movement feels too blocked; Harbour safety (on/off) if leaders turtle.

**Bot hints for simulation.**
- *State:* positions, grid (face-down / face-up type / empty), score piles, Sonars, hands, Cooling rows, round. Face-down cards are drawn uniformly at random from the unrevealed multiset when entered (this matches a shuffled deal).
- *Plans:* every ordered choice of 3 cards from hand, treating identical cards as identical (round 1: at most 9x8x7 orderings, later at most 120 distinct ones).
- *Strategic bot (one level of reading):* (a) score each rival plan by the rival's own greedy value (expected points gained minus points lost, using expected values for face-down cards); take the rival's top 10 plans as equally likely. (b) For each of its own plans, resolve it against each of those 10 with expected card values and average (own points change − rival points change), plus 0.3 per face-down card revealed safely and −0.5 if it ends a round orthogonally or diagonally next to a rival who will hold T next round. (c) Play the best plan. Ping when holding a Sonar and either a Salvage 3 is face up within 3 steps of both subs, or the rival is within 3 steps and the bot holds T.
- *Random bot:* chooses uniformly among distinct legal plans; pings with 50% chance when it may.
- *Checks worth logging:* win rate by seat, hits per game, rounds per game, lead changes (by score after each step), Mines triggered, rate at which the round cap ends the game, and how often a revealed Reef blocks a move.

## 8. Changelog

**v1 (first design).** No revisions yet.
