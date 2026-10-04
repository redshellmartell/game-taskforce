---
status: open
priority: normal
depends_on: [010]
---
# 011: Make the dashboard live and interactive (three stages, stop after each)

Queued by the owner for later. Do one stage at a time and **stop after each stage for the owner's review**. Do not start stage 2 or 3 without a go-ahead.

## Ground rules
- Read `CLAUDE.md`, `docs/BUILD-DASHBOARD.md` and `docs/dashboard-notes.md` first. Explain steps in plain language: the owner is new to coding.
- Work on a **new branch off `main` called `dashboard-interactive`**. Do **not** touch `claude/nice-allen-b9i0vi`: the taskforce pipeline uses it. (This overrides the usual "work on your session branch" rule for this task.)
- Build and test against `dashboard/sample-data/` only. Never edit real files in `games/`.
- The dashboard has been read-only so far. The owner explicitly approves the changes below, and only these. Keep everything else read-only.
- Do not start agents from the dashboard in stages 1 and 2.
- Add tests to `npm test` for anything you build.

## Stage 1: live refresh
- Push file changes to the browser automatically (server-sent events or a websocket on top of the existing file watcher), with no manual reload.
- Show a small "live / disconnected" indicator and reconnect automatically.
- Optional, behind a setting: a script `tools/sync/pull-loop.sh` that runs `git pull --ff-only` every 20 seconds on the current branch and stops if there are local changes.
- **Done when:** editing a file in `games/` changes the UI within about 2 seconds without a reload.

## Stage 2: one-click approvals
- Add Approve / Decline buttons (and the option buttons from each request) to the Approvals page.
- Add a server endpoint that updates only that request in `games/approvals.json` (`status`, `decision`, `decided_at`, `owner_notes`) and appends to `games/decisions.json`, using atomic writes. Reject anything else.
- The server must listen on localhost only.
- Show a clear "saved" or "error" message, and an optional notes field.
- **Done when:** clicking Approve on a sample request updates the sample files correctly and the UI reflects it live.

## Stage 3: auto-continue (propose first, do not build yet)
- Write a short design for a local runner that, after an approval, launches `claude -p "continue with approved work"` in the project folder.
- It must run `python3 tools/usage/usage.py --check` first and stop on exit code 2.
- It must run one task at a time, with a log and a stop button.
- Give the owner the plan and the risks, and **wait for the owner's go-ahead**. (An unattended agent on the owner's machine was blocked by the safety classifier when proposed earlier, so this needs the owner's explicit decision and possibly a permission rule in the owner's own settings.)

At the end of each stage: run `npm test`, summarise what changed in five lines, and tell the owner the exact commands to try it.

## Notes from the Director (what already exists, so nothing is built twice)
- **Live refresh mostly exists:** `dashboard/server/index.js` already watches the files with chokidar and pushes `changed` events over server-sent events (`/api/events`), and `src/useStudioState.js` reloads on them (plus a timer). What is missing for stage 1 is the visible live/disconnected indicator, automatic reconnect handling and its test, and `tools/sync/pull-loop.sh`. The two-way sync in `tools/sync/sync.sh` and `install-mac.sh` is separate and stays.
- **One-click approvals already exist in a first form:** `POST /api/approvals/:id` with `server/approvals.js` (`decideApproval`: changes only `status`, `decision`, `decided_at`, `owner_notes`; atomic write; 404/409/400 refusals; same-origin check; refused in sample mode) and the buttons and notes on `ApprovalsView.jsx`. What stage 2 adds or must verify: appending to `games/decisions.json`, working against sample data (currently refused in sample mode), a clear saved/error message, binding to localhost only (`app.listen(PORT)` currently listens on all interfaces), and tests.
- Related earlier work: `tools/usage/usage.py --check` (exit 2 = stop), `tools/sync/` (the owner's Mac sync and installer).
