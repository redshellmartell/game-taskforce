# Progress log

Written by Claude Code after each task, newest first. See `WORKFLOW.md` for the format.

## 2026-10-03 — Task 008: Lean mode setup and usage meter — done (one part skipped at the owner's request)
- **Idea bank.** `research/idea-bank.json` is seeded from Duel Flip's brief only (Duel Flip `in-pipeline`; the two other candidates `banked`, 22 and 20; details the brief did not record are `null`). `research/README.md` explains it ("Add to the idea bank: ..."). The Market & Portfolio page shows the bank with filters (status, players, length, mechanic) and whether a scan is due; the Market Intel room card now shows "Ideas banked" in place of "Avg opportunity" (still on the Market page). No research was run.
- **Skipped at the owner's request: tidying Duel Flip's simulation folder** (brief step 2). The owner said Duel Flip's data only needs changing where the UI or infrastructure requires it, and this did not. `games/duelflip/sim/v1/` and the loose experiment scripts are still there.
- **Usage meter** (`tools/usage/usage.py`, standard library only, 12 tests): reads this project's Claude Code logs (main conversation plus each sub-agent's own log and agent type), attributes usage by agent, model, game or area (paths in tool calls, then each game's `activity.jsonl` window) and day/hour, and appends counts only (no prompts or content) to `usage/sessions.jsonl` with `--record`. Claude Code's logs include its own `cost-state` totals, which I used to check the price table.
- **Differs from the brief: tokens, not dollars.** At the owner's request the meter is token-based ("usage tokens" = input + output + cache writes + cache reads at 0.1 weight). Dollars are an optional `--cost` column. The price table (`tools/usage/prices.json`) could not be filled from the pricing page (not reachable from the cloud session); instead Haiku matched Claude Code's own cost records exactly ($1 / $5 per million tokens, $0.01 per web search) and Sonnet's output, cache-read and cache-write rates were solved from three snapshots (its plain input rate is a placeholder). Opus has no price.
- **Added at the owner's request: a usage guard for scheduled runs.** `usage.py --check` returns 0 go, 1 warn, 2 stop, 3 not calibrated; `--calibrate 5h=<percent> 7d=<percent>` turns the plan percentages from the Claude app into token budgets. Calibrated from the owner's Pro readings (5-hour 98%, weekly 14%): about 10.2M usage tokens per 5-hour window and 71M per week. The stop percentage is **70%** (warn at 50%), in `studio-settings.json`. `CLAUDE.md` tells every scheduled or batch run to check first, and to run `--record` at the end of each task. Claude Code's logs do not contain the plan percentage, so the budgets are estimates; the weekly one is probably too small because the owner's reading includes non-studio use (the safe direction).
- **Ops page:** shows the guard windows, usage per pitched game in tokens, and usage by agent, game and week (tokens only). Also added at the owner's request: a **Test panel tab on the Playtest Lab** in the Agent Network, with the five personas, their calibration and links to each profile and evidence file.
- **First real usage numbers (this session, 10.8M usage tokens):** the Director (the main conversation) used **91%**, then market-researcher 5%, general-purpose 2%, playtester 1%. By area: dashboard 32%, panel 26%, Duel Flip 17%, usage tooling 14%. **Cache reads were 82% of usage**: the cost is mostly re-reading a long conversation on every step, not the agents' work. One long session filled a whole 5-hour Pro window. That is the main reason to run one task per session.
- **Lean-mode dry run** (no agents run, nothing written), "start a new game": the Director would first run the usage guard (currently STOP, the 5-hour window is full), then read the idea bank. The bank has only **2 banked ideas scoring 18 or more** (needs 3), so the rule sends it to a **market scan**, which is behind the `scan` approval gate: it would write a request to `games/approvals.json` and stop. It would **not** write a brief from the bank, which differs from what the brief expected; that follows from seeding the bank only from existing data. With the sample bank (4 strong ideas) it would choose a brief from the bank. To get past this without a scan, add one more idea ("Add to the idea bank: ...") or approve a scan.
- **Task 005 overspend (for the planning chat):** I finished task 005 before the lean-mode rules reached my branch, using about 30 searches per persona against the new limit of 10, plus a retry that could not run once the session's 200-search budget was used up. The research is in `panel/evidence/`; nothing needs redoing unless the owner wants better evidence.
- Checks: 44 dashboard tests, 12 usage tests, scripted browser checks. No screenshots.
- How the owner can see it: dashboard > Market & Portfolio (idea bank), Ops (usage and guard), Agent Network > Playtest Lab > Test panel. In a terminal: `python3 tools/usage/usage.py`, `--check`.
- Questions for the owner: (1) The first scheduled run is the real test of the guard; after it, send fresh plan percentages (5-hour and weekly) and I will recalibrate. (2) Should the idea bank get a third strong idea, or should the first new game start with an approved market scan? (3) The owner asked for a review session to settle remaining details; this entry lists the open points above.

## 2026-10-03 — Task 005: Test panel part 1 (personas) — done

### What is built
- `panel/personas/`: five profiles (strategist, casual, competitor, story, family) with complete frontmatter (weights add up to 1) and all the sections the brief asks for. Each links to its evidence file. None mention the eight calibration games.
- `panel/evidence/`: five evidence files (12 to 14 themes and reactions to ten well-known games each, about 60 to 75 URLs each, a "Gaps" section each). Every one says it rests on search-result summaries only.
- `panel/calibration.json`, `panel/calibrate.py`, `panel/README.md`, `panel/activity.jsonl`.
- `.claude/agents/market-researcher.md` has a new "Panel research mode"; `CLAUDE.md` has a "Player test panel" section ("refresh the panel research", "add a persona: ...").
- Calibration (8 games; mean error, limit 1.0): casual 0.44, competitor 0.36 (7 games), family 0.64 (7 games), story 0.62, strategist 0.38. All five are `trusted` on the first attempt, so no profile was tuned.

### What differs from the brief, and why
- **Evidence sources.** BoardGameGeek (including its XML API), Reddit, Wikipedia, Meeple Mountain and Dice Tower are blocked by the cloud environment's network policy, and so were most review sites when fetched. All evidence comes from web-search result summaries, not opened pages, and from reviewers and bloggers more than raw forum posts.
- **Search budget.** The session allows 200 web searches in total, and it ran out. A stricter second attempt at the "actual" ratings could not search and wrote all-null files over the first attempt (my mistake: I told it to overwrite). I recovered the first attempt's ratings from its saved transcript and used those. They are thin (about one search per game, many general rather than persona-specific). `calibration.json` says so: `baseline_quality: "low"`, and each persona has `confidence: "low"`.
- **The "trusted" flags are provisional.** Predictions and actuals both draw on the same language model's knowledge of these games, so agreement shows the profiles are consistent with how a model reads reviews, not independent ground truth.
- Two ratings are null because nothing could be supported: Terraforming Mars for the competitor, and Ticket to Ride for the family player.
- Profiles and evidence were done in two separate rounds, and the "actual" ratings were not read until after the blind predictions, so the check is fairer than a profile written with the answers in view.

### How the owner can see it
Open `panel/README.md`, then any file in `panel/personas/` (profile) and `panel/evidence/` (research). `panel/calibration.json` has each persona's predicted and actual ratings and error.

### Next
Tasks 006 (persona bots, free fun scoring, AI reviews, talking to personas) and 007 (personas in the dashboard) are unblocked and not started. Read their briefs first. To make the panel's evidence solid, see the questions below, then ask for "Refresh the panel research".

### Smaller notes
- Largest calibration miss: the story persona on Dixit (predicted 3.5, actual 5). Its profile has no example of an imaginative storytelling game. Worth adding at the next refresh, not before, so the test stays honest.
- Task 002 (Duel Flip data) is done and logged below; its changes are on this branch but not yet merged into `main` (no pull request has been opened for them).
- The working files used for calibration (predictions and recovered ratings) lived in the session's scratch folder and are not in the repository; their content is already in `panel/calibration.json`.

### Questions for the owner
- **Do you want the evidence rebuilt properly?** In the cloud environment's settings, allow `boardgamegeek.com`, `reddit.com` and the review sites under *Network access* (https://code.claude.com/docs/en/cloud-environments#network-access) and raise the web-search limit (the environment variable is `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`). Then a fresh session can run the refresh with real forum voices and persona-specific ratings.

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
