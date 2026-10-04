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

**Milestone 1: done.** Server (`/api/state`, `/api/file`, `/api/events`), sample data, KPI maths with tests (`npm test`), the Agent Network with side panels, the top bar with five KPIs and the activity feed.

**Milestone 2: done.** Learn mode ("?" markers, texts in `dashboard/src/content/learn/`) and Replay.

**Milestone 3: done.**
- **Studio Floor:** agent sidebar with a mini funnel, a room card per agent (status, current game and step, two key numbers), the activity feed with filters by agent and game, the selected-agent panel beside the cards, and the milestone ticker.
- **Pipeline:** one column per stage (plus a "Your ideas" column and a collapsed Killed list), the stage funnel, kill rate by stage, cycle time per game, average revision loops, first-pass playtest rate and stuck games. The numbers are computed in `server/kpis.js` and tested.
- **Game page:** header, scorecard with targets, critic radar, win rate by seat and by bot, game-length distribution, card win correlation (all Recharts), history timeline and document tabs. The game-length distribution needs an optional `length_histogram` in `playtest.json`; I added it to the playtester's instructions, and without it the chart says so and shows the mean.
- **Navigation:** Agent Network, Studio Floor, Pipeline. The Review Queue page belongs to Milestone 4.
- **Org-chart layout (owner request):** You at the top, the Director's Office below, the four specialists in a row under it with their handoff arrows and revision loops. `reportsTo` in `agents.json` says who reports to whom, so a specialist can later grow into a department.

**Added at the owner's request:** "+ New idea" (inject your own idea at any stage) and a "Talk to it" tab on every agent. The dashboard's only write is saving an idea file to `games/_inbox/` (`POST /api/ideas`, refused in sample mode). It never starts agents; the owner tells the Director to process the idea, and `CLAUDE.md` has the instructions for that.

**Milestone 4: done.** Review Queue (waiting pitches with how it plays, components, cost and KPI status; past decisions; human playtests and the agent-vs-human gap; read-only with a note on recording decisions through Claude Code), Quality Lab, Market & Portfolio and Ops. Charts that compare games are hidden behind a message until there are at least two games. The maths is in `server/kpis.js` and covered by `npm test` (34 tests).

**Dashboard v1 is complete.** Left out or simplified:
- Usage per pitch is a placeholder ("tracked once runs are automated"), as the spec says.
- "Simulated games in the last 24 hours" uses the time of each game's last playtester run, because the playtest file has no timestamp of its own.
- Problem types in the Quality Lab are found by matching keywords in the playtester's problem text, so unusual wording can land in no category.
- Review Queue "How it plays" is read from a "How it plays" heading in `pitch.md`; a pitch without that heading shows "Not in the pitch file yet".
- No buttons that run agents or record decisions (that is stage 3 in the spec).

**Added with task 008:** idea bank on Market & Portfolio (with a "scan due" indicator and the Market Intel room card), usage on the Ops page (token-based: guard windows, usage per pitched game, by agent, game and week; read from `usage/sessions.jsonl` and `usage/guard.json`), and a "Test panel" tab on the Playtest Lab (personas from `panel/`, calibration, profile and evidence; the file endpoint also serves `panel/personas/` and `panel/evidence/` Markdown).

Known quirk: the four reporting lines share one horizontal trunk, so clicking the trunk selects the last specialist; click a line's own vertical drop (or the node) to pick a specific one.

Notes on what differs from the plan:
- Added `remark-gfm` so tables in reports render properly.
- Agents that have no `activity.jsonl` yet (for example the first real game, `duelflip`, which predates the data files) get their activity inferred from the report files that exist, and the stage is worked out from those files. The panel marks such lines "inferred from file".
- The side panel sits beside the diagram instead of over it, so every node stays clickable.
- The revision lines use a small custom edge because React Flow's built-in curve goes flat when both ends point down.
- A first design put dotted lines from "You" to every agent; it looked cluttered, so "You" now has one line (pitch.md from the Director) and the step-in actions are the "+ New idea" button and each agent's "Talk to it" tab.
- Real-game KPIs show "no data yet" until agents write the JSON files described in `docs/dashboard-notes.md` section 4.

**Task 007 (test panel in the dashboard): done.** A Test Panel department sits under the Playtest Lab in the Agent Network (personas hidden until you click "show personas", then small nodes in their colours, pulsing while a `panel:<id>` activity line is running) and has a room card on the Studio Floor. New **Panel** page: one card per persona (status, games, average fun, harsh or generous, trust, latest verdict), a persona × game heatmap and "who is each game for". Clicking a persona (anywhere) opens its page with tabs Who they are, What they've played, Stats, Track record, Evidence and Talk to them (copy-a-prompt plus past conversations). The Game page has a Test panel section (rows per persona, matchup grid, rotation summary, agreement flag) and a "Panel report" document tab. KPIs (`panelStats` in `server/kpis.js`, tested): average fun and spread per game, calibration error, persona-versus-human gap per `player_type`. Sample data has panel scores for Lantern Heist and Tide Lords, reviews and conversations for Lantern Heist, and Casual "playing" on Ember Market.

**Review Queue buttons (owner request, 2026-10-04).** Approve for a prototype, Send back with notes and Reject, each with a confirm step and an optional note. A click appends one entry to `games/decisions.json` (`POST /api/pitch/:slug`, `server/pitch.js`, atomic, refused in sample mode and for games not in owner-review, and for a pitch already decided); `status.json` is never edited by the dashboard. A decided pitch leaves the queue and shows under "Decided, waiting for the Director" until the Director acts on it (rules in CLAUDE.md). 68 tests.

**Notes to agents and a clearer Approvals page (owner request, 2026-10-04).** The agent panel's "Talk to it" tab now has a **Send note** button: `POST /api/notes` (`server/notes.js`) saves `games/_notes/<time>-<agent>.md` (atomic, validated agent and game name, 4,000 characters, sample mode refused); the tab lists your notes to that agent as waiting or answered with the Director's reply. The "Save idea to inbox" button says why it is greyed out (it needs a name). Approvals are compact cards with a coloured stripe (green recommend approve, amber think, red stop), a `1/6` counter, the game, gate, critic and playtest tags, a three-line summary, the decision buttons immediately visible, and the long text behind a Details toggle. `tools/sync/sync.sh` also syncs `games/_notes/`. 72 tests.
