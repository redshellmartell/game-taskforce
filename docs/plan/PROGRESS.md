# Progress log

Written by Claude Code after each task, newest first. See `WORKFLOW.md` for the format.

## 2026-10-03 — Task 002: Backfill Duel Flip's dashboard data — done
- Created `games/duelflip/brief.json`, `critique.json`, `pitch.json`, `playtest.json` and `activity.jsonl`, plus `games/status.json` (Duel Flip only: stage `owner-review`, revision 1, verdicts NEEDS-FIXES and REVISE-MINOR).
- `sim/run.py` now has a `--json` flag: `python3 run.py 2000 --json ../playtest.json` re-runs the v2 simulation (128,000 bot games, about a minute) and writes `playtest.json`. I only added measurements; the game logic is untouched, and the original tables come out byte-for-byte identical. The wording of the verdict, problems and ambiguities is transcribed from `playtest-report.md` into `sim/notes.py`.
- The dashboard now shows Duel Flip with a full scorecard, critic radar, seat and bot win rates, game-length distribution, flagged design elements, an 8-step history and no "inferred from file" labels. Small dashboard changes to support this: correlation entries that are `null` are skipped in the chart, flagged elements are listed under it, the Quality Lab files flags like "inert" under dead content instead of "overpowered", and reconstructed log lines are labelled "reconstructed from commits".
- Numbers that differ from the report (all re-measured, nothing invented):
  - Seat 1 wins 53.3% in the strategic mirror (report: 51.9%) and the worst bot is 3.4 points from fair (report: "within 2"). This is sampling noise: the same bot gives 50.2% to 53.4% depending on sample size and seed set (about ±1.1 points at 2,000 games). Still inside the 5-point target.
  - Skill expression 38.6 points (strategic's average win rate minus random's); the report's table gives 66.9 - 28.6 = 38.3.
  - Length 23.4 turns (report: 23.5), lead changes 3.1 (report: 2.4-3.9), ties 0.5%, species bonus decides 5.2% of games (report: 4.8%).
  - Runaway-leader rate is 76%. The spec defines it at the halfway point; the report only measured one third of the way in (66-70%; I get 70% there). It is above the 65% target, so the dashboard shows it red. The report calls the snowball mild and acceptable, so this is a real measurement, not a new defect.
- Judgement calls (please check): estimated length 12 minutes comes from the report's narrated play, and the target 12.5 minutes is the middle of the brief's 10-15 range. "Closest existing game" is Port Royal with similarity `medium` (the critic said "very near" but did not recommend a KILL). The three twists (species bonus, Lifebuoy refund, bait) are recorded as design elements in `cards` with `win_correlation: null`, because a plain correlation is confounded; their flags are the playtester's own words. Prototype cost is `null` (the pitch only gives a retail target) and `prototype_ready` is `false` while the critic's required changes are open.
- Activity timestamps are real commit times from `git log`; two events from the same commit are one second apart so they keep their order. Every line is marked `"reconstructed": true`.
- How the owner can see it: run the dashboard (`cd dashboard && npm install && npm start`), open Pipeline, then click Duel Flip. Also see the top bar, Studio Floor, Review Queue and Quality Lab.
- Questions for the owner: with one real game the top bar reads "Pitch rate 100%" (red) and "Concepts in development 0". That is correct for a single game and will settle once a second game is run.

## 2026-10-03 — Task 001: Merge the dashboard branch into main and tidy up — done
- Merged `main` into the branch first (one conflict, in `README.md`: kept both the Dashboard section and the planning-workflow section; `CLAUDE.md` merged without conflict and keeps both the "Owner ideas inbox" and "Planning workflow" sections).
- Added a root `.gitignore` (`__pycache__/`, `*.pyc`, `node_modules/`, `dist/`, `.DS_Store`) and removed the three committed `__pycache__` files from `games/duelflip/sim/`.
- Merged the branch into `main` through [pull request 1](https://github.com/redshellmartell/game-taskforce/pull/1) (a regular merge commit, so the milestone history stays readable). `main` now contains `dashboard/`, `games/duelflip/` and `docs/plan/`.
- Checked before merging: `npm test` passes (34 of 34), a fresh checkout installs with `npm ci`, builds and serves the real Duel Flip game, and a scan of the diff found no secrets or oversized files.
- Differs from the brief: nothing, except that I asked the owner to confirm the merge before doing it, because it publishes to `main` and is hard to undo. The owner told me to judge for myself; I did, and went ahead.
- How the owner can see it: open https://github.com/redshellmartell/game-taskforce and check that `main` has a `dashboard/` folder. To run the dashboard: `git checkout main && git pull`, then `cd dashboard && npm install && npm start` and open http://localhost:4173.
- Questions for the owner: none. Next in the queue is task 002 (Duel Flip data files); tasks 005 to 007 (test panel) are also unblocked now.

## 2026-10-03 — Before this log existed

Summarised by the planning chat from the branch `claude/nice-allen-b9i0vi`:
- Dashboard milestones 1 and 2 done; parts of milestone 3 started (Projects board, Game page). Details in the Status section of `docs/BUILD-DASHBOARD.md`.
- Added "+ New idea" (owner ideas inbox) and "Talk to it" tabs.
- First game, Duel Flip, run through the pipeline and pitched as a feasibility test.
