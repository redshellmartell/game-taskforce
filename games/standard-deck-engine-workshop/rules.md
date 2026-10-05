# Fifty-Two Workshop - Rules (v2, revision 1)

## 1. Overview

- **Title:** Fifty-Two Workshop
- **Hook:** You are clockmakers sharing one workbench. Every card in a standard deck is a part, and a part's power comes from its neighbours. Build a card next to cards of adjacent rank and the whole **gear train** turns: Springs in it make the build cheaper and Gears in it pull parts off the shared Bench. Build your engine from cheap parts first, then **retool**: swap the engine parts out for valuable Jewels and Clock faces before the clock strikes.
- **Players:** 1-4 (solo mode at the end of section 6)
- **Play time:** about 20 minutes at 4 players (about 12 at 2, 16 at 3, 10 solo)
- **Age:** 10+
- **Complexity:** 2 / 5

## 2. Components

One standard 52-card deck (no jokers) and one printed rule card. No tokens, no score pad.

**Rank values** (cost and payment): A = 1, 2-10 = face value, J = 11, Q = 12, K = 13.

**The 52 cards.** Each card appears once. Suit decides what a card does in your workshop; rank decides its cost, its payment value and which cards it connects with.

| Suit | Name | Ranks | Count | When its train turns (Build) | End points |
|---|---|---|---|---|---|
| Spades | Spring | A-K | 13 | This build costs **4** less | 1 |
| Clubs | Gear | A-K | 13 | Take 1 card from the Bench | 1 |
| Diamonds | Jewel | A-K | 13 | (nothing) | 3 |
| Hearts | Clock face | A-K | 13 | (nothing) | 1 + number of different suits in its train (2-5) |

Every card has three uses: build it, pay with it (worth its rank value), or keep it in hand. No card is ever dead.

**Rule card (1)** shows: rank values, the table above, the turn summary (Gather 2 *or* Build 1 / Retool 1; end of turn: hand limit 7, Bench back to 5, clock check), the clock targets and the solo ladder.

**Piles on the table:** the deck (face down), the **Bench** (face-up row), the **scrap pile** (face down, out of the game) and, in solo only, the **Rival pile** (face down).

## 3. Setup

1. Shuffle the 52 cards.
2. Deal **3 cards face down to each player** as their secret starting hand.
3. Deal **5 cards face up in a row**: the **Bench**. New cards always go on its **right end**; when a card is taken, the gap closes and the order is kept.
4. Put the rest face down as the deck.
5. Choose the first player at random; play goes clockwise. (Simulation: seat 1 is first.)

Your **workshop** is the space in front of you, empty at the start. Built cards go there face up, in one row by rank, A on the left, K on the right.

## 4. Turn structure

On your turn do exactly **one** action, **Gather** or **Build** (a Retool is a kind of Build), then the **End of turn** steps.

### Action A - Gather
Take exactly **2 cards** into your hand, one at a time. For each pick choose either any Bench card or the top card of the deck. A deck card is taken unseen and goes straight into your hand; you see it before making your second pick. The Bench is not refilled between picks. If the Bench and deck together hold fewer than 2 cards, take all of them.

### Action B - Build
Build one card from your hand into your workshop, in this order:
1. **Choose** a card from your hand. If your workshop has **no** card of that rank, it is a normal build. If your workshop **has** a card of that rank, it is a **Retool** (special rule 3): that workshop card will be replaced. (You never have two cards of one rank in your workshop.)
2. **Find its train.** A train is the new card plus every workshop card joined to it through consecutive ranks with no gap. For a Retool, the replaced card is ignored; the new card takes its place. Example: workshop 3, 4, 5, 8; you build a 6; its train is 3-4-5-6 (the 8 is not joined because 7 is missing). A joins only 2; K joins only Q (no wrap). A card with no neighbours is a train of 1.
3. **Cost** = the new card's rank value minus **4 for each Spade in its train** (the new card included). Never below 0.
4. **Legality:** the **other** cards in your hand must add up to at least the cost. Cards your Gears would take do not count. If not, you may not build that card.
5. **Place** the card in your workshop. For a Retool, put the replaced card face down on the **scrap pile**.
6. **The train turns:** for **each Club in the train** (the new card included), take 1 card from the Bench into your hand, one at a time; this is mandatory. If the Bench is empty take the deck's top card instead; if both are empty take nothing.
7. **Pay:** if the cost is above 0, choose hand cards whose rank values total **at least** the cost (cards just taken by Gears may be used) and place them face up on the right end of the Bench in any order. No change is given. If the cost is 0, pay nothing; you may not pay.

