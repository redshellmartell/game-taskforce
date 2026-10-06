# Dead Reckoning - Rules (v2)

## 1. Overview

- **Title:** Dead Reckoning
- **Hook:** Two submarines hunt for salvage in a fog bank. Each round both captains secretly lay down three helm orders, and the two courses run at the same moment, step by step. You always know where your rival is and exactly which orders they still hold. You never know which ones they will play, or in what order. Orders you play stay face up for a round while your crew recovers, so every course you take tells your rival what you **can't** do next. The richest wrecks lie in the middle of the sea, right between you.
- **Players:** 2
- **Play time:** about 15 minutes (9-12 rounds)
- **Age:** 10+
- **Complexity:** 2 / 5

## 2. Components

- **25 grid cards:** 23 Sea cards (same back) and 2 Harbour cards (different back, always face up).
- **18 Helm cards:** 9 Blue (Player 1) and 9 Red (Player 2).
- **2 submarine tokens:** 1 Blue, 1 Red (coins work too).
- **Pencil and paper** for the round tally.

### Grid cards

Each Sea card shows a **zone mark** in one corner (B = Blue waters, M = Middle, R = Red waters), used only during setup.

| Card | Total | Blue waters (B) | Middle (M) | Red waters (R) | Effect when a sub enters it (section 4, step D) |
|---|---|---|---|---|---|
| Salvage 1 | 6 | 3 | 0 | 3 | Take the card into your score pile: worth 1 point. The square becomes open water. |
| Salvage 2 | 6 | 3 | 0 | 3 | Same, worth 2 points. |
| Salvage 3 | 3 | 0 | 3 | 0 | Same, worth 3 points. |
| Mine | 3 | 1 | 1 | 1 | Remove the Mine from the game (the square becomes open water); your sub stays on the square. You lose your **lowest-value** Salvage card (it leaves the game; if you have none, you lose nothing). Your remaining steps this round are **cancelled**. |
| Reef | 3 | 1 | 1 | 1 | Flip it face up and leave it on the grid for the rest of the game. Your sub **bounces**: it goes back to the square it started this step on. A face-up Reef can never be entered. |
| Sonar | 2 | 1 | 0 | 1 | Take the card and keep it face up in front of you. Later you may spend it to **ping** (section 4, phase 1). It is worth **0 points**. The square becomes open water. |
| **Total** | **23** | **9** | **5** | **9** | |
| Blue Harbour | 1 | - | - | - | Player 1's start square (C1). No effect when entered. While the **Blue** sub is on it, the Blue sub cannot be hit by torpedoes. |
| Red Harbour | 1 | - | - | - | Player 2's start square (C5). Same, for the **Red** sub. |

Salvage: 15 cards worth 27 points. Blue waters and Red waters hold **identical** sets of 9 cards (9 points each); the Middle holds all three Salvage 3 cards.

**Open water** is any square whose card has been removed (an empty gap in the grid) or a Harbour. Subs may move through and stop on open water freely. A square a sub is standing on is always open water.

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
3. Sort the 23 Sea cards by zone mark into three packets: **B** (9 cards), **M** (5 cards), **R** (9 cards). Shuffle each packet face down separately.
4. Deal face down, one card per square, in this order: packet R to row 5 from A to E (skipping C5), then row 4 from A to E; packet M to row 3 from A to E; packet B to row 2 from A to E, then row 1 from A to E (skipping C1).
5. Put the Blue sub on C1 and the Red sub on C5.
6. Each player takes their 9 Helm cards into hand, face up (Helm hands are open information).
7. Write "Round 1" on the paper. Play 12 rounds at most.

## 4. Turn structure

The game is played in **rounds**. Both players act at once in every round. A round has four phases.

**Score** at any moment means the total value of the Salvage cards in your score pile. Sonars are worth nothing.

