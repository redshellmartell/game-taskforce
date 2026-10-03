---
status: open
priority: normal
depends_on: [001]
---
# 002: Backfill Duel Flip's dashboard data

## Goal
Duel Flip was made before the agents started writing JSON data files, so its real KPIs show "no data yet". Create those files from what already exists, so the dashboard shows one real game end to end.

## Scope
- Create the data files described in `docs/dashboard-notes.md` section 4 and the formats in `CLAUDE.md` and `.claude/agents/*.md`, for `games/duelflip/` only:
  `brief.json`, `playtest.json`, `critique.json`, `pitch.json`, `activity.jsonl`, and Duel Flip's entry in `games/status.json`.
- Take every number from the existing reports or by re-running the current simulation (`games/duelflip/sim/run.py`, rules v2). Don't invent values; use `null` where something wasn't measured.
- Don't change the rules, reports or simulation logic. Small additions to `run.py` so it writes `playtest.json` are fine.

## Steps
1. Read `brief.md`, `playtest-report.md`, `critique.md` and `pitch.md`.
2. Write `brief.json`, `critique.json` and `pitch.json` from them.
3. Make `run.py` also write `playtest.json` in the agreed format, run it and check the numbers match the report (small differences from random seeds are fine; note them).
4. Write `activity.jsonl` reconstructing the history (research, design v1, playtest v1, revision, design v2, playtest v2, critique, pitch) using commit times from `git log` as timestamps, and mark each line `"reconstructed": true`.
5. Add Duel Flip to `games/status.json` with stage `owner-review`, revision 1 and its verdicts.
6. Open the dashboard with real data (not sample mode) and check Duel Flip's Game page and the top-bar KPIs.

## Done when
- The dashboard in real-data mode shows Duel Flip with scorecard, critic scores, balance numbers and history, without "no data yet" where data exists.
- The dashboard no longer marks Duel Flip's activity as "inferred from file".
- An entry is in `docs/plan/PROGRESS.md`, including any number that differed from the report.
