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

**Customise:**
- Agent room names and colours: `dashboard/agents.json`
- Plain-English agent summaries (the "How it works" tab): `dashboard/src/content/agents/`
- Sample data: `dashboard/sample-data/games/`

Build progress is tracked in `docs/BUILD-DASHBOARD.md` under "Status".