### Phase 1 - Ping (optional)
Only a player whose score is **strictly lower** than their rival's, and who holds a Sonar, may ping. If scores are tied, nobody may ping. So at most one player can ping in a round.
- **Ping:** remove one of your Sonars from the game. Your rival plots first, alone: they place their 3 Helm cards (phase 2) and turn their **step-1 and step-2** cards face up. Those two cards are locked in. Their step-3 card stays face down. Only then do you plot.

### Phase 2 - Plot
Each player chooses **exactly 3 Helm cards from their hand** and places them face down in a row: left card = step 1, middle = step 2, right = step 3. Without a ping, both players plot at the same time; when both have placed 3 cards, the plots are locked and cannot change.

### Phase 3 - Run the course
Resolve step 1, then step 2, then step 3. Each step runs A to E in order:

- **A. Reveal.** Both players turn their card for this step face up (if it is not already). A cancelled step (after a Mine) is still turned face up, but has no effect.
- **B. Aim.** Work out each sub's **target** square:
  - Move card: the adjacent square in that direction. If that is off the grid or a face-up Reef, the target is the sub's **current** square (the sub is blocked).
  - T card, or a cancelled step: the target is the current square.
- **C. Collision check.** If both targets are the same square, or each sub's target is the other sub's current square, the subs collide: **both** targets become their current squares. Nothing is entered, and a face-down card at a shared target stays face down and unseen.
- **D. Move and enter.** Each sub moves to its target. A sub that moved onto a new square **enters** it and applies its effect from the grid card table (a face-down card is flipped face up first). The two subs are on different squares, so the two effects are independent.
  - **Reef bounce conflict:** if a sub bounces off a Reef and the square it bounces back to is now occupied by the other sub (which moved there this step), the other sub also returns to the square it started this step on. Neither sub gains anything from this, because both squares are open water.
- **E. Fire.** Each player whose card this step is T (and not cancelled) fires a torpedo. If the rival sub is on any of the **8 squares surrounding** the firer's square (orthogonal or diagonal) and is not on its own Harbour, it is **hit**: the firer takes the **highest-value** Salvage card from the rival's score pile into their own. If both fire and both hit, work out both stolen cards first, then swap them. A hit on a rival with no Salvage takes nothing.

### Phase 4 - Cooling and round end
1. Take back into your hand the Helm cards in your **Cooling row** (the ones you played last round).
2. Move all 3 cards you played this round, face up, into your Cooling row, including cards whose steps were cancelled or blocked. They cannot be played next round.
3. Check the end of the game (section 6). If it has not ended, add 1 to the round tally and start the next round.

So in round 1 you choose from 9 cards; in every later round you choose from the 6 in your hand, and both players can see exactly which 6 those are.

### Every legal action, summarised
| Action | When legal | Choices |
|---|---|---|
| Ping | Phase 1, you hold a Sonar and your score is strictly lower than your rival's | Ping or not |
| Plot | Phase 2, always | Any 3 cards from your hand, in any order (moves into edges or known Reefs are legal and leave you in place) |

There are no other actions. Talk about plots is never binding; bluffing talk is allowed.

## 5. Special rules and timing

Three special rules:
1. **Cooling helm.** Cards you play sit face up for one round and then come back. Everyone can always see the full hand each player can plot from.
2. **Collisions.** Two subs never share a square. If they would end a step on the same square, or swap squares, neither moves that step.
3. **Torpedoes.** A T card fires after both subs move that step, hitting a rival on any of the 8 surrounding squares (unless it is on its own Harbour) and stealing its highest Salvage card.

Card effects (Mine, Reef, Sonar, Harbour) are printed on the cards and in the table in section 2.

Timing and edge cases:
- **Order inside a step** is fixed: reveal, aim, collision check, move and enter (with Reef bounce conflict), fire.
- **Moving onto the square the rival is leaving** is legal; it is a collision only if the rival moves onto your square at the same step.
- **Blocked or cancelled moves** still use up the Helm card, and the card still goes to the Cooling row.
- **Mines:** after a Mine, that player's later steps this round are cancelled; the rival's plan carries on. A sub that hit a Mine can still be torpedoed in that step or later steps.
- **Stealing and losing:** "highest" and "lowest" mean by value; between equal values it does not matter which card. Sonars can't be stolen or lost.
- **Ping eligibility** is checked once, at the start of phase 1, using scores at that moment.
- **Public information:** sub positions, face-up grid cards, score piles, Sonars held, both Helm hands and Cooling rows. Hidden: face-down Sea cards (the remaining mix in each zone is always known by counting) and each plot until it is revealed.

