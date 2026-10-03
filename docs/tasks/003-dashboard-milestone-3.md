---
status: open
priority: normal
depends_on: [001]
---
# 003: Finish dashboard milestone 3

## Goal
Complete the parts of milestone 3 still missing according to the Status section of `docs/BUILD-DASHBOARD.md`, so the owner can run the studio from the KPI screens and not only the Agent Network.

## Scope
From `docs/BUILD-DASHBOARD.md` milestone 3 and `docs/dashboard-notes.md` section 2:
1. **Studio Floor** screen: agent sidebar with mini funnel, room cards with status and two KPIs each (as listed in the spec), activity feed, selected-agent panel and milestone ticker.
2. **Pipeline charts** on the Projects board: funnel chart, kill rate by stage, cycle time per game.
3. **Game page charts** with Recharts, replacing the simple bars: seat win rates, bot win rates, game-length distribution (if the data has it), card win correlation, and the critic's six scores.
4. Add Studio Floor to the navigation.

Keep the existing Agent Network, Projects board, Learn mode and idea inbox working. Stay minimalist and read-only apart from the existing idea inbox.

## Done when
- Studio Floor, Projects board charts and Game page charts all work with sample data and with Duel Flip (after task 002), with a clear "no data yet" wherever data is missing.
- KPI targets from `CLAUDE.md` are shown as target lines or green/amber/red markers.
- `npm test` passes.
- The Status section of `docs/BUILD-DASHBOARD.md` and `docs/plan/PROGRESS.md` are updated.
