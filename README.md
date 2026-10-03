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
