# Playtest report: Heavenly Bodies v2 (Gearbox), cycle 1 (revision 1)

**Verdict: BROKEN (bots only, unvalidated).** The win-timing fix worked on its own terms (Long Night 95-100% down to 0-0.1%), but the game now ends in 3-8 turns, the first seat wins 62-67% at 2-3p, and the "strategic" bot loses to the "greedy" bot. Cause isolated: the sideways Shield. Budget used: 5 configs (below), 1,000 games per cell, panel 200 per seating (16,000 games per persona).

## Key numbers (all-strategic mirror, 1,000 games per count; `sim/results/*.json`)
| KPI (target) | Cycle 0 (2/3/4p) | Cycle 1 (2/3/4p) | Met? |
|---|---|---|---|
| Seat gap, points (<=5) | 0.3 / 2.2 / 0.6 | **16.9 / 29.1 / 18.4** | no |
| Mean turns (14-24 / 18-30 / 20-34) | 46 / 47 / 40 | **4.4 / 7.2 / 8.0** | no, 1/4 of band |
| Minutes at 0.4 per turn (12) | 18.5 / 18.7 / 15.8 | **1.8 / 2.9 / 3.2** | no |
| Long Night (<=10 / 10 / 15%) | 95 / 100 / 100% | 0 / 0 / 0.1% | yes |
| Pattern share mass / const / align | 5% patterns | 27/46/28, 34/45/21, 40/37/23 | yes (15-50%) |
| Captures per game (15-25) | 59 / 43 / 30 | 1.8 / 2.3 / 2.5 | no |
| Lead changes (>=2) | 21 | 0.64 / 1.76 / 2.06 | 4p only |
| Midpoint leader wins (<=65%) | 51% | 74.7 / 63.5 / 41.0% | 2p fails |
| Strategic vs random, points (>=20) | 99.6 / 100 / 99.3 | 98.0 / 95.8 / 92.3 | yes |
| Strategic vs greedy, points | +38 / +16 / -6 | **-14.0 / -8.0 / -13.1** | no (negative) |
Greedy vs random: +95.8 / +93.0 / +91.9. Greedy mirror: Critical Mass is 81 / 89 / 93% of pattern endings (strategic mirror 27 / 34 / 40%).

## Per-switch effect (each switch changed alone from the cycle 1 rules; turns / seat gap / Long Night, 2p | 3p | 4p)
| Switch change | 2p | 3p | 4p | Reading |
|---|---|---|---|---|
| Default (cycle 1) | 4.4 / 16.9 / 0% | 7.2 / 29.1 / 0% | 8.0 / 18.4 / 0.1% | |
| WIN_AT_END off (win at start) | 16.8 / 5.3 / 5% | 29.5 / 9.7 / 50% | 27.9 / 6.2 / 56% | the Long Night fix is real; cycle 0's timing is what swallowed patterns at 3-4p |
| SHIELD off | **22.6** / 5.5 / 20% | 33.7 / 20.9 / 83% | 30.4 / 26.2 / 87% | **the shield is the length lever**: captures 18 / 22 / 20 per game; 2p lands in band |
| REBOUND on | 2.3 / 40.2 / 0% | 4.4 / 20.3 / 0% | 5.5 / 36.9 / 0% | Rebound cut was right; it halves length again |
| CM 15 at every count | 4.1 / 19.5 | 7.2 / 29.1 | 8.1 / 16.7 | inert (CM share 37 / 34 / 29%); per-count thresholds earn nothing |
| RAINBOW off | 5.1 / 12.1; const 7% | 7.4 / 21.1; const 7% | 8.4 / 19.5; const 7% | rainbow is needed; without it Constellation is dead |
| DEEPSPACE_DRAW on | 4.4 / 16.8 | 6.9 / 28.8 | 7.9 / 19.4 | inert; keep it cut |
Arms: DECK40 4.7 / 7.3 / 8.0 turns (Long Night 0 / 0.8 / 1.5%), CAPTURE_TO_DS 4.7 / 7.3 / 8.1 turns; neither moves length, seat gap or runaway.

## Ablations (full bot minus ablated bot, points; need >=5)
| Bot | 2p | 3p | 4p |
|---|---|---|---|
| self-spin-only | 2.2 (inert) | 32.1 | 11.4 |
| shield-blind | 7.2 | 1.1 (inert) | 3.3 (inert) |
| threat-blind | 8.0 | 4.4 (inert) | 1.2 (inert) |
| defence-check (keeps big bodies in contacts) | 30.2 | 16.6 | 7.9 |
| no-recall | -1.8 (dead) | -1.9 (dead) | 0.0 (dead) |
| comet-blind | 3.4 | 0.1 (dead) | 0.9 (dead) |
Defence-check is a worse bot than strategic, so the cycle 0 "defence is cheap" oracle worry does not repeat. Recall and Comet-beats-Giant are dead twists. Self-spin-only is inert at 2p by construction (both orbits touch the opponent).

