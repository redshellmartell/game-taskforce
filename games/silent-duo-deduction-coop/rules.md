# Silent Duo - Rules v3.1

## 1. Overview

- **Title:** Silent Duo
- **Hook:** Two lighthouse keepers guide ships through the fog without saying a word. You can see the ships off your partner's rocks but not your own. The only way to tell your partner where a ship is: hand over two of your own lamps in the dark and let a flipped token pick which one shines. Every lamp you spend on a signal is a lamp you can no longer use to guide your own ships.
- **Players:** 2 (the standard game). 3 players is a **variant** (section 7.6). Fully co-operative: the team wins or loses together.
- **Play time:** about 20 minutes (about 21 turns at 2-player Standard in simulation).
- **Age:** 10+. **Complexity:** 2.5 / 5.

## 2. Components

| Item | Count | Details |
|---|---|---|
| Lamp cards | 50 | Values 1 to 10, five copies of each value. No other markings (art only). |
| Reference cards | 2 | Turn summary (no game function). |
| Reef tokens | 2 | Identical tokens. Start on the "safe" side; one is flipped to its "wrecked" side for each missed light. |
| Reveal token | 1 | Two-sided: one side "Low" (moon), the other "High" (sun). Flipped like a coin for every pair Offer. |

**Lamp card list**

| Value | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Copies | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 |

Lamp cards serve five roles during play, depending on where they are:

- **Ship** - a face-down card in front of a player; its value is the hidden number that player must find.
- **Hand card** - a card held by a player.
- **Fog** - face-down cards removed at setup without anyone looking. They never return; they only shorten the night and hide which values are left.
- **Draw deck** - the night clock.
- **Night pile** - face-down cards removed by Trim (only the trimmer has seen them; they never return).

Total: 52 cards and 3 tokens. No board, no dice.

## 3. Setup

1. **Choose a difficulty** by setting the Fog size F from this table (Standard is the default):

   | Players | Calm | Standard | Storm |
   |---|---|---|---|
   | 2 | 7 | 10 | 13 |
   | 3 (variant) | 5 | 8 | 11 |

   Standard values come from the v3 bot sweep (both bots inside a 40-60% win rate); Calm and Storm are one 3-card step either side. Humans deduce worse than bots, so human play will need re-tuning.

2. Shuffle all 50 Lamp cards face-down.
3. **Deal ships.** With 2 players, deal 3 cards face-down in a row in front of each player. With 3 players, deal 2 cards to each player. These are that player's **ships**, numbered left to right as seen by their owner (Ship 1, Ship 2, Ship 3). **An owner may never look at their own ships.** Every other player may look at them now and at any time (lift the card toward yourself, keeping it hidden from its owner).
4. **Deal the Fog.** Deal F cards face-down into the box, without anyone looking.
5. **Deal hands.** With 2 players, 5 cards each. With 3 players, 4 cards each. Players look at their own hand.
6. The remaining cards are the **draw deck**, face-down (2 players: 34 - F cards, so 24 at Standard; 3 players: 32 - F cards, so 24 at Standard).
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
- **Fitting cards:** a hand card *fits* the target if its value is strictly inside the open range (L < card < H) and is not V.
- **Pair Offer** (needs two fitting cards of **different values**):
  - Put both face-down beside the target ship, the **lower-value card on your left** and the higher-value card on your right. They may both be lower than V, both higher, or one on each side.
  - The ship's owner flips the Reveal token. "Low": you turn the lower card face-up. "High": you turn the higher card face-up. (Programs: choose the lower or higher card with probability 1/2 each.)
  - The unrevealed card goes back into your hand without being shown. Everyone knows only that it was higher (if "Low" was flipped) or lower (if "High" was flipped) than the revealed card.
