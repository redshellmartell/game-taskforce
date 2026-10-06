# Whiskerdark - Rules (v2)

(Formerly "Nine Lives Dungeon"; renamed in v2, see Changelog.)

## 1. Overview

- **Title:** Whiskerdark
- **Hook:** A cat creeps into a cellar that holds the same nine creatures every night, from a Moth to the Hound. You always know *what* is down there, never *where*. Each run you shove creatures back into the dark to rearrange the cellar, fight your way up from moths to the Hound, and escape. Each time you die, the creature that killed you becomes a Ghost: weaker and easier next time, so a loss teaches the cat something. The cat has nine lives; the session is over when they are spent.
- **Players:** 1 (solo only)
- **Play time:** about 10 minutes per run; a full session (two escapes) is about 30-40 minutes
- **Age:** 12+
- **Complexity:** 2 / 5

## 2. Components

10 poker-size cards and one tuckbox. You also need a pencil for the lives tally.

**Nine Cellar cards.** Each card shows its number (= its Danger), its name, its Trophy text (applies once you have beaten it) and its Ghost line. All nine cards share one common back.

| # | Name | Danger | Trophy trick (in your pack) | As a Ghost |
|---|---|---|---|---|
| 1 | Moth | 1 | **Glow** (no spend; once per turn while the Moth is Ready): look at 1 Dark card and put it back face down where it was. | Danger 0; may **Drift** |
| 2 | Mouse | 2 | **Dart** (spend, before you Fight): the card you Fight this turn has Danger -3. | Danger 0; may **Drift** |
| 3 | Spider | 3 | **Silk** (spend): make one Shove at once, as a free extra action; the Shoved card does not become Angry. You still take your Phase 2 action. | Danger 1; may **Drift** |
| 4 | Rat | 4 | **Scavenge** (spend): Ready up to 2 of your *other* Spent trophies. | Danger 2 |
| 5 | Crow | 5 | **Carry** (spend, before you Fight): you may swap the positions of any two grid cards; then the card you Fight this turn has Danger -2. | Danger 3 |
| 6 | Owl | 6 | **Wise** (no spend): while the Owl is Ready, your Claws are 2 higher. | Danger 4 |
| 7 | Snake | 7 | **Hypnotise** (spend, before you Fight): the card you Fight this turn has Danger at most 4. | Danger 5 |
| 8 | Fox | 8 | **Feint** (spend, before you Fight): this Fight causes no wounds. | Danger 6 |
| 9 | Hound | 9 | **Beat the Hound to escape** (the run is won at once). While the Hound is Lit and not a Ghost, it **Hunts** (Phase 3). | Danger 7; does not Hunt |

Every Ghost's Danger is its printed Danger minus 2 (minimum 0). The three smallest Ghosts (Moth, Mouse, Spider) can also **Drift** (special rule 3).

**One Cat card** (not part of the cellar; never shuffled in).
- *Front:* the turn summary (section 4), the Claws and wounds formulas, the three special rules (section 5) and the session ladder (section 6).
- *Back:* the **lives tally**: nine boxes labelled 1 Moth, 2 Mouse, 3 Spider, 4 Rat, 5 Crow, 6 Owl, 7 Snake, 8 Fox, 9 Hound; and two **escape** boxes. Mark them in pencil; erase them when a new session starts.

**Card states.** In the grid a card is **Lit** (face up) or **Dark** (face down), and **Angry** (turned sideways) or calm (upright). In your pack a trophy is **Ready** (upright) or **Spent** (turned sideways). "Spend a trophy" always means: turn one of your Ready trophies sideways (you choose which, unless a rule says otherwise). A Spent trophy gives no Claws and its trick cannot be used.

## 3. Setup

