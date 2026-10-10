# Critique: Heavenly Bodies v2 "Gearbox" (cycle 1)

**Verdict: REVISE-MAJOR.** Average **3.00** (previous 3.17, cycle 0; pitch bar 3.5). Bots only, unvalidated. The fix pass was text only and not re-simulated, so this judges the rules text plus the cycle 1 playtest (BROKEN, an overshoot).

| Area | Prev | Now | Why |
|---|---|---|---|
| Originality | 4 | 4 | Not re-checked (core mechanic unchanged). Closest: Orbita, similarity low. |
| Rules clarity | 3 | 4 | The 11 ambiguities are ruled and the sim follows the text. Shield and the sideways card read clearly in the logs. Soft spots: spinning an orbit with only a sideways body is a free pass (F10), and 2p contact geometry still needs a diagram. |
| Fun | 2 | 2 | A 3-turn 2p game is decided by the deal. The playtester, reading the logs as a player, found it boring and the spin choices irrelevant. Panel fun 2.87 (family 2.17). |
| Balance | 2 | 1 | Long Night is fixed (95-100% to 0%), but that is the only KPI that moved the right way. Seat gap passed in cycle 0 and now fails at every count (16.9 / 29.1 / 18.4). Length is 4.4 / 7.2 / 8.0 turns against 14-24 / 18-30 / 20-34. Captures 1.8 / 2.3 / 2.5 against 15-25. 2p midpoint leader wins 74.7%. Strategic loses to greedy by 8-14 points. Recall and Comet beats Giant are dead. Bar Raiser veto active. |
| Market fit | 3 | 2 | The owner's vision is simple, fun, kinetic, with cards changing owners. Simple and alternate win conditions are now delivered (all three patterns 21-46%). Kinetic is not: about 2 captures per game is not a "cards move around the table" game. A 2-3 minute game also misses the filler slot. |
| Production | 5 | 5 | 56 cards, nothing else, about $10-15. |

## Required changes from cycle 0: which were met
1. Win at the end of your own turn: **met, and it worked** (Long Night 95-100% to 0-0.1%; patterns now end the game).
2. Shorten the Deck / opening bodies: **not met**. The Deck was never the lever (DECK40 4.7 / 7.3 / 8.0 turns).
3. Cut Rebound and add a one-turn shield: **met, but the shield overshot.** It is the length lever (off gives 22.6 turns) and also the captures lever (18-22 per game), and it is too strong.
4. Captured bodies to Deep Space as an arm: **run, inert** (CAPTURE_TO_DS changes nothing). Keep captures going to hands.
5. Re-run ablations, cut or sharpen Recall: **run, not acted on.** Recall and comet-blind are dead at 3-4p, and the thresholds-by-count are inert.
6. Per-count knob and 2p length: **not met.** Threshold 17 and 1 opening body do not reach band at 2p.

Net: 1 of 6 cleanly met, 1 met with an overshoot. The average fell. Under the stop rule this is not yet "two cycles with no movement": the target moved (Long Night) and the diagnosis is sharper. It is also not a clean win.

## Strength and weakness
**Biggest strength:** the rules are now small and clear (56 cards, 3 special rules, about 80 player-facing lines). All three win patterns work (21-46% each), and strategic beats random by 92-98 points. The win-timing diagnosis (L14) was right and the fix was real. Opening 0 gave 8 / 15 / 18 turns, 2.4-6.5 lead changes and a 3p seat gap of 4.9, so there is a tested direction that nearly works.

**Biggest weakness:** one lever, the shield, trades off the two things the owner wants. With it, games are 3-8 turn races decided by tempo (first seat 62-67%) and almost nothing is captured. Without it, captures return (18-22 per game) but patterns die and Long Night comes back (20% / 83% / 87%). Repeats L14 (win checked in a disturbed board, now inverted), L13 (a fix that overshoots and worsens another number), L1/L12 (Recall, Comet beats Giant, shield-blind and threat-blind inert), L3 (2p runaway 74.7%) and L8 (every count has a different problem).

