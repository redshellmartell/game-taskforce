---
status: done
priority: high
depends_on: []
---
# 014: A switch for the taskforce (on/off, clicks start the work, resume where it left off)

**Draft written 2026-10-05 at the owner's request. Not `open` yet:** the owner and the planning chat should review it first. It overlaps task **011** (Step A one-click records, Step C auto-continue) and works with task **013** (learning loop, review cap). Decide the order when promoting it; the owner wants 013 and 014 before the rest of 011.

## Goal
The owner wants to **turn the taskforce on and off like a switch** from the dashboard, and not return to the chat for every small step. While it is on, the owner's clicks (approvals, pitch decisions, send-backs) are recorded automatically and **start the matching agent work**. While it is off, clicks are still recorded but nothing starts. Turning it off **saves the current state, or finishes the step in progress**, so turning it on again **picks up seamlessly where it left off**.

The owner is pinged only for the main steps (below), not for every stage.

## Owner's requirements (2026-10-05, from chat)
- Run the tool **when the owner pleases**, instead of scheduled tasks.
- Deactivate = save the current process or complete the final task if needed; activate = resume exactly where it stopped.
- Approvals and actions clicked in the tool are recorded **automatically** and then **initiate the agent work**.
- The owner should not need to come back to the chat for every little thing, only for the main steps or specific topics.

## Conditions (design around them)
- **The dashboard cannot start a cloud session.** "Activate" therefore means a **runner on the owner's Mac** (a small script that calls `claude -p`). A cloud heartbeat that reads the same switch is an optional later stage, not part of the first build.
- **Today `CLAUDE.md` says "the dashboard must never start agents".** The owner's go-ahead for this task is the explicit decision to change that rule, **for the runner only** (stage 3). Update `CLAUDE.md` and the Dashboard project section in the same stage, and say so plainly in `PROGRESS.md`.
- **The safety classifier blocked an unattended runner earlier** and has blocked the Director from editing control files and committing (reasons "Instruction Poisoning", "Self-Modification"). Expect it again. If it blocks, **stop and tell the owner; never work around it.** The owner may need to add permission rules in their own settings; draft the exact rules and let the owner apply them.
- **Usage:** the usage guard (`python3 tools/usage/usage.py --check`, stop at the configured percent, exit 2 = stop) is checked before every agent call. Local runs may bill the **plan** rather than cloud credits: the guard needs recalibrating from the plan percentages ("calibrate usage: 5-hour N%, weekly N%"); say so in the first run.
- **The owner is new to coding.** Plain language, exact commands, stop after each stage for review. Do not edit `dashboard/` beyond what each stage lists. Build and test against `dashboard/sample-data/`; never edit real files in `games/` while testing.
- The Mac follows `main` (sync every 20 seconds). A runner that works in the owner's own checkout commits and pushes from there, so the side-branch merge problem goes away.

## The Mac may sleep mid-run (owner, 2026-10-05: "it will be on when I start and stop; if it sleeps in the middle I am not sure")
Treat sleep as **normal, not an error**. Design so that a sleep never loses work and never needs the owner to repair anything:
- **Prevent idle sleep while running.** The runner starts under `caffeinate -i` (and `-s` when on power), so the Mac does not sleep from inactivity while the switch is on. Closing the lid on battery can still sleep it; that case is covered below. Releasing `caffeinate` on stop is automatic when the runner exits.
- **Heartbeat.** The runner rewrites `heartbeat` in `studio/run-state.json` every 30 seconds. The dashboard shows "running" only if the heartbeat is fresh (under 2 minutes) and otherwise shows **"interrupted (the Mac may have slept)"** with the time of the last heartbeat.
- **Sleep detection.** The loop compares the wall clock between iterations. A gap over 2 minutes means the Mac slept: any agent call that was in flight is treated as suspect (its connection is probably dead). The runner checks whether the step's expected output exists and is complete; if not it marks the step `to-redo`, and redoes it from the start.
- **Safe redo.** Every step must be safe to repeat: rules edits happen in place, a playtest re-runs from scratch, the activity log gets a new `start` line after an unmatched one (the dashboard treats the earlier unmatched `start` as "interrupted"), and a commit is only made when the step finished. No step may leave a game in a half-written state that the next step trusts.
- **Retry once on network errors,** then stop with `status: error` and a plain-English reason. (Answers the owner question below: retry once, then wait for the owner.)
- **Resume.** On switch-on, if `status` is `running` with a stale heartbeat, the runner treats it as interrupted, records that in `activity.jsonl`, and redoes the step. No owner action needed.
- **Test it:** stage 1 paper run includes a simulated sleep (kill the runner mid-step, resume, compare the result with an uninterrupted run); stage 3 includes a real test (start a step, close the lid for a minute, reopen).
- **Cloud fallback (stage 5)** is the real answer for long unattended runs while the Mac is off; the local runner is for sessions where the owner is at the Mac.

