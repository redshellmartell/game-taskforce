# Game Taskforce

A game studio think tank run by Claude Code agents. They research the tabletop market, design original board and card games, playtest them with simulations, and hand you finished pitches to prototype.

## The team

| Agent | Room | Job |
|---|---|---|
| Director (`CLAUDE.md`) | Director's Office | Runs the pipeline, decides what moves forward, reports to you |
| `market-researcher` | Market Intel | Finds market gaps and writes a design brief |
| `game-designer` | Design Studio | Designs the game and writes exact rules |
| `playtester` | Playtest Lab | Codes the game, runs thousands of bot games, plays narrated games |
| `critic` | Review Board | Checks originality, clarity, fun and balance; can kill a game |

## What to say to Claude Code

Open this repository in Claude Code and paste one of these.

**Make games**

- "Run the pipeline for a 2-player card game under 20 minutes."
- "Research 2-player card games under 20 minutes and pick the best idea."
- "Playtest `games/<slug>` again after the last revision."
- "Show me the status of all games."

**Record your decisions and real playtests** (these feed the dashboard KPIs)

- "Approve `<slug>`." / "Reject `<slug>` because ..." / "Send `<slug>` back: ..."
- "I built a prototype of `<slug>`."
- "We played `<slug>` with 3 players: fun 4, replay 3, clarity 5. Notes: ..."

**Build the dashboard**

- "Build milestone 1 of the dashboard from `docs/BUILD-DASHBOARD.md`."
- Then milestone 2, 3 and 4 the same way, one at a time.

## Where things are

| Path | What |
|---|---|
| `CLAUDE.md` | The Director's instructions and studio rules (revision limit, KPI targets, data formats) |
| `.claude/agents/` | One instruction file per agent; edit these to change how an agent works |
| `games/<slug>/` | Everything about one game: brief, rules, simulation code, reports, pitch, data files |
| `games/STATUS.md`, `games/status.json` | Where every game is in the pipeline |
| `docs/dashboard-notes.md` | Dashboard spec: KPIs, screens, data files |
| `docs/BUILD-DASHBOARD.md` | Step-by-step build instructions for the dashboard |
| `docs/reference/` | Screenshots of the UI that inspired the dashboard |

## Dashboard

A read-only, live control room for the agents. It shows who is working, how work flows between agents, and what they produced. It never starts agents, edits game files or calls an AI model.

**Start it** (needs Node.js 18 or newer):

```
cd dashboard
npm install     # first time only
npm start
```

Then open <http://localhost:4173>. It updates by itself within a couple of seconds when files in `games/` change.

**Sample vs real data:** if `games/` has no game folders yet, the dashboard shows clearly labelled sample data (a "Sample data" badge appears in the top bar). Run `npm run demo` to force sample data even when real games exist. `npm test` checks the KPI calculations.

**What it does:**
- **Agent Network:** an org chart. You are at the top, the Director's Office below you, and the four specialists under the Director. Grey org lines show who reports to whom; arrows show the files handed between the specialists. Click an agent to see what it is doing, how it works, its reports, and to leave it a note.
- **Studio Floor:** a room card per agent with status and two key numbers, the shared activity feed (filter by agent or game), a mini funnel and a milestone ticker.
- **Learn mode:** switch it on in the top bar for "?" markers that explain the concepts on screen.
- **Replay:** pick a game and step through how the team worked on it.
- **Pipeline:** pipeline health (funnel, kill rate by stage, cycle time, stuck games) and every game by stage. Click a game for its full overview page: scorecard, critic radar, balance charts, history and all its documents.
- **Review Queue:** pitches waiting for you, oldest first, each with how it plays, components, estimated cost and KPI status, plus your past decisions, real playtests and the agent-vs-human gap. Read-only: tell Claude Code "approve <game>" and it updates the files.
- **Quality Lab:** first-pass playtest rate over time, critic scores by revision, every game against its targets, and problem types that keep recurring.
- **Market & Portfolio:** opportunity scores, the mix by players, time, complexity, mechanic and theme, comparable titles, and common mechanics you have not tried yet.
- **Ops:** runs and failures per agent, simulated games, and each agent's recent events.
- Charts that compare games stay hidden behind a short message until there are at least two games.
- **+ New idea:** push an idea of your own into the pipeline at any stage. The dashboard saves it to `games/_inbox/`; then tell the Director "process my idea ..." and it runs the agents (see `CLAUDE.md`).

**Customise:**
- Agent room names, colours and who reports to whom: `dashboard/agents.json` (`reportsTo`)
- Plain-English agent summaries (the "How it works" tab): `dashboard/src/content/agents/`
- Sample data: `dashboard/sample-data/games/`

Build progress is tracked in `docs/BUILD-DASHBOARD.md` under "Status".

## Planning and building in parallel

Plan in a claude.ai chat, build in Claude Code. They share this repository: plans and task briefs live in `docs/plan/` and `docs/tasks/`, and Claude Code logs what it built in `docs/plan/PROGRESS.md`. See `docs/plan/WORKFLOW.md`.

- In Claude Code: **"Check for new tasks."**
- In the planning chat: **"Check the repo."**
