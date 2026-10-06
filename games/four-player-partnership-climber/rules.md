# Ladder Pairs (v1.1)

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
5. **First lead:** the player with the lowest score at the start of the hand. If several players tie for lowest (always so in hand 1), the first of them clockwise starting from the dealer's left leads.

## 4. Turn structure
Play goes clockwise in tricks. Players who have gone out are skipped.
1. **Lead.** The player on lead must play any one combination face up; the leader may never pass:
   - **Single:** 1 card (number card or Rope).
   - **Pair / Triple:** 2 / 3 number cards of the same rank.
   - **Run:** 3 or more number cards of consecutive ranks (no wrap: 12-13-1 is not a run).
   - There are no other types. Four cards of one rank are not a combination; play them as singles, pairs or a triple plus a single, across one or more tricks.
2. **Follow.** Each next player either:
   - **plays** a combination of the same type and the same number of cards with a strictly higher rank (a run is ranked by its top card), or
   - **passes.** Passing is always allowed when following. A player who passed may play later in the same trick, when their turn comes round again after someone else has played.
3. **Trick ends** when, since the last play, every other player still in the hand has passed in a row (one pass each). The cards go to a face-down discard pile. The player who made the last play leads the next trick (if that player is out: Relay, 5.2).
4. **Going out.** When you play your last card you are out. The trick continues without you. The first player to go out is "first out"; the second is "second out".