## 6. End of game and scoring

**The game ends at the end of a round (phase 4, step 3) if either is true:**
- all 15 Salvage cards have left the grid (in score piles or lost to Mines); or
- round 12 has just been played.

Cards left on the grid score nothing.

**Score:** the total value of the Salvage cards in your score pile. Sonars score nothing.

**Winner:** highest score. **Tiebreaker 1:** more Salvage cards in your score pile at the end (after all thefts and losses). **Tiebreaker 2:** more Salvage 3 cards in your score pile. **Still tied:** a draw (half a win each in simulations).

## 7. Design notes

**The twist: the cooling helm.** Plotting is simultaneous but never blind. Both subs are always in plain sight, and the Cooling rows show exactly which six orders each player can choose from. If they fired last round, they cannot fire now, so you can close in. If both their Norths are cooling, they can't come up the grid at you. The guess (which three, in what order) is narrowed by facts on the table.

**What v2 changes in play.** Each player's home waters hold the same 9 cards, so the fog near home can't hand one player a lead the other can't also find; what you missed is still there. The three 3-point wrecks sit in the middle row, between the subs, so the big points are won where subs meet: where collisions, torpedoes and reading the rival's hand decide things. In round 1, both subs can reach C3 by step 2 (N, N from either harbour), and if both try they collide, so the first decision is already a guess about the rival.

**Comeback (L3).** Three things, all aimed at runaway leader at most 65% and at least 2 lead changes per game:
1. *Mirrored home waters.* Round 1 cannot decide the game by the deal: both halves hold equal value, so a lucky first round only means finding your share sooner.
2. *Trailer's Sonar.* Only the player behind can ping, and a ping shows two of the leader's three steps, which usually sets up a sure torpedo or wins a race to a middle wreck.
3. *Torpedo steals the highest card.* The leader usually holds the 3s, so a hit swings up to 6 points. The middle-row 3s put the subs within range more often.

**Twist and special-card ablation (L1).** Each must lose clearly to the full strategic bot:
| Feature | Ignore-it bot | Must win at most |
|---|---|---|
| Cooling helm | Strategic bot that assumes the rival may play any of their 9 cards | 45% (target 40%: reading worth 10+ points) |
| Sonar ping | Strategic bot that never pings | 45% |
| Torpedo | Strategic bot that never plots T | 45% |
| Middle-row wrecks | Strategic bot that never enters row 3 | 45% |
| Harbour safety | Camper (ends rounds on Harbour when leading) must **not** win more than 55% | 55% |
Config ablation for the zoned deal: rerun with the v1 single-shuffle deal (same cards); runaway rate should be clearly higher with it.

**Target bands and knobs (2 players only).** Seat gap at most 5 points (the layout and rules are mirror-symmetric and nothing resolves by seat; if a gap appears, suspect the bots first). Runaway leader at most 65% and lead changes at least 2 (knob: how many steps a ping reveals, 2 vs 3). Reading value 10+ points (knob: Helm hand size, adding a second T per player, staying within the 20-card budget). Length 12-18 minutes (knob: round cap 10-12).

**Skill gap (L6).** Good play wins on route efficiency through home waters, timing the move into the middle row, torpedo timing against the rival's visible hand, and saving Sonar for the round it guarantees a hit. Target strategic vs random gap at least 20 points (v1: 75).

**Termination and length.** Every round ends after 3 steps; the game ends when Salvage runs out or after round 12, so it always ends. Expect 10-12 rounds at about 85 seconds each (designer estimate, not measured): 14-17 minutes, inside 12-18.

