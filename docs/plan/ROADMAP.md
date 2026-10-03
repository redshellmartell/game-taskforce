# Roadmap

_Last updated: 2026-10-03 by the planning chat._

## Where we are

- **Agent team:** five agents working (Director, market researcher, game designer, playtester, critic). First full pipeline run done.
- **First game:** Duel Flip, a 2-player push-your-luck card game. Pitched early as a feasibility test after one revision. Critic: REVISE-MINOR (fair and playable, but its three twists don't change how it plays, it's close to Port Royal, and the bait rules contradict themselves).
- **Dashboard v1: complete** (milestones 1-4) on the Claude Code branch `claude/nice-allen-b9i0vi`, not yet merged into `main`. Org-chart Agent Network, Studio Floor, Pipeline, Game pages, Review Queue, Quality Lab, Market & Portfolio, Ops, Learn mode, replay, "+ New idea" and "Talk to it".

## Now (Claude Code task queue)

| Task | What | Status |
|---|---|---|
| [001](../tasks/001-merge-and-housekeeping.md) | Merge the dashboard branch into `main`, clean up cache files | open |
| [002](../tasks/002-backfill-duelflip-data.md) | Create Duel Flip's dashboard data files so its KPIs show real numbers | open |
| [005](../tasks/005-test-panel-personas.md) | Test panel 1: five player personas grounded in real reviews, with calibration | open |
| [006](../tasks/006-test-panel-playtests.md) | Test panel 2: persona bots, free fun scoring, AI reviews for finalists, talking to personas | open |
| [007](../tasks/007-test-panel-dashboard.md) | Test panel 3: personas as characters in the dashboard, with pages, stats and chat | open |

Tasks 003 and 004 (dashboard milestones 3-4) were finished before their briefs were picked up.

## Next (to plan here)

- **Decide Duel Flip's future:** one more rules pass and re-simulation, or archive it as a successful test. The test panel's verdict (task 006) is useful input.
- **Second pipeline run** in a different space, so the portfolio and comparison views have something to compare.
- **Improve the agents from what Duel Flip taught us:** see "Lessons" in `IDEAS.md`.

## Later

- Interactive dashboard: record decisions, send games back with notes, ask personas and start agent runs from the UI.
- More agents: artist (print-and-play PDFs), rules editor, production planner, trend watcher.
- More personas once the first five are calibrated (for example a solo player, a party-game crowd, a collector).
- Themed "think tank" look on top of the minimalist dashboard.
- Running agents automatically on a schedule; options for running off the subscription (pay-per-use API with a spend cap, or a local open-source model for low-stakes persona chatter).
