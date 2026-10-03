# Dashboard and agent notes

Planning notes for the taskforce dashboard: a gamified UI where you watch the agents work and talk to them, similar in spirit to the "Tonka's Dungeon" system by Trevs Agents.

> **Reference status:** The reference video ("AI Agent ecosystem for autonomous businesses!", youtube.com/shorts/34F3calq358) couldn't be viewed from the build environment, only its title. The Gumroad listing describes the reference UI only as a custom, gamified dashboard with a theme you choose. Add screenshots to `docs/reference/` and update the "Reference UI" section below.

## Reference UI

_To fill in from screenshots:_ layout, how agents are drawn, how status and activity are shown, how you talk to agents, theme and art style, what we want to copy and what to skip.

## Build order

1. **Pipeline first.** Get at least one game through all five stages so the dashboard has real data to show.
2. **Read-only dashboard.** Shows agents, the game pipeline, reports and playtest charts. Reads files from the repository and runs nothing.
3. **Interactive dashboard.** Buttons and chat that start agent runs. This is where running costs begin (see "Running agents from the UI").
4. **Theme and polish.** Characters, animations, sounds, the "dungeon" feel.

## How the dashboard gets its data

The agents already write everything to files, so the dashboard reads those files. No database is needed at first.

| Dashboard shows | Comes from |
|---|---|
| Game pipeline board | `games/STATUS.md` (switch to `games/status.json` once the UI exists, as it's easier for code to read) |
| Game details | `brief.md`, `rules.md`, `playtest-report.md`, `critique.md`, `pitch.md` in each game folder |
| Playtest charts | a `results.json` written by each game's `sim/run.py`, next to the printed summary |
| Live agent activity | an activity log every agent appends to (see below) |
| Agent roster | `.claude/agents/*.md` plus `agents.json` for looks |

### Changes to make to the agents when the UI work starts

- **Activity log.** Each agent appends a line to `games/<slug>/activity.jsonl` when it starts, finishes a step, and finishes: `{"time", "agent", "game", "event", "message"}`. The dashboard turns these into "the playtester is running 2,000 games" style updates.
- **Machine-readable results.** The playtester writes `results.json` (win rates by seat and bot, game lengths, card usage). The critic adds its scores in a JSON block at the end of `critique.md`.
- **Status as JSON.** The manager writes `games/status.json` alongside `STATUS.md`.

## Agent roster and customisation

Each agent is one file in `.claude/agents/`. The part between `---` lines at the top is its configuration; the rest is its instructions.

- `name` - the ID the manager uses to call it
- `description` - when the manager should use it; this matters most for correct routing
- `tools` - what it may do (web search, read/write files, run code). Keep it minimal: the designer doesn't need web access, the researcher doesn't need to run code.
- `model` (optional) - a cheaper, faster model for simple agents, a stronger one for design and critique

To customise behaviour, edit the instructions: the researcher's rubric, the designer's principles, the playtester's thresholds (2,000 games, 5-point seat fairness) and the critic's verdict rules. Manager rules such as revision limits and the 18/30 cut-off live in `CLAUDE.md`.

For the dashboard, keep looks separate from behaviour in `agents.json`:

```json
{
  "market-researcher": { "title": "The Scout",     "avatar": "scout.png",     "color": "#c9a227" },
  "game-designer":     { "title": "The Artificer", "avatar": "artificer.png", "color": "#7b5ea7" },
  "playtester":        { "title": "The Gauntlet",  "avatar": "gauntlet.png",  "color": "#b5442f" },
  "critic":            { "title": "The Oracle",    "avatar": "oracle.png",    "color": "#3d7a8a" },
  "manager":           { "title": "Dungeon Master","avatar": "dm.png",        "color": "#e0d6c3" }
}
```

Agent ideas to add later: an **artist** (card layouts and a print-and-play PDF), a **rules editor** (makes rulebooks readable for new players), and a **trend watcher** (scheduled weekly market check).

## Running agents from the UI

Three ways, from cheapest to most automated:

1. **No runner.** You run the agents in Claude Code; the dashboard only watches the files. Costs nothing extra beyond your subscription. Start here.
2. **Buttons that send commands.** A small local server behind the dashboard starts Claude Code in non-interactive mode on your own computer (e.g. "playtest game X"), and the activity log streams progress back. Check Anthropic's current docs on whether this usage counts against the subscription or needs API billing.
3. **Fully autonomous.** Agents run on a server on a schedule using the Claude Agent SDK and API. Billed per use on top of a small server (a few dollars to ~$25/month). Only worth it once the pipeline reliably produces good games.

Safety rules that carry over to any setup: agents never publish, buy or contact anyone; a cap on revision loops and runs per day; a spend limit on any API key.

## Suggested tech for the dashboard

- **Front end:** a single web app (React + Vite, or plain HTML for the first version). Claude Code can build either.
- **Local server (from stage 3):** small Node or Python server that serves the repository's files and starts agent runs.
- **Live updates:** watch `activity.jsonl` files and push changes to the browser.
- **Charts:** a standard charting library for playtest results.

Views to build: agent roster (characters with idle/working state), pipeline board (games moving through the five stages), game detail page (all reports, charts, pitch), activity feed, chat with an agent, and a review queue where you approve, reject or send a game back with notes.
