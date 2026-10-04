# Nine Lives Dungeon - Rules (v1)

## 1. Overview

- **Title:** Nine Lives Dungeon
- **Hook:** A cat with nine lives creeps into a cellar that holds the same nine creatures every night, from a Moth to the Hound. You always know *what* is down there, never *where*. Each run you shove creatures back into the dark to rearrange the dungeon, fight your way up from mice to the Hound, and escape. Each time you die, the creature that killed you becomes a Ghost: a lesson the cat keeps for later runs. The nine cards are the cat's nine lives.
- **Players:** 1 (solo only)
- **Play time:** about 10 minutes per run; a full session (two escapes) is about 30-40 minutes
- **Age:** 12+
- **Complexity:** 2 / 5

## 2. Components

10 poker-size cards and one tuckbox. You also need a pencil (or any scrap of paper) for the lives tally.

**Nine Dungeon cards.** Each card shows its number (= its Danger), its name, its Room text (applies while it is in the dungeon grid), its Trophy text (applies once you have beaten it) and its Ghost line. All nine cards share one common back.

| # | Name | Danger | Room text (while in the grid) | Trophy text (in your pack) | As a Ghost |
|---|---|---|---|---|---|
| 1 | Moth | 1 | - | **Glow** (spend): look at up to 2 Dark cards, one at a time, and leave them face down where they are. | Danger 0 |
| 2 | Mouse | 2 | - | **Dart** (spend, before you Fight): the card you Fight this turn has Danger -3 (minimum 0). | Danger 0 |
| 3 | Spider | 3 | - | **Silk** (spend, before you Shove): the card you Shove this turn does not become Angry. | Danger 0 |
| 4 | Rat | 4 | - | **Scavenge** (spend): Ready up to 2 of your *other* Spent trophies. | Danger 0 |
| 5 | Crow | 5 | **Thief:** when the Crow becomes Lit, spend 1 Ready trophy (if you have any). | **Carry** (spend): swap the positions of any two cards in the grid; then apply the Lighting rule. | Danger 0, no Thief |
| 6 | Owl | 6 | - | **Wise** (no spend effect): while the Owl is Ready, your Claws are 2 higher. | Danger 0 |
| 7 | Snake | 7 | - | **Hypnotise** (spend, before you Fight): the card you Fight this turn has Danger at most 4. | Danger 0 |
| 8 | Fox | 8 | - | **Feint** (spend, before you Fight): this Fight causes no wounds. | Danger 0 |
| 9 | Hound | 9 | **Hunt:** at the end of each of your turns, if the Hound is Lit, spend 1 Ready trophy (if you have any). | **Beat the Hound to escape** (the run is won at once). | Danger 7, no Hunt |

**One Cat card** (not part of the dungeon; it is never shuffled in).
- *Front:* the turn summary (section 4), the Claws and wounds formulas, the three special rules (section 5) and the session ladder (section 6).
- *Back:* the **lives tally**: nine boxes labelled 1 Moth, 2 Mouse, 3 Spider, 4 Rat, 5 Crow, 6 Owl, 7 Snake, 8 Fox, 9 Hound; and two **escape** boxes. Mark them in pencil and erase them when a new session starts.

**Card states.** In the grid a card is **Lit** (face up) or **Dark** (face down), and **Angry** (turned sideways) or calm (upright). In your pack a trophy is **Ready** (upright) or **Spent** (turned sideways). "Spend a trophy" always means: turn one of your Ready trophies sideways (you choose which, unless a rule says otherwise).

## 3. Setup

Setup for a run (under 30 seconds):
1. Shuffle the nine Dungeon cards face down. (Simulation: a uniformly random permutation of cards 1-9.)
2. Deal them face down into a 3 x 3 grid in reading order: top row left to right, then the middle row, then the bottom row. The top row is the **doorway**. (Simulation: grid position i = 0..8 is row i div 3, column i mod 3; the deal is the permutation in that order.)
3. Turn the three doorway cards face up. They are Lit.
4. **The Hound sleeps deep:** if the Hound is in the doorway, swap it with the card at the bottom of the same column: the Hound goes face down into the bottom row, and that card comes up face up into the doorway. (You know where the Hound is this run.)
5. Your pack is empty. Thief does not trigger during setup.

Before the first run of a session, erase the lives tally and both escape boxes. The cards marked on the lives tally are **Ghosts** (special rule 3).

## 4. Turn structure

**Your Claws** = 2 + the number of your **Ready** trophies, + 2 more if the Owl is Ready. Spent trophies do not count.

A turn has three phases, always in this order.

