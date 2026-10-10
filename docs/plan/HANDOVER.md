# Handover (written 2026-10-10)

Read this first in a fresh session, after `CLAUDE.md`. It holds context that is not stated elsewhere in the repo. Then read `games/STATUS.md`, `games/approvals.json` and the retro `studio/retros/2026-10-06.md`.

## How the owner works
- New to coding: plain language, short steps, exact Terminal commands to copy. Cloud credits are limited (about $70 at the last count, expiring Nov 5). One task per session; long sessions cost more per step.
- **Usage guard** (`python3 tools/usage/usage.py --check`) was calibrated on 2026-10-06 to the Claude app's own percentages; it drifts, so recalibrate when it disagrees with the app ("calibrate usage: 5h=X 7d=Y"). Exit 2 means stop all agent work.
- Agents are run by hand: the owner says "run the taskforce" (the dashboard switch is only a signal; the dashboard never starts agents). Parallel agents are allowed only when the owner asks (up to 3 playtests at once worked fine).

## Standing decisions
- No BoardGameGeek / RPGGeek / VideoGameGeek fetching or API use (snippets are fine). Free third-party AI API declined. No unattended runner (the classifier blocked one; a click-to-fire cloud routine was discussed and dropped: the owner chose manual).
- **Review cap** (in `CLAUDE.md`): revision cycles run without a click up to the cap (4 per game during the learning period); at the cap or an early stop (critic says structural, or no movement) the Director raises a `review-cap` request. The owner counted older approved `-revision-N` requests inside the cap.
- Agent files are edited only with the owner's explicit OK. One-time edit done 2026-10-06: a pointer sentence in `game-designer.md`, `playtester.md`, `critic.md`. `CLAUDE.md` was edited once with the owner's approval (review cap).

## What exists for learning (task 013, in progress)
- `studio/lessons.md` (L1-L12), `studio/design-rules.md`, `studio/mechanics.md`, `studio/checklists.md`, `studio/scoreboard.md` (run `python3 tools/learning/scoreboard.py`), `studio/retros/2026-10-06.md`, `studio/learning-test-1.md`.
- `tools/sim-kit/` shared simulation kit (template, README, 7 tests; validated on Duel Flip). Playtesters should use it.
- Stage 4 (retros) has one retro; stage 5 (human ground truth) not started. **No human has played any game; every number is from bots.**
- Retro proposal 4 (a human playtest slot after cycle 2) needs a `CLAUDE.md` edit and the owner's OK. Proposed next checklist tweak (the designer shows a worked example where the twist pays in the scoring; lesson L12) is a studio-file edit I can make without agent-file edits.
- Owner idea parked: find public real-game rules and aggregate reviewer characteristics, then correlate with our playtests (see PROGRESS 2026-10-06). Needs the `deep-research` gate, the no-BGG rule and no personal data.

## Game status (see `games/STATUS.md`)
- Five `review-cap` requests are pending (all in `games/approvals.json`): `two-player-hidden-movement-grid` (recommend park), `asymmetric-duel-tug-of-war` (park), `silent-duo-deduction-coop` (pitch for a human playtest), `five-six-simultaneous-auction` (pitch for a human table test), `four-player-partnership-climber` (continue: one scoring-redesign cycle). A pitch needs the owner's explicit decision because the playtest verdicts are NEEDS-FIXES.
- `solo-nine-card-roguelike` (retitled **Whiskerdark**): playtest done, needs its fix-before-critic pass and critic. `heavenly-bodies` waits for the owner's design rulings (G1, G4, G7, G8, G10, G12/13, G27, G29); the unread designer note in `games/_notes/` is for it. `archetypes` waits for the owner's answers. `duelflip`, `grid-of-cards-area-control`, `standard-deck-engine-workshop` are in owner review.
- Learning test 1 (`four-player-partnership-climber`, Ladder Pairs): process improved (15-minute playtest, no dead cards, checklists followed) but the twist was inert again; critic 3.33. See `studio/learning-test-1.md`.

## Owner's Mac
- The dashboard syncs with GitHub through `tools/sync/` (pulls every 20s, pushes owner files incl. `studio/taskforce.json`). **The Mac must stay on `main`.** A sync conflict happened in `games/status.json` (a dashboard click edits it while the Director does too); fix: `cp games/status.json /tmp/x; git reset -q games/status.json; git checkout -- games/status.json`, then restart the sync. Offered but not built: stop clicks writing `status.json`.
- If the Pipeline tab shows fewer than all games, the Mac has not pulled (check `git status --short` for `UU`).

## Unmerged on this branch at handover
- Branch `claude/busy-cannon-ujcja7` holds the learning-test-1 work (Ladder Pairs brief, rules v1.1, playtest, critique, five `review-cap` requests on the dashboard side, lesson L12). Main stops at PR #14. **Ask the owner to merge a pull request first**, so the dashboard shows the requests.

## First moves for a new session
1. Read `CLAUDE.md`, this file, `games/STATUS.md`, `games/approvals.json`, pending notes in `games/_notes/`.
2. Fetch main; if the branch was merged, restart it from `origin/main`.
3. Do not start gated work without approval; check the usage guard before any agent call.
