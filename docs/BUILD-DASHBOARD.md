# Build instructions: Think Tank Dashboard v1

Instructions for Claude Code to build the first version of the dashboard. The full product spec (KPIs, screens, data files) is in `docs/dashboard-notes.md`. Read it first; this file says how to build it and in what order.

The owner is new to coding. Explain what you're doing in plain language as you go, keep the setup to as few commands as possible, and finish every milestone with something they can open and click.

## Scope of v1

- **Read-only.** The dashboard shows what the agents are doing and what they produced. It never starts agents, edits game files or calls an AI model.
- **Minimalist look.** Dark, flat, thin borders, one accent colour per agent. No pixel art or images.
- **Live.** When agent files in `games/` change, the screen updates within a couple of seconds without a reload.
- **Works with no games yet** by showing clearly labelled sample data.

## Tech choices

Use these unless there's a strong reason not to, and say so if you change one:

- **Location:** everything in `dashboard/`. Nothing outside that folder changes, except a short "Dashboard" section added to the root `README.md`.
- **Server:** Node.js + Express. It reads the repository's `games/` folder, `.claude/agents/*.md` and `dashboard/agents.json`, and serves:
  - `GET /api/state` - one JSON object with agents, games (status, briefs, playtest and critique data, pitches, decisions, human playtests), the merged activity feed and computed KPIs
  - `GET /api/file?path=...` - the text of one Markdown report, limited to files inside `games/` and `.claude/agents/`
  - `GET /api/events` - Server-Sent Events; send a `changed` event when any watched file changes (use `chokidar`)
- **Front end:** React + Vite (TypeScript optional; plain JavaScript is fine for a beginner to read).
  - Network diagram: **React Flow** (`@xyflow/react`)
  - Charts: **Recharts**
  - Markdown reports: **react-markdown**
- **Running it:** one command, `npm start` inside `dashboard/`, builds and serves everything on `http://localhost:4173`. `npm run dev` for development is a bonus.
- **Sample data:** `dashboard/sample-data/` mirrors the real `games/` layout (two or three fake games at different stages, covering every file type in section 4 of the spec). The server uses it when `games/` has no game folders, or when started with `npm run demo`. The UI shows a visible "Sample data" badge whenever it's in use.
- **Robustness:** a missing or half-written file must never crash the server or a screen. Skip it, log a warning, and show "no data yet" where the number would be.

## KPI calculations

Put all KPI maths in one file, `dashboard/server/kpis.js`, with a comment above each function naming the KPI from `docs/dashboard-notes.md`. Compute KPIs on the server so the front end only displays them. Each KPI returns `{ value, target, status }`, where status is `good`, `warn`, `bad` or `none` (no data or no target). Add a small test file that checks the calculations against the sample data, runnable with `npm test`.

## Milestones

Do one milestone at a time. At the end of each: run it, check it works, commit, and tell the owner what to open and try.

### Milestone 1: Server, sample data and the Agent Network

1. Set up `dashboard/` with the server, front end and sample data.
2. Create `dashboard/agents.json` with each agent's room name and colour (see section 7 of the spec).
3. Build the **Agent Network** home screen (spec section 2):
   - Nodes for Market Intel, Design Studio, Playtest Lab, Review Board, Director's Office and You, laid out left to right in the order work flows.
   - Edges labelled with the handoff file; dashed curved edges back to the Design Studio for revisions.
   - Node states from the latest activity: working (soft pulse), idle (dimmed), waiting for owner (amber ring), error (red).
   - Clicking a node opens a side panel with tabs **What it's doing**, **How it works** and **Its work**.
     - *How it works* shows a plain-English summary (write these in `dashboard/src/content/agents/`, one short file per agent) plus the agent's `description` and `tools` read from its `.claude/agents/*.md` file.
     - *Its work* lists the reports that agent wrote, newest first, and renders one when clicked.
   - Clicking an edge shows the handed-over file for the most recent game that passed along it.
4. Add the **top bar** with the five headline KPIs and the **activity feed** under the diagram.

Check: `npm start`, open the page, click every node and edge, then add a line to a sample `activity.jsonl` and watch the screen update.

### Milestone 2: Learn mode and replay

1. **Learn mode** toggle in the top bar. When on, "?" markers appear next to: agent, subagent, handoff file, activity log, simulation/playtest, verdict, revision loop, KPI. Each opens a 2-3 sentence explanation with a link to the real file in the repository. Keep the texts in `dashboard/src/content/learn/` so they're easy to edit.
2. **Replay:** choose a game, then step forwards and backwards (or press play) through its activity log. The diagram highlights the active agent and moves a dot labelled with the game's name along each handoff.

Check: turn Learn mode on and open every "?"; replay one sample game from start to finish.

### Milestone 3: Studio Floor, Pipeline and Game page

1. **Studio Floor** (spec section 2): agent sidebar with mini funnel, room cards with status and two KPIs each, activity feed, selected-agent panel, milestone ticker.
2. **Pipeline:** one column per stage, game cards, funnel chart, kill rate by stage, cycle time.
3. **Game page ("concept dossier"):** header, scorecard with targets, critic score chart, balance charts (seat win rates, bot win rates, game-length distribution, card win correlation), stage history timeline, and document tabs.
4. A simple navigation bar to move between Network, Studio Floor, Pipeline and Review Queue.

Check: open each sample game's page; every chart has data or a clear "no data yet".

### Milestone 4: Review Queue and remaining views

1. **Review Queue:** pitches waiting for the owner with scorecard, how it plays, components and cost; past decisions; human playtest results and the agent-vs-human gap. Read-only, with a note explaining that decisions are recorded for now by telling Claude Code (for example "approve ember-market").
2. **Quality Lab, Market & Portfolio, Ops** as described in the spec. Hide a view's charts behind a short message until there are at least two real games.

Check: everything works with sample data, and with `games/` containing a single real game.

## Finishing

- Add a "Dashboard" section to the root `README.md`: what it is, how to start it, how to switch between sample and real data, and where to customise agent names, colours and Learn mode texts.
- Note anything left out or simplified at the bottom of this file under "Status".

## Status

_Not started._