### Phase 1 - Tricks (optional)
Use any number of Trophy tricks, one at a time, each fully resolved before the next. To use a trick, the trophy must be Ready; using it spends it. Each trick may be used at most once per turn. Wise (Owl) is always on while the Owl is Ready and is never "used".
- **Glow, Scavenge, Carry** take effect at once.
- **Dart, Hypnotise, Feint** apply to the Fight you make in Phase 2 this turn; **Silk** applies to the Shove you make in Phase 2 this turn. If you take the other action, the trick is wasted (it stays Spent).

### Phase 2 - Action (exactly one)

**Action A - Fight.** Choose any one Lit card in the grid and resolve in this order:
1. **Danger:** start with the card's Danger (its Ghost Danger if it is a Ghost). Add 2 if it is Angry. Subtract 3 if you used Dart this turn. Minimum 0. Then, if you used Hypnotise this turn, lower it to 4 if it is above 4.
2. **Claws:** 2 + your Ready trophies (+2 if the Owl is Ready), counted now (after Phase 1).
3. **Wounds** = Danger minus Claws, minimum 0. If you used Feint this turn, wounds are 0.
4. If the wounds are **more than your Ready trophies**, the cat **dies** (section 5, Death). The run is lost. This card is the killer.
5. Otherwise spend one Ready trophy per wound (your choice which; the Owl may be spent).
6. If the card is the Hound, the cat **escapes**: the run is won. Stop here.
7. Put the card into your pack, Ready (upright). Its grid space is now **empty** and stays empty for the rest of the run.
8. Apply the **Lighting rule** (special rule 1): every Dark card orthogonally next to the new empty space turns face up. If the Crow (not a Ghost) turned face up, resolve Thief.

**Action B - Shove.** Legal only if the grid holds a Lit card that is **not Angry** and at least one Dark card.
1. Choose a Lit, calm card X and any Dark card Y (Y may be Angry).
2. Swap their positions. Y turns face up in X's old space (it keeps its Angry state). X turns face down in Y's old space.
3. X becomes **Angry** (special rule 2): place it sideways. Exception: not if you used Silk this turn.
4. If Y is the Crow (not a Ghost), resolve Thief.

There is no pass. A Fight is always legal, because the grid always holds at least one Lit card until the Hound is beaten (the doorway spaces are always either Lit or empty, and every card next to an empty space is Lit).

### Phase 3 - Hunt
If the Hound is in the grid, Lit, and not a Ghost: spend 1 Ready trophy (your choice). If you have none, nothing happens. Then the next turn begins.

### Every legal action, summarised
| Action / trick | When legal | Choices |
|---|---|---|
| Fight | Always (any Lit card) | Which Lit card; which trophies pay the wounds |
| Shove | A Lit calm card and a Dark card exist | Which Lit calm card; which Dark card |
| Glow (Moth) | Moth Ready, Phase 1 | Up to 2 Dark cards, chosen one at a time |
| Dart (Mouse) | Mouse Ready, Phase 1 | None |
| Silk (Spider) | Spider Ready, Phase 1 | None |
| Scavenge (Rat) | Rat Ready, Phase 1 | Which Spent trophies (up to 2, not the Rat) |
| Carry (Crow) | Crow Ready, Phase 1, at least 2 cards in the grid | Which two grid cards |
| Hypnotise (Snake) | Snake Ready, Phase 1 | None |
| Feint (Fox) | Fox Ready, Phase 1 | None |
| Spend (Thief, Hunt, wounds) | Forced | Which Ready trophy |

## 5. Special rules and timing

The game has exactly three special rules:
1. **Lighting.** A grid card is Lit (face up) if it is in the doorway (top row) or orthogonally next to an empty space; every other grid card is Dark (face down). Check this whenever a space empties or cards swap, and turn cards to match. A card turned face down this way keeps its Angry state.
2. **Anger.** A Shoved card becomes Angry: +2 Danger until it is beaten. An Angry card can never be Shoved again (it can still be moved by Carry). A beaten card goes to your pack upright and is no longer Angry.
3. **Ghosts (nine lives).** A card ticked on the lives tally is a Ghost for the rest of the session. A Ghost uses its Ghost Danger (0, or 7 for the Hound) and ignores its Room text (no Thief, no Hunt). Its Trophy trick works normally.

**Death.** The cat dies when a Fight's wounds are more than its Ready trophies. The run ends at once and is lost. On the lives tally, tick the box of the card that killed you. If that box is already ticked (a Ghost Hound can kill), tick the lowest-numbered unticked box instead. Every death ticks exactly one box, so the number of ticks is the number of lives lost.

