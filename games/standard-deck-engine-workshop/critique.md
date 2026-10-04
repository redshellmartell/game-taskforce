# Critique: Fifty-Two Workshop (revision 0)

**Verdict: REVISE-MAJOR**

Average score 3.0 (KPI at pitch: 3.5 or more). The 52-card engine-builder is a good gap and a cheap product. The first draft does not yet deliver its own promise: the engine does not pay, solo is trivially won, and the rules are heavier than the brief allows.

## Scores (1-5)

| Area | Score | Why |
|---|---|---|
| Originality | 3 | Brief's comparables checked (Wingspan Pocket, Sprawlopolis, banked Pocket Tableau). None is a standard-deck engine-builder, so no copying risk. The pieces are familiar: rank runs (rummy, Sprawlopolis-style adjacency), market row, pay-to-discard. I did not search further, so this is a judgement from the brief and rules, not a fresh scan. |
| Clarity | 2 | Brief asked for one page and at most 3 special rules. The game has trains, per-Spade discounts, per-Club pulls, a payment sum with no change, a Bench that grows past 5, a hand limit that feeds the Bench, Apprentice, round-finish logic and per-suit scoring with a Heart train bonus. Panel rules_simplicity is 0.149 on every persona. 11 ambiguities were listed against a target of zero. A new player could learn it, but not from one card. |
| Fun | 3 | Chain turns (8S, 7S, then a Club pulling a King) sound good. But the narrated game has one real decision per turn, a forced middle stretch and a leader who never changed after the middle. Strategic beats greedy by only 3 points at 2p, so most of the thinking is "take the most points now". Bot fun is 3.99 on average but 3.2 to 3.5 for family and casual, who are half the brief's audience. |
| Balance | 2 | Seat gaps (4.0 max) and runaway (36-60%) pass. Lead changes are on the floor (2.03). Fails: solo win rate 98.6% strategic and 68% random against a ~50% target; solo length 6 of 15 minutes; Spades have negative win correlation and K-spade -0.15; Hearts win (+0.10); the engine-minded bots lose to the long-mixed-Heart bot (31-33% against 40.6%). The no-progress loop is an open rule hole. |
| Market fit | 4 | Still matches the gap: standard deck, small box, solo-capable, 20 minutes. Drift risk: the engine is the brief's success test ("must feel like an engine-builder, not solitaire"), and current data says Hearts-in-a-mixed-train beats engine play. Interaction is mild (0.3-0.5 turns in 1 take a paid card), so the solitaire-variant risk named in the brief is not yet cleared. |
| Production | 5 | One standard deck and one rule card. Nothing to make. Only caveat: the rule card has to carry rank values, suit table, turn summary, clock table and solo ladder, which is a lot for one card. |

## Biggest strength
Near-zero production cost with a clear hook (a deck everyone owns, with suit as function, rank as cost and adjacency as power) and solid multiplayer numbers: seats, runaway and skill gap all pass.

## Biggest weakness
The advertised engine does not pay. The data says engine suits are the worse line, and strategic play barely beats greedy. The whole pitch is "an engine-builder on a standard deck", so this is a design failure, not a tuning footnote. The solo mode, which the brief called first-class, is untuned to the point of being no game.

## Required changes (each with the measure it should move)

1. **Make the engine pay.** Test one at a time: Spade discount 4, or Spade 2 points; Clubs pull 1 plus a 0-cost pull. Target: Spade and Club win correlation at or above 0; engine-minded bots (Planner, Optimiser) at or above the Flavour bot in the panel rotation; strategic vs greedy at 2p of 60% or more. Moves: Balance, Fun.
2. **Fix solo.** Set the win line so the strategic bot wins about 50% (31 is a guess; re-measure), make the Rival take 2 per turn or the 2 highest, and raise solo length toward 12-15 minutes (about 13+ turns' worth of real choices, not 19 trivial ones). Target: strategic solo 45-55%, random under 15%, estimated length within 16-24 minutes scaled to the 15-minute target (12-18). Moves: Balance.
3. **Close the stall loop** with the simplest rule, such as: remove the leftmost Bench card whenever the Bench holds more than 5 at end of turn. This also trims the Bench, which helps the clarity problem. Target: zero turn-cap hits in 46,000 games without a bot patch; rules ambiguity count drops by one.
4. **Cut rules weight.** Resolve all 11 ambiguities in the text (strike timing, deck-empty strike after refill, Apprentice tie, Club legality, no live score). Then simplify: consider dropping Apprentice if catch-up is not needed (seat gap is already 4.0), and give the Hearts bonus a simple count. Target: zero ambiguities; rules_simplicity above 0.149; rules card fits one side. Moves: Clarity.
5. **Add decisions and interaction.** The panel and the narrated game both show one real decision per turn and weak interaction. Ask the designer to give players a reason to Gather the rival's needed rank beyond a bot heuristic (for example, a visible rank gap rule), then re-measure. Target: lead changes 2.5 or more, rival-take rate above 0.5 per 1 turn, strategic vs greedy gap widened. Moves: Fun, Market fit.
6. **Re-check the length at 4p** (16.6 of 20 minutes, -17%): consider a target of 10 workshop cards, and re-measure after change 1, since stronger Spades will shorten games.

Do not change several balance knobs together. The playtester's budget allows one-at-a-time testing, so changes 1 and 2 should be run as separate experiments.

## Is another revision worth it?
Yes: the failures have concrete, testable fixes (suit values, the win line, a stall breaker), the multiplayer seat/runaway numbers already pass, and the idea scored 27/30 in the brief. Limit it to one revision and kill if the engine still does not outscore Hearts-mixed play afterwards.
