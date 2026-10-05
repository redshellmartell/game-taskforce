# Fifty-Two Workshop - Rules (v2.1, revision 1 tuning pass)

## 1. Overview

- **Title:** Fifty-Two Workshop
- **Hook:** You are clockmakers sharing one workbench. Every card in a standard deck is a part, and a part's power comes from its neighbours. Build a card next to cards of adjacent rank and the whole **gear train** turns: Springs in it make the build cheaper and Gears in it pull parts off the shared Bench. Later you can **retool**: swap a part for a valuable Jewel or Clock face of the same rank before the parts run out.
- **Players:** 1-4 (solo mode at the end of section 6; solo is not yet balanced, see section 7)
- **Play time:** about 20 minutes at 4 players (about 12 at 2, 16 at 3, 10 solo)
- **Age:** 10+
- **Complexity:** 2 / 5

## 2. Components

One standard 52-card deck (no jokers) and one printed rule card. No tokens, no score pad.

**Rank values** (cost and payment): A = 1, 2-10 = face value, J = 11, Q = 12, K = 13.

**The 52 cards.** Each card appears once. Suit decides what a card does in your workshop; rank decides its cost, its payment value and which cards it connects with.

| Suit | Name | Ranks | Count | When its train turns (Build) | End points |
|---|---|---|---|---|---|
| Spades | Spring | A-K | 13 | This build costs **3** less | **2** |
| Clubs | Gear | A-K | 13 | Take 1 card from the Bench | 1 |
| Diamonds | Jewel | A-K | 13 | (nothing) | 3 |
| Hearts | Clock face | A-K | 13 | (nothing) | 1 + number of different suits in its train (2-5) |

Every card has three uses: build it, pay with it (worth its rank value), or keep it in hand. No card is ever dead.

**Rule card (1)** shows: rank values, the table above, the turn summary (Gather 2 *or* Build 1 / Retool 1; end of turn: hand limit 7, Bench back to 5, clock check), the clock rules and the solo ladder.

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
3. **Cost** = the new card's rank value minus **3 for each Spade in its train** (the new card included). Never below 0. In a Retool, a replaced Spade gives no discount.
4. **Legality:** the **other** cards in your hand must add up to at least the cost. Cards your Gears would take do not count. If not, you may not build that card.
5. **Place** the card in your workshop. For a Retool, put the replaced card face down on the **scrap pile**.
6. **The train turns:** for **each Club in the train** (the new card included; a replaced Club does not count), take 1 card from the Bench into your hand, one at a time; this is mandatory. If the Bench is empty take the deck's top card instead; if both are empty take nothing.
7. **Pay:** if the cost is above 0, choose hand cards whose rank values total **at least** the cost (cards just taken by Gears may be used) and place them face up on the right end of the Bench in any order. No change is given. If the cost is 0, pay nothing; you may not pay.

**Retool example.** Your workshop is 4S, 5S, 6C, 7D; you hold 6H, 9D and 3C. You build the 6H: a Retool of the 6C. Its train is 4S-5S-6H-7D (the 6C is ignored). Cost 6 - 3 - 3 = 0, so you pay nothing. No Club is left in the train, so the Gears take nothing. The 6C is scrapped. The 6C scored 1; the 6H scores 1 + 3 suits (Spades, Hearts, Diamonds) = 4, so your score rises by 3, and your workshop still holds 4 cards.

### End of turn (always, in this order)
1. **Hand limit:** if you hold more than 7 cards, put cards of your choice on the **scrap pile** until you hold 7. Any hand card may be scrapped, including cards your Gears took this turn.
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
1. **Gear trains:** a build turns the new card's whole train. Each Spade in it cuts the cost by 3; each Club in it takes a Bench card.
2. **Spent parts go to the Bench:** payment goes face up on the right end of the Bench, where anyone can take it. At end of turn the Bench always goes back to exactly 5 (oldest cards slide under the deck, or new cards are dealt).
3. **Retool:** you may build a card of a rank you already have; it replaces that card, which is scrapped. A Retool does not add to your workshop count. The replaced card has no effect on that build (no discount, no Gear pull).

Timing and edge cases:
- **Order inside a Build** is fixed: choose, train, cost, legality, place (and scrap the replaced card), Gears take, pay. Spades only reduce the cost of the build they are in; Gears take before you pay, so you can never take back the cards you pay this turn.
- **Trains are counted at the moment of the build.** A later card that joins two trains makes one bigger train. Trains never break by normal builds; a Retool keeps the train intact because the new card has the same rank.
- **Same rank across players** is fine: any number of players may have a 7.
- **Hand limit** is checked only at End of turn step 1, after the action and payment.
- **Empty Bench during Gather or Gears:** take from the deck. **Empty deck:** it cannot be picked and refills stop. A card slid under an empty deck makes the deck non-empty again, so the clock does not strike that turn (the deck is checked after step 3).
- **Scrapped cards and Rival cards** never return and are not public in content.
- **Running score:** a player's score at any moment is what their workshop would score if the game ended now (section 6). It is public. (Simulation: lead changes are measured on running scores at the end of each full round.)
- **No simultaneous effects:** everything happens on the active player's turn, one step at a time.