## What it does

**State files (plain files, all in the repo):**
- `studio/taskforce.json`: `{ "active": false, "pause_mode": "after-step", "updated": "<time>", "by": "dashboard" }`. The switch. `pause_mode` is `after-step` (finish the running step, then stop) or `now` (interrupt, then stop).
- `studio/run-state.json`: the checkpoint: `{ "status": "running|paused|stopped|waiting-gate|usage-stop|error", "game": "<slug>", "stage": "...", "step": "...", "agent": "...", "started": "<time>", "last_done": "<activity id or line>", "reason": "<why it stopped>", "queue": ["<slug>", ...] }`. Written before every agent call and after every result.
- `studio/STOP`: an empty file. If it exists the runner stops at the next check, even if the dashboard is closed (the kill switch).
- Existing files remain the source of truth for the work itself: `games/status.json`, `STATUS.md`, `activity.jsonl`, `approvals.json`, `decisions.json`.

**The runner (`tools/runner/run.py` or `.sh`, written with the owner, tested in sample mode):**
1. Check `taskforce.json` (`active`), `studio/STOP`, and the usage guard. Not active, STOP present, or guard exit 2: write `run-state.json` and stop.
2. Pull the latest files (merge, not rebase; use `tools/sync/repair.py` on an `approvals.json` conflict). Record any owner click not yet recorded (see "Clicks" below).
3. Pick the next piece of work by the rules in `CLAUDE.md` (and, once task 013 is done, its review cap): approved revision, next stage of a game, pitch. Order by opportunity score. **One agent at a time.**
4. Write `run-state.json` (`running`, game, stage, step), append the activity `start` line, run the agent (`claude -p` with a short prompt that names the game, the stage and the files to read), append `done` or `error`, record the result in `status.json`/`STATUS.md`, commit and push.
5. Repeat from step 1.
6. Stop on: switch off; STOP file; guard stop; a request that needs the owner (gate, cap, pitch ready: `waiting-gate`); an error; an empty queue. Always write the reason into `run-state.json`.

