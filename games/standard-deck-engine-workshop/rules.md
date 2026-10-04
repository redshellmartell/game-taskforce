# Fifty-Two Workshop - Rules (v1)

## 1. Overview

- **Title:** Fifty-Two Workshop
- **Hook:** You are clockmakers sharing one workbench. Every card in a standard deck is a part, and a part's power comes from its neighbours. Build a card next to cards of adjacent rank and the whole **gear train** turns: the Springs in it make the build cheaper and the Gears in it pull more parts off the shared Bench. The parts you spend go back on the Bench, where your rivals can grab them.
- **Players:** 1-4 (solo mode in section 6)
- **Play time:** about 20 minutes at 4 players (about 12 at 2, 16 at 3, 15 solo)
- **Age:** 10+
- **Complexity:** 2 / 5

## 2. Components

One standard 52-card deck (no jokers) and one printed rule card. No tokens, no score pad: the score is counted from the table at the end.

**Rank values** (used for costs and payment): A = 1, 2-10 = face value, J = 11, Q = 12, K = 13.

**The 52 cards.** Each card appears once. A card's suit decides what it does in your workshop; its rank decides its cost, its payment value and which cards it connects with.

| Suit | Workshop name | Ranks | Count | When its train turns (Build) | End-of-game points |
|---|---|---|---|---|---|
| Spades | Spring | A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K | 13 | This build costs 3 less | 1 |
| Clubs | Gear | A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K | 13 | Take 1 card from the Bench | 1 |
| Diamonds | Jewel | A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K | 13 | (nothing) | 3 |
| Hearts | Clock face | A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K | 13 | (nothing) | 1 + the number of different suits in its train (2 to 5) |

Every card has three possible uses: build it into your workshop, spend it as payment (worth its rank value), or keep it in hand.

**Printed rule card (1)** shows: the rank values, the table above, the turn summary (Gather 2 *or* Build 1; end of turn: hand limit 7, refill Bench to 5), the clock-strike table (section 6) and the solo ladder.

## 3. Setup

1. Shuffle the 52 cards.
2. Deal **3 cards face down to each player** as their starting hand. Hands are secret.
3. Deal **5 cards face up in a row** in the middle of the table. This row is the **Bench**. New cards are always added to the **right end** of the Bench; cards taken from it close up the gap (order is kept).
4. Put the rest of the deck face down next to the Bench. There is no discard pile.
5. Choose the first player at random. Play goes clockwise. (Simulation: seat 1 is first.)

Each player's **workshop** is the space in front of them, empty at the start. Built cards go there face up, in one row ordered by rank, A on the left and K on the right.

## 4. Turn structure

On your turn, do exactly **one** action, **Gather** or **Build**, then the **End of turn** steps.

### Action A - Gather
Take **2 cards** into your hand, one at a time. Each can be any card on the Bench or the top card of the deck (your choice for each, decided one at a time; you see the first card before choosing the second). The Bench is not refilled between the two picks.
- **Apprentice (special rule 3):** if your workshop has strictly fewer cards than **every** other player's workshop, take **3 cards** instead of 2. (Never applies in solo.)
- If the Bench and the deck together hold fewer cards than you may take, take all of them.

### Action B - Build
Build exactly one card from your hand into your workshop, in this order:
1. **Choose** a card in your hand whose rank is **not** already in your workshop. (You may never hold two cards of the same rank in your workshop.)
2. **Find its train.** A **train** is a group of workshop cards with consecutive ranks and no gaps: the new card plus every workshop card joined to it through consecutive ranks. Example: your workshop is 3, 4, 5, 8; you build a 6; its train is 3-4-5-6 (the 8 is not joined, because 7 is missing). A only connects to 2 (there is no wrap from K to A). A card with no neighbours is a train of 1.
3. **Work out the cost:** the new card's rank value minus **3 for each Spade in its train** (counting the new card if it is a Spade). The cost is never below 0.
4. **Check you can pay:** the build is legal only if the **other** cards in your hand (not counting the card being built) add up to at least the cost. If not, you may not build that card.
5. **Place** the card in your workshop in rank order.
6. **The train turns (special rule 1):** for **each Club in the train** (counting the new card if it is a Club), take 1 card of your choice from the Bench into your hand, one at a time. If the Bench is empty, take the top card of the deck instead; if both are empty, take nothing.
7. **Pay (special rule 2):** choose cards from your hand whose rank values add up to **at least** the cost and place them face up on the **right end of the Bench**, in any order you choose. Cards you just took with Gears may be used. There is no change for overpaying. If the cost is 0 you pay nothing (you may not pay cards on a 0-cost build).