- **Single Offer** (legal only if your fitting cards for that ship all have **the same value**, so no Pair Offer on that ship is possible; two or more copies of one value count as one value, so a hand with 5, 5 as its only fitting cards may Single Offer a 5 but not Pair Offer):
  - Play one fitting card face-up beside the target ship. No token flip. Because every fitting card you hold has that one value, you have no choice of value. Since a fitting card is strictly inside (L, H), a Single card can never equal L or H.
- **Honest placement (both kinds):** you place the revealed card in the target ship's **Low row** if its value is lower than V, or its **High row** if it is higher. The side is fixed by the true comparison; you have no choice.
- Either kind of Offer costs exactly one card from your hand. Guaranteed meaning: V is strictly higher than every Low-row card and strictly lower than every High-row card, and every Offer narrows the open range.

**B. Light (guide one of your own ships)**
- **Target:** one of your own unlit ships.
- **Card:** play one card C from your hand face-up onto it. C must satisfy **L <= C <= H** for that ship (edge values L and H are legal). A card outside this window may not be played.
- **Resolver:** with 2 players, your partner; with 3 players, the player on your left. The resolver looks at V and compares:
  - **|C - V| <= 1 (lit):** the resolver turns the ship face-up. It is **lit**. The ship and C stay face-up in front of you for the rest of the game (public, out of play).
  - **|C - V| >= 2 (miss):** the resolver places C in that ship's Low row (if C < V) or High row (if C > V). Flip one Reef token to wrecked. If both Reefs are now wrecked, the team loses immediately (no draw).

**C. Trim (change your lamps)**
- Legal only while the draw deck has at least 1 card.
- Discard one card from your hand face-down onto the Night pile, without showing it.
- Then (instead of the normal Phase 2 draw) draw **2** cards from the draw deck, keep 1, and put the other face-down on the Night pile without showing it. If the deck has only 1 card, draw it and keep it. Only the trimmer sees these cards; no other player (including the third player in a 3-player game) sees any of them.

### Phase 2: Draw

- After an Offer or a Light (lit or miss, unless the game has ended), draw 1 card from the draw deck. If it is empty, do not draw.
- After a Trim, the draw was already done in the Trim action. After a skipped turn, do not draw.
- Hand size therefore stays constant until the deck runs out.

### Phase 3: Check the end

- If every ship is lit, the team wins immediately.
- If the draw deck became empty during this turn (by any draw, including a Trim), the **Last Watch** begins after this turn (section 6).

## 5. Special rules and timing

### 5.1 The Silence rule and the communication model

After setup step 9, players may not speak, write, gesture, time their plays on purpose, or otherwise communicate about cards, ships or plans. Only rules questions, "your turn", and the win or loss may be said.

**Pre-game agreements are allowed.** Before setup step 9 players may agree any conventions they like. The rules do not ban codes; they make every public play carry one honest meaning and make extra coded meaning unreliable and costly (section 7.3).

Public events, visible to every player:

| Event | What every other player observes | What stays hidden |
|---|---|---|
| Pair Offer | Who offered, which ship, the Reveal token result, the revealed card's value and row | The unrevealed card's value (only that it is above or below the revealed one) |
| Single Offer | Who offered, which ship, the card's value and row (and so that the offerer held no other fitting value for that ship) | Nothing else |
| Light (lit) | Who, which ship, C, the ship's value | Nothing |
| Light (miss) | Who, which ship, C and its row; one Reef wrecked | The ship's exact value |
| Trim | Who trimmed | Both cards sent to the Night pile |
| Skip | Who was skipped | - |
| Always | Draw deck and Night pile sizes, and F | The cards in them and in the Fog |

Each player additionally knows privately: their own hand, the values of every ship that is not theirs, every card they have sent to the Night pile, and the value of the unrevealed card in each of their own Pair Offers. Nobody else learns these. Nobody ever learns their own unlit ships' values, the Fog, or another player's hand except through these events.

### 5.2 Legality summary

