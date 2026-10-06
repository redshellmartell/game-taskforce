# Silent Duo - Rules v2

## 1. Overview

- **Title:** Silent Duo
- **Hook:** Two lighthouse keepers guide ships through the fog without saying a word. You can see the ships off your partner's rocks but not your own, and the only way to tell your partner where a ship is: hand over two of your own lamps in the dark and let a flipped token pick which one shines. Every lamp you spend on a signal is a lamp you can no longer use to guide your own ships.
- **Players:** 2-3 (best at 2). Fully co-operative: the team wins or loses together.
- **Play time:** about 20 minutes (about 24-28 turns).
- **Age:** 10+. **Complexity:** 2.5 / 5.

## 2. Components

| Item | Count | Details |
|---|---|---|
| Lamp cards | 50 | Values 1 to 10, five copies of each value. No other markings (art only). |
| Reference cards | 2 | Turn summary (no game function). |
| Reef tokens | 2 | Identical tokens. Start on the "safe" side; one is flipped to its "wrecked" side for each missed light. |
| Reveal token | 1 | Two-sided: one side "Low" (moon), the other "High" (sun). Flipped like a coin for every Offer. |

**Lamp card list**

| Value | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Copies | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

Lamp cards serve five roles during play, depending on where they are:

- **Ship** - a face-down card in front of a player; its value is the hidden number that player must find.
- **Hand card** - a card held by a player.
- **Fog pile** - face-down cards set aside at setup (nobody looks); a time reserve that Beacons can bring back.
- **Draw deck** - the night clock.
- **Night pile** - face-down cards removed by Trim (only the trimmer has seen them; they never return).

Total: 52 cards and 3 tokens. No board, no dice.

## 3. Setup

1. **Choose a difficulty** by setting the Fog size F: Calm F = 4, Standard F = 8, Storm F = 12. Standard is the default for both 2 and 3 players (provisional; see 7.6).
2. Shuffle all 50 Lamp cards face-down.
3. **Deal ships.** With 2 players, deal 3 cards face-down in a row in front of each player. With 3 players, deal 2 cards to each player. These are that player's **ships**, numbered left to right as seen by their owner (Ship 1, Ship 2, Ship 3). **An owner may never look at their own ships.** Every other player may look at them now and at any time (lift the card toward yourself, keeping it hidden from its owner).
4. **Deal the Fog pile.** Deal F cards face-down to one side, without anyone looking.
5. **Deal hands.** With 2 players, 5 cards each. With 3 players, 4 cards each. Players look at their own hand.
6. The remaining cards are the **draw deck**, face-down (2 players: 34 - F cards, so 26 at Standard; 3 players: 32 - F cards, so 24 at Standard).
7. Put the 2 Reef tokens safe side up and the Reveal token in the middle.
8. Choose the first player at random. Play passes clockwise.
9. **From now on the Silence rule applies** (section 5.1).

Each ship has two signal rows next to it: the **Low row** on the owner's left and the **High row** on the owner's right.

**Open range.** For every unlit ship, let L be the highest card in its Low row (0 if empty) and H the lowest card in its High row (11 if empty). The ship's value is one of the integers strictly between L and H. L and H are public.

## 4. Turn structure

On your turn, do these phases in order.

### Phase 1: Take exactly one action

If at least one of the actions below is legal, you must take one of them (your choice). If none is legal, your turn is **skipped**: you do nothing, do not draw, and play passes on. (Before the draw deck is empty this cannot happen, because Trim is always legal then.)

**A. Offer (signal a ship)**
- **Target:** one unlit ship that is *not* yours (so you can see its value V).
- **Cost:** choose exactly **two** cards from your hand such that:
  - the two cards have **different values**,
  - **neither** value equals V, and
  - **both** values are **inside the ship's open range** (strictly greater than L and strictly less than H).
  So an Offer is only possible on a ship whose open range still holds at least 3 values.
- **Placement:** put both cards face-down beside the target ship, the **lower-value card on your left** and the higher-value card on your right.
- **Random reveal:** the ship's owner flips the Reveal token. "Low": you turn the lower card (left) face-up. "High": you turn the higher card (right) face-up. (Programs: choose the lower or higher card with probability 1/2 each.)
- **Honest placement:** you place the revealed card in the target ship's **Low row** if its value is lower than V, or its **High row** if it is higher. The side is fixed by the true comparison; you have no choice.
- The unrevealed card goes back into your hand without being shown. Everyone knows only that it was higher (if "Low" was flipped) or lower (if "High" was flipped) than the revealed card.
- Guaranteed meaning: V is strictly higher than every Low-row card and strictly lower than every High-row card, and every Offer narrows the open range.

