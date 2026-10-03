---
status: in-progress
priority: high
depends_on: [001]
---
# 008: Lean mode setup and usage meter

## Goal
The owner wants the studio to run lean on their subscription. The planning chat has already changed the agent instructions (models per agent, playtester and critic budgets, batched research with an idea bank, "Lean mode" in `CLAUDE.md`). This task sets up what those changes need, and measures real usage per agent and per game so we can see what actually costs the most.

## Scope

### 1. Idea bank
- Create `research/idea-bank.json` in the format in `.claude/agents/market-researcher.md`.
- Seed it from what exists: Duel Flip's idea (status `in-pipeline`, `game_slug: "duelflip"`) and the other candidates from `games/duelflip/brief.md` as `banked` or `rejected` with their scores. Set `last_scan` to the date of Duel Flip's research. Don't run any new research.
- Add `research/README.md`: what the bank is, statuses, and how to add your own idea ("Add to the idea bank: …").
- Dashboard: show the idea bank on the Market & Portfolio page (ideas by status and score, with filters by player count, length and mechanic) and its size on the Market Intel room card. Read-only.

### 2. Tidy Duel Flip's simulation folder
Apply the new playtester rule "one simulation folder": remove `games/duelflip/sim/v1/` (it stays in git history) and move the one-off experiment scripts into `sim/experiments/`. Make sure `run.py` still works and the numbers don't change.

### 3. Usage meter
Claude Code saves a log of every session, including token counts for each step and for each sub-agent. Write `tools/usage/usage.py` (Python, standard library only) that:
1. Finds the Claude Code session logs for this project on the machine it runs on (look in `~/.claude/projects/`; check the current Claude Code docs for the log location and format rather than guessing).
2. Totals input, output and cached tokens per session, per model and per agent (the main session counts as `director`; sub-agent runs are attributed to their agent name).
3. Attributes usage to games where possible, using the times in each game's `activity.jsonl`, and to `research`, `dashboard` or `other` otherwise.
4. Adds an "API-equivalent cost" column using a price table in `tools/usage/prices.json` (fill it from the current Anthropic pricing page and record the date), clearly labelled as an equivalent, not a charge.
5. Appends a summary per session to `usage/sessions.jsonl` (no prompts or content, only counts, names and times) so data from cloud sessions is kept in the repository.

Add to `CLAUDE.md`: at the end of every task or game stage, run `python tools/usage/usage.py --record` and commit the result.

Dashboard: replace the "usage per pitch" placeholder on the Ops page with real data from `usage/sessions.jsonl`: usage by agent, by game and by week, plus "usage per pitched game". Add the `usage per pitch` KPI test.

### 4. Lean-mode check
After the setup, do a short dry run: ask the Director (in this session) what it would do for "start a new game", without running agents, and confirm it chooses a brief from the bank rather than a market scan. Note the answer in `PROGRESS.md`.

## Done when
- `research/idea-bank.json` is seeded and visible on the dashboard.
- `games/duelflip/sim/` has one current version and still produces the same headline numbers.
- `python tools/usage/usage.py` prints a table of usage by agent and model for this project, and `--record` appends to `usage/sessions.jsonl`.
- The Ops page shows usage by agent and by game.
- `npm test` passes.
- `PROGRESS.md` entry includes the first real usage numbers: which agent and which task used the most so far.

## Notes for the builder
If the session logs aren't available in a cloud session, make the script work wherever it can, record what you can, and explain in `PROGRESS.md` what the owner needs to run on their Mac to get the full picture.