- **Pair Offer:** target is another player's unlit ship; you hold two fitting cards (L < card < H, not V) of different values.
- **Single Offer:** target is another player's unlit ship; you hold at least one fitting card and all your fitting cards for that ship have the same value.
- **Light:** you have an unlit ship and a card C with L <= C <= H for it.
- **Trim:** the draw deck has at least 1 card (your hand is never empty then).
- Lit ships cannot be targeted. Values may repeat among ships. Whether a Pair or a Single Offer is legal is decided per target ship: you may Single-Offer on one ship even while a Pair Offer is legal on another ship (your choice).

### 5.3 Resolution details

- Signal rows only grow; cards in them never move. Lit ships keep their rows on the table; they no longer matter.
- The Pair Offer reveal is decided only by the Reveal token, and Light results only by the comparison. Nobody chooses how anything resolves.
- With 3 players, any player may Offer on any ship that is not their own; the ship's owner flips the Reveal token and the offerer places the card. A Light is resolved by the player on the lighter's left. If any player who can see the ship notices a wrong result (wrong row, lit/miss error), they may point it out as a rules question and it is corrected before the next turn begins. (Programs: every resolution is correct.)
- Simultaneous effects: a Light that lights the last unlit ship wins at once. A miss that wrecks the second Reef loses at once, before any draw.
- No ties can arise: the game is co-operative and every comparison is strict or exact.

### 5.4 Empty deck

- When the draw deck is empty: no more draws; Trim is illegal; the Last Watch runs (section 6). Last Watch turns are Offer, Light or skip only.
- A Trim or a Phase 2 draw that takes the last card of the draw deck empties it; the Last Watch then begins after that turn.

## 6. End of game and scoring

The game ends in exactly one of these ways:

1. **Win:** all ships are lit (checked immediately after each Light).
2. **Loss by reef:** the second Reef token is wrecked.
3. **Loss by dawn:** after the turn in which the draw deck empties, the **Last Watch** begins: every player takes exactly one more turn, in clockwise order, starting with the player to the left of the one who emptied the deck and ending with that player. A skipped turn counts as that player's Last Watch turn. If any ship is still unlit after the Last Watch, the team loses. A win or a reef loss during the Last Watch ends the game at once.

**Termination and turn cap.** Before the Last Watch every turn removes at least 1 card from the draw deck and nothing ever adds cards to it, so the game lasts at most (starting draw deck + number of players) turns: 2 players at Standard 24 + 2 = 26; 3 players at Standard 24 + 3 = 27. Simulations use this as the turn cap; reaching it is a bug.

**Score (for tracking and the simulation):** a win scores 10 + (cards left in the draw deck at the moment of winning). A loss scores the number of ships lit. No tiebreakers (co-operative).

## 7. Design notes

### 7.1 What the game is about

You hold the information your partner needs, and your partner holds the information you need. Every turn is a three-way pull:

- **Offer** - spend a card to narrow a partner's ship. With two fitting cards you choose the pair and the token chooses which is shown (ship 7, open range 1-10: offer 5 and 6, or 6 and 9 to bracket it). With only one fitting value you play it openly.
- **Light** - spend a card to guide your own ship. Within 1 is enough, so an open range of three values lets you play the middle safely. Lighting on a wider range risks a Reef, and with only one free miss that risk is serious.
- **Trim** - fish for a better lamp at the price of extra time: a Trim burns 2 deck cards instead of 1.

### 7.2 The twist: signals are paid for with the lamps you need

The cards you signal with are the cards you need to light your own ships, and you don't yet know which values you will need. On top of that, the **double-lamp Offer**: you choose two cards, the token picks one. This is the game's one twist (pair-blind ablation: -8.9 at v2) and half of the anti-code design. The Beacon (v2) is cut: it was a flat time bonus, not a decision (section 8).

### 7.3 Why a pre-agreed code should not pay