## 5. Special rules and timing (3 special rules)
1. **Ropes.** A Rope is only ever a single (rank 14 or 15). Playing it shows your team colour to everyone. Equal ranks never beat each other, so a 15 cannot beat a 15. Your Rope is a card in your hand, so your hand is empty only after you have played it (this is not an extra restriction).
2. **Relay.** If a trick ends and the player who made the last play is out, the lead goes to that player's partner (always still in the hand, since the hand ends at the second player out). The partner leads and must show their Rope face up if it is still in hand, then keep it in hand; if they already played it, the team is already known. Either way, the partnership is now public. The partner must lead as normal (no pass).
3. **Uphill.** Using the scores at the start of the hand (before that hand's scoring), every player whose score is 4 or more below the highest score (difference >= 4) is Uphill for that hand. An Uphill player scores double their team's points for that hand. (The lowest player also leads first: Setup step 5.)
- **Talk.** No talk about cards or teams. Plays may only carry meanings that every player knows; private signal agreements are cheating.
- **Information.** Played cards stay visible until the trick ends; anyone may ask how many cards a player holds. Scores are public.
- **Hand ends** at once when the second player goes out, even mid-trick. Unplayed cards in that trick are irrelevant.
- **Turn cap.** A turn is one play or one pass. If a hand reaches 200 turns, it ends; players not yet out are then ranked by fewest cards left, ties sharing the better place. This cannot happen under these rules (at most 44 plays, each followed by at most 3 passes: 176 turns); it is a safety rule only.

## 6. End of game and scoring
1. At the end of each hand, all players show their Rope colour.
2. **Team points:** the team of the first player out gets 3; the team of the second player out gets 1 (one team may get both: 4). The other two players score nothing beyond their team's share.
3. Each player scores their team's points, doubled if Uphill. Record scores on paper.
4. **End:** the game ends after hand 6 (match cap: 6 hands). Highest total wins.
5. **Ties** (applied only among the players tied for highest total, in order): (a) most hands in which you were first out; (b) better finish in hand 6, ranked first out, then second out, then the other players by fewer cards left at the end of hand 6; (c) players still tied after (b) all share the win.

## 7. Design notes
- **The twist:** partners are hidden and re-dealt every hand, revealed only by game events (a Rope played, a Relay, the end of the hand). Scores are individual, so every hand asks "is that player my partner, and do I want them to score?". Uphill sharpens it: helping an unknown partner might be helping the leader.
- **Tensions:** a Rope is your best single, but playing it tells everybody your colour (and tells your partner everything). Passing to let a suspected partner win a trick wins the hand if right and hands tempo to an opponent if wrong. Going out with an unbeatable last play triggers Relay and sets up a 4-point sweep.
- **Measured (v1 sim, bots only, unvalidated):** the twist does not yet change best play. Partner-reading bots do not beat simple greedy bots (Reader minus Greedy -1.5 / -2.5 points), and the partner-blind bot beats Reader by 7 points. All four ablations fail the >= 5 loss test. This is a design question for the critic and the owner; v1.1 changes no mechanic.
- **Partner configurations:** the 3 pairings (across, adjacent left, adjacent right) are each dealt with chance 1/3. In every pairing both teams have the same seat shape, so the only asymmetry is who leads first; the lowest scorer leads, and ties rotate with the dealer, so over 6 hands seats are symmetric (measured seat gap 0.9 points).
- **Comeback (L3):** Uphill doubles the points of any player 4+ behind and gives the lowest player the first lead. Round 1 cannot decide the game: one hand is worth at most 4 points and a trailer can score 8. Measured: runaway leader 40% (passes), but lead changes 1.13 (fails >= 2); with Uphill off runaway rises to 66%, so Uphill carries the whole comeback load.
- **Not Tichu:** no fixed partners, no calls, no card passing, no Dragon/Phoenix/Dog/Mah Jong (Ropes are plain top singles that set teams), no card-point or 1-2 scoring (3/1 finish points, individual totals), 6 hands of 11 cards (25 minutes, not 60).
- **Skill (L6):** intended: reading partners from passes and Ropes, timing the Rope, sequencing runs, and choosing when to let a trick go. Measured: Reader minus Random 74.8 points (1 vs 3), but the gap is "sensible legal play vs random", not partner reading (Reader does not beat Greedy).

### Target bands and knobs
- Seat balance gap <= 5 points (4 players only). First-lead team scores 3+ in 50-60% of hands, and within 5 points across the three pairings and the leader's partner position (left, across, right). Knob: first-out points (3) vs second-out (1). Measured: seat gap 0.9 (passes); first-lead team 61.0% (just above band), pairing spread 3.6 (passes).
- Runaway leader <= 65%, lead changes >= 2. Knob: Uphill threshold (4) and multiplier (x2; fallback +2). Measured: 40% (passes) and 1.13 (fails).
- Code attack: a pair of bots with a private signal must gain <= 3 points over honest bots. Knob if it fails: "Open Rope" (the first leader plays with their Rope face up). Measured: -0.1 (passes, but weak evidence since partner knowledge barely pays).
- Reveal timing: median first Rope play between tricks 3 and 6. Knob: Rope ranks (lower them to 0.5 and 13.5 to push earlier reveals). Measured: median trick 3 (Greedy 4), low edge of band.

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
- **v1.1 (fix-before-critic):** wording only, closing the 9 playtest ambiguities with the readings the simulation used (Relay reveal when the Rope is already played, four of a kind, first/second out, Uphill at hand start with >= 4, tie-break order and shared win, trick end, leader cannot pass, turn cap); Known gaps and Playbook check updated to measured v1 numbers. No mechanic or number changed.

## Known gaps
- **Hidden partners do not yet change best play (sim, high):** all four ablations fail (A1 partner-blind -7.0, A2 -1.2, A3 -0.4, A4 -3.2 per bot; needed +5), and Reader does not beat Greedy. Passing to a partner earns nothing because points come only from going-out order. Left for the critic and the owner; not addressed in this pass.
- **Skill gap only against Random (L6 repeat):** Reader minus Random 74.8 / 36.7 points, Reader minus Greedy -2.5 / -1.5.
- **Lead changes 1.13 per game (target >= 2):** scores move only at hand end (max 5), and Uphill carries the whole comeback (Uphill off: runaway 66%, lead changes 0.53).
- **Dead turns:** 42% of follow turns have no legal play; about 1.9 runs of 3+ forced passes per hand (L11). Needs a human feel check.
- **First-lead team 61.0%** scores 3+ (band 50-60%), slightly high.
- **Length:** 54 turns per hand, estimated 27.3 minutes (target 25) at 6 s per decision; about 37 minutes at slower pace. Time one real hand.
- Code attack is forbidden by rule, not prevented by mechanics; the bot check (-0.1) is weak evidence while partner knowledge barely pays.
- 12 set-aside cards per hand add luck and blunt card counting. Knob: deal 11 each and set 8 aside (untested).
- Rules text (sections 1-6) is about 55 lines (under the 60-90 target), but no one has timed a teach (L7).
- Simulation cannot test whether guessing partners is fun, human bluffing or table talk, or the theme.

## Playbook check
1. **Family:** read "Trick-taking and hands" (trap: strategic bot only ties greedy, and lead changes resting on one mechanism) and "Deduction and co-op" (trap: code signalling). Measured: both trick-taking traps hit (Reader ties Greedy; Uphill carries all comeback); code attack passes (-0.1).
2. **Comeback:** Uphill (x2 points for players 4+ behind, lowest leads first). Measured: runaway 40% (passes), lead changes 1.13 (fails >= 2).
3. **Ablations:** A1 partner-blind -7.0, A2 reveal-blind -1.2, A3 Uphill-blind -0.4, A4 Relay-blind -3.2 per bot: all four fail the >= 5 test, so the hidden-partner twist does not yet change best play. Uphill-off variant: runaway +26 points (Uphill rule matters as a rule, not as a bot decision). Open for the critic and the owner.
4. **Self-check (v1.1):** closed the 9 playtest ambiguities in wording: Relay when the partner's Rope is already played (partnership public either way), four of a kind (not a type; split it), first/second out defined and non-out players score only their team share, Uphill uses start-of-hand scores with difference >= 4, tie-break order with shared win, trick end (every other in-hand player passes in a row since the last play), pass-then-play allowed, leader (including after Relay) cannot pass, turn cap stated as unreachable safety rule, going out requires playing the Rope (consequence, not a rule). No dead card (all five play types are used: Single 98.5%, Rope 88.4%, Pair 56.1%, Run 49.7%, Triple 9.2%).
5. **Band and knob:** seat gap 0.9 (<= 5, passes); first-lead team 61.0% (band 50-60%, slightly high), pairing spread 3.6 (passes); knobs first-out/second-out points (3/1) and Uphill threshold 4.
6. **Ends:** after hand 6; a hand ends at the second player out (cap 200 turns, max possible 176, never hit). Measured 54 turns per hand, about 27.3 minutes vs 25 target (inside +-20%, sensitive to pace).
7. **Budget:** sections 1-6 are about 55 lines, 3 special rules (Ropes, Relay, Uphill) vs one page and 3 promised.
8. **Re-run list:** v1.1 changes wording only, matching the simulation's readings, so no re-run is needed; any future lever change re-runs A1-A4, Uphill-off, Relay-off, code attack and all three bots (L10).