Setup for a run (under 30 seconds):
1. Shuffle the nine Cellar cards face down. (Simulation: a uniformly random permutation of cards 1-9.)
2. Deal them face down into a 3 x 3 grid in reading order: top row left to right, then the middle row, then the bottom row. The top row is the **doorway**. (Simulation: grid position i = 0..8 is row i div 3, column i mod 3; the deal is the permutation in that order.)
3. Turn the three doorway cards face up. They are Lit.
4. **The Hound sleeps deep:** if the Hound is in the doorway, swap it with the card at the bottom of the same column: the Hound goes face down into the bottom row, and that card comes up face up into the doorway. **Only in this case** do you know where the Hound is at the start; otherwise you know only that it is in one of the six Dark spaces. (This applies to a Ghost Hound too.)
5. Your pack is empty.

Before the first run of a session, erase the lives tally and both escape boxes. Cards ticked on the lives tally are **Ghosts** (special rule 3).

## 4. Turn structure

**Your Claws** = 2 + the number of your **Ready** trophies, + 2 more if the Owl is Ready.

A turn has three phases, always in this order.

### Phase 1 - Tricks and Drift (optional)
Use any number of tricks, one at a time, each fully resolved before the next. To use a trick its trophy must be Ready. Each trick may be used **at most once per turn**, even if Scavenge readies its trophy again the same turn. Wise is always on while the Owl is Ready and is never "used".
- **Glow** does not spend the Moth: look at one Dark card. It stays Dark and keeps its state.
- **Scavenge** takes effect at once: turn up to 2 of your Spent trophies other than the Rat upright.
- **Silk** takes effect at once: spend the Spider and make one Shove (Action B, steps 1-2 and 4), except that the Shoved card X does **not** become Angry. Silk needs the same things as a Shove (a Lit calm card and a Dark card); if they do not exist, you cannot use Silk.
- **Dart, Carry, Hypnotise, Feint** apply to the Fight you make in Phase 2 this turn. If you Shove instead, they are wasted (they stay Spent). Carry's swap (if you make one) happens at once, when you use Carry; each swapped card keeps its Angry state, neither becomes Angry, then apply Lighting.
- **Drift** (only for a Ghost Moth, Ghost Mouse or Ghost Spider that is Lit in the grid): take that card into your pack, Ready. Its space becomes empty; apply Lighting. Drift is not a trick and costs nothing; you may Drift each such Ghost when it is Lit.

### Phase 2 - Action (exactly one)

**Action A - Fight.** Choose any one Lit card in the grid and resolve in this order:
1. **Danger:** start with the card's Danger (its Ghost Danger if it is a Ghost). Add 2 if it is Angry. Subtract 3 if you used Dart this turn. Subtract 2 if you used Carry this turn. Minimum 0. Then, if you used Hypnotise this turn and the Danger is above 4, lower it to 4.
2. **Claws:** 2 + your Ready trophies (+2 if the Owl is Ready), counted now (after Phase 1, before this card joins your pack).
3. **Wounds** = Danger minus Claws, minimum 0. If you used Feint this turn, wounds are 0.
4. If the wounds are **more than your Ready trophies**, the cat **dies** (section 5, Death). The run is lost; this card is the killer.
5. Otherwise spend one Ready trophy per wound (your choice which; the Owl and Moth may be spent).
6. If the card is the Hound, the cat **escapes**: the run is won. Stop here.
7. Put the card into your pack, Ready (upright, not Angry). Its grid space is now **empty** for the rest of the run.
8. Apply the **Lighting rule** (special rule 1).

**Action B - Shove.** Legal only if the grid holds a Lit card that is **not Angry** and at least one Dark card.
1. Choose a Lit, calm card X and any Dark card Y (Y may be Angry).
2. Swap their positions, then apply Lighting: Y is now Lit in X's old space (it keeps its Angry state); X is Dark in Y's old space unless that space is in the doorway or next to an empty space.
3. X becomes **Angry** (special rule 2): turn it sideways. (A Silk Shove skips this step.)
4. The Shove is over.

There is no pass. A Fight is always legal: until the Hound is beaten the grid holds at least one Lit card (doorway spaces are always Lit or empty, and any card next to an empty space is Lit).

