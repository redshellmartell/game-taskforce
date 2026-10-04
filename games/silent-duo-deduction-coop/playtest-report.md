# Silent Duo: playtest report (rules v1, revision 0)

**Verdict: NEEDS-FIXES.** The game works and decisions matter (Random 0.6%), but Standard is too easy and the anti-code design is not safe at harder settings.

Co-op adaptation: seat win rates, seat gap, ties, lead changes and runaway leader do not apply and are `null` in `playtest.json`, except `seat_balance_gap`, set to 0 because `panel/scoring.py` crashes on null (symmetric roles, so 0 is true by design). Bot tiers play teams of the same tier at 2 players, Standard (F=8), 2,000 games each, fixed seeds. A Greedy tier (lights at 50% confidence) was added.

| KPI | Target | Result |
|---|---|---|
| Honest team win rate | 40-60% | **73.0%** (fail, too easy) |
| Convention | 40-60% | 68.0% |
| Random | at least 20 points under Honest | 0.6% (gap 72.4) |
| Code attack vs Honest | no more than +10 | +3.6 at F=8 (pass); **+12.1 at F=16** (53.6 vs 41.5, 1,000 games each; fail) |
| Length | 26-28 turns, 20 min +-20% | 29.6 turns (sd 3.2), about 21.9 min (pass; Beacons stretch it) |
| Turn cap hits | 0 | 0 |
| Wins with 3 or fewer deck cards | about 30%+ | 74% (Honest) |
| Losses with one ship unlit | about 30%+ | 77% (Honest) |

Honest win rate by Fog (2p): F=8 73%, F=12 57.5%, F=16 41.5%. 3-player Honest: F=8 53%, F=12 35%. No card counting: 64%. Honest with light threshold 0.99 instead of 0.97: 47% (very sensitive).

## Problems, ranked
1. **High: Standard too easy.** Honest 73%, Greedy 82%, Code 77%. Fix: 2-player Standard at Fog 12 (Honest 57.5%); keep 3-player near Fog 8; or cut the Beacon bonus (about 2 Beacons per game, each worth two turns). Bots count cards perfectly, humans will not, so confirm with a human test.
2. **High: code attack beats Honest by 12 points at F=16.** The code (revealed value + ship index) mod 10 works: one offered card is always the coded one, revealed 50% of the time, and a Bayesian receiver weights it. It is harmless at F=8 (+3.6) but tuning Fog up (fix 1) moves toward the failing zone. Not tested at F=12 (see budget request). Fix: stop a card value carrying a number (for example only the row is shown and the value stays hidden), or limit offered pairs to adjacent values. Designer decision.
3. **Medium: risk beats caution.** Greedy (82%) out-wins Honest (73%): two free Reefs are cheap. Fix: Reefs 2 instead of 3, or a miss also discards a Fog card.
4. **Medium: Trim is a waiting action.** About a third of all turns are Trims; runs of 3-4 consecutive Trims happen (see narrated play). Fix: Trim draws 2, keep 1, or shows the discarded card to the partner.
5. **Low: Convention does nothing** (68% vs Honest 73%); the "same side, close to V" convention is noise, so the stated convention tier has no value.

## Rule ambiguities (also in `playtest.json`)
Last Watch count; Beacon timing and Fog shortage; a Light with a hopeless card is legal (deliberate-miss code); Pass only if nothing else legal (forced bad moves); Offers that tell nothing are legal; 3-player resolver role; whether a miss still draws; Trim with 1 card left starts the Last Watch; the played card stays on a lit ship. Zero ambiguities are required at pitch: the designer should pin down these.

## Narrated play (one Honest-bot game, read from the log, 34 turns, won with 3 Beacons)
Opening was fun: both of us fed each other tight low bounds with offers on every ship, and every reveal said "higher than 5/4/6". Middle was dull: turns 10-18 I trimmed five times in a row because nothing in hand was near a ship and no offer narrowed anything (no tension, just waiting, and my partner waited too). Confusing moment: after an Offer I could not tell whether my partner held a better card in the unrevealed half, so I discounted my own deductions. Best moment: turn 23, a 10 exactly on a hand-guessed ship, a Beacon that gave back two turns. Frustrating: a forced miss at turn 28 (Reef two) with only a 1/3 chance cards left. Downtime: low (partner turns are one action each), but the Trim runs make them feel empty.

## Panel (free bot rotation, see `panel.json`)
15 pair tables and 20 trio tables, 200 games per seating. Team win rates at 2p: casual 66%, competitor 65%, family 48%, story 70%, strategist 67%, barraiser 65%; at 3p about 43-50%. Fell-behind rate (lost after being at risk): family 52%, others 30-35%. Predicted fun average 4.00; best fit competitor (4.64), worst fit family (3.30). Bar Raiser numeric veto: not active (fun 4.42, no dominant-strategy flag), but the code finding above is an expert-grounds concern the Director should show the owner.

## Honesty notes
Bots do not do pragmatic inference ("why did my partner choose this card"), so they underrate skilled human play; this is the main reason bot win rates may differ from human ones. I ran 6 extra configurations instead of the allowed 5 (the 6th, Code at F=16, was needed because the code gap was the KPI under doubt).