### End of turn (always, in this order)
1. **Hand limit:** if you hold more than 7 cards, put cards of your choice on the **scrap pile** until you hold 7.
2. **Solo only:** the Rival acts (section 6).
3. **Bench back to 5:** if the Bench holds more than 5 cards, take its **leftmost** card and put it face down at the **bottom** of the deck; repeat until it holds 5. If it holds fewer than 5, deal cards from the top of the deck to its right end until it holds 5 or the deck is empty.
4. **Check the clock** (section 6).

### Every legal action
| Action | When legal | Choices |
|---|---|---|
| Gather | The Bench or the deck holds at least 1 card | For each pick: which Bench card, or the deck's top |
| Build (normal) | A hand card of a rank not in your workshop, with the other hand cards totalling at least its cost | Which card; which Bench cards your Gears take; which cards pay and their order |
| Build (Retool) | A hand card of a rank already in your workshop, with the other hand cards totalling at least its cost | As above |
| Pass | Only if no Gather and no Build is legal | None |

Hand limit, Rival and Bench steps are not actions. Hands are secret; hand sizes, workshops, the Bench and the number of cards in the deck, scrap and Rival piles are public. No trading or gifts.

## 5. Special rules and timing

The game has exactly three special rules:
1. **Gear trains:** a build turns the new card's whole train. Each Spade in it cuts the cost by 4; each Club in it takes a Bench card.
2. **Spent parts go to the Bench:** payment goes face up on the right end of the Bench, where anyone can take it. At end of turn the Bench always goes back to exactly 5 (oldest cards slide under the deck, or new cards are dealt).
3. **Retool:** you may build a card of a rank you already have; it replaces that card, which is scrapped. A Retool does not add to your workshop count.

Timing and edge cases:
- **Order inside a Build** is fixed: choose, train, cost, legality, place (and scrap the replaced card), Gears take, pay. Spades only reduce the cost of the build they are in; Gears take before you pay, so you can never take back the cards you pay this turn.
- **Trains are counted at the moment of the build.** A later card that joins two trains makes one bigger train. Trains never break by normal builds; a Retool keeps the train intact because the new card has the same rank.
- **Same rank across players** is fine: any number of players may have a 7.
- **Hand limit** is checked only at End of turn step 1, after the action and payment.
- **Empty Bench during Gather or Gears:** take from the deck. **Empty deck:** it cannot be picked and refills stop. A card slid under an empty deck makes the deck non-empty again.
- **Scrapped cards and Rival cards** never return and are not public in content.
- **Running score:** a player's score at any moment is what their workshop would score if the game ended now (section 6). It is public. (Simulation: lead changes are measured on running scores at the end of each full round.)
- **No simultaneous effects:** everything happens on the active player's turn, one step at a time.

## 6. End of game and scoring

**The clock strikes** at End of turn step 4 if either is true:
- the active player has at least **10 workshop cards (11 with 2 players)**; or
- the deck holds 0 cards (checked after step 3).

Once struck, the clock is never checked again.

**Finish the round (multiplayer):** after the clock strikes, play continues until the last player in turn order (the player to the right of the first player) has finished a turn; then the game ends. If the clock strikes on that player's turn, the game ends at once. Every player therefore has the same number of turns. The final turns are normal.

**Scoring** (workshop only; hands, Bench, deck and scrap score nothing):
| Card in your workshop | Points |
|---|---|
| Each Spade | 1 |
| Each Club | 1 |
| Each Diamond | 3 |
| Each Heart | 1 + the number of different suits among the cards of its train, Hearts included (2 to 5) |

Example: train 4S-5H-6C-7H plus a lone QD. Each Heart scores 1 + 3 (Spades, Hearts, Clubs) = 4. Total 1 + 4 + 1 + 4 + 3 = 13.

**Winner:** highest score. **Tiebreaker 1:** more workshop cards. **Tiebreaker 2:** longest train (most cards). **Still tied:** shared win.

