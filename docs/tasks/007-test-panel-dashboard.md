---
status: open
priority: high
depends_on: [006]
---
# 007: Test panel, part 3: personas in the dashboard

## Goal
The owner should feel like they know their test group: each persona is a recognisable character in the dashboard, with their own page, opinions, track record and statistics, and the owner can talk to them.

## Scope
Dashboard only, keeping the minimalist style and the read-only rule (talking to a persona uses the existing copy-a-prompt approach from the "Talk to it" tab). Update the sample data so every new view works in sample mode.

### 1. Test Panel department in the org chart
- Add a **Test Panel** department to `dashboard/agents.json` with `reportsTo: "playtester"`, so it appears under the Playtest Lab in the Agent Network.
- The Test Panel node can be expanded to show each persona as a small node (initials in their colour). Collapsed by default.
- Node states work like the other agents: playing (pulse), idle, waiting, error, read from `activity.jsonl` lines with `"agent": "panel:<id>"`.
- Add a Test Panel room card to the Studio Floor (personas currently playing, average fun given, last game reviewed).

### 2. The Panel page (new navigation item)
A "lounge" with one card per persona, each showing:
- initials avatar in their colour, name, archetype and tagline
- current status ("reviewing duelflip", "idle")
- games played, average fun given, and how harsh or generous they are compared with the panel average
- calibration status: trusted or not, with their error
- their latest one-line verdict, in their voice

Plus a panel-wide comparison: a persona × game heatmap of fun scores, and a "who is each game for" summary.

### 3. Persona profile page (click a persona anywhere)
Tabs:
- **Who they are** - the profile: sketch, loves, pet peeves, how they play, rating anchors (rendered from their persona file)
- **What they've played** - every game they reviewed: scores, would-buy and price, best and worst moment, the change they'd make, a link to the full review
- **Stats** - their rating distribution; their scores compared with the panel average and the critic; predicted (code) versus written (AI) ratings; how their bot performed (win rate, how often it fell behind)
- **Track record** - calibration games (predicted versus real reception) and, once human playtests with a matching `player_type` exist, their predictions versus real players of their type
- **Evidence** - the research behind them, with sources and last-refreshed date
- **Talk to them** - pick a game, type a question, copy the prompt ("Ask the Strategist about duelflip: …") to paste into Claude Code; below it, their past conversations from `conversations.jsonl`

### 4. Game page: Panel section
- A row per persona: avatar, fun, replay, would-buy, one-line verdict
- Agreement indicator (spread of fun scores): "the panel agrees" or "the panel is split"
- Best fit and worst fit audience
- Link to `panel-report.md`

### 5. KPIs and Learn mode
- New KPIs in `server/kpis.js` with tests: panel average fun per game, panel spread, persona calibration error, and persona-versus-human gap per player type.
- Learn mode "?" entries for: persona, test panel, calibration, predicted versus written rating.

## Done when
- In sample mode and with Duel Flip's real panel data, the owner can open the Panel page, click each persona, see all tabs filled (or a clear "no data yet"), and copy a "Talk to them" prompt.
- The Test Panel appears under the Playtest Lab in the Agent Network and on the Studio Floor.
- `npm test` passes.
- `docs/BUILD-DASHBOARD.md` Status and `docs/plan/PROGRESS.md` updated.
