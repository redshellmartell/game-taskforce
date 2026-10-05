# Pitch: Nine Fields (`grid-of-cards-area-control`)

## 1. Title and hook
**Nine Fields.** Nine drifting islands in a 3x3 grid, four explorers each. Crowd an island to its limit and the tide shoves its whole row or column, pushing one island off the edge of the world and into your pocket. Wait too long and a storm does it for you.

## 2. Stats
- Players: 3-4 recommended (2 playable, a known weaker mode)
- Play time: about 20 minutes
- Age: 10+
- Complexity: 2.5 / 5

## 3. Why it's worth making
Micro area-control on a tiny grid is a small but real niche, and the owner's focus is cards with few components. The brief scored it 24/30 (demand 3, gap 3, originality 4). The critic finds the flood-by-crowding plus quarter-turn axis swap unmatched among the comparables; the closest game, Contactics, is a low-similarity match.

## 4. How it plays
Each turn you do one action: land a pawn on an island or sail one to another. When an island is full, its trigger player makes a binary choice: cash the whole island now, or push the far end of its row or column off the edge and keep a locked prize turned to a new axis. If the board goes quiet for too many turns, a storm floods the fullest island for you. The game ends when the last island has been placed, and whoever holds the most claimed islands wins. Players trailing on trophies get the brakes in their favour: the fewest-trophies tiebreak and the storm direction choice.

## 5. Playtest highlights
- About 62,000 bot games on revision 1 across 2, 3 and 4 players. At 3-4 players every target passes: lead changes 3.15 and 3.28, early leader wins 55.5% and 48.9%, seat gap 2.6 and 2.7 points, length about 20 minutes, no stalls, no dead cards.
- Biggest fix (revision 1): a storm replaced the stall ending, the final tiebreak became seat-neutral, six rules gaps were closed with a worked example.
- A bot that deliberately stays low on trophies to steer the storm wins at or below a fair share, so the catch-up rule is not an exploit.
- Critic: PASS, average 3.83 (originality 4, clarity 4, fun 3, balance 4, market fit 3, production 5). Panel predicted fun 3.60; the Bar Raiser did not veto.

## 6. Remaining risks
- **Two players is the weaker mode:** early leader wins 66.4% at 10,000 games (target 65), about 24 minutes (target 20), and the storm fires about once per game, so it is effectively a 2-player rule. Expert 2-player play makes runaway worse. Pitched as a 3-4 player game with 2p flagged.
- **No human has played it at any count.** Bot play cannot test table talk, the feel of the direction choice at 3-4 players, or whether the quarter turn and axis swap are easy to read.
- **Family persona would not buy it (2.59)**, so market fit is 3.
- **Three small wording gaps** the critic flagged have been fixed in the rules (storm island need not be full, a storm flood can end the game, a shared win is possible in about 1-2.5% of games).
- **Fun and market fit rest on free bot scores,** not persona reviews or human tests.

## 7. Components
- 30 Island cards
- 16 pawns (4 in each of 4 colours)
- One rules card (nothing else needed; scores are kept as claimed cards)

## 8. Suggested next step for a physical prototype
Print or hand-make the 30 island cards (the card list is in the rules) and use coloured tokens for the 16 pawns. Play a 3-player game first, then a 2-player game, and record each session in `human-playtests.json` (fun, replay, clarity, player type). Watch the storm direction choice and whether the quarter turn is easy to read.
