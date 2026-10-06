# Critique: Silent Duo (rules v2.1, playtested at v2; revision 1 / cycle 1)

**Verdict: REVISE-MINOR.** Average 3.67/5 (was REVISE-MAJOR, 3.5).

Caveats. Everything below is bots only and unvalidated; no human has played it. Human teams deduce worse than Honest, so real win rates will be lower than shown. Fun and Market fit lean on free bot-predicted panel scores (fun 3.98, worst fit family 3.07). The activity log is left to the Director (no clock).

## Scores

| Area | Score | Note |
|---|---|---|
| Originality | 3 | Unchanged core mechanic (Hanabi-like hidden own info, Crew-style silence; the double-lamp token-flip Offer is the new device). Not re-checked, as instructed. |
| Rules clarity | 4 | v2.1 closed the 10 ambiguities, 4A and 5.2 agree. Still about 227 lines against a "one page" promise (L7, untimed). |
| Fun | 3 | Turns 1-10 are good puzzles. The middle is flat: Trim is 30% of turns, 3+ Trim runs in 61% of 2p games, and 60% of Trims happen because no Offer is legal. Narrated game ends in a forced double miss. |
| Balance | 3 | Big improvement at 2p, but 3p, Greedy-vs-Honest at 3p, Beacon and Trim KPIs still fail (see below). |
| Market fit | 4 | Still cards-only, tuckbox, about 18 minutes, 2-3 players. Family fit weak (3.07), a known drift, not new. |
| Production | 5 | 50 cards, 2 reference cards, 3 tokens. |

## Originality
Closest: Hanabi (medium). Others: The Crew, Bomb Busters, Sky Team. Core mechanic unchanged; no copying; not a KILL.

## Rules clarity
A new player can learn the turn from `rules.md`. Remaining issues are small: the rulebook length (L7), and the "Known gaps" section still says the anti-code claim is "not simulated" and "Standard F = 8 is provisional", which is stale now that the playtest has run. Update the gaps and the 7.7 target text to the real numbers. The Offer legality rule (three distinct values strictly inside the open range) is correct but is the root of the Trim problem and is hard to explain in one sentence.

## Fun
- Strength: every early Offer is a real choice (which ship, which pair), and a Beacon on turn 2 is a happy moment.
- Weakness: from about turn 11 on, players hold cards that fit no open range, so they Trim and wait. 60% of Trims are forced by the legality rule. The playtester's own narrated game spent 7 of 9 turns Trimming and then lost to luck of the draw. That is the pacing problem the v1 critique already named, only half-fixed: share dropped from 38% to 30%, runs of 3+ are still in 61% of games.
- Comeback (L3 adjacent, co-op): 7.4 claims Trim selection repairs a bad deal. Data shows Trim-blind loses 12-16 points, so the keep choice matters, but a mechanism that fires on 30% of turns is a crutch, not a comeback. Closeness KPIs (late wins, near-losses) are in `sim/results.json` and were not summarised in the report; the Director should check them.

## Balance (playbook check)
- Two bots (L2): Honest and Greedy plus Random, spread reported. Good.
- Co-op band (L5): 2p F8 56/58 is in band (was 73/82). The F knob worked. 2p F12 42/47 also in band.
- Every player count (L8): 3p F8 Honest 38% is under band; Greedy beats Honest by 9.4 (target at most 5). The playtester proposes F6 (43/53) but that is an untested rules default and the Greedy gap stays at 9.7. At 3p, risk-taking pays more than caution, which is the same "caution does not pay" symptom the 2-Reef change cured at 2p only. 3p is the weakest mode and "best at 2" is already the rules' own claim; consider dropping 3p or labelling it variant.
- Ablations (L1): pair-blind 8.9/7.9, trim-blind 15.9/12.0, no card counting 13.8/10.0 all pass. **Beacon-blind 0.5/0.9 fails**: the Beacon is a flat time gift (removing it outright costs Honest 11.3 points, so it does matter as a balance dial but not as a decision). The rule is not dead but it is not a twist either; the design currently advertises it as one.
- Code attack: +1.0 (F8), +3.0 (F12), pass. F16 not re-run; it was the failing point (+12.1) and is not a supported setting now, so this is acceptable but should be run once after the next change to Offer legality, since loosening legality is the likely fix and it reopens the code channel.
- Skill gap 54.7 (target 20): pass. Random 1.2%.
- Length 18.1 minutes (-9%): pass. Turn-cap hits 0.
- Trim 30% of turns (target under 25%): fail. 3+ Trim runs 61% (target under 10%): fail. Beacons 2.0 per game: borderline pass.

## Market fit and production
No drift. Cost is trivial, about 2 USD of printing for 52 cards.

## Biggest strength
The 2p difficulty knob now works: Honest and Greedy land at 56/58 with a skill gap of 55 and a code attack that no longer pays. The core Offer puzzle is novel and cheap to produce.

## Biggest weakness
Pacing in the middle game: Trim as a forced waiting action (30% of turns, 61% of games with 3+ Trim runs, mostly because the anti-code legality rule leaves no legal Offer). This repeats **L3** (flat, decided-by-luck stretch), **L8** (3p out of band, Greedy beats Honest) and **L1** (Beacon-blind ablation fails: a twist that is not a decision). It is the same Trim complaint the v1 critique raised; the v2 fix reduced it but did not meet the KPI.

## Required changes (REVISE-MINOR)
1. **Stop the Trim stall.** Loosen Offer legality so it is rarely impossible (for example allow an Offer when only one card is inside the range, shown as the legal revealed card, or allow Offer after a Trim). Target: Trim under 25% of turns, 3+ Trim runs under 10% of games. Re-run Code attack at F8 and F12 (must stay at most Honest + 10), and keep 2p Honest/Greedy in 40-60%.
2. **Make Beacon a decision or cut it.** Either let a player choose between a safe Light and holding for an exact hit with a visible cost, or cut it and drop F accordingly. Target: Beacon-blind loses at least 5 points, or the rule is removed and 2p band re-confirmed.
3. **Fix 3p.** Set F = 6 as the 3p Standard and re-test, aiming for Greedy minus Honest at most 5 and both bots in 40-60; if that cannot be reached in one pass, mark 3p as a variant (2p only in the pitch). Target: balance score.
4. **Update `rules.md` Known gaps and 7.3/7.6 text** to the measured results; keep the line count from growing (L7).
5. Optional: summarise close-game shares (late win, near-loss) in the report.

## Remaining problems: mechanical or structural?
Mechanical. Each has a named fix inside the existing rules (legality threshold, Beacon wording or cut, F per player count). The only real tension is that loosening Offer legality could reopen the code channel; that is a test, not a redesign, and Code attack has about 7 points of headroom at F12.

## Is another revision worth it?
Yes: one more cycle, because the problems are mechanical, the 2p numbers are in band, and the next revision should target Trim share under 25% with 3+ Trim runs under 10% while Code attack stays at most Honest + 10. If Trim share does not fall below 25% after that cycle, stop and take the human playtest instead of iterating on bots.
