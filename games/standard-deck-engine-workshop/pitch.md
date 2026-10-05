# Pitch: Fifty-Two Workshop (`standard-deck-engine-workshop`)

## 1. Title and hook
**Fifty-Two Workshop.** You are clockmakers sharing one workbench, and every card in a standard 52-card deck is a part. Build a card next to cards of adjacent rank and the whole gear train turns: Springs make builds cheaper, Gears pull parts off the shared Bench, and later you can retool a part for a valuable Jewel or Clock face. It needs nothing but a deck of cards and one printed rule card.

## 2. Stats
- Players: 2-4 recommended (1-player mode included but unproven)
- Play time: about 12 minutes at 2 players, 16 at 3, 20 at 4 (solo about 10)
- Age: 10+
- Complexity: 2 / 5

## 3. Why it's worth making
Setup time is named as board gaming's top barrier to getting games played, and small-box, solo-capable games are growing. This one needs **no custom components at all**: any standard deck plus a printed rule card. The brief scored 27/30 (owner fit 5, producibility 5, simulatability 5). Engine building is usually tied to custom card powers; here the powers come from rank and suit. The closest comparable is Sprawlopolis (low similarity).

## 4. How it plays
On your turn you either gather 2 cards (from a shared face-up row of 5 called the Bench, or blind from the deck) or build 1 card into your workshop. A build costs the card's rank, paid with hand cards whose ranks add up to at least that cost; spent cards go to the Bench, so payments feed your rivals. Built cards with consecutive ranks form a gear train. Spades take 3 off a build's cost and score 2 points, Clubs take a Bench card, Diamonds score 3 and Hearts score 1 plus the number of different suits in their train. Retool lets you build a rank you already have, scrapping the old card. The game ends when one player reaches 9, 10 or 11 workshop cards (4, 3 or 2 players) or the deck runs out, which happens in about 85% of 4-player games.

## 5. Playtest highlights
- Revision 1: 62,000 headline games with no turn-cap hits and no bot patching.
- Multiplayer passes: seat gap about 1 point, strategic beats random by 68 points, runaway leader 55% / 41% / 34% at 2 / 3 / 4 players, 4-player game about 17.7 minutes, 0 dead cards, lead changes 2.1 to 2.6.
- Biggest fixes: a guaranteed game end (the first draft could stall forever), the Spade buff, Retool as a mid-game decision (worth about 8 skill points), 15 rule ambiguities closed.
- Critic: REVISE-MINOR, average 3.67 (up from 3.17); recommends pitching it as a multiplayer game with solo flagged.

## 6. Remaining risks
- **The engine arc is unproven.** Spade correlation was negative in every configuration the bots tried, Spades are mostly spent as payment, and Retool is used only 0.4 times per game. Only human play can show whether building an engine feels rewarding.
- **Solo is unbalanced and unmeasured.** It was a free win at 98.8% in testing; the win line was raised from 31 to 40 but not re-simulated, and the target length (about 10 minutes) is shorter than the brief's 15.
- **Strategic beats greedy only about 59 to 61%,** so skill is shallower than the 60%+ target aims for.
- **The Family persona's predicted fun is 2.96** (overall panel fun 3.93).
- **4-player ties are 10-13%.**
- **Originality was not re-searched** (BoardGameGeek not checked); fun and market fit rest on free bot scores, not human play.

## 7. Components
- 1 standard 52-card deck (no jokers)
- 1 printed rule card

## 8. Suggested next step for a physical prototype
Print the rule card and use any deck of cards. Play a 3-player game and a 4-player game first, then a 2-player game, and record each session in `human-playtests.json` (fun, replay, clarity, player type). Watch whether the gear-train arithmetic is quick to read, whether anyone builds Spades on purpose, and whether Retool ever gets used. Time a solo game with a stopwatch.
