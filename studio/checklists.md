# Role checklists (each agent reads its own section; the Director checks that the output shows them)

Built 2026-10-06 from the first retro (`studio/retros/2026-10-06.md`). Everything rests on bot simulation; no human has played any game.

## Designer: end `rules.md` with a "Playbook check" block, one line each
1. **Family:** which section of `studio/mechanics.md` you read, and the one trap it names for your game.
2. **Comeback:** the mechanism and the KPI it serves (runaway leader <= 65%, lead changes >= 2).
3. **Ablations:** for each twist, the bot that ignores it and the margin it must lose by (>= 5 points) at EACH player count.
4. **Self-check:** dead cards and ambiguities you found and fixed (list them); undefined cases (empty deck, ties, simultaneous effects).
5. **Band and knob:** target win rate or balance band per player count or mode, and the one tuning knob.
6. **Ends:** why the game ends, a turn cap, expected length vs the brief.
7. **Budget:** rules length (lines) and special rules vs the brief's promise.
8. **Re-run list:** which ablations the playtester must re-run after this change. Any cap, ceiling, legality or tie-break change means re-run ALL of them.

## Playtester
1. Read `tools/sim-kit/README.md`; use the kit and the template; do not rewrite an existing sim on a revision.
2. **Time box about 20 minutes.** Stop at the first clear verdict. Put further ideas under "untested suggestions"; ask for a `budget` approval to exceed the configuration limit.
3. At least two reference bots of different strength; report the spread (`round_robin`); never tune to one bot.
4. Run the designer's ablation bots at every player count, and **all of them again after any cap, ceiling, legality or tie-break change**.
5. Treat a number within about 2 points of a target as unsettled (`wilson`); raise games there only.
6. Report each KPI against the target and against the previous run, list ambiguities and dead cards, and say what simulation cannot test. Mark the verdict "bots only, unvalidated".

## Critic
1. Check the designer's "Playbook check" block exists and matches the data.
2. **Stop rule (use this wording):** if the remaining problem is structural (it appears with every bot or pairing, or two levers pull against each other), or two cycles in a row did not move the numbers the revision targeted, say another bot cycle is not worth it and recommend a human playtest or park. Otherwise name the one KPI the next revision must move.
3. Judge ablations at every player count; an inert twist or lever is a finding (L1).
4. Name repeated lessons in `weakness`. If the Bar Raiser veto is active, put it first.
5. Be explicit about which findings are bot artefacts or unconfirmed (L2).
