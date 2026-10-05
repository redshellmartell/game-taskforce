# Taskforce runbook (switch, checkpoint, resume)

For task 014. The runner (stage 3) follows this file. Until then a Director session can follow it by hand. Code: `tools/runner/` (`state.py`, `loop.py`, `digest.py`, tests in `test_runner.py`).

## The files
| File | Written by | Meaning |
|---|---|---|
| `studio/taskforce.json` | dashboard (stage 2), or by hand | The switch: `active`, `pause_mode` (`after-step` or `now`), `updated`, `by` |
| `studio/run-state.json` | the runner | The checkpoint: `status`, `game`, `stage`, `step`, `agent`, `started`, `heartbeat`, `last_done`, `reason`, `queue` |
| `studio/STOP` | the owner | Empty file. If it exists the runner stops at the next check, even with the dashboard closed |
| `games/*/activity.jsonl`, `status.json`, `approvals.json`, `decisions.json` | agents and the Director | The source of truth for the work itself |

`status` is one of `running`, `paused`, `stopped`, `waiting-gate`, `usage-stop`, `error`. The dashboard shows **interrupted** when `status` is `running` but the heartbeat is older than 2 minutes (for example the Mac slept).

## The loop (one agent at a time)
1. **Check** (`state.stop_reason`): the switch is on, `studio/STOP` does not exist, and `python3 tools/usage/usage.py --check` is not exit 2. Otherwise write the reason into `run-state.json` and stop.
2. **Pull** the latest files (merge, not rebase; `tools/sync/repair.py` for an `approvals.json` conflict). Record any owner click not yet recorded.
3. **Resume** (`state.resume_action`): `redo-step` if a step was in flight and the runner was interrupted (stale heartbeat, or stopped or errored mid-step), `fresh` otherwise.
4. **Pick** the next piece of work using `CLAUDE.md`: an approved revision, the next stage of a game, or a pitch. Highest opportunity score first. If a request needs the owner (a gate, the review cap, a pitch ready), write `waiting-gate` and stop.
5. **Run the step:** `begin_step` (checkpoint + activity `start` line), run the agent, then `finish_step` (activity `done` line, record in `status.json` and `STATUS.md`). Commit and push only when the step finished.
6. **Repeat** from 1.

## Pausing
- **after-step** (default): the running agent call finishes and is recorded, then the runner stops with `paused`.
- **now**: interrupt the agent. The step is not marked done, so a resume redoes it.

## Sleep and interruptions
Treat a sleep as normal. Run under `caffeinate -i`. The runner rewrites `heartbeat` every 30 seconds. A gap of more than 2 minutes between loop checks means the machine slept: check the in-flight step's output and redo the step from the start if it is incomplete. Every step must be safe to repeat (rules are edited in place, a playtest re-runs from scratch, a commit happens only when the step finished). On a network error retry once, then stop with `error` and a plain reason.

## Manual mode (the owner's decision, 2026-10-05: "keep agents manual")
No unattended runner is built. The safety classifier blocks one, and the owner chose to keep agents manual. The switch and the checkpoint are still used, with a Director session as the runner:
- **The switch is a go / pause signal.** In a session the owner starts ("run the taskforce"), the Director reads `studio/taskforce.json`. If `active` is false it does nothing but report. If true it works through the loop below, one agent at a time, until the switch goes off, `studio/STOP` appears, the usage guard says stop, or a decision is needed.
- **The dashboard never starts agents.** Turning the switch on records the owner's intent only. The status text says so.
- **Clicks are recorded by the dashboard itself** (decision entry, history line, a send-back's revision request). The Director then acts on them; it does not need to be told "continue with approved work".
- **The Director keeps the checkpoint:** write `studio/run-state.json` (`state.begin_step` / `finish_step` / `stop`) around each step, and log `start` and `done` lines in `games/<slug>/activity.jsonl` with real times. Agents without a shell never write their own activity lines.
- **Which step is next** (derive it from `games/status.json` and `approvals.json`): a game in `brief` with an approved greenlight needs design; in `playtest` it needs the playtester; in `critique` with no verdict it needs the critic; with a verdict it needs a decision (PASS goes to the pitch; otherwise raise a revision request, or run the next revision if one is approved after the verdict); `owner-review` waits for the owner.
- **A run ends** by writing the stop reason into `run-state.json`, committing and pushing. A later session resumes from the checkpoint; a step with a `start` line and no `done` line is redone.
- **Sleep and interruptions** matter only for a local runner; in a session the Director just redoes an interrupted step.
- **Not built:** the local runner and the notifications (stages 3 and 4 of task 014). Revisit only if the owner changes this decision and adds the permission rule in their own settings.

## What each agent prompt must contain
The game slug, the stage, the files to read, the output files to write, "return a summary of at most 10 lines", and for agents without a shell (designer, critic, market researcher, panel player) "do not write activity lines or guess times". The runner writes those lines with the real time.

## What never runs on its own
Greenlights for new games, market scans, panel research, budget increases and free-API requests are the owner's decisions. A game that reaches its review cap stops for the owner (task 013).

## Checking it works
`python3 -m unittest tools/runner/test_runner.py` includes a simulated sleep: a run killed mid-step and resumed ends in the same state as an uninterrupted run, and a switch-off pauses after the running step. `python3 tools/runner/digest.py` prints the one-page digest.