v1's hat-guessing code gained +12.1 at the loosest Fog. v2 closed it; at v2 the code attack measured Honest +1.0 (F 8) and +3.0 (F 12). The v3 Single Offer keeps the channel closed because it gives the offerer **no choice of value**: it is legal only when every fitting card has one value. A team that wants a coded single card must hold exactly that card and no other fitting value, which it cannot arrange without Trims that cost 2 deck cards each. The rest of the argument is unchanged:

1. **No free values.** Every offered card lies inside the open range and narrows the ship, so a coded card is also an honest (usually poor) signal.
2. **Neutral randomness.** The Pair Offer reveal is a token flip, so a coded card is shown only half the time and the receiver cannot tell which half.
3. **No hopeless Lights.** A Light card must be within L..H, and a deliberate miss costs one of only two Reefs.
4. **No free face-up play.** Trim and skips are face-down or empty; they carry at most "I trimmed".

Natural reading ("my partner offered far from the edge, so they lacked closer cards"; "a Single Offer means no other fitting value") is intended skill, not a code.

### 7.4 Comeback, early luck and pacing

Co-op has no leader; the question is whether a bad start can be recovered. A bad deal (hands far from the ships) is repaired by Trim selection (draw 2 keep 1; trim-blind ablation -15.9 at v2); the first 4-6 turns are Offers, so round 1 decides nothing. v2's middle game stalled on forced Trims. The v3 Single Offer lets a hand with one fitting value signal, but it moved Trim share only from 29% to 25% (single-blind check); hands with no fitting card still Trim, and 3+ Trim runs remain common (Known gaps). Trim is the right move when no card fits anything, or when an Offer would waste the lamps you need.

### 7.5 Deduction depth and skill gap

Interval narrowing; card counting (five of each value; ships, rows, lit cards, your own Night cards and Single Offers are evidence); reading the partner's pair choice; and timing (light now on a 3-value range or narrow further first). Skill gap target: Honest at least 20 points above Random (v2: 54.7).

### 7.6 Target band and the one tuning knob, per player count

- **Knob:** the Fog size F, set per player count (section 3 table). Nothing else is tuned.
- **2 players (standard game):** band **40-60%** for both bots at Standard. Measured v3 sweep: F 6 Honest 63.0 / Greedy 73.8; F 9 52.1 / 62.1; **F 10 48.6 / 56.2 (Standard)**, 21.0 turns, a little under the 22-26 target. Greedy beats Honest by about 8-11 at every F (target at most 5).
- **3 players (variant):** measured F 2 61.9 / 72.9, F 6 45.8 / 60.4; **F 8 40.6 / 51.9 (Standard)**. Greedy +11 over Honest; see Known gaps.
- Humans deduce worse than bots, so a human test should re-tune F; move F, not another rule.

### 7.7 Notes for the playtester (bots, ablations, KPIs)

- Bot observation is exactly the table in 5.1 plus private knowledge. The Reveal token and all shuffles use the RNG.
- **Reference bots (two strengths, L2):** Honest (range tracking and card counting; lights when its best card lights with at least about 0.95 probability, or at lower confidence when the deck has 4 or fewer cards and no Reef is wrecked); Greedy (lights at about 50% confidence, no card counting). Plus Random. Both bots use Single Offers when legal and useful by their own rule; no setting is tuned to one bot.
- **Knob sweep (both bots):** 2p F in {7, 10, 13}; 3p F in {5, 8, 11} (v3 measured 2p F 3-10 and 3p F 0-8; see 7.6). Report win rates, turns and Trim KPIs per cell.
- **Code attack:** the v1 hat-guessing code restricted to legal v3 Offers (Single Offers included) plus any legal miss-code, 2p. Must be no more than Honest + 10 (v3: +2.8 at F 6, +2.3 at F 10).
- **Ablations (each must lose at least 5 points to Honest, 2p Standard and 3p Standard):** Pair-blind (random legal pair on the chosen ship); Trim-blind (keeps a random one of the two drawn cards); No card counting.
- **Single-blind check (not a twist test):** a bot that never makes Single Offers, to show how much of any Trim drop comes from this rule (L10).
- **Targets:** both bots in 40-60% at each count's Standard; Greedy no more than Honest + 5 (2p required; 3p reported); Random at least 20 under Honest; Code attack as above; Trim under 25% of turns and runs of 3+ consecutive Trims by one player in under 10% of games, at both counts; share of Trims made with no legal Offer; length 22-26 turns (20 minutes +-20%); zero turn-cap hits; close-game shares (wins with 3 or fewer deck cards left, losses with one ship unlit).