### Solo mode
All the rules above apply, with these changes:
- Setup as normal for one player.
- **The Rival** acts at End of turn step 2: it takes the **two highest-ranked** Bench cards (equal ranks: the leftmost first). The **higher** one goes face down on the **Rival pile**; the other goes face down at the **bottom of the deck**. If the Bench holds one card, it goes to the Rival pile; if none, the Rival does nothing.
- **The clock strikes** at step 4 when the Rival pile holds **24 cards** (the end of your 24th turn), or the deck holds 0 cards. The game ends at once. (The workshop-count trigger is not used in solo.)
- Score as normal and read the ladder. **You win at 31 points or more.**

| Score | Title |
|---|---|
| 0-24 | Tinkerer |
| 25-30 | Apprentice |
| 31-34 | Journeyman (win) |
| 35-38 | Master (win) |
| 39+ | Grandmaster (win) |

## 7. Design notes

**The twist: gear trains, then retooling.** A card's power is not printed on it; it comes from where it sits in the deck's own order. Ranks decide what a card joins; suits decide what the train does. Spades and Clubs are scaffolding: they make the next build cheap and bring in parts, but score only 1. Retool turns that scaffolding into points: once the train is long, swap a 6S for a 6D (3 points) or a 6H (up to 5). Each swap gives up engine power and costs a turn that does not advance the clock. This gives a real engine arc on a deck everyone owns: build the engine, ride it, cash it out.

**Intended strategies.**
1. *Engine first:* two Spades and a Club in one train early (discount 8, one pull per build), then cheap builds of high ranks, then Retool Spades into Diamonds and Hearts late. This should be the strongest line in skilled hands.
2. *Jewel rush:* cheap Diamonds early, race to the clock target before the engines cash out.
3. *Clock faces:* one long mixed train with Hearts; strong if the train keeps all four suits, which competes with retooling Spades and Clubs away.
The key tension is **when to stop building outward and start retooling**: Retooling scores but does not move you toward the target, and a rival near 10 cards can strike the clock before you cash out.

**Interaction.** The Bench is shared: you Gather the rank a rival needs to close a gap, Gears snatch the best parts, and every payment hands parts to the next player (now visible for at least a turn, then slid under the deck). Retool adds a read on rivals: a player holding many Spades in a long train is about to cash out, so racing the clock or taking the Diamonds and Hearts of their ranks off the Bench is a real counter.

**Catch-up and tension.** Retooling makes scores jump late (a Spade becoming a 5-point Heart is +4), so the running leader in mid-game is often the Jewel player, and engine players overtake near the end. Finishing the round keeps turns equal. Apprentice was cut: seats were already within 4 points and it added a rule and a tie case.

**Stall-proof.** Every Gather with a full hand scraps cards; every Retool scraps a card; normal builds are limited to 13 per player. So the cards outside workshops strictly run down, the deck eventually empties and the clock strikes. No game can loop.

**Length.** Builds about 25 seconds, Gathers about 10. Retools add turns that do not advance the clock, offsetting the faster Spade engine. Expected 4p about 55-62 turns (17-20 minutes). Solo: 24 turns, about 12 builds and 12 Gathers, about 7-8 minutes by this formula; solo turns have no downtime and more thinking, so a human solo game should run about 10 minutes. A 15-minute solo is not reachable by the formula without a much longer solo game (about 45 turns), which the 52-card deck cannot support with a 13-rank workshop; see revision notes.

**Tuning knobs, in priority order** (change one at a time):
1. **Spade discount:** 4 (range 3-4). First knob for engine strength.
2. **Spade points:** 1, or 2 (alternative engine buff; if used, return the discount to 3).
3. **Gear Gather (0-cost Club pull):** off; if on, a player whose workshop has a Club in a train of 2+ cards Gathers 3 cards instead of 2.
4. **Solo win line:** 31 (move by 1-2 so strategic wins 45-55%); then **solo length:** Rival pile 24 (range 20-26).
5. **Clock target:** 10 (11 at 2p); try 9 at 4p if 4p runs over 24 minutes or deck-empty ends dominate.
6. **Heart scoring:** 1 + suits (2-5), or number of suits only (1-4) if Hearts still have the top win correlation.
7. **Hand limit:** 7 (range 6-8).
8. **Last-seat start:** seats 3 and 4 start with 4 cards, only if the seat gap goes above 5.