**Timing and edge cases.**
- **Order inside a Fight** is fixed: Danger, Claws, wounds, death check, pay, escape check, to pack, Lighting, Thief.
- **Claws are counted once,** at Fight step 2. Spending trophies to pay wounds (including the Owl) does not change that Fight's wounds.
- **Several cards lit at once:** turn them all face up together, then resolve Thief if the Crow was among them. Thief resolves once per time the Crow turns face up.
- **The Hound turning face up** (by Lighting or as the Y card of a Shove) has no immediate effect; Hunt checks only in Phase 3.
- **Escape beats everything:** beating the Hound ends the run before Lighting, Thief or Hunt.
- **Spending with nothing Ready:** Thief and Hunt do nothing; only wounds can kill.
- **Glow with fewer than 2 Dark cards:** look at those there are. Looking never changes a card's state.
- **Memory:** you may remember everything you have seen (including Dark cards you Shoved or Glowed) and deduce Dark cards by elimination, since all nine cards are always in play. You may not look at Dark cards except with Glow.
- **Carry** swaps any two grid cards (Lit or Dark, Angry or calm); each keeps its Angry state; then apply Lighting. Carry never makes a card Angry. (The Crow is in your pack when you Carry, so Carry can never trigger Thief.)
- **Run length is bounded:** each Fight removes a card and each normal Shove angers a calm card, and Silk can be used at most twice (once, plus once more if Scavenge readies the Spider). A run always ends within 20 turns.
- **No simultaneous choices:** everything resolves one step at a time in the order written.

## 6. End of game and scoring

**A run** ends when you escape (beat the Hound: **won**) or the cat dies (**lost**). After a won run, tick one escape box. After a lost run, tick a lives box (section 5, Death). Then set up the next run with all nine cards; the ticks stay.

**A session** ends when you tick your **second escape box** (session won) or your **ninth lives box** (session lost). Your **session score** is the number of unticked lives boxes when the session ends (0 if lost).

| Session score (lives left) | Title |
|---|---|
| 9 | Top Cat |
| 7-8 | Shadow Prowler |
| 5-6 | Cellar Cat |
| 3-4 | Scruffy Survivor |
| 1-2 | Last Whisker |
| 0 (session lost) | Ninth Life Spent |

There are no ties to break; compare sessions by score, then by fewer runs played.

**Quick play:** a single run is a complete 10-minute game: escape to win, die to lose. Keep any ticks for your next session or erase them.

## 7. Design notes

**The twist: a known dungeon in an unknown order.** The nine creatures are the same every run, so the game is never about *what* you meet, only *where*: a permutation puzzle with hidden positions. The cat's main tool rearranges the dark itself: a Shove pushes a creature you are not ready for back into the dark and drags an unknown one into the light, at the price of that creature coming back Angry. Lighting spreads from every room you clear, so each Fight is also a reveal: clear the Rat and you might wake the Hound next door. Because the composition is fixed, every reveal narrows down the rest, and a careful player can deduce where the Hound sleeps. The nine cards are also the nine lives: each death writes its lesson onto the dungeon as a Ghost, so a loss changes the next run instead of just ending.

**One number does three jobs.** Ready trophies are your Claws, your armour (they pay wounds) and your tricks. Every spend makes you weaker for the next fight. Peeking with the Moth, paying the Crow, feeding the Hound and taking a wound all come out of the same small pool, so every turn asks: grow, look, hide, or strike?

**Every card matters every run.**
- *Low cards (Moth, Mouse, Spider)* are your way in: at Claws 2 you can only Fight cleanly at Danger 1-2, so the first turn is "fight the Moth or Mouse if you can see it, or Shove to find one". Their tricks are cheap early tools: information, a small cut, a safe Shove.
- *Middle cards (Rat, Crow, Owl)* are the economy: Scavenge refunds spends, Thief taxes you when the Crow appears, Carry is a free rearrangement, and Wise rewards keeping the Owl unspent.
- *High cards (Snake, Fox)* are push-your-luck prizes: beating them costs wounds, but Hypnotise or Feint turns the Hound fight from "needs 4 Ready" into "needs 1-2 Ready".
- *The Hound* is the goal and the clock: while it is Lit it eats a Ready trophy every turn, which freezes your growth. Hide it (Shove, but then it is Angry at 11), race it, or come back with a Snake or Fox.

**Strategies to expect.** (1) *Straight climb:* clean Fights in rising order to 4 Ready, then the Hound (Danger 9 against Claws 6 is 3 wounds). (2) *Gambit:* take wounds to beat the Snake or Fox mid-run, then strike the Hound cheaply. (3) *Hide and seek:* Glow and deduction to locate the Hound, clear rooms away from it, Shove it deep if it lights too early. (4) *Owl tank:* keep the Owl Ready for +2 Claws and pay with everything else.

**Catch-up and tension.** Deaths make the next run easier: the killer (usually the Hound or a creature fought in desperation) becomes a Ghost: a free trophy, or a Hound with Danger 7 that never hunts. Escapes do not make the dungeon easier, so the session gets kinder only as you lose lives, and the score is the lives you keep. The Hound's Hunt keeps the end of a run tense: it is often Lit before you are ready.

