# Tug of Crowns - Rules (v1)

## 1. Overview

- **Title:** Tug of Crowns
- **Hook:** Two rival court advisors, the steady Treasurer and the sly Whisperer, bid cards in a series of audiences to drag one crown along a shifting court toward their own throne. The court itself fights back: the closer the crown gets to one throne, the harder the court resists.
- **Players:** 2 (one plays the Treasurer, one plays the Whisperer)
- **Play time:** about 15 minutes (7 rounds at most)
- **Age:** 12+
- **Complexity:** 2/5

## 2. Components

49 cards in total. No dice, no board, no tokens required.

- 20 Treasurer cards (gold backs)
- 20 Whisperer cards (violet backs)
- 9 Court track cards
- 2 side reference cards (half A5 each) - optional; their text is the "Side rules" in section 5. They are not part of any deck.

The crown's position is shown by turning the track card it occupies sideways (90 degrees). Any coin may be used as a crown marker instead; it changes nothing.

Each deck card shows a name, an **Influence** value (a whole number) and up to two **keywords**. Keywords are explained in section 4.4.

### 2.1 Treasurer deck (20 cards)

| Card | Copies | Influence | Keywords |
|---|---|---|---|
| Tax Collector | 4 | 2 | Bank |
| Granary | 2 | 3 | Bank |
| Ledger | 3 | 3 | Steady |
| Gold Purse | 3 | 4 | - |
| Mint Master | 2 | 5 | - |
| Royal Loan | 2 | 1 | Spend 2 |
| Patron | 2 | 2 | Spend 1, Steady |
| Treasury Vault | 1 | 1 | Spend 3, Steady |
| Chancellor's Seal | 1 | 6 | Steady |

Totals: 20 cards, printed Influence 58; 6 Bank cards, 7 Steady cards, 5 Spend cards (up to 9 coins spendable).

### 2.2 Whisperer deck (20 cards)

| Card | Copies | Influence | Keywords |
|---|---|---|---|
| Gossip | 4 | 1 | Echo |
| Shadow Envoy | 1 | 2 | Echo, Retort |
| Courtier | 3 | 3 | - |
| Spymaster | 2 | 4 | - |
| Silencer | 3 | 1 | Hush |
| The Whisper | 1 | 5 | Hush |
| False Witness | 2 | 1 | Hush, Retort |
| Eavesdropper | 2 | 2 | Retort |
| Veiled Threat | 2 | 3 | Retort |

Totals: 20 cards, printed Influence 42; 5 Echo cards, 6 Hush cards, 7 Retort cards.

### 2.3 Court track (9 cards)

Positions are numbered from the Treasurer's end to the Whisperer's end. "Leader" means the player whose half the crown is in; "trailer" means the other player. At position 0 there is no leader or trailer.

| Position | Card | Court rule while the crown is here |
|---|---|---|
| T4 | Treasurer's Throne | Treasurer wins immediately when the crown arrives here. |
| T3 | Gates of the Throne | Trailer draws 2 extra cards at round start. Leader needs a margin of 3 or more to win a round. |
| T2 | Divided Court | Trailer draws 1 extra card at round start. Leader needs a margin of 2 or more to win a round. |
| T1 | Murmurs | Trailer draws 1 extra card at round start. |
| 0 | Empty Throne | No rule. |
| W1 | Murmurs | Trailer draws 1 extra card at round start. |
| W2 | Divided Court | Trailer draws 1 extra card at round start. Leader needs a margin of 2 or more to win a round. |
| W3 | Gates of the Throne | Trailer draws 2 extra cards at round start. Leader needs a margin of 3 or more to win a round. |
| W4 | Whisperer's Throne | Whisperer wins immediately when the crown arrives here. |

The track is exactly symmetric: each side's cards are mirror images.

## 3. Setup

1. Lay the 9 track cards in a row in the order T4, T3, T2, T1, 0, W1, W2, W3, W4. The Treasurer sits at the T4 end, the Whisperer at the W4 end.
2. Turn the position 0 card (Empty Throne) sideways: the crown starts there.
3. Decide who plays which side (players choose, or one player shuffles the two reference cards face down and the other picks one).
4. Each player shuffles their own 20-card deck and places it face down as their draw pile.
5. Each player draws 6 cards. Hands are hidden from the opponent; hand sizes are public.
6. Each player leaves room next to the track for their **contest row** (cards played this round) and a **discard pile**. The Treasurer also leaves room for a face-down **Treasury** (starts empty).
7. Begin round 1. The round counter starts at 1 (players track it aloud or by the number of rounds played; the game lasts at most 7 rounds).

## 4. Turn structure

The game is played in **rounds** (up to 7). Each round has four phases in this order.

### 4.1 Phase 1: Draw

- Round 1: skip this phase (players already have 6 cards).
- Rounds 2-7: each player draws 2 cards from their own draw pile. Then the trailer (if any) draws the extra cards given by the court rule of the crown's current position (1 at positions 1 and 2, 2 at position 3).
- If a draw pile is empty, that player draws as many as remain and the rest are lost. Discard piles are never reshuffled.
- There is no hand limit.

