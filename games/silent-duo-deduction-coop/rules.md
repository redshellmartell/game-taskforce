# Silent Duo - Rules v1

## 1. Overview

- **Title:** Silent Duo
- **Hook:** Two lighthouse keepers guide ships through the fog without saying a word. You can see the ships off your partner's rocks but not your own, and the only way to tell your partner where a ship is: hand over two of your own lamps in the dark and let fate pick which one shines. Every lamp you spend on a signal is a lamp you can no longer use to guide your own ships.
- **Players:** 2-3 (best at 2). Fully co-operative: the team wins or loses together.
- **Play time:** about 20 minutes (about 26-28 turns).
- **Age:** 10+. **Complexity:** 2.5 / 5.

## 2. Components

| Item | Count | Details |
|---|---|---|
| Lamp cards | 50 | Values 1 to 10, five copies of each value. No other markings (art only). |
| Reference cards | 2 | Turn summary (no game function). |
| Reef tokens | 3 | Identical tokens. Start on the "safe" side; one is flipped to its "wrecked" side for each missed light. |

**Lamp card list**

| Value | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Copies | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

Lamp cards serve four roles during play, depending on where they are:

- **Ship** - a face-down card in front of a player; its value is the hidden number that player must find.
- **Hand card** - a card held by a player.
- **Fog pile** - face-down cards set aside at setup (nobody looks); a time reserve that Beacons can bring back.
- **Draw deck** - the night clock. Every turn uses up one card.
- **Night pile** - face-down cards discarded by the Trim action (nobody looks).

Total: 52 cards and 3 tokens. No board, no dice.

## 3. Setup

1. **Choose a difficulty** by setting the Fog size F: Calm F = 4, Standard F = 8, Storm F = 12. (Standard is the default and the playtest target.)
2. Shuffle all 50 Lamp cards face-down.
3. **Deal ships.** With 2 players, deal 3 cards face-down in a row in front of each player. With 3 players, deal 2 cards to each player. These are that player's **ships**. Number each player's ships from left to right as seen by their owner (Ship 1, Ship 2, Ship 3). **An owner may never look at their own ships.** Every other player may look at them now and at any time during the game (lift the card toward yourself, keeping it hidden from its owner).
4. **Deal the Fog pile.** Deal F cards face-down to one side, without anyone looking.
5. **Deal hands.** With 2 players, 5 cards each. With 3 players, 4 cards each. Players look at their own hand.
6. The remaining cards are the **draw deck**, face-down (2 players, Standard: 26 cards; 3 players, Standard: 24 cards).
7. Put the 3 Reef tokens safe side up in the middle.
8. Choose the first player at random. Play passes clockwise.
9. **From now on the Silence rule applies** (see section 5.1).

Each ship has two signal rows next to it: the **Low row** on the owner's left and the **High row** on the owner's right.

## 4. Turn structure

On your turn, do exactly these phases in order.

### Phase 1: Choose and resolve exactly one action

You must take one of the three actions below if any is legal. You may **Pass** only if none of the three is legal.

**A. Offer (signal a ship)**
- **Target:** one unlit ship that is *not* yours (so you can see its value V).
- **Cost:** choose exactly **two** cards from your hand that meet both conditions:
  - the two cards have **different values** from each other, and
  - **neither** card's value equals V.
- Place the two cards face-down beside the target ship.
- **Random reveal:** the ship's owner (who cannot see V) picks up both face-down cards, shuffles them out of sight (behind their back or under the table) and turns exactly one face-up. Each card has a 50% chance. (Programs: choose one of the two uniformly at random.)
- **Honest placement:** you (the offerer) place the revealed card in the target ship's **Low row** if its value is lower than V, or its **High row** if its value is higher than V. You have no choice; the side is fixed by the true comparison. (With 3 players, the third player may check.)
- The unrevealed card goes back into your hand face-down. Nobody but you learns its value.
- Meaning, guaranteed by the rules: V is strictly higher than every card in the ship's Low row, and strictly lower than every card in its High row.

**B. Light (guide one of your own ships)**
- **Target:** one of your own unlit ships.
- Play one card from your hand face-up onto it.
- **Resolver:** with 2 players, your partner; with 3 players, the player on your left. The resolver looks at the ship's value V and compares it with the played card's value C:
  - **|C - V| <= 1 (lit):** turn the ship face-up. It is **lit**. The played card stays on it. Both cards are out of play.
  - **C = V exactly (Beacon):** as lit, and also a **Beacon**: move the top 2 cards of the Fog pile (or all of them if fewer remain) face-down to the bottom of the draw deck, without looking at them. If the draw deck is already empty when the Beacon happens, the Beacon has no extra effect.
  - **|C - V| >= 2 (miss):** the resolver places the played card in that ship's Low row (if C < V) or High row (if C > V), exactly like a signal. Flip one Reef token to its wrecked side. If that was the **third** wrecked Reef, the team loses immediately.