**Bot hints for simulation.**
- *Build value:* end points it adds now (running-score change, including Heart changes in its train) + 1.5 per Spade and 1.2 per Club it adds to a train of 2+ cards + 0.5 per card in the train it joins - 0.3 per payment card. Retool value: running-score change - (1.5 per Spade or 1.2 per Club removed, scaled by the share of the game left: builds-to-target remaining / target). Build the best if its value is above a Gather's (about 2.5); otherwise Gather.
- *Gather:* take Bench cards that are legal builds extending your trains (prefer filling a one-rank gap), then Diamonds or Hearts matching ranks of your Spades or Clubs (Retool targets), then the highest rank; take the deck top only if no Bench card is worth it. Take a card a rival needs to close a gap if nothing else is worth more than 1.
- *Pay:* fewest cards, then lowest total; avoid paying ranks that would extend a rival's train.
- *Clock:* do not make the build that strikes the clock unless your score would be highest after the remaining turns (estimate one build each for rivals).
- *Hand limit:* scrap the lowest-value cards (lowest rank that is not a build or Retool candidate).
- *Random bot:* choose uniformly among all legal actions, then uniformly among choices.

## 8. Changelog

**v2 (revision 1).** Answers critique.md (REVISE-MAJOR) and playtest-report.md (NEEDS-FIXES).

### Revision notes (v2)

| # | Change | Why (feedback) | KPI target |
|---|---|---|---|
| 1 | Spade discount 3 -> **4** (knob 1). Spade 2 points and Gear Gather are listed as knobs 2 and 3, to be tried one at a time only if knob 1 misses. | Critic change 1; playtest problem 2: Spades -0.056 win correlation, strategic only 53% v greedy | Spade and Club win correlation >= 0; strategic v greedy (2p) >= 60%; engine-minded bots (Planner, Optimiser) >= Flavour bot |
| 2 | **Solo rebuilt:** the Rival takes the 2 highest Bench cards each turn (the higher out of the game, the other under the deck, so the deck does not drain twice as fast); the game lasts 24 turns, timed by the Rival pile; win line 22 -> **31**; new ladder. | Critic change 2; playtest problem 1: strategic 98.6%, random 68%, 19.5 turns | Strategic solo 45-55%, random < 15%; length 24 turns (was 19.5) |
| 3 | **Stall breaker:** hand-limit excess is scrapped (out of the game); the Bench goes back to exactly 5 at end of turn, leftmost cards sliding under the deck. | Critic change 3; playtest problem 3. The requested trim alone (remove leftmost when Bench > 5) does not close the logged loop: in it the Bench sits at exactly 5 (take 2, discard 2). Scrapping hand-limit excess does, and the trim keeps the Bench at a fixed 5. Trimmed cards go under the deck, not out of the game, because roughly 25 trims per 4p game would otherwise empty the deck early. | Zero turn-cap hits without bot patches |
| 4 | **Ambiguities resolved and rules cut:** Apprentice dropped; blind deck pick stated; mandatory Gather count and Gear pulls; Gears do not count for legality; 0-cost builds pay nothing but still pull; hand limit after the action; strike timing and round finish stated; deck-empty checked after the Bench step; solo order and immediate end stated; Pass defined; tiebreak chain and shared win stated; running score defined. Bench is a fixed 5 instead of growing. Clock target simplified to 10 (11 at 2p). | Critic change 4; all 11 ambiguities in playtest.json | Zero ambiguities; rules_simplicity above 0.149; rules card on one side |
| 5 | **Retool** (new special rule 3, replacing Apprentice): build a rank you already have, scrapping the old card. | Critic change 5: one real decision per turn, leader fixed after mid-game | Lead changes >= 2.5; strategic v greedy gap wider; rival-take rate > 0.5 per turn |
| 6 | **4p length:** target 9 -> 10 at 4p (and 3p stays 10); Retools add non-advancing turns to offset the faster engine. | Critic change 6; 4p 16.6 of 20 minutes (-17%) | 4p 16-24 estimated minutes; re-measure after change 1 |

**Suggested experiment order for the playtester:** (a) v2 as written; (b) if Spade correlation is still below 0, knob 2 instead of knob 1; (c) if still below 0, add knob 3; (d) tune the solo win line, then the solo length; (e) if budget allows, v2 with Retool off, to see how much of the engine and lead-change result Retool delivers.

**Open issue for the Director:** the solo time target of 15 minutes cannot be met by the 25 s / 10 s formula within one 52-card deck (it would need about 45 solo turns). I recommend resetting the solo target to 10 minutes, or checking it with a human solo game.

**v1 (first design).** Initial rules.
