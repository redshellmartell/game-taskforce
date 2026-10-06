# Critique: Ladder Pairs (revision 0, rules v1.1, playtested at v1)

**Verdict: REVISE-MAJOR** (all numbers bots only, unvalidated; no human has played it). Average 3.33 (target >= 3.5 at pitch).

Playbook check block: present, and it matches `playtest.json` and the report (A1 -7.0, A2 -1.2, A3 -0.4, A4 -3.2; runaway 0.403; lead changes 1.13; seat gap 0.9). The designer was honest and listed the failures under Known gaps. Ablations were run at 4 players only, which is the only supported count (fine). Three bots were used (Random, Greedy, Reader), so L2 is covered.

## Scores (1-5)
| Area | Score | Why |
|---|---|---|
| Originality | 3 | Climb/shed plus a called-partner idea. No copied rules or card text (no Dragon/Phoenix/Dog, no calls, no card passing, own scoring). It is a recombination of Big Two/Tichu and Sheepshead-style hidden partners, and the brief's own rubric warned of a 2. See below. |
| Clarity | 4 | About 55 rules lines, 3 special rules, v1.1 closed the 9 ambiguities. Small doubts: Relay timing (reveal-then-lead) and Uphill threshold arithmetic need a human read-through. Nobody has timed a teach (L7). |
| Fun | 2 | The headline twist does nothing. Narrated hand: waiting with no legal play, then "nothing I did for the partner mattered". 42% forced passes and runs of 3+ forced passes 1.9 per hand are a dead-turn problem (L11). Panel fun 3.68 is a predicted number from a bot model that scores the same skill and catch-up inputs for every persona, so it is weak support; family persona is worst fit at 3.24. |
| Balance | 3 | Seats 0.9 gap and runaway 0.403 pass. Lead changes 1.13 fail (target >= 2). First-lead team 61% (band 50-60, unsettled). Uphill alone carries the comeback (off: runaway 0.663, lead changes 0.53). |
| Market fit | 3 | Still a fit for the gap on paper (a lighter 25-minute climbing game). But the gap claim rests on hidden partners mattering, and they do not, so what is left is a simplified Big Two with random teams. Length is 27 min at the playtester's pace but 37 at a slower one, which would break the 20-30 band. |
| Production | 5 | 56 cards (standard deck plus 4 Rope cards), pencil and paper. Cheap and easy. |

## Strength and weakness
- **Strength:** clean, short, producible ruleset with healthy seat balance and runaway numbers, and the designer reported the failure honestly instead of hiding it.
- **Weakness:** the core twist is inert (L1) and the skill gap is "sensible vs random" only (L6): Reader does not beat Greedy (-2.5 / -1.5) and the partner-blind bot beats the partner-reading bot by 7. Also repeats L3 (lead changes under 2, one comeback mechanism), L11 (42% forced passes) and L7 (no teach timing).

## Originality check (2 searches, 0 page reads)
Closest existing game: **Tichu** (similarity medium; shared genre mechanics: climb, same-type beats, pass, shed, team scoring). Secondary: **Sheepshead/Skat** called partner (hidden partner by card held) and the "Secret Partners" EDH casual variant (cards dealt decide secret partners, revealed by playing). Searches found no climbing game with per-hand hidden partners set by dealt Rope cards, so the combination appears open (search snippets only, not exhaustive). No rules or text copied: not a KILL. Honest note: the twist is the only differentiator, and it currently does no work, so the real-world distinction from Big Two is thin.

## Stop-rule assessment: structural, not mechanical
The remaining problem is **structural**. It appears with every bot and every variant (9 Reader variants tried in `e1.py`, best only ties Greedy), and the cause is identified: points come only from finishing order, so helping a partner earns nothing and costs tempo. A tuning pass (Uphill threshold 3, set-aside count, first-out/second-out points) will not fix it. Two levers also pull against each other: making partner help pay (team credit) will raise comeback/lead-change variance but also risks making Greedy-vs-Reader gaps depend on the new credit rule instead of on reading. Per the stop rule, another *tuning* bot cycle is not worth it.

## Required changes (one scoring-level redesign, then re-run everything together per L10)
1. **Make partner help pay.** Change the score so the team result depends on both partners' play (for example team credit per trick won by either partner, or a Relay that gives the finisher's partner a real bonus), then re-run A1-A4, Uphill-off, Relay-off, code attack, and all three bots at once. Target: A1 partner-blind loses to Reader by >= 5 points per bot, and Reader beats Greedy by >= 5 in 1 v 3 (so the strategic gap is about reading, not just legality). Moves: Fun, Balance, the L1/L6 findings.
2. **Add a second comeback source or lower the Uphill threshold to 3.** Target: lead changes >= 2 with runaway still <= 65%.
3. **Cut forced-pass dead turns** (e.g. deal 9-10 or allow a legal "any single" pull-in), target forced passes under 30% of follow turns and fewer than 1 run of 3+ per hand. Keep it a separate single-change test.
4. **Time a real hand** (human) to settle length (27 vs 37 min).

## Is another revision worth it?
**Yes, but only one cycle and only the scoring redesign (change 1).** The diagnosis is clear (partner help has no payoff), the fix is a single lever, and the premise of the game rests on it. KPI that must move: A1 partner-blind margin from -7.0 to >= +5, and Reader minus Greedy from -2.5 to >= +5. If that does not move after this one cycle, park the game or take it to a human playtest rather than continuing bot cycles. Alternatively, because the stop rule treats this as structural, the owner may prefer to park now; the game's best-case outcome is a decent Big Two variant. Recommend one cycle, then pitch or park.