**Intended variety targets (replace seat balance and lead changes; the playtester measures these).**
- Strategic bot, no Ghosts, over all 362,880 layouts: run win rate **40-60%** (brief band 35-65%). Random bot at least **20 points lower**.
- **Several routes to escape:** among strategic wins, at least 10% use Feint, at least 10% use Hypnotise, and at least 25% use neither.
- **No forced opening:** the strategic bot's first action is a Shove in 20-60% of layouts (about 36% of layouts have no Moth or Mouse in the doorway).
- **Killers vary:** the Hound causes 40-75% of deaths, and at least 4 different cards each cause at least 5% of deaths.
- **Zero dead cards:** each non-Hound card is beaten, Shoved, or forces a spend (Thief) in at least 25% of runs; each trick is used in at least 15% of runs in which it is Ready at some point; Wise changes a Fight's wounds in at least 15% of runs where the Owl is Ready.
- **Length:** median run of 7-12 turns. Time model: 30 seconds setup, 50 seconds per turn (a hidden-information puzzle), 15 seconds per trick used, 15 seconds for the tally after a run; target 8-12 minutes per run.
- **Carry-over:** a single Ghost raises the next run's win rate by 5-25 points on average (the Hound Ghost will be the biggest); sessions average 3-4 runs; no session score holds more than 40% of sessions.

**Tuning knobs for the playtester** (change one at a time, in this order): base Claws (2; try 1 or 3); Anger bonus (+2; try +1 or +3); Hunt (soft drain as written; try "only if not fought this turn" or lethal "if you have none, the cat dies"); Hypnotise cap (4; try 3 or 5); Dart (-3; try -2); Ghost Hound Danger (7; try 6 or 8); escapes per session (2; try 3 if runs come out under 8 minutes); the setup Hound swap (on; try off).

**Simulation notes.**
- *Layouts:* a run is fully determined by the deal permutation, the Ghost set and the player's choices. Index layouts by the lexicographic rank of the permutation (0 to 362,879). Run the strategic bot exhaustively for the empty Ghost set and for each of the 9 single-Ghost sets (3.6 million runs); simulate sessions (for example 20,000) with uniformly random deals for each run.
- *Random bot:* seed its RNG with the layout index. Each turn, for each Ready trick in card-number order, use it with probability 1/2 (uniform random legal targets); then choose uniformly among all legal actions (each Fight target, each Shove pair); pay wounds and spends with uniformly random Ready trophies.
- *Strategic bot (outline; the playtester may improve it, but it must be deterministic):*
  1. *Knowledge:* track every card seen and every swap; deduce a Dark card when only one identity is unaccounted for.
  2. *Strike:* if the Hound is Lit, find the cheapest set of tricks (fewest spends; Scavenge first if it helps) that makes the Hound Fight survivable; if one exists, use it and Fight the Hound.
  3. *Hide:* if the Hound is Lit, calm, cannot be struck this turn, and you have fewer than 3 Ready trophies: Shove it (with Silk if Ready) into the Dark space farthest (orthogonal steps) from every empty space and from the doorway; ties: highest grid index. If it is Angry, Carry it there if the Crow is Ready.
  4. *Look:* if the Moth is Ready, the Hound's position is unknown, you have at least 2 Ready trophies and at least 3 unknown Dark cards, Glow the unknown Dark cards that the planned Fight would light (else the lowest-index unknown ones).
  5. *Grow:* among Lit non-Hound cards with 0 wounds, Fight the one that does not light a space known to hold the Hound (unless you would then have 4+ Ready); then prefer the one lighting fewer unknown Dark cards while the Hound is unknown; then the higher Danger; then the lower grid index.
  6. *Push:* if no clean Fight exists, take the Fight (optionally with Dart) that leaves you at least 1 Ready with the smallest net loss; a Snake or Fox Fight counts its trick as worth 2.
  7. *Shove:* otherwise Shove the highest-Danger Lit calm card (Silk if Ready) to the space defined in step 3.
  8. *Forced:* if only fatal Fights remain, Fight the Hound if Lit, else the Lit card with the highest number (its Ghost helps most next run).
  - *Spending order* (wounds, Thief, Hunt): Moth, Spider, Crow, Mouse, Rat, Snake, Owl, Fox (first Ready one in this list; skip the Rat while you have 2+ Spent others). Use Scavenge when you have 2 Spent others, or 1 if it makes a strike possible.
- *Greedy baseline bot* (for comparison): Fight the lowest-Danger Lit card that you can survive; if none, Shove the highest-Danger Lit calm card into the lowest-index Dark space; never use tricks.

## 8. Changelog

**v1 (first design).** No revisions yet.
