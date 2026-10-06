# Critique: Last Bid Standing (revision 2, rules v3, playtested at v3)

**Verdict: REVISE-MINOR** (bots only, unvalidated; no human has played it). My own stop rule from the last critique now applies: stop designing and test with humans, or park.

| Area | Score | Previous |
|---|---|---|
| Originality | 3 | 3 |
| Rules clarity | 3 | 3 |
| Fun | 3 | 3 |
| Balance | 3 | 3 |
| Market fit | 3 | 3 |
| Production | 5 | 5 |
| **Average** | **3.33** (target 3.5 at pitch) | 3.33 |

## What changed since revision 1
- **Fixed:** Hype share 56/64% to 48/48% (target 45-50). The ceiling knob works cleanly (cap 3: 41%, cap 5: 53%). Mechanical, and it did not hurt the skill gap (lone strategic 31.2/32.5, planner 36.8/37.0).
- **Fixed:** open income cut at no visible cost. Rule count and memory burden fall.
- **Kept passing:** seat gap 1.1/2.1, runaway 48/45%, lead changes 3.3/3.6, length 18.5/19.7 min, forced passes 4.3/3.1%, no dead cards.
- **Not fixed:** 6p last-round flip 25% (target 20%); 5p 19% passes.
- **Got worse:** ignore-crash was the one twist that passed (+7.5/+5.5). It is now +3.0/-2.9 at 5p and -1.6/-2.5 at 6p. The ceiling made the crash worth at most 4 points a lot, so it is inert (L1). A revision that fixed one KPI broke the only twist that passed.

## Originality (3)
Core mechanic unchanged, no new search. Closest remains Burnout/Pairs (tied bids cancel). Similarity low to medium, no copying. The Hype-from-losing-bids hook is the distinctive part, and it is also the part that is least tested.

## Rules clarity (3)
Clean: three special rules, defined income procedure, tie-breaks, edge cases, a worked example. Face-down income removes the memory burden. Remaining: about 85 player-facing lines and about 175 in the file against a one-page promise (L7), teach untimed. The playtester's 3 ambiguities are minor. Tiebreakers need hands revealed at the end (add one line). The round-14 income draw exists only to feed a tiebreaker, which is odd text. The crash tie-break still means adding up rows of printed values. The Bid-card/Paddle same-back trick works on paper but is unproven with real hands.

## Fun (3)
Rounds 1-4 and the carried rich block are good moments. Weak points: a dud round where a tied 7 cancels and two lots sit; a thin mid-game when 3 players pass at once; and the narrated game says the winner was whoever took value 4-5 lots early, "not the one who steered the crash". The ceiling also made the crash reveal "a smaller surprise". So the hook (the bubble) is now a smaller part of the experience. Panel fun 3.44, worst fit family. Table talk and bluffing untestable.

## Balance (3)
Structural numbers are good. The design's claims are not:
- **L1, ablations:** ignore-crash fails at both counts. Ignore-hype flips sign at 5p (-5.3 strategic, +10.5 planner) though +16/+21 at 6p. Ignore-ties wins at 5p (-6.9/-3.0) and passes only at 6p. Ignore-cap passes for strategic only. So at 5p the three advertised mechanisms (Hype, crash, ties) are not shown to be skill levers; at 6p only Hype and ties are. The skill gap (31-37) must then come from general odds estimation and lot choice, which nearly any auction has.
- **L2, bot spread:** gap runs greedy 18.5/12.3, lite 26.6/22.8, strategic 31.2/32.5, planner 36.8/37.0. Greedy fails 20, and the spread shows skill is tied to bot depth. Mixed gap passes (14.1/11.2; planner 9.2/6.5).
- **L3 comeback:** runaway and lead changes pass, but 6p last-round flip 25% and crash identity flipping in the last round 33% at 6p says the end is a late scramble.
- **L8:** 5p and 6p behave differently on three ablations; the same deck being "built for both" is not borne out.
- L10 respected this cycle (single-change configs), which is why I can read the results.

## Market fit (3)
No drift: 5-6 players, simultaneous, cheap, card-only. Appeal rests on humans enjoying probability estimation, and "family" is the worst-fit persona for a probability-estimation game with losing bids burned.

## Production (5)
78 cards, no board, no tokens, about $15. Nothing hard to make.

## Biggest strength
The design is now tunable and well behaved on the structural KPIs (Hype share 48/48%, seat gap about 1-2, lead changes 3.3-3.6, runaway under 50%) with one clean knob, at a $15 card-only cost.

## Biggest weakness
The advertised twists do not demonstrably matter: ignore-crash fails at both counts, and ignore-hype and ignore-ties flip sign at 5p (L1, with L2 in the bot-dependent gap and L8 in the 5p/6p split). The ceiling that fixed Hype share also deflated the crash. The skill gap (31-37) is real in simulation but comes from general bidding skill, not the designed hook.

## Mechanical vs structural
- **Mechanical (small):** 6p flip 25% to 20% (running crash tie-break total or freeze Hype before round 14); add "hands revealed for tiebreaks"; drop or explain round-14 income; trim text.
- **Structural:** the crash is inert under a ceiling, and the cap-and-crash pair pulls against each other (cap makes Hype safe to ignore, crash needs Hype to be worth fighting over). Ties are a skill lever only at 6p. These are design-level, not tweaks. Untested option: make the crash bite (crashed category's lots score 0 printed value or -2), which is a new mechanic and a guess.

## Required changes (only if the owner wants one more step)
1. Before any more cycles, a human table test of 5 or 6 players, 2-3 games, with the current v3 rules. KPIs: human fun and replay scores, whether players notice the crash and the ties, teach time. Bots cannot answer whether the hook works.
2. If a revision is run anyway, one change only: make the crash bite (printed value reduction), re-measure ignore-crash at both counts (target at least +5) and Hype share (45-50%).
3. Add the end-of-game hand reveal line (clarity), and a running crash tie-break (6p flip at most 20%).

## Is another revision worth it?
**No: the stop rule I set was "if Hype share and the ablations do not move, stop"; Hype share moved, but the ablations did not (ignore-crash regressed from pass to fail), and the remaining failures are about whether the central twists matter, which is structural (L9). Put the game in front of humans, or park it; do not spend a third bot-only cycle.**