Diamonds and Hearts do nothing when the train turns; they score at the end.

### End of turn (always, in this order)
1. **Hand limit:** if you hold more than 7 cards, place cards of your choice from your hand on the right end of the Bench until you hold 7.
2. **Solo only:** the Rival takes a card (section 6, solo mode).
3. **Refill:** if the Bench has fewer than 5 cards, deal cards from the top of the deck to its right end until it has 5 or the deck is empty. (The Bench may hold more than 5 cards; it is never reduced to 5.)
4. **Check the clock** (section 6).

### Every legal action, summarised
| Action | When legal | Choices |
|---|---|---|
| Gather | The Bench or the deck holds at least 1 card | For each of 2 (or 3) picks: any Bench card or the deck's top card |
| Build | You hold a card whose rank is not in your workshop, and your other hand cards total at least its cost | Which card; which Bench cards your Gears take; which cards you pay with and their order on the Bench |
| Pass | Only if neither Gather nor Build is legal | None |
| Hand limit | You hold 8+ cards at end of turn | Which cards go to the Bench |

There are no other actions. Hands are secret but the number of cards in each hand is public. Players may not trade or give cards.

## 5. Special rules and timing

The game has exactly three special rules:
1. **Gear trains** - a build turns the new card's whole train: each Spade in it cuts the cost by 3, each Club in it takes a Bench card.
2. **Spent parts go to the Bench** - payment (and hand-limit excess) goes face up onto the Bench, where anyone can take it.
3. **Apprentice** - a player with strictly the fewest workshop cards gathers 3 instead of 2.

Timing and edge cases:
- **Order inside a Build** is fixed: choose, find train, cost, legality check, place, Gears take, pay. Spades reduce the cost of the build they are part of; they never give cards or refunds. Gears take before you pay, so you can never take back the cards you pay this turn.
- **Trains are counted at the moment of the build.** Cards built later that join two trains make one bigger train for later builds. Trains never break: built cards never leave the workshop.
- **Same rank:** any number of players may have the same rank in their workshops; one player may not have it twice. A card whose rank you already built can still be paid or kept.
- **Empty Bench during Gather:** take from the deck. **Empty deck:** you may not pick it; Bench refills stop.
- **No simultaneous effects:** everything happens on the active player's turn, one step at a time.
- **Public information:** all workshops and the Bench are face up; hand sizes are public; the deck is not.

## 6. End of game and scoring

**The clock strikes** at step 4 of End of turn if either is true:
- the active player now has at least the **target** number of workshop cards: **9 cards with 4 players, 10 with 3 players, 11 with 2 players or solo**; or
- the deck is empty.

**Multiplayer:** once the clock strikes, finish the round: players keep taking turns until the player on the first player's right has finished a turn, so everyone has had the same number of turns. (If the clock strikes on that player's turn, the game ends at once.) These final turns are normal; the clock is not checked again; refills simply stop if the deck is empty. Then score.

