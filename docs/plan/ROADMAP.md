# Roadmap

_Last updated: 2026-10-03 by the planning chat._

## Where we are

- **Agent team:** five agents working (Director, market researcher, game designer, playtester, critic). First full pipeline run done.
- **First game:** Duel Flip, a 2-player push-your-luck card game. Pitched early as a feasibility test after one revision. Critic: REVISE-MINOR (fair and playable, but its three twists don't change how it plays, it's close to Port Royal, and the bait rules contradict themselves).
- **Dashboard:** milestones 1 and 2 done on the Claude Code branch `claude/nice-allen-b9i0vi` (Agent Network, KPIs, activity feed, Learn mode, replay), plus a Projects board, Game page, "+ New idea" and "Talk to it". Not yet merged into `main`.

## Now (Claude Code task queue)

| Task | What | Status |
|---|---|---|
| [001](../tasks/001-merge-and-housekeeping.md) | Merge the dashboard branch into `main`, clean up cache files | open |
| [002](../tasks/002-backfill-duelflip-data.md) | Create the dashboard data files for Duel Flip so its KPIs show real numbers | open |
| [003](../tasks/003-dashboard-milestone-3.md) | Finish milestone 3: Studio Floor and proper charts | open |
| [004](../tasks/004-dashboard-milestone-4.md) | Milestone 4: Review Queue, Quality Lab, Market & Portfolio, Ops | open |

## Next (to plan here)

- **Decide Duel Flip's future:** one more rules pass and re-simulation (the pitch's own advice), or archive it as a successful test and move on. See `IDEAS.md`.
- **Second pipeline run:** pick a direction different from Duel Flip so the portfolio and Quality Lab views have something to compare.
- **Improve the agents from what Duel Flip taught us:** see "Lessons" in `IDEAS.md`.

## Later

- Interactive dashboard (stage 3): record decisions, send games back with notes and start agent runs from the UI.
- More agents: artist (print-and-play PDFs), rules editor, production planner, trend watcher.
- Themed "think tank" look on top of the minimalist dashboard.
- Running agents automatically on a schedule.
