---
status: open
priority: high
depends_on: [008]
---
# 010: Approval gates in the dashboard

## Goal
The Director now stops at approval gates (see "Approval gates" in `CLAUDE.md`) instead of running revision loops, scans and other usage-heavy steps on its own. The owner needs to see what's waiting, understand each request quickly, and decide from the dashboard.

## Scope

### 1. Approvals inbox
- A **Waiting for you** badge in the top bar with the number of pending requests from `games/approvals.json`; clicking it opens the Approvals page.
- **Approvals page:** pending requests oldest first. Each card shows the gate type, game, age, summary, why it's needed, expected outcome, usage estimate (S/M/L/XL, or the measured average once task 008's usage data exists), the Director's recommendation, and the options as buttons.
- For `revision` gates, also show the critic's "Is another revision worth it?" answer and the key KPI numbers from the last playtest next to their targets, so the owner can see whether the last loop moved anything.
- Below: decided and expired requests, with the decision and any notes.

### 2. Recording a decision from the dashboard
- Clicking an option asks for confirmation and optional notes, then writes only that request's `status`, `decision`, `decided_at` and `owner_notes` in `games/approvals.json` (`POST /api/approvals/<id>`, refused in sample mode).
- This is the dashboard's second allowed write, next to the ideas inbox. It still **never starts agents**: the page then shows the prompt to paste into Claude Code ("Continue with approved work"), with a copy button.
- Add to `CLAUDE.md`: when the owner says "continue with approved work", read `games/approvals.json`, act on every request decided since the last run, and record each in `games/decisions.json`.

### 3. Gates on the rest of the dashboard
- Agent Network and Studio Floor: an agent or game waiting at a gate shows the amber "waiting for you" state with the gate name.
- Game page: gate history in the timeline (requested, decided, by whom, usage estimate versus actual where known).
- Pipeline: a "Waiting for approval" marker on game cards.
- Ops: number of revision loops proposed, approved and declined, and the usage saved by declined loops (estimate).
- Learn mode: "?" entries for approval gate, usage estimate and approval modes.
- Settings (read-only display): the current `approval_mode` from `studio-settings.json`, with the phrase to change it.

### 4. Sample data
Add sample requests covering each gate type and status.

## Done when
- With sample data, the owner can see pending requests, decide one from the dashboard, and see it move to "decided" with the copy-prompt shown.
- A real request written by the Director appears within a few seconds.
- `npm test` passes, including tests for the approvals endpoint (only decision fields change; unknown ids and sample mode are refused).
- `docs/BUILD-DASHBOARD.md` Status and `docs/plan/PROGRESS.md` updated.
