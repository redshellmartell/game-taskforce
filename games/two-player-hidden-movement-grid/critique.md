# Critique: Dead Reckoning (revision 0)

**Verdict: REVISE-MAJOR**

Average 3.33 (target 3.5 at pitch). The structure is sound and the seat and skill numbers are good. But two KPIs fail, one card is dead, and the core promise ("reading the rival beats luck") is not shown in the numbers.

## Scores (1-5)
| Area | Score | Note |
|---|---|---|
| Originality | 3 | Mechanic mix is familiar; see below |
| Rules clarity | 3 | One-page goal missed; 6 ambiguities; many sub-rules |
| Fun | 3 | Good peaks, dull middle; skill is mostly routing, not reading |
| Balance | 3 | Seat and skill pass; runaway 0.79, lead changes 1.5, dead Sonar ping |
| Market fit | 3 | Still a fast 2-player duel with no downtime, but a family fit of 2.91 |
| Production | 5 | 25 grid cards + 18 helm cards + 2 tokens; trivial and cheap |

Average: 3.33.

## Originality
- **Closest: Creep in Silent (2021)**, a two-player submarine game where each side lays three movement cards from a six-card hand and estimates the rival's position. Similarity is **medium**. Dead Reckoning differs in a few ways. It uses a shared grid of face-down salvage, it is a score race, and its cooling row makes both hands public. I only saw search snippets, so I can't compare the rules in detail. Check this before any prototype is shown to others.
- **Submarine (wargame)**: simultaneous plotted movement, but a hidden position. Low similarity.
- **Onitama**: shares only "a limited set of move cards, and what you played shapes what you can do next" (its cards rotate, so the idea is similar). It is open, alternating and deterministic, so similarity is **low-medium**. The "cards you used are visible and temporarily unavailable" idea is the nearest overlap, and is not unique to either game.
- **Nine Fields**: the overlap is only "a grid of face-down cards". It is 2-4 players, alternating turns and area control. Dead Reckoning is a simultaneous duel with no area control. Similarity **low**; the brief's distinction holds.
- No copied rules or text found, so no automatic KILL.

## Rules clarity
A new player could learn the basic loop (plot three, resolve step by step), but not cleanly. Problems:
- Step order has six sub-phases (reveal, aim, collision, move/enter, reef bounce clash, fire). The brief asked for a one-page rule set with at most 3 special rules. The "three special rules" label hides Mine cancellation, Reef bounce and its clash, Harbour immunity, Sonar scoring and ping order, and two tiebreakers.
- The six ambiguities in `playtest.json` must be closed: Sonar counting for lead and ping order, Reef bounce clash wording, cooling of cancelled cards, same face-down target, tiebreak counts after thefts, and ping priority.
- Scoring a held Sonar as 1 point while also letting it be spent makes "who is behind" unclear.
- The panel's rules_simplicity metric is 0.09 for every persona, the lowest metric across the board.
- The Reef bounce clash is the likeliest rule to be played wrongly at a table. It could be dropped (see changes).

## Fun
- **Strong:** no downtime; the torpedo plus forced-collision comeback in the narrated round 2 was a real tense moment; the cooling row is a neat, readable hook.
- **Weak:** round 1 is a coin flip and sets the lead (the narrated game was 6-0 after round 1 with no decisions). About 75% of games end at the round-10 cap with Salvage still on the grid, so a leader coasts. Blind bots lose only 55-45 to bots that read the cooling row, so the signature mechanic is worth about 5 points. The playtester says the skill gap (75 points) comes from route efficiency, not from outguessing. That makes this a "pick the best path through fog" game with a light guessing layer, not the hidden-movement duel the brief promised.
- The panel fun of 3.75 is inflated by the bots' skill gap. The casual, story and family scores (3.19, 3.26, 2.91) are the more honest ones for the 10+ audience in the brief, and those players lose to skilled players 67-75% of the time.

## Balance (against KPI targets)
| KPI | Result | Target | Status |
|---|---|---|---|
| Seat gap | 1.4 | <= 5 | pass |
| Strategic vs random | 75 points | >= 20 | pass |
| Length | 9.6 rounds, about 14.8 min (designer's 85 s per round estimate) | 12-18 min | pass, unmeasured |
| Runaway leader | 0.79 | <= 0.65 | **fail** |
| Lead changes | 1.50 | >= 2 | **fail** |
| Dead cards | Sonar ping | 0 | **fail** (never pinging wins 50.0%) |
| Ambiguities | 6 | 0 | **fail** (minor) |
| Dominant strategy | none found | none | pass |

Also note: the panel's family seat win rates are 48.7% vs 41.4%, so the seat gap may be larger with weak players. Not enough data to say more.

## Market fit
Still matches the gap: a two-player, simultaneous, low-downtime duel with a grid of cards and cheap parts. It drifted slightly. The brief wanted "a real rock-paper-scissors layer", but the sim shows luck of the fog and routing dominate. The family audience (brief: "adults and families 10+") is the worst fit (would not buy).

## Production
About 45 cards and 2 tokens, no board. Needs two distinct card backs for the Harbours, two coloured helm decks, and clear icons for the 5 helm cards. Cost around $15. No hard-to-make parts.

## Biggest strength
A very cheap, no-downtime two-player design with a clear hook (the visible cooling row) and good seat balance and skill gap.

## Biggest weakness
Early fog-flip luck decides most games (runaway 0.79, 1.5 lead changes, a round-1 coin flip), and the signature reading layer adds only about 5 points of skill. The game does not yet deliver the "outguess your rival" experience it is sold on.

## Required changes
Change one or two at a time and re-run the same experiments.
1. **Reduce early-fog luck.** Options: make most Salvage worth 1 and 2 (for example 8x1, 4x2, 1x3), cut Mines from 4 to 2, or give each player a free peek at 2 face-down cards in setup. Aims to cut the runaway rate from 0.79 toward 0.65 and raise lead changes toward 2.
2. **Fix the comeback gap.** For example a hit victim cannot be hit again until their next-but-one round, plus a rule that a trailer's first Salvage taken in a round scores +1. Must raise torpedo-driven lead changes without making torpedo spam dominant (E1 was 47.8%, so there is room). KPI: lead changes >= 2.
3. **Make Sonar matter.** Replace the ping with "reveal two steps", or "peek at one face-down card", and re-run E4. KPI: dead cards = 0 (never-ping must fall to 45% or less).
4. **Stop coasting on the cap.** Either raise the cap to 12 rounds or end the game when one player leads by 8 or more with no Salvage within reach. Keep length at 12-18 minutes. KPI: runaway leader and length within +-20%.
5. **Raise the value of reading.** Test a deeper bot; if cooling-row reading is still under 10 points, let the cooling row also affect something visible, such as Salvage taken by a played card. KPI: blind-vs-reading gap above 10 points.
6. **Close all 6 ambiguities** and cut sub-rules. Consider removing the Reef bounce clash (make the other sub simply stay) and the Sonar-counts-1-point rule. KPI: ambiguities = 0, rules_simplicity above 0.09 in the panel.
7. **Find out about Creep in Silent.** Compare in one search. If the similarity is higher than medium, the differences must be made clearer in the rules.

## Is another revision worth it?
**Yes.** The core loop, seat balance and skill gap are healthy, the failures are narrow and measurable, and each fix has a named KPI. I expect it to reach REVISE-MINOR or PASS in one loop if luck and comeback are both fixed. If revision 1 does not move the runaway rate below 0.70, stop and park it.