### 4.2 Phase 2: Choose the lead

- One player, the **chooser**, decides who takes the first turn of the contest (the **lead**). The chooser may pick themselves or the opponent.
- Round 1: the Treasurer is the chooser.
- Later rounds: the player who lost the previous round is the chooser. If the previous round was tied, the chooser is the same player who chose in the previous round.

### 4.3 Phase 3: Contest

Players alternate turns, starting with the lead. On your turn you must do exactly one of these:

- **Play a card:** place one card from your hand face up in your contest row. Resolve its keywords (section 4.4) immediately.
- **Pass:** you take no more turns this round. A player with no cards in hand must pass.

Once a player has passed, the other player keeps taking turns alone (one card per turn) until they also pass. The contest ends as soon as both players have passed.

Exception: the Whisperer's **Retort** keyword (section 4.4) lets the Whisperer play after passing.

### 4.4 Keywords

Treasurer keywords:

- **Steady** - This card cannot be chosen as the target of a Hush.
- **Bank** - In Phase 4 (Cleanup), this card goes face down into the Treasury instead of the discard pile (even if it was Hushed). Each card in the Treasury is one **coin**; its face no longer matters. The Treasury holds at most 3 cards; if it is full, the extra Bank card is discarded instead.
- **Spend X** - When you play this card, you may discard 0 to X cards from your Treasury to your discard pile. This card gains +2 Influence for each card discarded this way, for this round. You choose the number when you play the card; it cannot be changed later.

Whisperer keywords:

- **Hush** - When you play this card, choose one card in the Treasurer's contest row that is not Steady and not already Hushed. Turn it sideways: its Influence is 0 for the rest of the round, including any Spend bonus. If there is no legal target, Hush has no effect (the card still counts its own Influence).
- **Retort** - If you have already passed this round, then immediately after the Treasurer plays a card (and its keywords resolve) you may play one Retort card from your hand to your contest row, resolving its keywords. You remain passed. At most one Retort may be played after each Treasurer card. A Retort card may also be played normally on your turn before you pass.
- **Echo** - In Phase 4 (Cleanup), if the Whisperer did **not** win this round (lost or tied), this card returns to the Whisperer's hand instead of the discard pile.

### 4.5 Phase 4: Resolve and cleanup

1. **Totals.** Each player adds up the Influence of all cards in their contest row (Hushed cards count 0; Spend bonuses count). An empty row totals 0.
2. **Margin.** Margin = higher total minus lower total.
3. **Round winner.** The player with the higher total wins the round, unless they are the leader and the court rule of the crown's current position requires a larger margin (2 at position 2, 3 at position 3); then the round is **tied**. Equal totals are also a tie. The trailer and players at position 0 need only a margin of 1.
4. **Move the crown.** If there is a winner, move the crown toward the winner's throne by **1 position if the margin is 1-4**, or **2 positions if the margin is 5 or more**. On a tie, the crown does not move. Turn the new position's card sideways and straighten the old one.
5. **Throne check.** If the crown reached T4 or W4, that player wins immediately; the game ends.
6. **Cleanup.** Bank cards go to the Treasury (in any order the Treasurer chooses, up to the cap). Echo cards return to the Whisperer's hand if the Whisperer did not win. All other contest cards go to their owners' discard piles. Straighten Hushed cards as they leave.
7. If this was round 7, the game ends (section 6). Otherwise begin the next round.

## 5. Special rules and timing

### Side rules (the text on each half-A5 reference card)

**Treasurer - "Coin wins the court."** Keywords: Steady, Bank, Spend X (as in 4.4). Treasury: at most 3 face-down coins; its size is public.

**Whisperer - "A word in the right ear."** Keywords: Hush, Retort, Echo (as in 4.4).

### Timing and conflicts

- **Order inside a play:** the card enters the contest row, then its keywords resolve in the order printed (Spend is chosen on entry; Hush picks its target on entry; Retort only governs when the card can be played).
- **A Retorted Hush:** after the Treasurer plays a card, a passed Whisperer may Retort with False Witness and Hush that same card, if it is not Steady. Play then returns to the Treasurer, who may keep playing or pass.
- **Retorts and the end of the contest:** a Retort can only follow a Treasurer card. Once the Treasurer passes, no more Retorts are possible and the contest ends (provided the Whisperer has already passed).
- **Hush targets** can only be cards already in the Treasurer's contest row. A Hush never affects cards played later.
- **Court rules** are read from the crown's position at the moment they apply: extra draws use the position at the start of Phase 1; the margin requirement uses the position at the start of Phase 4 (the crown cannot move during a contest).
- **Empty draw pile:** draw what remains; the game still continues to round 7. A player with an empty hand simply passes.
- **Empty Treasury:** Spend cards can still be played; they just get no bonus.
- **Hidden and public information:** hands and draw piles are hidden. Contest rows, discard piles, hand sizes, draw pile sizes and Treasury size are public. Players may look through any discard pile at any time.
- **Randomness:** the only random element is the shuffle of each deck at setup.

