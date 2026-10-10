# Critique: Heavenly Bodies v2 "Gearbox" (cycle 0)

**Verdict: REVISE-MAJOR.** Average 3.17 (pitch bar is 3.5). All evidence is bots only; the fix pass was not re-simulated, so this judges the text plus the playtest numbers.

| Area | Score | Why |
|---|---|---|
| Originality | 4 | No close comparable found in 2 searches. Orbita is a track-and-margin duel with no captures. dnup is a shedding game. Spin-any-orbit with neighbour contacts that crash is not in either. Similarity: low. |
| Rules clarity | 3 | The fix pass closed the 12 ambiguities and the core loop is easy to say. Weak spots: West/East contact geometry (hard to picture at 2p, where both contacts are with the same opponent), spinning a non-neighbour at 4p, Rebound and Recall interplay, hand overflow between turns. |
| Fun | 2 | Per the narrated play: the first capture is fun, then it blurs into a hunt for the best capture. A full orbit never survives, so nobody plans a pattern. The result is a last-rounds lottery. Panel fun (4.03) is inflated by churn and is not evidence. |
| Balance | 2 | Seat gap passes (0.3 / 2.2 / 0.6). Everything else fails. Long Night is 95-100% against a band of 10-15%. Pattern wins are about 0-5%. Length is 40-47 turns against a 12-minute target. Greedy beats strategic at 4p. Rebound, Deep Space and Recall are marginal or inert. |
| Market fit | 3 | The brief's gap and the owner's vision are kinetic play and alternate win conditions. Kinetic is delivered (59/43/30 captures per game). Alternate win conditions are not: one fallback decides almost every game. Running 16-19 minutes also misses the filler slot. |
| Production | 5 | 56 cards, no other components, about $10-15. Trivial to make. |

**Simplicity (under 10 minutes to learn):** plausible. The 5-line teach script is honest, and there are 3 special rules, on budget with the brief. Two things threaten it. The contact geometry is spatial and may need a diagram on the Star card. Rebound plus Recall adds timing text that earns nothing, since Rebound is inert. Cutting Rebound makes this clearer, not weaker. Nobody has timed a teach (L7).

**Biggest strength:** spin-any-orbit is a real decision, not a cosmetic one. The self-spin-only ablation loses by +10 to +18 in the base game and by +26 to +34 in the win-at-end variant. Comet beats Giant also passes its ablation (+19 to +83). The game feels like a gearbox, and that is the owner's vision.

**Biggest weakness:** the win conditions are dead. A formed pattern survives to its owner's turn 0.0-0.2% of the time. An oracle probe with perfect information finds an unbreakable pattern in under 1% of positions. This is an ending-rule problem, not a tuning problem. It repeats L3 (no working comeback), L1 (twists that do not change play: Rebound, Recall, Deep Space), and L8 (4p fails where 3p nearly works). It also touches L4: the printed turn cap was wrong.

**Structural or fixable?** The core (spin, crash, capture) is sound. The break is the "must survive a full round" win timing, and the playtester has already shown a variant that nearly works: win at the end of your own turn gave 3p at 20 turns, Long Night 12.5%, and pattern wins split mass 42 / alignment 39 / constellation 5. So this is fixable in cycles. It does not need a new game. Two caveats apply. Pattern shares were not measured at 2p or 4p, where the variant breaks (2p ends in 4.9 turns, 4p stays at 58% Long Night). And the variant leaves Constellation weak. Two or more cycles without movement means recommend human playtest or park.

## Required changes for cycle 1 (single-change experiments, L10; re-run every ablation at every count, L13)

1. **Win check at the end of your own turn** (after Crash), with a per-count Critical Mass threshold as the knob (for example 15 at 3p, higher at 2p, lower at 4p). Moves: pattern wins from under 5% to 15-50% each (the 3p variant measured mass 42 / alignment 39 / constellation 5), Long Night from 95-100% to 15% or less, turns to 14-34.
2. **Shorten the Deck to about 32-36 cards** by cutting duplicates evenly across Sizes. If a cut is hard, use opening bodies = 3 or a lower round cap instead. Moves: turns toward 20-30 and minutes toward 12. Do this only after change 1, because Long Night would otherwise just end games sooner.
3. **Cut Rebound.** It is inert (runaway unchanged) and fires on about 70% of turns. Replace it only if the data demands it. A cleaner comeback is a one-turn shield on a newly launched body, so tempo does not swing every turn. Moves: captures per game (59/43/30 toward 15-25), the 4p greedy-beats-strategic gap, and runaway leader staying at or below 65%.
4. **Test, do not guess:** captured bodies to Deep Space instead of the hand. It is the strongest anti-churn lever, but it removes "cards changing owners", which the owner asked for. Run it as an alternative arm, not the default.
5. **Re-run ablations** for the weak ones (Recall: +2.0 / -4.0 at 3-4p, Deep Space-only: -2.9 to +8.0) and cut or sharpen whichever stays under 5 points. Add a keep-a-Giant-at-each-contact defence bot to check the oracle result is not a bot artefact. Use at least two reference bots (L2) and fix the Long Night tie rate (5-8% shared wins at 3-4p).
6. **Per-count decision:** 2p wins in 4.9 turns under change 1, so give it its own knob (a higher threshold or a 5-Size minimum). If 4p cannot reach band, drop it (design-rules 4).

**Protect:** spin-any-orbit (including opponents' orbits), Comet beats Giant, 56 cards with no extras, three patterns with simple names, the 5-minute teach, seat balance, and "launch never crashes".

**Is another revision worth it?** Yes. The core already passes its twist ablations, the diagnosis is clear (win timing), and one tested variant is near band at 3p. If cycle 1 does not move Long Night under 30% at 3p, stop and recommend a human playtest or park.