## 6. End of game and scoring

**The clock strikes** at End of turn step 4 if either is true:
- the active player has at least **10 workshop cards (11 with 2 players)**; or
- the deck holds 0 cards (checked after step 3).

Once struck, the clock is never checked again.

**How games usually end.** At 4 players the deck normally runs out first (about 85% of simulated games, with players at 6-8 workshop cards); the card target is the early finish for a player who builds fast. At 2-3 players the card target almost always ends the game.

**Finish the round (multiplayer):** after the clock strikes, play continues until the last player in turn order (the player to the right of the first player) has finished a turn; then the game ends. If the clock strikes on that player's turn, the game ends at once. Every player therefore has the same number of turns. The final turns are normal.

**Scoring** (workshop only; hands, Bench, deck and scrap score nothing):
| Card in your workshop | Points |
|---|---|
| Each Spade | 2 |
| Each Club | 1 |
| Each Diamond | 3 |
| Each Heart | 1 + the number of different suits among the cards of its train, Hearts included (2 to 5) |

Example: train 4S-5H-6C-7H plus a lone QD. Each Heart scores 1 + 3 (Spades, Hearts, Clubs) = 4. Total 2 + 4 + 1 + 4 + 3 = 14.

**Winner:** highest score. **Tiebreaker 1:** more workshop cards. **Tiebreaker 2:** longest train (most cards). **Still tied:** shared win.

### Solo mode
All the rules above apply, with these changes:
- Setup as normal for one player.
- **The Rival** acts at End of turn step 2: it takes the **two highest-ranked** Bench cards (equal ranks: the leftmost first). The **higher** one goes face down on the **Rival pile**; the other goes face down at the **bottom of the deck**. If the Bench holds one card, it goes to the Rival pile; if none, the Rival does nothing.
- **The clock strikes** at step 4 when the Rival pile holds **24 cards**, or the deck holds 0 cards. The pile count is the rule; it is normally reached at the end of your 24th turn, later if the Rival found an empty Bench. The game ends at once. (The workshop-count trigger is not used in solo.)
- Score as normal and read the ladder. **You win at 40 points or more.**

| Score | Title |
|---|---|
| 0-31 | Tinkerer |
| 32-39 | Apprentice |
| 40-43 | Journeyman (win) |
| 44-47 | Master (win) |
| 48+ | Grandmaster (win) |

## 7. Design notes

**The twist: gear trains and retooling.** A card's power is not printed on it; it comes from where it sits in the deck's own order. Ranks decide what a card joins; suits decide what the train does. Spades and Clubs make builds cheaper and bring in parts; Retool lets a player swap a built card for a better-scoring one of the same rank, at the cost of a turn that does not move them toward the card target.

**What the data shows (honest description).** In bot play Spades are mostly spent as payment rather than built into engines: their win correlation stays slightly negative (-0.015 with discount 3 and 2 points, the best of the configurations tried). Bots rarely build trains longer than 3 and Retool about 0.4 times per game, yet Retool is worth about 8 points of strategic-over-greedy skill. The intended arc (build an engine, ride it, retool late) is **a hypothesis, untested with humans**; bots do not plan trains. The first human playtest should check whether players pursue it and enjoy it.

**Strategies to watch for in human play.**
1. *Engine:* Spades and a Club in one train early, cheap high-rank builds, then Retool into Diamonds and Hearts. Unproven.
2. *Jewel rush:* cheap Diamonds early, aiming at the card target (mainly at 2-3 players, where the target ends the game).
3. *Clock faces:* one long mixed train with Hearts. The Hearts-heavy persona bot wins most often in the panel.
4. *Spades as currency:* spend Spades as payment and build what pays now; this is what most bots do.
The key tension is **when to stop building outward and start retooling**: Retooling scores but does not advance the card target, and at 4 players the deck clock runs regardless.

**Interaction.** The Bench is shared: you Gather the rank a rival needs to close a gap, Gears snatch the best parts, and every payment hands parts to the next player (visible for at least a turn, then slid under the deck).

**Catch-up and tension.** Retooling makes scores jump late (a Spade becoming a 5-point Heart is +3). Finishing the round keeps turns equal. Measured: runaway leader 55/41/34% (2/3/4p); 4p lead changes 2.61 with this config.

**Stall-proof.** Every Gather with a full hand scraps cards; every Retool scraps a card; normal builds are limited to 13 per player. So the cards outside workshops strictly run down, the deck eventually empties and the clock strikes. No game can loop.