**Scoring** (count each player's workshop; cards in hand and on the Bench score nothing):
| Card in your workshop | Points |
|---|---|
| Each Spade | 1 |
| Each Club | 1 |
| Each Diamond | 3 |
| Each Heart | 1 + the number of different suits (Spades, Clubs, Diamonds, Hearts) among the cards of its train, Hearts included: 2 to 5 |

Example: train 4S-5H-6C-7H plus a lone QD. Each Heart scores 1 + 3 (Spades, Hearts, Clubs) = 4. Total 1 + 4 + 1 + 4 + 3 = 13.

**Winner:** highest score. **Tiebreaker 1:** more workshop cards. **Tiebreaker 2:** longest train (most cards). **Still tied:** shared win.

### Solo mode
Use all the rules above with these changes:
- Setup as normal with one player (hand of 3, Bench of 5). The Apprentice rule never applies.
- **The Rival clockmaker:** at End of turn step 2, the Rival removes the **highest-ranked card** on the Bench from the game (ties: the leftmost of those cards). Put it face down in a Rival pile; it never returns. If the Bench is empty, the Rival takes nothing.
- The clock strikes when you have **11 workshop cards** or the deck is empty; the game ends **immediately** at that point.
- Score as normal and read the ladder. **You win at 22 points or more.**

| Score | Title |
|---|---|
| 0-17 | Tinkerer |
| 18-21 | Apprentice |
| 22-25 | Journeyman (win) |
| 26-29 | Master (win) |
| 30+ | Grandmaster (win) |

## 7. Design notes

**The twist: gear trains.** A card's power is not printed on it; it comes from where it sits in the deck's own structure. Ranks decide what a card joins, suits decide what the joined train does. A Spade Four is a weak part on its own and a strong one in the middle of a five-card train, because it discounts every later build that joins that train. A Club in a long train pulls a card off the Bench every time that train grows. Builds compound: the longer and better-mixed your train, the cheaper and more productive each new card becomes, which gives the game a real engine arc on a deck everyone owns.

**Every suit has a job, every rank has a use.**
- *Spades* make builds cheap (engine, cost). *Clubs* bring parts in (engine, cards). *Diamonds* are flat points that fit anywhere (safe, late). *Hearts* reward mixed trains: up to 5 points when their train holds all four suits, only 2 in a pure-Heart train. Hearts want engine cards beside them; that is the main build-order puzzle.
- *Low ranks* are cheap to build but poor money. *High ranks* are expensive to build but the best money (a King pays for anything). The workshop target (9-11 different ranks) forces everyone to climb into the expensive ranks late, which is where Spade discounts pay off. A card you cannot build (rank already in your workshop) is still payment, so no card is dead.

**Interaction, not parallel solitaire.** The Bench is shared and public: you Gather the 7 a rival needs to close a gap, Gears snatch the best parts, and every payment hands parts to the next player. Paying with a King is efficient but gifts a King; paying 4 + 5 keeps the King but costs two cards. The clock is a race: a rushing engine player can end the game before the point-builders finish, so everyone watches workshop counts.

**Catch-up and tension.** Apprentice gives the player furthest behind on builds a 50% bigger Gather. Points are scored only at the end and mostly depend on how trains finish (a late card that joins two trains can lift several Hearts at once), so the visible leader is not locked in. Finishing the round keeps turns equal.

**Strategies to expect.** (1) *Engine first:* two or three Spades and a Club in one train, then cheap builds every turn. (2) *Jewel rush:* cheap Diamonds early, Gather a lot, take the Apprentice bonus. (3) *Clock faces:* one long mixed train with Hearts in it, built carefully for 4-5 points per Heart. The race target makes (1) end the game fast and (3) risky.

**Length.** Builds take about 25 seconds, Gathers about 10. A player needs roughly 15-17 turns to reach the target, so about 55-65 turns at 4 players is about 18-22 minutes.

**Tuning knobs for the playtester** (change one at a time): Spade discount (2-4); Diamond points (2-4); clock target (plus or minus 1); hand limit (6-8); starting hand by seat (seat 3 and 4 start with 4 cards) if seat gap exceeds 5; solo win line (set so a strategic bot wins about 50%).

**Bot hints for simulation.**
- *Build evaluation:* for each legal build, value = end points it adds now (including the Heart increase for every Heart whose train it joins or mixes) + 1.5 per Spade and 1.2 per Club it adds to a train of 2+ cards + 0.5 per card in the train it joins − 0.3 per payment card. Build the best if its value is above a Gather's value (about 2.5); otherwise Gather.
- *Gather:* take Bench cards that are legal builds extending your trains (prefer ones filling a one-rank gap), then the highest-ranked card; take the deck top only if no Bench card is worth it. Also take a card a rival needs to close a gap if nothing else is worth more than 1.
- *Pay:* choose the set with total at least the cost that has the fewest cards, then the lowest total; avoid paying ranks that would extend a rival's train.
- *Clock:* do not make the build that strikes the clock unless your score would be highest after the remaining turns (estimate rivals' gains as one build each).
- *Random bot:* choose uniformly among all legal actions, then uniformly among choices.

## 8. Changelog

**v1 (first design).** No revisions yet.
