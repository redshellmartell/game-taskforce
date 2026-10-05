# Handover (written 2026-10-04)

Read this first in a fresh session, after `CLAUDE.md`. It holds context that is not stated elsewhere in the repo.

## How the owner works
- The owner is new to coding: plain language, short steps, exact terminal commands to copy.
- Cloud credits are "free" (~$70 left, expire Nov 5). The plan usage meter shows 0%, so cloud sessions bill credits, not the plan. The usage guard (`tools/usage/usage.py --check`) can read STOP in a long session; it is an estimate and needs recalibrating (review-session item).
- Long sessions cost more per step. Prefer a fresh session per task or batch.

## Standing decisions (and why)
- **No BoardGameGeek / RPGGeek / VideoGameGeek fetching or API use.** Owner chose to skip anything that might violate terms. Web-search snippets are fine. Details in `CLAUDE.md` "Research rules".
- **No unattended agent runner.** The safety classifier blocked it, and the owner has not decided. Options offered: run by hand, an owner-allowed permission rule, or a scheduled cloud run. Task 011 stage 3 needs the owner's explicit go-ahead.
- **Free third-party AI API declined** (task 009 blocked). A local Ollama test on the owner's Mac is optional and was not run.
- **Dashboard never starts agents.** Its only writes are listed in `CLAUDE.md` "Dashboard project".
- **Pitch decisions need `"kind": "pitch"`** in `games/decisions.json`; without it an old gate "approve" hid Duel Flip from the Review Queue.

## Owner's Mac setup
- The dashboard runs locally and syncs with GitHub through `tools/sync/` (pulls every 20s, pushes only the owner's files).
- Pushing from the Mac needs a GitHub personal access token (not the password). The owner has made one.
- `tools/sync/repair.py` fixes the `games/approvals.json` conflicts that happened after pulls.
- Untested on a real Mac: `install-mac.sh` (background install) and auto-restart. Treat them as unverified.
- Dashboard fixes only reach the Mac after it pulls and the dashboard restarts.
- **The Mac must stay on `main`.** On 2026-10-04 it was left on an old `claude/...` branch, so it never saw merged work and the Approvals buttons looked missing. Cloud sessions work on their own branch; the owner merges the pull request into `main`, then the Mac catches up within about 20s.
- `claude/quirky-rubin-3ooa5m` (Review Queue pitch-decision change plus a sync box) is unmerged and 52 commits behind `main`; it conflicts with `main` in `dashboard/package.json`, `dashboard/server/index.js` and `ReviewQueueView.jsx`. Update it before any merge.

## Known gaps and half-finished items
- Panel calibration is thin (snippets only, no BGG). Mean error 0.38, trusted at low confidence.
- Bar Raiser veto thresholds are untuned. Heavenly Bodies has an active veto (G4 first-player draw).
- Agents' guessed timestamps: the dashboard clamps future times and marks them `~`; `tools/activity/fix_future_times.py` repairs the logs. Agents without a shell must not write their own times.
- Several playtesters exceeded the 5-config budget (6-7 configs); this was disclosed to the owner. Keep to the budget.
- Review-session list (panel-player improvements, billing plan vs credits, veto tuning, RPG scope, evidence refresh) is in `docs/plan/PROGRESS.md`.

## Pending owner decisions (check `games/approvals.json` for the live list)
- Revisions approved by the owner on the dashboard, not yet run: `grid-of-cards-area-control-revision-1`, `asymmetric-duel-tug-of-war-revision-1` (recorded in `decisions.json`). Pitch chosen for `three-player-trick-taker`: `pitch.md` not yet written.
- `silent-duo-deduction-coop-revision-1`
- New `-revision-1` requests after the 25+/30 run: `standard-deck-engine-workshop` (recommend approve), `five-six-simultaneous-auction` (recommend park), `solo-nine-card-roguelike` (recommend approve), `two-player-hidden-movement-grid` (recommend approve)
- `heavenly-bodies-revision-1`: recommend the owner answers the design rulings first (G1, G4, G7, G8, G10, G12/13, G27, G29)
- `archetypes-greenlight`: recommend answering its six open questions first
- `three-player-trick-taker-pitch-or-revise` (pitch recommended)
- `duelflip-revision-3` (recommend approve: bait hurdle fix only; revision 2 left playtest NEEDS-FIXES, critic REVISE-MINOR 3.42, runaway leader 74.8% to be documented). Last allowed loop.
- Unread owner note `games/_notes/20261004T122552Z-game-designer.md` (Heavenly Bodies comparables: Bang!, Smash Up, Fluxx, Exploding Kittens, Sushi Go; MTG/Dominion rejected; Love Letter/Coup/Munchkin brackets). Pass it to the designer, critic and Bar Raiser, then move it to `games/_notes/_done/` with a Director's reply.

## Task 013 (learning loop), in progress
- Built: scoreboard (`python3 tools/learning/scoreboard.py`), `studio/lessons.md`, `studio/design-rules.md`, agent read-lines, `review_cap` settings, dashboard `review-cap` gate. **Blocked:** `CLAUDE.md` edit refused by the classifier; text waits in `docs/plan/013-claude-md-patch.md`. Until applied, every revision still needs a `revision` approval. Stages 4 and 5 not started.

## Queued work
- Task 011: dashboard live/interactive, three stages, branch `dashboard-interactive`. **Read the 2026-10-04 (evening) entry in `docs/plan/PROGRESS.md` first**: it has the owner's "click, then see the effect" requirement and the Step A/B/C plan.
- Task 012: role-playing games in the pipeline (RPGs need a different playtest approach; say plainly what simulation cannot test).

## First moves for a new session
1. Read `CLAUDE.md`, this file, `games/STATUS.md`.
2. Read pending notes in `games/_notes/`.
3. Ask whether the owner wants "continue with approved work". Do not start gated work or research without approval.