**B. Light (guide one of your own ships)**
- **Target:** one of your own unlit ships.
- **Card:** play one card C from your hand face-up onto it. C must satisfy **L <= C <= H** for that ship (so C could light at least one value still in the open range). A card outside this window may not be played.
- **Resolver:** with 2 players, your partner; with 3 players, the player on your left (the third player may check). The resolver looks at V and compares:
  - **|C - V| <= 1 (lit):** the resolver turns the ship face-up. It is **lit**. The ship and C stay face-up in front of you for the rest of the game (public, out of play).
  - **C = V exactly (Beacon):** lit as above, and also a **Beacon**: move the top 2 cards of the Fog pile (all of them if fewer than 2 remain) face-down to the bottom of the draw deck, without looking. If the draw deck is empty at that moment (only possible during the Last Watch), the Beacon moves nothing.
  - **|C - V| >= 2 (miss):** the resolver places C in that ship's Low row (if C < V) or High row (if C > V). Flip one Reef token to wrecked. If both Reefs are now wrecked, the team loses immediately (no draw).

**C. Trim (change your lamps)**
- Legal only while the draw deck has at least 1 card.
- Discard one card from your hand face-down onto the Night pile, without showing it.
- Then (instead of the normal Phase 2 draw) draw **2** cards from the draw deck, keep 1, and put the other face-down on the Night pile without showing it. If the deck has only 1 card, draw it and keep it.

### Phase 2: Draw

- After an Offer or a Light (lit or miss, unless the game has ended), draw 1 card from the draw deck. If it is empty, do not draw.
- After a Trim, the draw was already done in the Trim action. After a skipped turn, do not draw.
- Hand size therefore stays constant until the deck runs out (an Offer costs exactly one card; the unrevealed card returns to your hand).

### Phase 3: Check the end

- If every ship is lit, the team wins immediately.
- If the draw deck became empty during this turn (by any draw, including a Trim), the **Last Watch** begins after this turn (section 6).

## 5. Special rules and timing

### 5.1 The Silence rule and the communication model

After setup step 9, players may not speak, write, gesture, time their plays on purpose, or otherwise communicate about cards, ships or plans. Only rules questions, "your turn", and the win or loss may be said.

**Pre-game agreements are allowed.** Before setup step 9 players may agree any conventions they like. The communication model is therefore: the public events below, read in the light of any pre-game agreement. The rules do not ban codes; they make every public play carry one honest meaning and make extra coded meaning unreliable and costly (section 7.3).

Public events, visible to every player:

| Event | What every other player observes | What stays hidden |
|---|---|---|
| Offer | Who offered, which ship, the Reveal token result, the revealed card's value and row | The unrevealed card's value (only that it is above or below the revealed one) |
| Light (lit) | Who, which ship, C, the ship's value, whether it was a Beacon | Nothing |
| Light (miss) | Who, which ship, C and its row; one Reef wrecked | The ship's exact value |
| Trim | Who trimmed | Both cards sent to the Night pile |
| Skip | Who was skipped | - |
| Always | Draw deck, Fog pile and Night pile sizes | The cards in them |

Each player additionally knows privately: their own hand, the values of every ship that is not theirs, and any card they have sent to the Night pile. Nobody ever learns their own unlit ships' values, the Fog pile, or another player's hand except through these events.

### 5.2 Legality summary

- **Offer:** target is another player's unlit ship whose open range holds 2 or more legal values that are not V; you hold two cards of different values, both inside the open range, neither equal to V.
- **Light:** you have an unlit ship and a card C with L <= C <= H for it.
- **Trim:** the draw deck has at least 1 card (your hand is never empty then).
- Lit ships cannot be targeted. Values may repeat among ships.

### 5.3 Resolution details

- Signal rows only grow; cards in them never move. Lit ships keep their rows on the table; they no longer matter.
- The Offer reveal is decided only by the Reveal token, and Light results only by the comparison. Nobody chooses how anything resolves.
- With 3 players, any player may Offer on any ship that is not their own; the ship's owner flips the Reveal token and the offerer places the card. A Light is resolved by the player on the lighter's left. The third player has no extra role.
- Simultaneous effects: a Light that lights the last unlit ship wins at once (a Beacon then is irrelevant). A miss that wrecks the second Reef loses at once, before any draw.
- No ties can arise: the game is co-operative and every comparison is strict or exact.

### 5.4 Empty decks

- **Draw deck empty:** no more draws; Trim is illegal; the Last Watch runs (section 6). A Beacon then moves nothing.
- **Fog pile empty:** Beacons still light the ship but move nothing.
- During the Last Watch a player with no legal Offer or Light is skipped.