**Rule budget (L7).** Three special rules plus four card effects; this file's teach sections (2-6) run about 100 lines. The brief's one-page promise is not met (see Known gaps).

**Strategies to expect.** *Prospector:* clear your home waters fast, accept the one Mine. *Raider:* go straight for the middle wrecks and fight there. *Hunter:* shadow the leader with T in hand, ideally after they used their own T. *Trailer:* hold a Sonar for the round the leader must cross open sea.

**Distinct from Nine Fields:** that is 2-4 players, alternating, area control on shifting rows; this is a simultaneous duel on a grid that is only revealed and emptied.

**Brief deviation:** plots are made with 9 Helm cards per player (within the 20-extra-card budget) instead of on paper; cards make plots unambiguous and enforce cooling. Paper is used only for the round tally.

**Bot hints for simulation.**
- *State:* positions, grid (face-down with zone / face-up type / empty), score piles, Sonars, hands, Cooling rows, round. A face-down card is drawn uniformly at random from the unrevealed cards **of its zone** when entered.
- *Plans:* every ordered choice of 3 cards from hand, identical cards treated as identical.
- *Bots (L2):* keep v1's greedy and strategic bots; add a deeper one if budget allows, and report the spread. Strategic ping rule: ping when allowed and either it holds T in hand and the rival is within 3 steps, or a middle-row square is face down or holds a face-up Salvage 3 within 3 steps of both subs.
- *Log:* seat win rate, hits, rounds, lead changes (by score after each step), pings, Mines, cap-end rate, collisions in round 1.

## 8. Changelog

**v2 (revision 1).** Fixes from `playtest-report.md` and `critique.md` (rev 0); no other changes.
- **Early fog luck decides games (runaway 0.79, lead changes 1.5; critique change 1):** Sea cards are dealt in three zones; Blue and Red waters hold identical sets, and all three Salvage 3 cards are in the middle row. Card mix changed: one Mine became a Salvage 1, one Sonar became a Salvage 2 (Mines 4 to 3, Sonars 3 to 2, Salvage 13 to 15, 24 to 27 points).
- **Comeback gap (critique change 2):** ping is now the trailer's tool only (strictly lower score); the middle-row wrecks bring subs into torpedo range more often. No new tokens or rules.
- **Sonar a dead card (E4 never-ping 50.0%; critique change 3):** a ping now reveals steps 1 **and** 2; only the trailer may ping; Sonar no longer scores 1 point.
- **Coasting on the round-10 cap (75% of games; critique change 4):** cap raised to 12 rounds; Salvage running out still ends the game.
- **Reading worth only ~5 points (E3; critique change 5):** no new mechanic; the contested middle row and the two-step ping put more of the game on reading the visible hand. Ablation target set at 45% or less for the cooling-blind bot.
- **The 6 ambiguities (playtest.json):** (1) Sonars are worth 0 and never count in score; (2) Reef bounce clash reworded as "Reef bounce conflict", stating the other sub returns and that both squares are open water; (3) cancelled and blocked cards cool like any played card; (4) a shared face-down target stays face down and unseen; (5) tiebreak counts the score pile at game end, after thefts and losses, Sonars excluded; (6) ping priority removed: only the strictly lower score may ping, nobody on a tie.

## Known gaps

- **One-page rules / at most 3 special rules (brief, L7):** not met; three special rules plus four card effects and about 100 lines of teach text.
- **Comeback and reading value are argued, not measured:** all v2 changes are untested; the runaway, lead-change and cooling-blind targets need the playtester's two-bot runs. The critic's stop rule applies (park if runaway stays above 0.70).
- **Creep in Silent (2021) similarity** (critique change 7) not checked: the designer has no search access.
- **Setup time:** sorting 23 cards by zone mark adds about a minute; total should stay under 2 minutes, unmeasured.
- **Family fit (panel 2.91)** not addressed by this revision.
- **Round length (85 s)** is still a designer estimate.