### Phase 3 - Hunt
If the Hound is in the grid, Lit, and not a Ghost: spend 1 Ready trophy (your choice). If you have none, nothing happens. This applies however the Hound became Lit this turn (by a Shove, a Silk Shove, a Carry swap, a Drift or a Fight's Lighting). Then the next turn begins.

### Every legal action, summarised
| Action / trick | When legal | Choices |
|---|---|---|
| Fight | Always (any Lit card) | Which Lit card; which trophies pay the wounds |
| Shove | A Lit calm card and a Dark card exist | Which Lit calm card; which Dark card |
| Glow (Moth) | Moth Ready, Phase 1, a Dark card exists | Which Dark card |
| Dart (Mouse) | Mouse Ready, Phase 1 | None |
| Silk (Spider) | Spider Ready, Phase 1, a Lit calm card and a Dark card exist | Which Lit calm card; which Dark card |
| Scavenge (Rat) | Rat Ready, Phase 1 | Which Spent trophies (up to 2, not the Rat) |
| Carry (Crow) | Crow Ready, Phase 1 | Whether to swap; if so, which two grid cards |
| Hypnotise (Snake) | Snake Ready, Phase 1 | None |
| Feint (Fox) | Fox Ready, Phase 1 | None |
| Drift | A Ghost Moth, Mouse or Spider is Lit, Phase 1 | Whether to Drift it |
| Spend (Hunt, wounds) | Forced | Which Ready trophy |

## 5. Special rules and timing

The game has exactly three special rules:
1. **Lighting.** A grid card is Lit (face up) if it is in the doorway (top row) or orthogonally next to an empty space; every other grid card is Dark (face down). Lit or Dark depends only on position: check it every time a space empties or cards swap (Fight, Shove, Silk, Carry, Drift) and turn cards to match. A card turned face down this way keeps its Angry state.
2. **Anger.** A card moved by a normal Shove becomes Angry: +2 Danger until it is beaten. An Angry card can never be Shoved again (Carry can still move it). A beaten card goes to your pack upright and is no longer Angry.
3. **Ghosts (nine lives).** A card ticked on the lives tally is a Ghost for the rest of the session. A Ghost's Danger is 2 lower (minimum 0: Moth 0, Mouse 0, Spider 1, Rat 2, Crow 3, Owl 4, Snake 5, Fox 6, Hound 7), and a Ghost Hound does not Hunt. Its trophy trick works normally once you have it. A Ghost Rat to Hound must be beaten by a Fight like any card (it costs your action). A Ghost Moth, Mouse or Spider can instead **Drift** into your pack, Ready, without a Fight and without using your action (Phase 1).

**Death.** The cat dies when a Fight's wounds are more than its Ready trophies. The run ends at once and is lost. On the lives tally, tick the box of the card that killed you. If that box is already ticked (a Ghost can kill), tick the lowest-numbered unticked box instead. Every death ticks exactly one box, so the number of ticks is the number of lives lost.

**Timing and edge cases.**
- **Order inside a Fight** is fixed: Danger, Claws, wounds, death check, pay, escape check, to pack, Lighting.
- **Claws are counted once,** at Fight step 2, before the beaten card joins your pack. Paying wounds (including with the Owl) does not change that Fight's wounds.
- **Several cards lit at once:** turn them all face up together.
- **The Hound turning face up** has no immediate effect; Hunt checks only in Phase 3 of the same turn.
- **Escape beats everything:** beating the Hound ends the run before Lighting or Hunt.
- **Spending with nothing Ready:** Hunt does nothing; only wounds can kill.
- **Glow with no Dark card:** cannot be used. Looking never changes a card's state.
- **Silk then Shove:** after a Silk Shove you may still take a normal Shove (or a Fight) in Phase 2.
- **Carry without a Fight:** if you used Carry and then Shove, the swap stands but the -2 is wasted.
- **Memory:** you may remember everything you have seen (including Dark cards you Shoved, Glowed or moved) and deduce Dark cards by elimination, since all nine cards are always in the grid or your pack. You may not look at Dark cards except with Glow.
- **Termination:** every turn's Phase 2 action is a Fight or a normal Shove. Every Fight removes a card for good (at most 9 Fights), and every normal Shove turns a calm card Angry for good (at most 9, since an Angry card can never be Shoved and only beaten cards lose Anger by leaving the grid). Silk Shoves, Carry swaps and Drifts happen in Phase 1 and never add turns; Silk and Carry are each usable at most twice per run (once, plus once more after the Rat's single Scavenge). So a run always ends within 18 turns. Simulation turn cap: 20 turns; reaching it counts as a loss and must never happen.
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