**C. Trim (change your lamps in silence)**
- Legal only while the draw deck has at least 1 card.
- Discard one card from your hand face-down onto the Night pile. Nobody looks at it, ever.

**Pass** - only if no action above is legal. Do nothing.

### Phase 2: Draw

- After Offer, Light or Trim, draw 1 card from the draw deck (if it is empty, do not draw). Your hand size therefore stays constant until the deck runs out (the unrevealed Offer card returns to your hand, so an Offer costs you exactly one card).
- After a Pass, do not draw.

### Phase 3: Check the end

- If every ship is lit, the team wins immediately.
- If this turn emptied the draw deck, the **Last Watch** begins (see section 6).

## 5. Special rules and timing

### 5.1 The Silence rule (the communication model)

After setup step 9, players may not speak, write, gesture, time their plays on purpose, or otherwise communicate anything about cards, ships or plans. The only things that may be said are rules questions, "your turn", and the win or loss.

The **only channels of information** between players are these public events, all of which are visible to every player:

| Event | What every other player observes | What stays hidden |
|---|---|---|
| Offer | Who offered, which ship, the revealed card's value and its row (Low/High) | The unrevealed card's value |
| Light (lit) | Who, which ship, the card's value, the ship's value, whether it was a Beacon | Nothing |
| Light (miss) | Who, which ship, the card's value and its row; one Reef wrecked | The ship's exact value |
| Trim | Who trimmed | Which card was discarded |
| Pass | Who passed | - |
| Draw | Deck size, Fog pile size, Night pile size | The drawn card |

Each player additionally knows privately: their own hand, and the values of every ship that is not theirs. Nobody ever learns the values of their own unlit ships, the Fog pile, the Night pile, or another player's hand, except through the events above.

**Pre-game agreements.** Players may discuss strategy before setup step 9, but the rules give every play only one guaranteed meaning (the honest comparison above). The design (section 7) makes extra "code" meanings unreliable rather than banning them.

### 5.2 Legality checks

- An Offer is illegal if you hold fewer than two cards of different values that are both different from the target ship's value. If no target ship allows a legal Offer, you cannot Offer.
- A Light is illegal if you have no unlit ships or no cards in hand.
- Trim is illegal when the draw deck is empty or your hand is empty.
- Lit ships cannot be targeted by Offer or Light.
- Values may repeat among ships (five copies of each value exist).

### 5.3 Resolution details

- Signal rows only grow; cards in them are never removed or moved. A ship's possible values are always the integers strictly between the highest Low-row card (or 0 if empty) and the lowest High-row card (or 11 if empty).
- If a ship is lit, its signal rows stay on the table; they no longer matter.
- The resolver of a Light and the offerer in an Offer must follow the comparison exactly. There are no choices in resolving.
- With 3 players, an Offer on a ship is always resolved by that ship's owner (reveal) and the offerer (placement); a Light is resolved by the player on the lighter's left.
- Ties: none can arise (fully co-operative; all comparisons are strict or exact).
- Simultaneous effects: a Light that is both lit and the last unlit ship wins at once; the Beacon is irrelevant then. A miss that wrecks the third Reef ends the game at once, before drawing.

### 5.4 Empty decks

- **Draw deck empty:** no more draws; Trim becomes illegal; the Last Watch runs (section 6). A Beacon after the deck is empty has no extra effect (the Fog cards stay in the Fog pile).
- **Fog pile empty:** Beacons still light the ship but add no cards.
- A player whose hand becomes empty during the Last Watch can only Pass.

## 6. End of game and scoring

The game ends in exactly one of these ways:

1. **Win:** all ships are lit (checked immediately after each Light).
2. **Loss by reef:** the third Reef token is wrecked.
3. **Loss by dawn:** the draw deck becomes empty (a player draws its last card). This starts the **Last Watch**: each player, beginning with the next player clockwise, takes exactly one more turn (so the player who drew the last card takes the final turn). If any ship is still unlit after the Last Watch, the team loses.

Turn count reference (Standard, no Beacons): 2 players, 26 drawing turns + 2 Last Watch turns = 28 turns. 3 players, 24 + 3 = 27 turns.

**Score (for tracking and the simulation):** a win scores 10 + (cards left in the draw deck at the moment of winning). A loss scores the number of ships lit. There are no tiebreakers; the game is co-operative.

## 7. Design notes

### What the game is about

You hold the information your partner needs, and your partner holds the information you need. The core decision every turn is a three-way pull:

- **Offer** - spend a card to narrow down a partner's ship. You choose which ship and which two cards, but chance chooses which of the two is shown. Good offers use two cards that both say something useful (for a ship worth 7: offer a 5 and a 6, so either one shows "higher than 5" or "higher than 6"). Bad offers waste a card.
- **Light** - spend a card to guide your own ship, using what your partner has told you. Lighting only needs to be within 1, so a range of three values (for example "between 5 and 9", which means 6, 7 or 8) lets you play the middle value safely. Lighting earlier on a wider range risks a Reef.
- **Trim** - say nothing and change a card. Silence is information: a Trim tells your partner "I had no good offer and no safe light", which hints at what your hand lacks.