**Clicks:** the dashboard server, on a click, writes the complete effect itself: the request update in `approvals.json`, an entry in `games/decisions.json` (`kind: "pitch"` for pitch decisions; a gate answer has no `kind` and names the request id in `notes`), and a history line in `games/status.json` ("approved: queued"). A pitch send-back creates its own `revision` request (the owner's notes are the brief). Atomic writes; localhost only; reject anything else. (This is task 011 Step A; do not build it twice.)

**Pause and resume:**
- *Pause after step* (default): the running agent call finishes, its result is recorded, the checkpoint is written, then the runner stops with `status: paused`.
- *Stop now*: interrupt the agent process; the step is marked `to-redo` in `run-state.json`; nothing half-written is trusted.
- *Resume (switch on):* the runner reads `run-state.json`. A step with a `start` line but no `done` line is **redone from the start** (rules edits are in place and a playtest can simply re-run; write each agent prompt so a repeat is safe). It then carries on with the queue, including any clicks made while it was off.

**Notifications (only the main events):** a pitch is ready; a game needs a decision (cap reached or gate); the run stopped on usage or an error; a weekly digest (scoreboard, what each game did, what the studio learned). Channel is the owner's choice (push or email). Everything else stays in the dashboard.

## Stages (stop after each stage for the owner's review; do not start the next without a go-ahead)

### Stage 1: runbook, checkpoint and digest (free)
- Write `docs/ops/taskforce-runbook.md`: the runner's loop, the stop reasons, the pause and resume rules, the `taskforce.json` and `run-state.json` formats, and what each agent prompt must contain (game slug, stage, files to read, "do not write activity lines or guess times").
- Write `tools/runner/digest.py`: builds the one-page digest from the existing files. Unit tests with sample files.
- Do a **paper run**: the builder plays the runner by hand on sample data to prove a stop and a resume work.
- **Done when:** the runbook and digest exist, tests pass, and a stop-and-resume (including a simulated sleep: kill mid-step, then resume) on sample data ends in the same state as an uninterrupted run.

### Stage 2: the switch and click records (dashboard, no runner)
- Dashboard: an On/Off control, a pause-mode choice, and a status panel (active/paused/stopped, game, stage, step, why it stopped), reading `taskforce.json` and `run-state.json` live. The control writes `taskforce.json` through a small localhost endpoint (atomic write; refused in sample mode unless pointed at sample data).
- Step A from task 011: a click writes its whole effect (see "Clicks").
- Tests (`npm test`) for the endpoints and the status panel.
- **Done when:** clicking On/Off changes the file and the panel; clicking Approve on a sample request writes the three records and the UI shows the effect live. Nothing starts agents yet.

### Stage 3: the local runner (needs the owner's explicit go-ahead; this changes the "dashboard never starts agents" rule)
- Build `tools/runner/` as described above, with a Start/Stop button wiring in the dashboard (the dashboard starts and signals the runner process; it does not call agents itself).
- Begin with a **supervised mode: run one step, then stop**. Run it with the owner three times before enabling continuous mode.
- Draft the permission rules the owner must add to their own Claude Code settings, and the exact steps. If the classifier blocks anything, stop and ask.
- Update `CLAUDE.md` ("Dashboard project", gates and the default first command) and `docs/plan/HANDOVER.md`.
- **Done when:** with the switch on, a sample approval starts the matching agent work and the result appears in the dashboard; switching off pauses cleanly after the step; switching on resumes from the checkpoint; the usage guard stops the run at the limit (test with a low stop percentage).

### Stage 4: notifications and the weekly digest
- Send the main-event notifications through the channel the owner chose. The weekly digest is generated by `digest.py`.
- **Done when:** a pitch-ready event and a usage stop each notify the owner once, and nothing else does.

### Stage 5 (optional, later): a cloud heartbeat
- A scheduled cloud routine that reads the same `taskforce.json` and does one step when the switch is on, for when the Mac is off. Only after the local runner has proved itself, and only with the owner's approval of the credit cost.


## Outcome (2026-10-05): stages 1 and 2 built; stages 3 to 5 not built, by owner decision
The owner decided to **keep agents manual**. The safety classifier blocked the unattended runner ("Create Unsafe Agents"), so stage 3 (the local runner), stage 4 (notifications, which depend on it) and stage 5 (a cloud heartbeat) were **not built**. Built and tested:
- **Stage 1:** `docs/ops/taskforce-runbook.md` (including a "Manual mode" section), `tools/runner/state.py`, `loop.py`, `digest.py` and 12 tests (`python3 -m unittest tools/runner/test_runner.py`), including a simulated sleep and resume.
- **Stage 2:** the On/Off switch in the dashboard top bar (writes `studio/taskforce.json` only), the status panel text, and click effects (a gate click writes its `decisions.json` entry and the game's history line; a pitch send-back to the designer raises its own pending revision request). The server now listens on `127.0.0.1` only. 88 dashboard tests pass.
In manual mode the switch is a go/pause signal for Director sessions, and the dashboard never starts agents. If the owner later wants the runner, the draft design is in this brief and a draft implementation can be rewritten in a fresh session; the owner would add the permission rule in their own settings.

## Out of scope
- Changing the approval gates. Greenlights, market scans, panel research, budget and free-API requests stay the owner's decisions. The review cap and learning loop belong to task 013.
- Any research, scraping or BoardGameGeek access.
- Editing real game files while testing.

## Success measures
- The owner can leave the runner on for a session and come back to a short digest, with no manual "continue with approved work".
- A pause and a resume reach the same state as an uninterrupted run (tested).
- No step runs after a usage stop, a STOP file or a switch-off.
- The owner is notified only for the main events.

## Questions for the owner (answer in the planning chat or `PROGRESS.md`)
- ~~Does the Mac usually stay on and awake?~~ Answered 2026-10-05: not always; it is on when the owner starts and stops the run, and may sleep in between. See "The Mac may sleep mid-run".
- Which notification channel: push, email, or both?
- What daily or weekly usage limit should stop the runner, besides the guard?
- After a stop on an error, should the runner retry once, or always wait for the owner? (Draft default: retry once on a network error, then wait.)