**Why the game ends:** a run cannot last more than 18 turns (section 5, Termination); every run ticks an escape or a lives box, so a session ends after at most 10 runs.

**Quick play:** a single run is a complete 10-minute game: escape to win, die to lose.

## 7. Design notes

**The twist: a known cellar in an unknown order.** The nine creatures are the same every run, so the game is never about *what* you meet, only *where*. Shove pushes a creature you are not ready for back into the dark and drags an unknown one into the light, at the price of it coming back Angry. Lighting spreads from every room you clear, so each Fight is also a reveal. Because the set is fixed, every reveal narrows down the rest, and a careful player can deduce where the Hound sleeps. Each death writes a lesson onto the cellar as a Ghost.

**One number does three jobs.** Ready trophies are your Claws, your armour (they pay wounds) and your tricks. Two trophies are worth keeping Ready rather than spending: the Owl (+2 Claws) and the Moth (a free peek every turn). Spending either to pay a wound is a real choice.

**What each trick is for (and its ablation test).** For every trick, the playtester runs the full bot and an "ignore-it" bot that never uses that trick; the full bot must win at least 5 points more, and the trick must be used in at least 15% of runs where it is Ready.
- *Glow:* a free peek each turn; finds the Hound and safe fights. Ablation: bot never Glows.
- *Dart:* the cheap Fight cut. Ablation: never Darts.
- *Silk:* tempo: hide the Hound (or dig for a low card) and still Fight the same turn, with no Anger. Ablation: never Silks.
- *Scavenge:* refund. Ablation: never Scavenges.
- *Carry:* a -2 Fight cut plus an optional rearrangement (pull the Hound out of the light, or bring a known low card into it). Ablation: never Carries; second ablation: Carries without ever swapping (tests whether the swap matters; if not, the swap is cut in v3).
- *Wise, Hypnotise, Feint:* as v1. Ablation: never spend the Owl first / never use Hypnotise / never use Feint.
- *Drift and Ghost Danger:* ablation is the single-Ghost lift itself (target +5 to +25 per Ghost).
- *Shove/Anger and Lighting* are the core; ablation: bot with Anger off must win more (Anger is a cost), bot that never Shoves must lose at least 5 points.

**Comeback and early luck.** Solo, so the KPI is not runaway leader but "a bad layout is not a lost run": Shove and Silk dig out a fightable card when the doorway has nothing safe, Scavenge refunds spends late, and Hypnotise or Feint let a damaged cat still strike the Hound. Across a session, each death makes the next run easier (a Ghost), so a bad start is recoverable. What keeps turn 1 from deciding the run: the doorway is never the Hound, and the Shove always exists.

**Ghosts (catch-up).** Every Ghost is 2 Danger weaker. Large Ghosts (Rat to Hound) still cost a Fight and an action, and Owl 4, Fox 6 and Crow 3 now usually need one or two trophies first, which caps their v1 lift of +38 to +44. Small Ghosts (Moth, Mouse, Spider) were already easy to beat, so instead they Drift: a free trophy without spending the turn, as soon as they are Lit. Escapes do not make the cellar easier; the session gets kinder only as you lose lives, and the score is the lives you keep.

**Target band and tuning knob (solo win rate).** Target: a competent human wins **40-60%** of first runs (no Ghosts). Bots cannot measure "competent human" (v1: outline 19%, lookahead 81%), so the playtester reports at least two bots and the spread, and the band is checked only by human sessions. Bot sanity bands: fixed outline bot 25-60%, lookahead bot at most 90%, random at least 20 points below the outline bot. Do not tune to one bot. **The one tuning knob is Hunt:** easier = "Hunt only on turns you did not Fight"; base = soft drain (as written); harder = "if you have no Ready trophy, the cat dies". Base Claws stays 2 (a knife edge in v1).

