# Critique: Tug of Crowns (rules v2, revision 1)

**Verdict: REVISE-MAJOR** (one last, narrowly scoped revision; see "Is another revision worth it?")

Note: no panel-report.md exists. Fun and Market fit rest on `panel.json` bot predictions (average fun 3.30, competitor 4.03, family 2.67) and the narrated play. Originality was not re-checked: the core mechanic did not change (closest game remains Tug of Roar, medium).

## Scores (1-5)

| Area | Score | Reason |
|---|---|---|
| Originality | 3 | Unchanged from revision 0. Hush/Retort/Echo plus Treasury/Spend is a fresh mix on a known tug-track bidding pattern. |
| Clarity | 4 | Up from 3. All 8 ambiguities resolved, Retort has its own section, margin rules deleted. Still two keyword sets and a chooser rule; panel rules_simplicity was very low last time and has not been shown to improve. |
| Fun | 3 | Panel fun 3.30 (flat). The narrated game has one good round (three Hushes, 12-11 win), but a dull round 2, 15% of games end abruptly in round 2, and 31% by round 3. The lead choice is again a solved decision. |
| Balance | 2 | Down from 3. Side gap 10.9 (target 5) and it flips with skill (Treasurer 58% random, about 38% greedy/strategic). Always-lead-self 63% vs always-give 43% (target 40-60). A greedy always-lead bot beats the strategic bot. Passing: skill gap +56, early leader 49%, centre endings 0%. Lead changes 1.83 (target 2, near miss). Experiments were not re-run after the coin bug fix. |
| Market fit | 3 | Still on the brief's gap (cards only, 2P, asymmetric, short). Casual and family bots remain the weak audience. Average 12.7 min vs 15 target is acceptable. |
| Production | 5 | 47 cards, no dice, no board. |

**Average: 3.33** (below the 3.5 pitch bar; same as revision 0, with Clarity up and Balance down).

## Biggest strength
Revision 1 fixed the structural pacing problems from revision 0: no dead-centre endings, lead changes up from 1.15 to 1.83, zero ambiguities, and a skill gap of +56. The game now reaches decisive endings.

## Biggest weakness
The lead mechanic is unstable. Five variants each left one policy dominant (self 65%, balanced but meaningless, give 60%, self 59%, self 63%). The one variant with balanced policies (E2, no extra card) makes the choice barely matter and gives the Treasurer 62%. This shows the lead-bonus is a knife-edge lever, not a tuning-by-small-steps one.

## Tuning or structural?
Mixed. The track, pacing and clarity work is sound and only needs tuning (double-move margin 6 fixes early endings and probably the last 0.17 lead changes). The "chooser picks the lead, and the lead gets a card" idea is structural: it has failed in both of its forms (give it away, then take it). Another card-size tweak is a 6th guess at the same dial. The side gap (10.9, skill-dependent) is a second problem, largely independent, and cannot be tuned until the lead is fixed.

## Required changes
1. **Stop tuning the card bonus; remove the lead decision as a decision.** Either (a) the loser of the last round always leads (no choice, no extra card), or (b) the lead alternates, or (c) the playtester's non-card price (lead reveals one hand card, or plays first card face down) with the choice kept. Prefer (a) or (b): shortest rules, no solved choice. If E2-style (no bonus) is used, expect the Treasurer at about 62% and handle that in item 2. KPI: any fixed lead policy 40-60% (n/a if no choice); Balance 2 to 3+.
2. **Close the side gap with one lever at a time, in the order of section 7:** after item 1, if the Treasurer is above 55% (random) or below 45% (strategic), adjust the Treasury cap or Spend bonus. Test side gap against random, greedy and strategic bots separately; require the gap at most 5 in the strategic mirror and no more than 10 across the skill ladder. KPI: side gap at most 5; improves Balance.
3. **Double-move margin 6.** Target: games ending by round 3 below 20% (now 31%), lead changes at least 2.0, runaway leader at most 65%. Improves Fun and Balance.
4. **Re-run all experiments on the fixed simulator** (the coin bug was found after the five experiments). KPI: numbers on the corrected sim only.
5. **Optional, low:** drop The Whisper to 4 Influence or cut it to a single copy if it stays at +17 points. Improves Balance.

## Is another revision worth it?
Yes, once and with a changed approach: delete the lead-choice dial instead of retuning it, since the other problems (pacing, clarity, no dead ends) are already fixed and measurable. If revision 2 still shows a side gap above 8 or fun below 3.3, park the game rather than use revision 3: it would then be a competitive-player niche filler, not a pitch.

## Recommendation to the owner
Do not pitch now (average 3.33, balance FAIL, no dominant-strategy-free lead). Revise once more with the changes above (usage M), or park. Pitch-as-is is not advised.