## 6. End of game and scoring

The game ends in exactly one of these ways:

1. **Win:** all ships are lit (checked immediately after each Light).
2. **Loss by reef:** the second Reef token is wrecked.
3. **Loss by dawn:** the draw deck becomes empty. After the turn in which it empties, the **Last Watch** begins: every player takes exactly one more turn, in clockwise order, starting with the player to the left of the one who emptied the deck and ending with that player. If any ship is still unlit after the Last Watch, the team loses.

**Termination and turn cap.** Before the Last Watch every turn removes at least 1 card from the draw deck, and Beacons can add at most F cards in total, so the game lasts at most (starting draw deck + F + number of players) turns: 2 players at Standard, 26 + 8 + 2 = 36. Simulations should use this as the turn cap; reaching it is a bug.

**Score (for tracking and the simulation):** a win scores 10 + (cards left in the draw deck at the moment of winning). A loss scores the number of ships lit. No tiebreakers (co-operative).

## 7. Design notes

### 7.1 What the game is about

You hold the information your partner needs, and your partner holds the information you need. Every turn is a three-way pull:

- **Offer** - spend a card to narrow a partner's ship. You choose the ship and the pair; the token chooses which is shown. Good pairs make both outcomes useful (ship 7, open range 1-10: offer 5 and 6, or 6 and 9 to bracket it).
- **Light** - spend a card to guide your own ship. Within 1 is enough, so an open range of three values lets you play the middle safely. Lighting on a wider range risks a Reef, and with only one free miss that risk is serious.
- **Trim** - fish for a better lamp at the price of extra time: a Trim burns 2 deck cards instead of 1. It is the right move when your hand fits nothing, and a costly one to repeat.

### 7.2 The twist: signals are paid for with the lamps you need

The cards you signal with are the cards you need to light your own ships, and you don't yet know which values you will need. On top of that, the **double-lamp offer**: you choose two cards, the token picks one. This gives a skilled hidden-information choice (a pair where both halves help) and is half of the anti-code design.

### 7.3 Why a pre-agreed code should not pay (to be confirmed by simulation)

v1 claimed codes lose to honest play; the v1 simulation showed a hat-guessing code gaining +3.6 points at F = 8 and +12.1 at F = 16. v2 closes the free channels the code used:

1. **No free values.** Both offered cards must lie inside the ship's open range, so every offered card narrows that ship. A card chosen for its coded meaning must also be an honest signal, usually a poor one (far from V), so a coded offer costs honest information on the target ship. The open range shrinks after every offer, so the freedom to pick values shrinks too.
2. **Neutral randomness.** The reveal is a token flip, not a human shuffle, so a team cannot agree on "always reveal the left card". A coded card is shown only half the time, and the receiver cannot tell when the honest half was shown.
3. **No hopeless Lights.** A Light card must be within the window L..H, and a deliberate miss costs one of only two Reefs, so miss-codes are nearly unaffordable.
4. **No free face-up play.** Trim and skips are face-down or empty; they carry at most "I trimmed".

Natural reading ("my partner offered far from the edge, so they lacked closer cards") is intended skill, not a code.

### 7.4 Comeback and early luck

Co-op has no leader; the "comeback" question is whether a bad start can be recovered. A bad deal (hands far from the ships) is repaired by Trim selection (draw 2 keep 1); a late, precise team earns time back with Beacons; the first 4-6 turns are Offers, so round 1 decides nothing. Closeness KPI (v1: 74% of wins with 3 or fewer deck cards left, 77% of losses with one ship unlit; target about 30% or more each) should be re-checked.

### 7.5 Deduction depth and skill gap

Interval narrowing; card counting (five of each value; ships, rows, lit cards, the Reveal token result and your own Night cards are all evidence); reading the partner's pair choice; and timing (light now on a 3-value range or wait for an exact Beacon). Skill gap target: Honest at least 20 points above Random (v1: 72 points).

### 7.6 Target band and the one tuning knob

- **Band:** a competent team wins **40-60%** at Standard, at 2 players and at 3 players separately, judged on the spread of two bots (Honest and Greedy), never on one bot.
- **Knob:** the Fog size F, set separately per player count if needed. Nothing else is tuned. Standard F = 8 is provisional for both counts: v2 makes the game harder than v1 (2 Reefs, Trim burns 2 cards, restricted Offers and Lights), so the v1 result (2p Honest 73% at F = 8) no longer applies. The Standard F for each count is chosen from the sweep in 7.7 after a human test, not from one bot.