**Skill gap.** Good play beats random play through shove targets (where the Hound goes), when to stop growing and strike, and which trophy to spend. v1 gap: 19 to 81 points; target at least 20.

**Variety targets (the playtester measures these).**
- Among strategic wins: at least 10% use Feint, at least 10% use Hypnotise, at least 25% use neither.
- First action is a Shove in 20-60% of layouts (strong bot), killers: Hound 40-75% of deaths and at least 4 cards each cause 5% or more.
- Zero dead cards: each non-Hound card is beaten or Shoved in at least 25% of runs; each trick is used in at least 15% of runs where it is Ready; Wise changes a Fight's wounds in at least 15% of runs where the Owl is Ready.
- Length: median run 7-12 turns; time model 30 s setup, 50 s per turn, 15 s per trick, 15 s tally; target 8-12 minutes.
- Carry-over: each single Ghost raises the next run's win rate by 5-25 points; sessions average 3-4 runs; no session score holds more than 40% of sessions.

**Rule budget.** Brief promise: rules on one page, at most 3 special rules. Special rules: 3 (Lighting, Anger, Ghosts). Player-facing teach (sections 2-6) is about 110 lines, roughly two pages of text; the Cat card summary is one card face. Over the one-page promise: see Known gaps.

**Simulation notes.**
- *Layouts:* a run is fully determined by the deal permutation, the Ghost set and the player's choices. Index layouts by the lexicographic rank of the permutation (0 to 362,879). Run the reference bots on the empty Ghost set and on each of the 9 single-Ghost sets; simulate sessions with uniformly random deals.
- *Random bot:* seed its RNG with the layout index. Each turn, for each Ready trick and each possible Drift in card-number order, use it with probability 1/2 (uniform random legal choices; Carry swaps with probability 1/2, then a uniform random pair); then choose uniformly among all legal actions; pay wounds and spends with uniformly random Ready trophies.
- *Outline bot (fixed in v2; deterministic):*
  1. *Knowledge:* track every card seen and every move; deduce a Dark card when only one identity is unaccounted for. The Hound's position is known from setup only if the setup swap happened.
  2. *Drift* every Lit small Ghost unless it would light a space known to hold the Hound while you have fewer than 3 Ready trophies.
  3. *Glow:* if the Moth is Ready and an unknown Dark card exists, Glow the lowest-index unknown Dark card that the planned Fight would light, else the lowest-index unknown Dark card.
  4. *Strike:* if the Hound is Lit, find the cheapest set of tricks (fewest spends; Dart, Carry, Hypnotise, Feint; Scavenge first if it helps) that makes the Hound Fight survivable; if one exists, use it and Fight the Hound.
  5. *Hide:* if the Hound is Lit, calm, cannot be struck, and you have fewer than 3 Ready trophies: Shove it (as a Silk Shove if the Spider is Ready, then continue to step 6) into the Dark space farthest (orthogonal steps) from every empty space and from the doorway; ties: highest grid index. If it is Angry and the Crow is Ready, use Carry to swap it there, then continue (Carry's -2 applies to this turn's Fight).
  6. *Grow:* "clean" means Danger at most current Claws (Claws counted before the new trophy joins). Among Lit non-Hound cards with a clean Fight, Fight the one that does not light a space known to hold the Hound (unless you would then have 4+ Ready); then prefer the one lighting fewer unknown Dark cards while the Hound is unknown; then the higher Danger; then the lower grid index.
  7. *Push:* if no clean Fight exists, take the Fight (optionally with Dart and/or Carry, no swap) that leaves you at least 1 Ready trophy after paying, with the smallest net loss (trophies spent minus 1 for the trophy gained); a Snake or Fox Fight counts its trophy as worth 2.
  8. *Shove:* otherwise Shove the highest-Danger Lit calm card X. Y is the Dark card chosen in this order: never a card known or deduced to be the Hound; first a known card whose Danger is at most current Claws (lowest Danger first); else the lowest-index unknown Dark card. If the Spider is Ready, make it a Silk Shove, then re-run steps 4-8 for Phase 2.
  9. *Forced:* if only fatal Fights remain and no Shove is legal, Fight the Hound if Lit, else the Lit card with the highest number.
  - *Spending order* (wounds, Hunt): Mouse, Crow, Spider, Rat, Snake, Moth, Owl, Fox (first Ready one; skip the Rat while you have 2+ Spent others). Use Scavenge when you have 2 Spent others, or 1 if it makes a strike possible.
