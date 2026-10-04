AMBIGUITIES = [
 "Gather when picks are optional: taking from the deck is blind (top card goes straight to hand); simulated as such.",
 "Apprentice with a tie for fewest workshop cards: 'strictly fewer than every other player' read literally, so no bonus on a tie.",
 "Clock striking on the last-seat player's own turn ends the game at once; if it strikes earlier, play continues to the end of that round (seat n finishes). Interpreted as written.",
 "Deck-empty clock: checked after the refill, so the clock can strike the moment the last card is dealt to the Bench; the deck is NOT empty while any of those cards could still be drawn.",
 "Build legality counts only the other cards in hand BEFORE Gears pull; the rules say this explicitly, but a Club build that is illegal by hand total could be legal after Gears. Simulated as written.",
 "Cost 0 builds: paying is forbidden; no ambiguity, but a 0-cost build with Gears still pulls cards.",
 "Hand limit discards may be the cards just paid? No: discard is after payment; interpreted as discards happen after the build.",
 "Solo: Rival acts before refill and the clock is checked after refill; the 'deck empty' strike can come before 11 builds. Interpreted as written.",
 "Pass: only if neither Gather nor Build is legal (Bench and deck empty and no legal build). Counted in stats.",
 "Same-rank tiebreak sequence: score, workshop cards, longest train, then shared win (shared wins count as fractional wins).",
 "'Best' progress for lead changes: provisional score of the workshop at the end of each full round (the rules have no live score).",
]

VERDICT = "NEEDS-FIXES"
REVISION = 0
PROBLEMS = [
 {"severity": "high", "problem": "Solo win line (22) is trivially met: a strategic or greedy bot wins about 98.5% and even the random bot wins 68%; the ladder titles above Apprentice mean nothing. Solo also runs about 19.5 turns (about 6 estimated minutes) against a 15-minute target.",
  "evidence": "2,000 solo games per bot: random 68.0% (avg 23.9), greedy 98.4% (avg 30.9), strategic 98.6% (avg 30.4), rush 67.0%.",
  "fix": "Raise the win line to about 31+ (untested: strategic average is 30.4, so aim for about 50% at 31); make the Rival take 2 cards per turn or the 2 highest cards so solo is longer and tighter; re-measure."},
 {"severity": "medium", "problem": "The engine suits do not pay. Spades have a negative win correlation (-0.06 overall, K-spade -0.15) and Hearts a strongly positive one (+0.10); Spades and Clubs are built only 14% and 11% of the time against 20% for Diamonds. The advertised 'engine first' strategy is not clearly the best line, and Strategic beats Greedy by only 3 to 9 points.",
  "evidence": "Win correlation by suit in the 4-player strategic mirror (8,000 workshops): S -0.056, C +0.031, D -0.013, H +0.100. Strategic v greedy 53.1% (2p). Engine-heavy planner bot v greedy 55.6%, optimiser v greedy 57.6%. In the panel rotation the Flavour (story) bot, which just builds long mixed trains with Hearts, wins the most (40.6% over all tables, 16,000 games) against the engine-minded Planner (33.0%), Optimiser (32.4%) and Expert (31.8%).",
  "fix": "Strengthen the engine: Spade discount 4 (knob in the notes) or give Spades 2 points; test one at a time. This is also a skill-ceiling issue: beyond not playing randomly, the decisions barely beat 'take the most points now'."},
 {"severity": "medium", "problem": "Rules allow a no-progress loop: Gather, then hand-limit discards put the same cards back on the Bench, the Bench stays at 5 so the deck never shrinks, and the clock never strikes. A cautious or threshold-based player can do this forever.",
  "evidence": "Before a bot fix, 8 of 2,000 strategic 2-player games (0.4%) hit the 600-turn cap; the log shows two players swapping 6C/5C/3H endlessly with 7-card hands and 1 workshop card each. After the fix (a full hand forces a build) there were 0 cap hits in 46,000 games, so humans rarely hit it, but the rule is open.",
  "fix": "Add a stall breaker: for example, discarded cards go to the Bench and then the leftmost Bench card is removed from the game whenever the Bench has more than 5 cards, or a player who Gathers with a full hand must Build."},
 {"severity": "low", "problem": "Last seat has a steady advantage (it sees the whole round and always gets a final turn).",
  "evidence": "Strategic mirrors: 2p seat 2 wins 54.0%, 3p seat 3 37.2%, 4p seat 4 28.3%; max deviation from fair 4.0 / 3.9 / 3.3 points (KPI 5). Noise is about 1 point at 2,000 games.",
  "fix": "No change needed now; if it grows after other fixes, give seats 3 and 4 a 4-card start (knob in the notes)."},
 {"severity": "low", "problem": "Length at 4 players is close to the lower limit and solo is far short; 2p and 3p are fine.",
  "evidence": "Estimated minutes (25s per build, 10s per gather): 2p 11.1 vs 12 (-7%), 3p 14.5 vs 16 (-9%), 4p 16.6 vs 20 (-17%), solo about 6 vs 15.",
  "fix": "Raise the 4-player target to 10 workshop cards, or accept; check against a human playtest because the time-per-action estimate is the designer's, not measured."},
 {"severity": "low", "problem": "Lead changes sit right on the 2.0 floor and score ties are common at 4 players.",
  "evidence": "Lead changes 2.03 (2p), 2.31 (3p), 2.08 (4p). Exact score ties 6.2% / 9.0% / 13.4%; tiebreakers resolve all but about 1% (shared wins).",
  "fix": "Watch after the engine fix; the tiebreakers (cards, then longest train) work."},
]
ESTIMATED_MINUTES = 16.6
TARGET_MINUTES = 20
