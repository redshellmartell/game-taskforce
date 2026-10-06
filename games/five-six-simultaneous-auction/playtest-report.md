# Playtest report: Last Bid Standing, rules v3 (revision 2)

**Verdict: NEEDS-FIXES (bots only, unvalidated).** 88,000 simulated games; 2,000 per table kind at 5 and 6 players, 1,000 per extra configuration. No human has played it.

## Key numbers (5p / 6p, targets from CLAUDE.md and rules v3)
| KPI | Target | v3 5p / 6p | v2 |
|---|---|---|---|
| Hype share of points | 45-50% | 48% / 48% | 56% / 64% |
| Lone strategic gap vs 5 random | >= 20 | S 31.2 / 32.5, Planner 36.8 / 37.0, Lite 26.6 / 22.8, greedy 18.5 / 12.3 | 25.3 |
| Mixed 3+3 gap vs random | >= 5 | S 14.1 / 11.2, Planner 9.2 / 6.5 | 11.8 |
| Seat gap (all-strategic) | <= 5 | 1.1 / 2.1 | - |
| Runaway leader (half-way) | <= 65% | 48% / 45% (late 60%) | - |
| Lead changes | >= 2 | 3.3 / 3.6 | - |
| Length | 20 min +-20% | 18.5 / 19.7 min, 14 rounds fixed | 16 |
| Forced passes | <= 13% | 4.3% / 3.1% | 5.1% |
| Lots left on block | <= 5 | 3.9 / 4.0 | 2.9 |
| Last-round winner flip | <= 20% | 19% / 25% | 20% / 27% |
| Crash identity flips in last round | - | 17% / 33% | - |
| Ties / turn cap hits | - | 0.1% / 0.5% / 0 | - |

## Ablations (full bot win rate minus ablated bot, points; strategic / planner)
| Ablation | 5p | 6p | Target >= +5 |
|---|---|---|---|
| ignore-hype | -5.3 / +10.5 | +16.1 / +20.9 | inconsistent at 5p (sign flip persists) |
| ignore-crash | +3.0 / -2.9 | -1.6 / -2.5 | FAIL both (v2 +7.5/+5.5) |
| ignore-ties (public counts only; income is face down) | -6.9 / -3.0 | +8.1 / +9.3 | pass 6p only; ignoring ties WINS at 5p |
| ignore-cap | +8.5 / +5.8 | +5.9 / +1.4 | pass for strategic; planner marginal at 6p |

## Which change worked (single-change configs, L10)
- **Ceiling +4 worked for Hype share.** No cap (face-down income, same everything else): 57% / 63%. Cap 3: 41%. Cap 4: 48% / 48%. Cap 5: 53% / 53%. Knob confirmed, cap 4 sits in band at both counts.
- **The ceiling did not cut the skill gap**: lone S gap 28.1 / 28.7 without cap vs 31.2 / 32.5 with cap 4 (cap 3: 30.6 / 33.3; cap 5: 29.6 / 31.2).
- **Ceiling lowered 6p last-round flip** 32% to 25%; 5p 20% to 19% (not enough at 6p).
- Cutting open income cost nothing measurable: face-down lone gap is above v2's 25.3 (note the bots also changed: cap-aware valuation, so only the no-cap row is a clean comparison).
- Hand 5 (E4): Hype share unchanged, forced passes 1.7% at 5p, flip 25% / 26%: no gain.
- E5 "income 1" was a no-op: the sim hard-codes K=2, so it only shows seed noise (lone gap 30.3 / 32.0 against 31.2 / 32.5).

## Problems, ranked
1. **High. Ignore-crash fails at both counts (L1).** Evidence above. With a ceiling of +4 the crash costs at most 4 points a lot and bots that ignore it lose nothing. Fix: pick one: drop "steer the crash" from the skill claims, or make the crash bite (single change, then re-test).
2. **Medium. Ignore-hype and ignore-ties are not stable across counts or bots (L2).** At 5p the strategic bot does better ignoring Hype (-5.3) and both bots do better ignoring ties; at 6p both ablations lose clearly. The tie rule is a skill lever at 6p only. Fix: state it as pacing only at 5p, or confirm with a third bot.
3. **Medium. 6p last-round winner flip 25% against 20%, crash flips 33%.** Fix: shorten the Hype race or add a last-round rule; test as one change.
4. **Low. Ceiling is mostly a score scaler** (ignore-cap +1.4 to +8.5). Acceptable per rules v3.
5. **Low. Skill depends on bot depth:** greedy lone gap 15.4 (below 20), lite 24.7, strategic 31.8, planner 36.9. The 5/6 mixed gap of the planner (7.8) is above 5.

## Dead cards
None dead. Pass is played 30% of rounds and is neutral (win corr -0.04). Bid 1-3 shows negative correlation (-0.19), which reflects weak hands rather than a bad card; Bid 10-11 +0.18; lot values 4 and 5 correlate most with winning (0.37, 0.34), lot value 2 least (0.07, but still scores). No card is flagged.

## Ambiguities hit
1. Round-14 income still happens (only matters for tiebreakers).
2. Tiebreakers 1 and 2 use hidden hands; rules do not say hands are revealed at the end (assumed yes).
3. Income reshuffle step 2 with K rounding was implemented as written; no hole found.
No new rule hole needed an interpretation beyond these.

## How it felt (narrated play, 5p log, one game)
Rounds 1-4 felt lively: four-way bids, 11 and 10 both taking lots, burns going into Clocks and Silver. Round 5 was a dud: two players bid 7 and cancelled, nobody took a lot, and two lots sat there. That was the fun spike (the rich block builds) but also a frustration for the two players who lost cards for nothing. Rounds 8-13 repeated a pattern: only 2-3 bids a round while three players passed to draw, so the table felt thin and the block grew to 4 lots, which made the later 8-11 bids feel like jackpots. Hype went 6/8/4/6 at the end, so Silver crashed and the +4 ceiling applied to the rest: the winner was the one who kept taking value-4 and 5 lots early, not the one who steered the crash. Decisions per turn: 3-4 real choices. Downtime is low (simultaneous). The crash reveal at the end was the right surprise; the +4 ceiling made it a smaller one.

## What simulation cannot test
Fun, teach time, reading the rules, memory or table talk, whether people really like losing a 7 to a tie, spite and kingmaking in round 14, bluffing with real people, and whether the face-down Paddle trick works with real hands. All verdicts are bots only, unvalidated.

## Untested suggestions
Crash penalty variant; end Hype one round early; a spite bot for round 14; bid range 1-12 at cap 4; a no-op income-1 config fixed to the sim.

Panel (free bots, panel.json): average fun 3.44, best fit competitor, worst fit family.