- *Greedy baseline bot:* Fight the lowest-Danger Lit card you can survive; if none, Shove the highest-Danger Lit calm card into the lowest-index Dark space; never use tricks or Drift.
- *Lookahead bot:* as in v1 (determinised Monte Carlo); it must now model Glow, Silk, Carry (with and without a swap) and Drift.

## 8. Changelog

**v2 (revision 1).** One targeted pass on `critique.md` (REVISE-MINOR, 3.33) and `playtest-report.md` (NEEDS-FIXES).
- **Renamed** "Nine Lives Dungeon" to **Whiskerdark** (critic: title and theme collide with *Nine Lives: Rogue-and-Write*, 2020). The cards are now "Cellar cards".
- **Ghosts reworked** (critic change 1; playtest lift Moth 0 to Owl +44): every Ghost is 2 Danger weaker instead of Danger 0, which caps Crow at 3, Owl at 4 and Fox at 6 (Hound stays 7). Small Ghosts (Moth, Mouse, Spider) gain **Drift**: free into your pack, Ready, when Lit. The design note's "free trophy" now means exactly this; large Ghosts must be fought.
- **Glow** no longer spends the Moth: one free peek per turn while Ready (was spend for 2 peeks; used 0.5% by the strong bot).
- **Silk** is now a free extra Shove with no Anger, then your normal action (was "your Shove does not anger"; used 0.3%). It covers hiding the Hound without losing the turn.
- **Carry** is now "before you Fight: optional swap of any two grid cards, then Danger -2" (was a bare swap; used 0.15% and never modelled). A bot can use it as a Fight discount and optionally the swap.
- **Cut Thief** (the Crow's Room text) and the "Room text" column (critic change 4). Only the Hound's Hunt remains, stated in Phase 3.
- **Ambiguities closed:** Hound position is known only when the setup swap happened; Scavenge cannot re-enable a trick already used this turn; a Hound lit by any means is hunted in Phase 3 of the same turn; Lighting is position-only and applies after every swap, explicitly including Carry; Claws for "clean" Fights are counted before the new trophy joins (bot steps 6-7); the outline bot never Shoves Y = known Hound (fixes the loop).
- Stated the target band, the single tuning knob (Hunt), the turn bound (18, sim cap 20), why the game ends, and the rule budget. Base Claws unchanged at 2.

## Known gaps

- **Rule budget over the promise:** the player-facing rules are about two pages of text, not one; 3 special rules is met, but seven tricks plus Drift is a heavy teach for complexity 2. Not cut further in this pass (no new mechanics, only fixes).
- **Untested numbers:** the Ghost lifts (Danger -2 and Drift), the new Glow, Silk and Carry use rates, and the effect of removing Thief on the win rate are design estimates; all need the playtester's re-run. Removing Thief makes the game slightly easier; Silk and free Glow may too.
- **Win-rate band is unverifiable by bots** (L2, L5); only human sessions can place a competent player in 40-60%.
- **Grindy opening** (no Moth or Mouse in the doorway) is left as is, per the critic, until human sessions confirm it.
- **Memory burden** rises with free Glow (more seen Dark cards to remember); untested with humans.
- **Flat surface needed** for sideways Angry and Spent cards (commuter play).
- **Title clearance:** "Whiskerdark" has not been searched for existing products.
