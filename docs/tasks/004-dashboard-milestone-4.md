---
status: open
priority: normal
depends_on: [003]
---
# 004: Dashboard milestone 4

## Goal
Add the remaining views so the dashboard covers every KPI area in the spec.

## Scope
`docs/BUILD-DASHBOARD.md` milestone 4 and `docs/dashboard-notes.md` section 2:
1. **Review Queue** page: pitches waiting for the owner, each with scorecard, how it plays, components and estimated cost; past decisions; human playtest results and the agent-vs-human gap. Read-only, with a note on how to record a decision by telling Claude Code.
2. **Quality Lab:** design-quality trends across games, a table of every game's balance KPIs, and recurring problem types.
3. **Market & Portfolio:** portfolio mix charts, opportunity scores, comparable titles.
4. **Ops:** agent activity history, runs and failures per agent, simulated games.
5. Views that compare games show a short message until at least two real games exist (sample data always shows them).

## Done when
- All four views work with sample data, and with real data containing only Duel Flip.
- Navigation includes them, and Learn mode has a "?" on any new concept.
- `npm test` passes.
- The Status section of `docs/BUILD-DASHBOARD.md` and `docs/plan/PROGRESS.md` are updated.
