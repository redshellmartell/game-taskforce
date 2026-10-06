# Ladder Pairs (v1)

## 1. Overview
- **Hook:** a climbing card game where your partner changes every hand and is secret until the ropes come out. Today's partner is tomorrow's rival.
- **Players:** exactly 4. **Time:** about 25 minutes (6 short hands). **Age:** 12+. **Complexity:** 2/5.
- Each hand, the two players holding the same colour of Rope are a team. Beat the current play or pass; be first to empty your hand. Team points go to both partners, but the winner is one player.

## 2. Components (56 cards, pencil and paper)
| Cards | Count | Rank | Use |
|---|---|---|---|
| Number cards: four suits, ranks 1 to 13 (a standard deck: A=1, J=11, Q=12, K=13) | 52 | 1-13 | singles, pairs, triples, runs |
| Sun Rope 14, Moon Rope 14 | 2 | 14 | single only; colour sets your team |
| Sun Rope 15, Moon Rope 15 | 2 | 15 | single only; colour sets your team |

Suits never matter. Each colour has one 14 and one 15, so both teams always hold equal Ropes.

## 3. Setup (each hand)
1. Hand 1: choose a dealer at random. After each hand the dealer passes clockwise.
2. Shuffle the 4 Ropes and deal 1 face down to each player. Look at it secretly.
3. Shuffle the 52 number cards, deal 10 to each player, and set the last 12 aside face down unseen. They are not used this hand.
4. Each player holds 11 cards. Your partner is the player with the other Rope of your colour.
5. **First lead:** the player with the lowest score (ties, and hand 1: the first tied player clockwise from the dealer's left).

## 4. Turn structure
Play goes clockwise in tricks. Players who have gone out are skipped.
1. **Lead.** The player on lead must play any one combination face up:
   - **Single:** 1 card (number card or Rope).
   - **Pair / Triple:** 2 / 3 number cards of the same rank.
   - **Run:** 3 or more number cards of consecutive ranks (no wrap: 12-13-1 is not a run).
2. **Follow.** Each next player either:
   - **plays** a combination of the same type and the same number of cards with a strictly higher rank (a run is ranked by its top card), or
   - **passes.** Passing is always allowed when following. A player who passed may play later in the same trick.
3. **Trick ends** when every other player still in the hand has passed since the last play. The cards go to a face-down discard pile. The player who made the last play leads the next trick.
4. **Going out.** When you play your last card you are out. The trick continues without you.

## 5. Special rules and timing (3 special rules)
1. **Ropes.** A Rope is only ever a single (rank 14 or 15). Playing it shows your team colour to everyone. Equal ranks never beat each other, so a 15 cannot beat a 15. You cannot go out without playing your Rope.
2. **Relay.** If a trick ends and the player who made the last play is out, the lead goes to that player's partner, who shows their Rope (if still in hand) and leads.
3. **Uphill.** At the start of each hand, every player whose score is 4 or more below the highest score is Uphill for that hand. An Uphill player scores double their team's points for that hand. (The lowest player also leads first: Setup step 5.)
- **Talk.** No talk about cards or teams. Plays may only carry meanings that every player knows; private signal agreements are cheating.
- **Information.** Played cards stay visible until the trick ends; anyone may ask how many cards a player holds. Scores are public.
- **Hand ends** at once when the second player goes out, even mid-trick. Unplayed cards in that trick are irrelevant.
- **Turn cap.** A turn is one play or one pass. If a hand reaches 200 turns (it cannot under these rules: at most 44 plays, each followed by at most 3 passes), it ends; players are then ranked by fewest cards left, ties sharing the better place.

## 6. End of game and scoring
1. At the end of each hand, all players show their Rope colour.
2. **Team points:** the team of the first player out gets 3; the team of the second player out gets 1 (one team may get both: 4).
3. Each player scores their team's points, doubled if Uphill. Record scores on paper.
4. **End:** the game ends after hand 6 (match cap: 6 hands). Highest total wins.
5. **Ties:** most hands in which you went out first; then better finish in hand 6 (first out, second out, then fewer cards left); then the tied players share the win.

## 7. Design notes
- **The twist:** partners are hidden and re-dealt every hand, revealed only by game events (a Rope played, a Relay, the end of the hand). Scores are individual, so every hand asks "is that player my partner, and do I want them to score?". Uphill sharpens it: helping an unknown partner might be helping the leader.
- **Tensions:** a Rope is your best single, but playing it tells everybody your colour (and tells your partner everything). Passing to let a suspected partner win a trick wins the hand if right and hands tempo to an opponent if wrong. Going out with an unbeatable last play triggers Relay and sets up a 4-point sweep.
- **Partner configurations:** the 3 pairings (across, adjacent left, adjacent right) are each dealt with chance 1/3. In every pairing both teams have the same seat shape, so the only asymmetry is who leads first; the lowest scorer leads, and ties rotate with the dealer, so over 6 hands seats are symmetric.
- **Comeback (L3):** Uphill doubles the points of any player 4+ behind and gives the lowest player the first lead. Round 1 cannot decide the game: one hand is worth at most 4 points and a trailer can score 8.
- **Not Tichu:** no fixed partners, no calls, no card passing, no Dragon/Phoenix/Dog/Mah Jong (Ropes are plain top singles that set teams), no card-point or 1-2 scoring (3/1 finish points, individual totals), 6 hands of 11 cards (25 minutes, not 60).
- **Skill (L6):** reading partners from passes and Ropes, timing the Rope, sequencing runs, and choosing when to let a trick go. Target strategic minus random at least 20 points.

### Target bands and knobs
- Seat balance gap <= 5 points (4 players only). First-lead team scores 3+ in 50-60% of hands, and within 5 points across the three pairings and the leader's partner position (left, across, right). Knob: first-out points (3) vs second-out (1).
- Runaway leader <= 65%, lead changes >= 2. Knob: Uphill threshold (4) and multiplier (x2; fallback +2).
- Code attack: a pair of bots with a private signal must gain <= 3 points over honest bots. Knob if it fails: "Open Rope" (the first leader plays with their Rope face up).
- Reveal timing: median first Rope play between tricks 3 and 6. Knob: Rope ranks (lower them to 0.5 and 13.5 to push earlier reveals).

### Bot hints for the playtester
- **Random:** uniform over legal actions (including pass when following).
- **Greedy (weak reference):** leads the combination that sheds most cards with the lowest top rank (run > triple > pair > single); follows with the lowest legal beat; plays a Rope only when it is the only beat or with 3 or fewer cards left; never beats a partner known for certain (Rope colour seen).
- **Reader (strong reference):** belief model: each other player is partner with chance 1/3; a Rope of my colour sets that player to 1, other colour sets them to 0 and the other two to 1/2; Relay sets the leader to 1 for the out player. Soft update: a player who beats a trick held by X lowers P(X is their partner). Passes when P(trick holder is partner) >= 0.6 unless they can go out; weights scores (avoid feeding the leader, feed Uphill partners).
- **Ablation bots** (each must lose to Reader by >= 5 win-rate points in 2+2 mixed tables, seats rotated):
  - A1 **Partner-blind:** Reader that treats all three others as opponents (tests the hidden-partner twist).
  - A2 **Reveal-blind:** Reader that never updates from Rope plays or Relay (tests the Rope reveal).
  - A3 **Uphill-blind:** Reader that ignores scores and Uphill when choosing whom to let win; also run Uphill off as a rule variant (runaway must be >= 5 points worse without it).
  - A4 **Relay-blind:** Reader with no preference for unbeatable last plays; also run Relay off (lead to next player clockwise) as a variant.
  - **Code attack:** two Readers that agree "my first single of the hand is odd if Sun, even if Moon" vs two honest Readers.
- Report forced-pass rate (follow turns with no legal play) and runs of 3+ forced passes (L11).

## 8. Changelog
- **v1 (cycle 0):** first design from the brief.

## Known gaps
- Rules text (sections 1-6) is 51 lines (under the 60-90 target, about one page), but no one has timed a teach (L7).
- Code attack is forbidden by rule, not prevented by mechanics; only the bot check will show if private signals pay.
- 12 set-aside cards per hand add luck and blunt card counting; unknown whether this lowers the skill gap (L6). Knob: deal 11 each and set 8 aside.
- Ropes as top singles may be held to the end, making reveals late (brief risk 1); the reveal-timing band above tests it.
- Lead changes are capped at 5 per game (scores move only at hand end); Uphill is the main source, so watch reliance on it (Trick-taking trap).
- Simulation cannot test whether guessing partners is fun, human bluffing or table talk, or the theme.

## Playbook check
1. **Family:** read "Trick-taking and hands" (trap: strategic bot only ties greedy, and lead changes resting on one mechanism) and "Deduction and co-op" (trap: code signalling); here the risks are Reader barely beating Greedy and a private signal code.
2. **Comeback:** Uphill (x2 points for players 4+ behind, lowest leads first), serving runaway leader <= 65% and lead changes >= 2.
3. **Ablations:** 4 players only: A1 partner-blind, A2 reveal-blind, A3 Uphill-blind (+ Uphill-off variant), A4 Relay-blind (+ Relay-off variant), each losing to Reader by >= 5 points; code attack gain <= 3.
4. **Self-check:** fixed Ropes as pairs (singles only), equal-rank beats (strictly higher), run wrap (none), lead player going out (Relay; partner is always still in), trick end with out players, mid-trick hand end, Uphill in hand 1 (nobody), first-lead ties, four of a kind (not a type: split it), passing then playing (allowed), leader passing (not allowed), turn cap fallback ranking, final ties; no dead card (every rank is a single and sits in pairs, triples or runs; Ropes must be played to go out).
5. **Band and knob:** seat gap <= 5, first-lead team 50-60% per pairing; knob first-out/second-out points (3/1); comeback knob Uphill threshold 4.
6. **Ends:** after hand 6; a hand ends at the second player out (cap 200 turns, max possible 176); expected about 4 minutes per hand, 24-26 minutes vs 25 target.
7. **Budget:** sections 1-6 are 51 lines, 3 special rules (Ropes, Relay, Uphill) vs one page and 3 promised.
8. **Re-run list:** first pass, so run all: A1-A4, Uphill-off, Relay-off, code attack, both reference bots plus Random.