**Length.** Builds about 25 seconds, Gathers about 10. Measured 4p about 57 turns (about 18 minutes); at 4p the deck empties first in about 85% of games. Solo: 24 turns, about 7.5 minutes by formula; human solo time is unmeasured.

**Solo is not yet balanced.** At the old line of 31 strategic bots won 98.8% and greedy 97.4%. The new line of **40 is sized from score medians (strategic about 40, greedy about 38) and has not yet been re-simulated**, and those medians were measured before Spades were worth 2 points, so the line may need to rise again. Expected about 52% strategic, 40% greedy, near 0% random. Greedy close to strategic means solo still lacks pressure; that would need a new rule and is out of scope for this pass.

**Tuning knobs, in priority order** (change one at a time):
1. **Solo win line:** 40 (re-simulate first; move so strategic wins 45-55%); then **solo length:** Rival pile 24 (range 20-26).
2. **Spade discount / points:** 3 and 2 (tested alternative: 4 and 1).
3. **Gear Gather (0-cost Club pull):** off (tested: no gain).
4. **Clock target:** 10 (11 at 2p); try 9 at 4p only if the card target should end more 4p games.
5. **Heart scoring:** 1 + suits (2-5), or number of suits only (1-4) if Hearts keep the top win correlation.
6. **Hand limit:** 7 (range 6-8).
7. **Last-seat start:** seats 3 and 4 start with 4 cards, only if the seat gap goes above 5.

**Bot hints for simulation.**
- *Build value:* end points it adds now (running-score change, including Heart changes in its train) + 1.5 per Spade and 1.2 per Club it adds to a train of 2+ cards + 0.5 per card in the train it joins - 0.3 per payment card. Retool value: running-score change - (1.5 per Spade or 1.2 per Club removed, scaled by the share of the game left: builds-to-target remaining / target). Build the best if its value is above a Gather's (about 2.5); otherwise Gather.
- *Gather:* take Bench cards that are legal builds extending your trains (prefer filling a one-rank gap), then Diamonds or Hearts matching ranks of your Spades or Clubs (Retool targets), then the highest rank; take the deck top only if no Bench card is worth it. Take a card a rival needs to close a gap if nothing else is worth more than 1.
- *Pay:* fewest cards, then lowest total; avoid paying ranks that would extend a rival's train.
- *Clock:* do not make the build that strikes the clock unless your score would be highest after the remaining turns (estimate one build each for rivals).
- *Hand limit:* scrap the lowest-value cards (lowest rank that is not a build or Retool candidate).
- *Random bot:* choose uniformly among all legal actions, then uniformly among choices.

## 8. Changelog

**v2.1 (revision 1 tuning pass).** Answers critique.md (REVISE-MINOR, required edits 1-5). No new rules or mechanics.

### Revision notes (v2.1)

| # | Change | Why (feedback) | KPI effect |
|---|---|---|---|
| 1 | Spade discount 4 -> **3**, Spade points 1 -> **2**. | Critic edit 1; playtest config table | Tested: strategic v greedy 61.2% (target 60), 4p lead changes 2.61 (target 2.5); Spade correlation -0.015 (still below 0) |
| 2 | Solo win line 31 -> **40**, ladder rescaled. | Critic edit 2; playtest problem 1 (98.8% solo wins) | **Not yet re-simulated**; expected strategic about 52% |
| 3 | Section 6 states that 4p games normally end on an empty deck (85%), the card target being the early finish. | Critic edit 3; playtest problem 4 | Clarity |
| 4 | Four ambiguities closed: a replaced Spade or Club has no effect in a Retool; hand-limit scrap may take cards Gears took; solo end is the Rival-pile count; a trimmed card refilling an empty deck prevents the strike that turn. Retool worked example added. | Critic edit 4; playtest ambiguity list | Zero known ambiguities |
| 5 | "Engine first is strongest" removed; engine described as an untested hypothesis, Spades as mostly currency. | Critic edit 5; playtest problem 2 | Honest pitch |

**v2 (revision 1).** Answered critique.md (REVISE-MAJOR) and playtest-report.md (NEEDS-FIXES): Spade discount 3 -> 4; solo rebuilt (Rival takes the 2 highest Bench cards, 24 turns, win line 31); stall breaker (hand-limit excess scrapped, Bench back to exactly 5); 11 ambiguities resolved and Apprentice cut; Retool added as special rule 3; clock target 10 at 3-4p, 11 at 2p.

**Open issue for the Director:** the solo time target of 15 minutes cannot be met by the 25 s / 10 s formula within one 52-card deck (it would need about 45 solo turns). Recommend resetting the solo target to 10 minutes or checking it with a human solo game.

**v1 (first design).** Initial rules.