### 7.7 Notes for the playtester (bots, ablations, KPIs)

- Bot observation is exactly the table in 5.1 plus private knowledge. The Reveal token and all shuffles use the RNG.
- **Reference bots (two strengths):** Honest (range tracking and card counting; lights when its best card lights with at least about 0.95 probability, or at lower confidence when the deck has 4 or fewer cards and no Reef is wrecked); Greedy (lights at about 50% confidence, no card counting). Plus Random (uniform legal action). The Convention tier is dropped (v1: no value).
- **Code attack:** the v1 hat-guessing code (revealed value + ship index) mod 10, restricted to legal v2 Offers, plus any legal miss-code. Test at F = 8 and F = 12, 2 players.
- **Ablation bots (each must lose at least 5 points to Honest, else the feature is a dead rule):**
  - Pair-blind: offers a random legal pair on the ship it would have chosen (tests the double-lamp choice).
  - Trim-blind: on a Trim keeps a random one of the two drawn cards (tests the Trim choice).
  - Beacon-blind: never delays a safe Light to try for an exact hit (tests the Beacon).
  - No card counting (v1: 64% vs 73%, passed).
- **Targets:** Honest and Greedy both in 40-60% at the chosen Standard F; Greedy no more than Honest + 5; Random at least 20 under Honest; Code attack no more than Honest + 10 at F = 8 and F = 12; Trim under 25% of turns with runs of 3+ consecutive Trims by one player in under 10% of games; Beacons about 2 or fewer per game; length 24-28 turns (20 minutes +-20%); zero turn-cap hits.
- Report win rates for F in {4, 8, 12} at 2 and 3 players for Honest and Greedy (the knob sweep).

### 7.8 Rule budget

About 200 lines of rules text with 4 special rules (double-lamp Offer with the Reveal token, Light window and Beacon, Trim draw-2-keep-1, Last Watch). The teach is a one-page reference card's worth of actions but the rulebook is longer than one page (see Known gaps).

## 8. Changelog

- **v2 (revision 1).** Targeted fixes from `playtest-report.md` and `critique.md`; no new mechanics beyond what the fixes need.
  - Code channel (critic change 1; playtest +12.1 at F = 16): both offered cards must be inside the open range; deliberate hopeless Lights are illegal (Light window L <= C <= H).
  - Secret-shuffle trust gap (critic clarity): the owner's hidden shuffle is replaced by a flipped Reveal token choosing the lower or higher card (1 token added). Neutral randomness also stops "always reveal left" agreements.
  - Make caution pay (critic change 3; Greedy 81.6% vs Honest 73%): Reefs 3 to 2; the second miss loses.
  - Trim was a waiting action (critic change 4; 38% of turns, runs of 3-5): Trim now draws 2, keeps 1, Night-piles the other. It gives a real hand-fixing choice and costs double time, so runs of Trims are punished.
  - Difficulty (critic change 2; Honest 73%): handled by the three changes above, which all make the game harder; Fog stays the single knob, Standard F = 8 provisional, band 40-60% per player count, no Fog chosen from one bot (L2).
  - Pass flagged as dead: Pass removed as an action; a player with no legal action is skipped (only possible in the Last Watch).
  - Convention tier dropped from the bot notes (critic change 6).
  - Silence vs pre-game codes: decided; pre-game agreements are allowed and the design must withstand them (5.1, 7.3).
  - Ambiguities fixed: Last Watch order (6); Beacon timing, Fog shortage and empty deck (4 B, 5.4); hopeless Lights (now illegal); forced bad moves and Pass (Phase 1); Offers that tell nothing (now illegal); 3-player roles (5.3); a miss draws unless the game ended (Phase 2); Trim with 1 card left (4 C, Phase 3); the played card stays face-up on a lit ship (4 B).
- v1: initial design from the brief.

## 9. Known gaps

- **Anti-code claim unproven.** v2 restricts the code channel but it is not yet simulated. If Code attack still beats Honest by more than 10 points at F = 12, the fallback (a mechanic change, needs a revision decision) is to require both offered cards on the same side of V.
- **Standard Fog not set by data.** F = 8 is provisional; human teams deduce worse than bots, so the critic's 2-session human test should set the final value per player count.
- **Beacon may be a weak twist.** If the Beacon-blind ablation loses by under 5 points, the Beacon should be cut in a later revision.
- **Rule budget (L7):** the rulebook is about 200 lines, over a one-page teach; untimed.
- **3-player mode** tested less than 2-player (v1: 53% at F = 8); its band must be confirmed separately (L8).
- **Audience drift:** bot-predicted family fun 3.3; not addressed in this revision.