## Is the owner's kinetic vision still in the game?
Mostly not, in the default rules. Spin-any-orbit is there as a verb, but with about 2 captures per game, cards almost never change owners, and spinning is nearly a free pass (the self-spin-only ablation is +2.2 at 2p, which is inert by construction). In cycle 0 the churn was the whole game (30-59 captures) but the win patterns were dead. The design now has the opposite problem. The owner's vision is "both at once": enough captures to feel the gearbox (I would call 8-15 per game the real target, not the old 15-25), and a pattern ending that still fires. No data point yet has both. The best candidate (opening 0) reaches only 2.1 / 3.5 / 3.7 captures.

## Structural or fixable in cycles?
**Probably fixable, with one more cycle; not proven.** The break is one coupled lever, not the core. The reasons to think so: opening 0 moved length, lead changes and the 3p seat gap in the right direction with a single change, and two untested shield variants sit between "full" and "none". The reasons for doubt: the shield-on regime reaches captures near 3 and the shield-off regime kills patterns, and nothing between them has been measured. If a sweep of the middle region finds no cell with captures of at least 8, turns in band and seat gap of at most 5 at 2 of 3 counts, treat it as structural (the "race to a pile" and "constant churn" aims are in tension) and stop.

## Required changes for cycle 2 (sweep first, then one coherent rule set; L10, L13)
**Step 0, free: a sweep before the designer commits.** The playtester runs these cells at 2/3/4p (1,000 games each, two bots) and reports turns, captures, seat gap, lead changes, Long Night:
- Shield variants: full (now), none, **Comet/Giant only** (shield protects only against a Comet or a Giant), **until the next spin of that orbit by anyone**.
- Each crossed with opening bodies 0 and 1.
- Best cell(s) crossed with Critical Mass +1 (17 / 16 / 15).
Test the shield variants first, with opening 0 held fixed, because the shield is the lever that controls both length and captures.

Then the designer adopts the single best cell as a coherent set, not a bundle:
1. **Opening bodies 0** (or 1 at 2p, if that is what the sweep picks). KPI: turns into 14-24 / 18-30 / 20-34 (now 8 / 15 / 18), lead changes at least 2 (now 2.4 / 5.2 / 6.5, already met), runaway at most 65% (2p now 0.80).
2. **A weaker shield, chosen by the sweep** (Comet/Giant-only or until the next spin of that orbit). KPI: captures at least 8 per game at every count (now 2.1-3.7), Long Night at most 10 / 10 / 15%, and 2p turns toward band.
3. **Seat compensation for the last seat** (draw 2 on its first turn), tested as its own cell. KPI: seat gap at most 5 at 2 / 3 / 4p (opening 0 alone: 11.6 / 4.9 / 10.0).
4. **Cut Recall** unless its ablation passes at 5 points in the chosen cell, and cut or rework Comet beats Giant if Giants are still captured under 0.5 times per game. This lowers the rules count. KPI: zero dead twists at pitch (design-rules 2). Also drop the inert switches (CM_BY_COUNT, DEEPSPACE_DRAW, DECK40, CAPTURE_TO_DS) from the text.
5. **Re-run all ablations at every count after the change** (self-spin-only, shield-blind, threat-blind, comet-blind, no-Recall), plus strategic vs greedy. KPI: strategic at least as good as greedy (now -14 / -8 / -13) and every kept twist losing by at least 5 points. Note that self-spin-only is inert at 2p by construction, so use a different test of spin value there.

**Protect:** win-at-end-of-turn (the real fix), rainbow Constellation, 56 cards, spin any orbit, captures going to hands, launch never crashes.

## Continue or stop?
**Is another revision worth it?** Yes, one more cycle only, sweep-first: the diagnosis is clear, a single-change experiment already moved most KPIs, and the missing cells are cheap to run. Success means captures of at least 8, turns in band at 2 of 3 counts and a seat gap of at most 5 at 2 of 3 counts. If cycle 2 misses that, stop: park or take it to a human playtest rather than a cycle 4. Bots cannot say whether a 15-turn game with a few captures feels kinetic, so I also recommend a human playtest of the best sweep cell (or even the cycle 1 rules as a 3-minute filler) as soon as a candidate is in band, ahead of any more bot tuning.

Lessons this repeats: L13, L14, L12, L3.