### The twist: signals are paid for with the lamps you need

The cards you signal with are the same cards you will need to light your own ships, and you don't yet know which values you will need. Spending your only 7 on a signal might be the right move, or it might strand your own Ship 2. On top of that comes the **double-lamp offer**: you choose two cards, chance picks one. It is new to the genre and does two jobs. It gives a hidden-information decision with real skill (choosing a pair where both cards are useful) and is the main anti-code device (below).

### Why a pre-agreed code cannot collapse the game

The brief's red flag is that "the card you play is the only signal" can turn into a fixed code. Silent Duo answers this structurally rather than by forbidding it:

1. **Every public play has one meaning guaranteed by the rules, and it is honest.** An offered card's row is fixed by the true comparison; a Light's result is fixed by the resolver. A code can only add meaning through *which* card and ship were chosen, never through how they are placed.
2. **The random reveal corrupts codes.** A code such as "the value I reveal on Ship 1 tells you Ship 2's value" only works if *both* offered cards carry the same coded message. Because the two cards must have different values, a coded message in one card is matched by noise in the other, chosen at random 50% of the time, and the receiver cannot tell which happened. Honest content is always true; coded content is wrong about half the time. Codes therefore lose to honest play over time.
3. **There is no free face-up play.** The only play without a forced meaning (Trim) is face-down, so it carries one bit at most ("I trimmed").
4. **Deliberately missing a Light as a code costs a Reef**, and only two Reefs can be spent before the third one loses. Each miss also burns a card and a turn.
5. **Even perfect information does not guarantee a win.** The lighter still has to hold a card within 1 of the ship, and with about 28 turns for 6 ships, card supply and timing remain a puzzle after everything is known.

Natural conventions such as "I offer cards close to the ship" or "I offer two cards on the same side" are allowed and intended. They only sharpen the honest content and reward reading your partner.

### Deduction depth

- **Interval narrowing** from signal rows (shown on the table).
- **Card counting:** there are five copies of each value. The ship values are drawn from the same deck, so visible ships, signals and lit cards tell you which values are scarce. Example: if you can see three 7s and hold two 7s, your own ship cannot be a 7.
- **Reading choices:** a revealed 3 in the Low row of a ship your partner could have signalled more tightly suggests they did not hold a 4, 5 or 6. Their other ships, and what they kept, tell you what they need.
- **Ships at the edges** (1, 2, 9, 10) can be pinned down by a single signal, and a Beacon (exact hit) buys two more turns from the Fog. That gives a real choice between lighting now on a range of three values and spending another turn to try for an exact hit.

### Balance and catch-up

- The game is co-operative with symmetric roles, so seat balance is not a factor. No player can dictate, because each player alone holds the values of their partner's ships.
- Tension curve: Reefs allow two risky lights. Beacons give back time to a team that plays precisely. The Last Watch makes the final round tense.
- Difficulty dial: Fog size F (4/8/12) controls the number of turns without changing any rule.

### Notes for the playtester (bot design and KPIs)

- **Bot observation** must be exactly the table in 5.1 plus that bot's private knowledge. The Offer reveal and all shuffles must use the RNG.
- Suggested bot tiers:
  - **Random:** a uniformly random legal action with random legal targets and cards.
  - **Honest:** tracks each own ship's possible range plus card counting. Lights the middle of the range when the range has 3 or fewer values (or 4 or fewer with 2 Reefs safe and 4 or fewer deck cards left). Otherwise Offers the pair that best narrows the partner's widest-range ship, preferring cards it does not need for its own likely values. Trims its least useful card when no offer narrows a range.
  - **Convention:** Honest plus agreed pair rules (for example, always offer two cards on the same side, as close to V as possible), with the receiver updating on that rule.
  - **Code attack:** a hat-guessing style code, where (revealed value + ship index) mod 10 encodes another ship's value, plus deliberate-miss codes, to test the red flag.
- **Targets:**
  - Honest or Convention bots at Standard win 40-60%.
  - Random wins at least 20 points less (expected under 5%).
  - The Code attack bot must **not** beat the best Honest or Convention bot by more than 10 points. If it does, the anti-code design has failed.
  - Average length is 26-28 turns (about 20 minutes).
- Seat balance and lead changes do not apply to a co-op game. Instead, report **lateness**: the share of wins with 3 or fewer deck cards left, and the share of losses with all but one ship lit. Both should be substantial (around 30% or more) for the game to feel close.
- **Tuning levers, in order:** Fog size F; the lighting tolerance (within 1); the number of Reefs; the Beacon bonus (2 cards).

## 8. Changelog

- v1 (2026-10-04): initial design from the brief. No revisions yet.