### 7.8 Rule budget

About 200 lines of rules text with 3 special rules (double-lamp Offer with its Single fallback, Trim draw-2-keep-1, Last Watch); the Beacon cut removed one. The rulebook is longer than one page (see Known gaps).

## 8. Changelog

- **v3.1 (edit pass after cycle 2 critique, no new mechanics).** Fog table reset from the v3 bot sweep (2p Standard F 10, 3p Standard F 8; critic change 1); the four Single Offer and Last Watch rulings written in (change 2); stale 7.4, 7.6 and Known gaps text updated to measured numbers, Trim stall listed as open (change 3).

- **v3 (revision 2).** Targeted fixes from the cycle 1 `playtest-report.md` and `critique.md`; no new mechanics.
  - **Trim stall** (critic change 1; Trim 30% of turns, 3+ runs in 61% of 2p games, 60% of Trims with no legal Offer): added the **Single Offer**, legal only when all your fitting cards for a ship share one value. A hand with one fitting card now signals instead of waiting. Value choice stays at zero, so the code channel stays closed (7.3). Pair Offer legality is unchanged.
  - **Beacon cut** (critic change 2; Beacon-blind -0.5/-0.9, needs 5; Beacons off -11.3): it was a time gift, not a decision. The Fog no longer returns, the C = V case is gone, and the Fog per count is lowered to give the time back (7.6). Turn cap is now deck + players.
  - **3 players** (critic change 3; Honest 38% at F 8, Greedy +9.4): labelled a **variant** with its own Fog column and band; the Greedy gap is a known gap. 2 players is the standard game.
  - Known gaps and 7.3/7.6 updated to the measured v2 numbers (critic change 4); Beacon text removed, so the line count did not grow.
  - Kept: Reefs 2, Trim draw-2-keep-1, the hopeless-Light ban, pair legality.
- **v2.1 (fix-before-critic, wording only).** Closed the 10 playtest ambiguities with no rule or balance change.
- **v2 (revision 1).** Both offered cards inside the open range; hopeless Lights illegal; Reveal token replaces the owner's shuffle; Reefs 3 to 2; Trim draws 2 keeps 1; Pass removed; pre-game agreements allowed; Fog as the single knob.
- v1: initial design from the brief.

## 9. Known gaps

- **First human-playtest question: do Trim runs feel like downtime?**
- **Trim stall is open (known structural problem).** Runs of 3+ Trims by one player happen in 54% of 2p games and 49% of 3p games (target under 10%); Trim is about 25% of turns. It comes from hands that fit no open range, which the anti-code Offer legality causes; bot cycles will not fix it. Next step is a human test, not another bot revision.
- **Fog values are bot-tuned.** 2p F 10 and 3p F 8 come from the v3 sweep; humans deduce worse than bots, so expect to lower F after human play.
- **Length:** 2p Standard runs about 21 turns in simulation, a little under the 22-26 target.
- **Greedy beats Honest by about +11** (2p and 3p; target at most 5). Probably a bot artefact (Honest lights too cautiously), but unconfirmed. 3p stays a variant until it passes (L8).
- **Anti-code holds:** code attack +2.8 (F 6) and +2.3 (F 10) at v3, limit 10.
- **Rule budget (L7):** about 200 lines, over a one-page teach; untimed.
- **Audience drift:** bot-predicted family fit 3.07; not addressed.