## Other configs run
- **Fallbacks (2p only):** threshold 17: 4.6 turns, seat gap 15.1 (mass share 17%). 1 opening body: 6.5 turns, gap 11.3, min 5 turns. Both: 6.5 turns, gap 12.0. None reach 14.
- **New test (mine): opening 0 / opening 1 at every count** (orbit starts empty or with 1 body; this targeted "2p too fast"): opening 0 gives 8.3 / 14.8 / 18.3 turns, seat gap 11.6 / 4.9 / 10.0, lead changes 2.4 / 5.2 / 6.5, runaway 0.80 / 0.50 / 0.33, Long Night 0 / 0 / 1.5%, captures 2.1 / 3.5 / 3.7. Opening 1: 6.5 / 11.4 / 14.8 turns. Best direction found, still short at 2p and short on captures.
- **Suspicion check:** Critical Mass crowding out the others is false for the strategic bot (27-40%), true for the greedy bot (81-93%): CM is the easy line for a naive player, the other two need planning. 2p being too fast is true by a factor of four.

## Problems (ranked; full list in `playtest.json`)
1. **High. 3-8 turn race.** Cause is the Shield (SHIELD off: 22.6 / 33.7 / 30.4 turns). A launched body is untouchable, so a 4-body pattern lands on the 2nd-3rd own turn (3 turns is the 2p minimum and the mean is 4.4). Fix: pick one: (a) no shield and shrink the Deck/thresholds for 3-4p (untested), or (b) keep the shield, start with 0 bodies (+8 to +11 turns), and raise every Critical Mass threshold by 1 (untested combination).
2. **High. Seat 1 wins 62-67% at 2-3p** (gap 16.9 / 29.1 / 18.4). Short races reward tempo. Opening 0 cuts it to 4.9 at 3p; shield off to 5.5 at 2p. Extra: the last seat draws 2 on its first turn.
3. **High. Strategic loses to greedy** (-14 / -8 / -13). Simple "biggest bodies" play wins through Critical Mass, so decisions barely matter beyond card quality. Re-check once games are long enough for captures to bite.
4. **Medium. Dead or near-dead twists:** Recall, Comet beats Giant (Giants captured 0.1 times per game), shield-blind and threat-blind at 3-4p. Captures per game 1.8 / 2.3 / 2.5 against 15-25. Re-test after problem 1; cut Recall if still inert.
5. **Medium. Runaway/lead changes:** midpoint leader wins 74.7% at 2p. An "armed" position (one launch from a pattern) is attacked 83 / 79 / 77% of the time but a hand card refills it: still armed 100 / 61 / 48% at the owner's next turn. The visible-threat comeback barely works at 2p.
6. **Low. CM_BY_COUNT and DEEPSPACE_DRAW are inert;** DECK40 and CAPTURE_TO_DS do nothing for length. Drop them.

## Rule ambiguities (11, in `playtest.json`; none blocking)
Main ones: Long Night last tie-break needs "including that player" (the player whose Draw found the Deck empty counts as soonest); Rebound plus Shield (both launched bodies sideways?) only matters if Rebound returns; a single shielded body makes a spin a free "pass"; the sideways mark moves with the spin and stands up at Wake (written, sim follows it).

## How it felt (two bot-played logs, read as a player; no human play)
- **2p game (3 turns):** both open with 2 bodies, I launched S1, then S3, and on my second turn F2 completed 1-2-3-4. Opponent never got a second turn. Boring and decided by the deal; none of my spin choices mattered. No downtime (nothing to wait for).
- **3p game (4 turns):** one capture (F4 took F1) when P1 spun my orbit; I won on Critical Mass 15 on my second turn. The only interesting moment was that capture; I then built the pile quickly.
- **Is the sideways shield clear?** In the logs (`S1~` for sideways) yes: sideways bodies are labelled, show in contacts and move with the spin without a special case. Written rule: clear. Not tested with humans. The problem is the effect (too strong), not the clarity.

## Panel (free bots; 6 personas, 50 tables at 2-4p, 200 games per seating)
Best fit competitor (3.45), worst fit family (2.17), average fun 2.87. Bar Raiser veto active (seat advantage 16.9 points).

## What to try next (untested suggestions)
1. Shield off plus opening 0 at 3-4p (shield off gave 2p 22.6 turns; opening 0 added +4 turns at 2p).
2. Keep the shield but let it protect only against Comets/Giants or only until the next spin of that orbit by anyone (halves its length effect).
3. Opening 0 with every Critical Mass threshold +1 (17 / 16 / 15).
4. Last-seat compensation (draw 2 on first turn).

## Sim-kit improvements
Added `simkit.run_match_parallel` (fork-based; accepts lambdas; `post` builds small rows in the worker) with a test (`python3 -m unittest discover tools/sim-kit`, 8 pass) and a README line. Heavy sections now take 2-30 s per cell instead of minutes. Suggest next: a built-in "armed position" tracker and a mixed-seat ablation helper for 3-4 players.

## What simulation cannot test
Fun, teaching time, table talk, whether a 3-turn game feels like a game. Every verdict is bots only, unvalidated.
