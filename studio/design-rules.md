# Design playbook (one page; read before designing, playtesting or critiquing)

Built only from lessons seen in three or more games (`studio/lessons.md`). Everything below rests on bot simulation; no human has played any game. A rule that is not met must be listed in `rules.md` under "Known gaps".

## Designer: satisfy before handing over
1. **Comeback (L3).** Name the mechanism that lets a trailing player win and the KPI it serves (runaway leader at most 65%, lead changes at least 2). Say what keeps round 1 from deciding the game.
2. **Twist ablation (L1).** For every advertised twist or special card, write the "ignore-it bot" and the win rate it must lose to (at least 5 points under the full bot). A twist that cannot be tested this way is cut or reworked.
3. **Self-check pass (L4).** Before handover, walk every card and rule once: no card that is never the best play, no rule with two readings, no undefined case (empty deck, ties, simultaneous effects). List each fix you made.
4. **Target band and knob (L5, L8).** For each supported player count, and for solo or co-op, state the intended win rate or balance band and one tuning knob. Drop a player count you cannot support rather than ship it unbalanced.
5. **Termination and length (L4).** Say why the game ends, give a turn cap, and give the expected length against the brief's target.
6. **Rule budget (L7).** State the rules length (lines) and number of special rules against the brief's promise; teach text over budget is a known gap.
8. **Re-run after lever changes (L10, L11).** After any cap, ceiling, legality or tie-break change, every ablation is re-run at every player count; a lever can silently make another one inert.
7. **Skill gap (L6).** Say where good play beats random play (target gap at least 20 points) and which decisions carry it.

## Playtester: bot rules
- Build at least **two reference bots of different strength** (for example a greedy and a lookahead bot) plus the ablation bots from rule 2. Report the spread. **Never tune a game to a single bot (L2).**
- Stay inside the configuration budget in the agent file; ask for a `budget` approval before exceeding it.
- Report every KPI against the targets in `CLAUDE.md` and flag any single-bot result as unconfirmed.
- State plainly what simulation cannot test: fun, teaching time, table talk, bluffing with real people, whether the rules are readable. Mark every verdict "bots only, unvalidated".

## Critic: also check
Is there a stated comeback mechanism and does the data show it working (L3)? Did the designer's ablation tests run, and does each twist matter (L1)? Were two or more bots used (L2)? Is any player count or solo mode unbalanced (L5, L8)? Lessons in `lessons.md` that this game repeats should be named in `weakness`.