## 6. End of game and scoring

The game ends at the first of these:

1. **Throne:** the crown reaches T4 (Treasurer wins) or W4 (Whisperer wins) in Phase 4, step 5.
2. **Round 7 ends:** the leader (the player whose half the crown is in) wins.

**Tiebreaker (crown on position 0 after round 7):** the player who won the most recent round that moved the crown wins. If no round moved the crown, the Treasurer wins (this situation should be close to impossible; the playtester should report how often it happens).

There are no points; the result is a win or a loss.

## 7. Design notes

### Intended play and tensions

- **Every turn is an auction step.** Playing a card raises your bid; passing locks your bid. The player who passes second gets the last word but has to spend cards to win. The core decision every turn: commit another card now, or save it for a round that matters more? Winning by exactly enough is efficient; winning by 5 or more moves the crown twice, which is the only fast way to a throne.
- **Treasurer (steady, resources).** High raw Influence (58 printed vs 42). Bank cards turn into coins that pay for big Spend plays later, so the Treasurer plans a round or two ahead. Steady cards are the safe bids when the Whisperer is holding Hushes. Main tension: dump coins into a Spend card (strong, but non-Steady Royal Loans can be Hushed and lose the coins) or play safe Steady cards.
- **Whisperer (tricky, reactive).** Low raw Influence, but Hush deletes Treasurer cards and Retort lets the Whisperer pass as a bluff and strike back after the Treasurer commits. Echo cards come back after a lost round, so the Whisperer can afford to throw cheap rounds and fight the important ones. Main tension: pass early to set up Retorts (risking that the Treasurer simply wins cheaply), or fight on your turn.
- **Reading the opponent:** both sides can count the other's discard pile, so late rounds reward remembering what is left (for example, "the Whisper and both False Witnesses are gone, so my Royal Loan is safe now").

### The twist: the court fights back

The 9 track cards are not just spaces. The closer the crown gets to one throne, the more the court helps the trailer: extra draws, and the leader needs a bigger margin to move the crown. Pulling the crown back toward the center is easy; pushing the last step needs one decisive round, and it usually takes a 2-step push (margin 5+) or a margin of 3+ at the gates. This creates built-in catch-up and lead changes without any side-specific rule, so the track never adds asymmetry to balance.

### Balance approach: symmetric power, asymmetric means

Both decks are built to the same budget: about 60 "effective Influence" over a game. The Treasurer's is mostly printed (58) plus coin conversions (each Bank card is worth about +2 later, about +8 to +12 per game in practice). The Whisperer's is 42 printed plus Hush (6 cards that each remove about 3 Influence when a target exists) plus Echo recycling (cheap cards reused in lost rounds) plus the timing advantage of Retort. The track, setup and round structure are identical for both sides.

**Balance levers, in the order we suggest tuning them** (each moves one side by roughly 1-3 win-rate points per step; change one at a time):

1. **Spend bonus per coin** (+2). Going to +1 weakens the Treasurer a lot; it is the coarse lever.
2. **Treasury cap** (3). Raising to 4 helps the Treasurer; lowering to 2 hurts it.
3. **Number of Steady cards** (7). Moving the Steady keyword on or off one Ledger (3 copies) changes how many Hush targets exist.
4. **Hush count** (6). Swap one Silencer for a Courtier (or back).
5. **Echo condition** ("did not win"). Changing it to "lost" (not on ties) weakens the Whisperer; "always" strengthens it a lot.
6. **Single-card values (fine tuning):** Gold Purse (Treasurer, 4) and Courtier (Whisperer, 3) are the designated plus-or-minus-1 dials; each step changes that deck's printed total by 3.
7. **Round 1 chooser** (Treasurer) and the **position-0 tiebreaker** (Treasurer): flip to the Whisperer if the Treasurer is ahead by a point or two.
8. **Court strength** (shared): the extra draws at positions 1-3 and the margin requirements (2 and 3). Raise them if leaders run away; lower them if too many games end at position 0 or the crown stalls.

### Notes for the playtester (bot coding)

- **Legal actions on a turn:** pass, or play any card in hand; for Spend, choose 0 to min(X, Treasury size) coins; for Hush, choose one legal target (or none if there is none). After each Treasurer play, a passed Whisperer has the extra choice "Retort with card R, or decline".
- **Lead change:** count one each time the crown moves from one half to the other (T-side to W-side or back). Landing on position 0 does not count; a move from T1 through 0 to W1 in one push counts as one.
- **Suggested simple strategic heuristic:** keep a target margin for the round (the minimum needed, or 5 if a 2-step push wins the game or crosses the center), play the cheapest card that keeps you at or above it, and pass otherwise; save Hush and Spend cards for rounds where the crown is at position 2 or 3.
- **Watch for:** Whisperer win rate by number of Hush targets available; how often the crown sits at position 0 after round 7; average rounds played (target 6-7 with some throne wins).

## 8. Changelog

- v1 (2026-10-04): first version from the brief.
