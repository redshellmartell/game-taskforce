# Roadmap

_Last updated: 2026-10-03 by the planning chat._

## Where we are

- **Agent team:** five agents working (Director, market researcher, game designer, playtester, critic). First full pipeline run done.
- **First game:** Duel Flip, a 2-player push-your-luck card game. Pitched early as a feasibility test after one revision. Critic: REVISE-MINOR (fair and playable, but its three twists don't change how it plays, it's close to Port Royal, and the bait rules contradict themselves).
- **Dashboard v1: complete** (milestones 1-4), merged into `main`. Org-chart Agent Network, Studio Floor, Pipeline, Game pages, Review Queue, Quality Lab, Market & Portfolio, Ops, Learn mode, replay, "+ New idea" and "Talk to it".

## Now (Claude Code task queue)

| Task | What | Status |
|---|---|---|
| [001](../tasks/001-merge-and-housekeeping.md) | Merge the dashboard branch into `main`, clean up cache files | done |
| [002](../tasks/002-backfill-duelflip-data.md) | Create Duel Flip's dashboard data files so its KPIs show real numbers | open |
| [008](../tasks/008-lean-mode-and-usage-meter.md) | Lean mode setup: idea bank, tidy simulations, usage meter per agent and game | open |
| [010](../tasks/010-approval-gates-dashboard.md) | Approval gates in the dashboard: waiting-for-you inbox, decide from the UI | open |
| [005](../tasks/005-test-panel-personas.md) | Test panel 1: five player personas grounded in real reviews, with calibration | open (after 008) |
| [006](../tasks/006-test-panel-playtests.md) | Test panel 2: persona bots in rotation, free fun scoring, Haiku reviews, talking to personas | open |
| [007](../tasks/007-test-panel-dashboard.md) | Test panel 3: personas as characters in the dashboard | open |
| [009](../tasks/009-free-model-experiment.md) | Experiment: persona work on free models (local Ollama on the Mac or a free API) vs Haiku | open |

Tasks 003 and 004 (dashboard milestones 3-4) were finished before their briefs were picked up.

**Lean mode is on** (2026-10-03): models set per agent, playtester and critic budgets, batched research into `research/idea-bank.json`. See "Lean mode" in `CLAUDE.md`.

**Approval gates are on** (2026-10-03): the Director stops and asks before market scans, starting design on a new brief, every revision loop, panel research and reviews, going over budget, and sending content to free AI providers. See "Approval gates" in `CLAUDE.md`.

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
