# Dashboard spec: Game Think Tank

The dashboard is the control room of a small game studio think tank. It answers the questions a game company's leadership asks every week:

- **Is the idea pipeline healthy?** How many concepts are in development, where are they stuck, how many make it through?
- **Are the designs any good?** Are they balanced, original, clear and fun, and are they getting better?
- **Are we aiming at the right market?** Which gaps are we chasing, and is the portfolio varied?
- **What is ready to make?** Which pitches are waiting for a decision, and what would a prototype cost?
- **Is the team working well?** Which agents are busy, stuck or failing, and what does each pitch cost to produce?

Every number on screen should help answer one of these. If a widget doesn't, cut it.

**Look:** minimalist first. Same layout and interactions as the reference UI, none of the pixel art. The themed look is a later layer.

---

## 1. KPIs

Each KPI lists its definition, where its data comes from, and a target where one makes sense. Targets are starting points to adjust after the first few games.

### Pipeline health (the funnel)

| KPI | Definition | Source | Target |
|---|---|---|---|
| **Concepts in development** | Games not yet pitched, killed or archived | `status.json` | 1-3 at a time |
| **Stage funnel** | Count of games that reached each stage: Brief → Design → Playtest → Critique → Pitch → Owner-approved → Prototyped | `status.json` stage history | - |
| **Pitch rate** | Pitches ÷ briefs started | `status.json` | 20-40% (lower means research is aiming badly, higher means filters are too soft) |
| **Kill rate by stage** | Where games die, as a % of games entering that stage | `status.json` | Most kills early (brief or first playtest), few at critique |
| **Average revision loops** | Design → playtest → critique loops per pitched game | `status.json` | ≤ 2 |
| **Cycle time** | Time from brief to pitch | stage timestamps | Track the trend |
| **Stuck games** | Games with no activity for over 24h, or waiting for the owner | `activity.jsonl`, `status.json` | 0 |

### Design quality

| KPI | Definition | Source | Target |
|---|---|---|---|
| **First-pass playtest rate** | % of new designs that get PASS on their first playtest | `playtest.json` | Rising over time |
| **Seat balance** | Largest gap between any seat's win rate and a fair share | `playtest.json` | ≤ 5 points |
| **Skill expression** | Strategic bot's win rate minus random bot's | `playtest.json` | ≥ 20 points (decisions matter) |
| **Game length vs target** | Simulated average length compared with the brief's play-time target | `playtest.json`, `brief.json` | Within ±20% |
| **Lead changes** | Average times the lead changes per game | `playtest.json` | ≥ 2 (tension until the end) |
| **Runaway leader rate** | % of games won by whoever led at the halfway point | `playtest.json` | ≤ 65% |
| **Dead or broken content** | Cards/actions never worth taking, or with outsized win correlation | `playtest.json` | 0 at pitch |
| **Rules ambiguities** | Ambiguities the playtester had to resolve | `playtest.json` | 0 at pitch |
| **Critic scores** | Average of originality, clarity, fun, balance, market fit, production (1-5 each) | `critique.json` | ≥ 3.5 at pitch |

### Market and portfolio

| KPI | Definition | Source | Target |
|---|---|---|---|
| **Opportunity score** | Brief rubric score (out of 30) for each game | `brief.json` | ≥ 18 to proceed |
| **Portfolio mix** | Games by player count, play time, complexity, core mechanic and theme | `brief.json` | No single mechanic over 40% |
| **Comparable titles** | Named competitor games per brief, with their BGG rating or crowdfunding result where found | `brief.json` | ≥ 2 per brief |
| **Originality score** | Critic's originality score; flag any "too close to an existing game" | `critique.json` | ≥ 3 |

### Production readiness

| KPI | Definition | Source | Target |
|---|---|---|---|
| **Component count** | Total cards, tokens, dice, boards per pitched game | `pitch.json` | Within the brief's budget |
| **Estimated prototype cost** | Rough print-and-play or print-on-demand cost | `pitch.json` | Track |
| **Prototype-ready** | Pitch has full rules, component list and (later) printable files | `pitch.json` | - |

### Owner decisions and real-world testing

The parts only you can do. They are the most important numbers on the dashboard because they check whether the agents' judgement matches reality.

| KPI | Definition | Source | Target |
|---|---|---|---|
| **Review queue** | Pitches waiting for your decision, and how long they've waited | `status.json` | Cleared weekly |
| **Owner approval rate** | % of pitches you approve | `decisions.json` | Rising over time |
| **Prototypes built** | Games you've made physically | `decisions.json` | - |
| **Human playtest score** | Average rating from your real playtests (fun, would play again, clarity; 1-5) | `human-playtests.json` | - |
| **Agent-vs-human gap** | Critic's fun score minus the human fun score | `critique.json`, `human-playtests.json` | Close to 0; a big gap means the critic needs recalibrating |

### Team operations

| KPI | Definition | Source | Target |
|---|---|---|---|
| **Agents active** | Agents working now, out of the total | `activity.jsonl` | - |
| **Runs per agent** | Tasks completed per agent this week | `activity.jsonl` | - |
| **Failure rate** | Runs that ended in an error or were abandoned | `activity.jsonl` | < 10% |
| **Simulated games** | Bot games run today and in total | `playtest.json` | - |
| **Usage per pitch** | Usage or cost spent per finished pitch (once runs are automated) | run logs | Falling over time |

---

## 2. Screens

### Home screen: the Agent Network (learning-first)

The owner is new to agents, so the home screen makes the system visible rather than abstract. It is a web diagram of the team:

- **Nodes are agents**, arranged in the order work flows: Market Intel → Design Studio → Playtest Lab → Review Board → Director's Office → You. The owner is a node too, because the system ends with a human decision.
- **Lines are handoffs**, labelled with the file that travels along them (`brief.md`, `rules.md`, `playtest-report.md`, `critique.md`, `pitch.md`). Feedback loops are drawn as curved lines going back to the Design Studio, labelled "revision".
- **Live state:** a working agent's node glows; when it hands work on, a small dot labelled with the game's name travels along the line. Idle agents are dimmed; an agent waiting for you gets an amber ring; an error is red.
- **Click a node** to open the agent panel with tabs:
  - **What it's doing** - current task and its step-by-step progress from the activity log, in plain language
  - **How it works** - a short plain-English explanation of this agent's job, what it reads, what it writes, which tools it's allowed and why, and a link to its instruction file
  - **Its work** - the reports it produced, rendered in place
  - **Talk to it** - chat (stage 3)
- **Click a line** to see the actual file that was handed over and which game it was for.
- **Learn mode toggle:** when on, small "?" markers explain the concepts on screen, such as what an agent is, what a subagent is, why the playtester writes code, what a handoff file is, what the activity log is, and why the critic can kill a game. Each explanation is two or three sentences with a link to the file where you can see it for real.
- **Replay:** pick a game and play back its journey through the network step by step, so you can see exactly how the team collaborated on it.

The KPI views below are a click away. The Agent Network is for understanding the team; the KPI dashboards are for running the studio.

### KPI screen: the Studio Floor

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ GAME THINK TANK   Concepts 3 │ Pitch rate 33% │ Avg critic 3.8 │ Review 1 │ 2/5 ● │
├─────────────┬───────────────────────────────────────────────────────────────┤
│ Agents      │ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐        │
│ ● Director  │ │ MARKET INTEL  │ │ DESIGN STUDIO │ │ PLAYTEST LAB  │        │
│ ● Research  │ │ ● idle        │ │ ● working     │ │ ● idle        │        │
│ ● Designer  │ │ 4 briefs      │ │ ember-market  │ │ 18,000 sims   │        │
│ ● Tester    │ │ avg 21/30     │ │ rev 2 of 3    │ │ 1st pass 40%  │        │
│ ● Critic    │ └───────────────┘ └───────────────┘ └───────────────┘        │
│             │ ┌───────────────┐ ┌───────────────┐                          │
│ Funnel      │ │ REVIEW BOARD  │ │ DIRECTOR'S    │                          │
│ Brief    6  │ │ (critic)      │ │ OFFICE (mgr)  │                          │
│ Design   4  │ │ ● idle        │ │ ● waiting     │                          │
│ Playtest 3  │ │ avg 3.8 / 5   │ │ 1 pitch for   │                          │
│ Critique 2  │ │ 2 kills       │ │ your review   │                          │
│ Pitch    2  │ └───────────────┘ └───────────────┘                          │
├─────────────┴─────────────────────────────┬─────────────────────────────────┤
│ Activity feed                             │ Selected agent / game panel     │
│ 13:02 Playtest  2,000 sims: seat 1 +3pts  │                                 │
│ 13:05 Critic    ember-market REVISE-MINOR │                                 │
├───────────────────────────────────────────┴─────────────────────────────────┤
│ ▸ PITCH READY: Ember Market  ▸ KILLED: Tide Lords (too close to an existing game) │
├─────────────────────────────────────────────────────────────────────────────┤
│ Studio Floor · Pipeline · Quality Lab · Market & Portfolio · Review Queue · Ops │
└─────────────────────────────────────────────────────────────────────────────┘
```

- **Top bar:** five headline KPIs: concepts in development, pitch rate, average critic score at pitch, review queue size, agents active.
- **Room cards (one per agent):** status dot (idle / working / waiting for you / error), current game and step, plus that department's two key numbers:
  - Market Intel: briefs written, average opportunity score
  - Design Studio: current game, revision number out of the 3-loop limit
  - Playtest Lab: games simulated, first-pass rate
  - Review Board: average critic score, kills
  - Director's Office: pitches waiting for you, stuck games
- **Sidebar:** agent list and a mini funnel.
- **Activity feed:** every agent's updates in one stream, filterable by agent or game.
- **Ticker:** milestone events only (pitch ready, game killed, balance problem found, owner decision recorded).
- **Click an agent:** side panel with tabs Now · Reports · Log · Settings (Chat comes later).
- **Click a game anywhere:** opens its game page.

### Pipeline

A board with one column per stage (Brief, Design, Playtest, Critique, Pitch, Your review, Prototyped) and games as cards. Each card shows title, player count, play time, opportunity score, latest verdict and revision count. Beside it, the funnel chart, kill rate by stage, and cycle time per game. Archived and killed games sit in a collapsed column with the reason they died.

### Game page

Everything about one game in one place, the "concept dossier":

- **Header:** title, hook, players, time, complexity, current stage, verdicts so far.
- **Scorecard:** opportunity score, critic's six scores (radar or bar chart), and the design-quality KPIs with pass/fail markers against their targets.
- **Balance charts:** win rate by seat, win rate by bot type, game-length distribution, card/action win correlation.
- **History:** timeline of every stage and revision, with what changed and why.
- **Documents:** brief, rules, playtest report, critique and pitch, rendered in tabs.
- **Your decision:** approve, reject, or send back with notes (stage 3; in v1 this shows the decision recorded in the files).

### Quality Lab

Design-quality trends across all games: first-pass playtest rate over time, average critic scores by revision, seat balance and skill expression for every game in one table, and recurring problem types (e.g. "runaway leader" in 3 of 5 games) so the designer's instructions can be improved.

### Market & Portfolio

Portfolio mix charts (player count, play time, complexity, mechanic, theme), opportunity scores for every brief, comparable titles, and gaps nobody has explored yet. This is where you spot that every game is a 2-player card game and steer the researcher elsewhere.

### Review Queue

Pitches waiting for you, oldest first, each with its scorecard, the one-paragraph "how it plays", component list and estimated prototype cost. Below it, your past decisions and human playtest results, with the agent-vs-human gap.

### Ops

Agent status history, runs and failures per agent, simulated games, and (once runs are automated) usage per pitch.

---

## 3. Minimalist v1 style

- Dark background, flat panels with thin borders; one accent colour per department, used only for borders, status dots and that department's charts.
- Sans-serif for text, monospace for numbers and logs. KPIs are big numbers with a small label and a trend arrow; green/amber/red only when a KPI is compared with its target.
- No images or animation, apart from a soft pulse on a working agent's status dot.
- Desktop first; the Studio Floor should collapse to a single column on a phone.

**v1 is read-only.** It watches the repository's files and updates live. No buttons that run agents. When no game has run yet, it shows clearly labelled sample data.

---

## 4. Data files (written by the agents from the first run)

All dashboard numbers come from these files, so the agents write them from day one, even before the UI exists.

| File | Written by | Contains |
|---|---|---|
| `games/status.json` | Director (manager) | Every game: slug, title, current stage, stage history with timestamps, revision count, verdicts, kill reason |
| `games/<slug>/brief.json` | Market researcher | Target players/time/complexity, mechanics, theme, opportunity score and rubric breakdown, comparable titles |
| `games/<slug>/playtest.json` | Playtester | Verdict, games simulated, seat win rates, bot win rates, game-length stats, lead changes, runaway leader rate, card/action stats, ambiguities, problems |
| `games/<slug>/critique.json` | Critic | Verdict, six scores, biggest strength and weakness, closest existing game |
| `games/<slug>/pitch.json` | Director | Title, hook, specs, component list with counts, estimated prototype cost |
| `games/<slug>/activity.jsonl` | Every agent | One line per event: `{"time", "agent", "game", "event", "message"}` |
| `games/decisions.json` | You (via the dashboard later; by hand or by asking Claude for now) | Your approve / reject / send-back decisions, and prototypes built |
| `games/<slug>/human-playtests.json` | You | Real playtest sessions: date, players, fun, replay, clarity (1-5), notes |

The exact field names are defined in the agent files and `CLAUDE.md`.

---

## 5. Reference UI

Screenshots: `docs/reference/reference-map-view.png` and `docs/reference/reference-room-grid.png` (photos of a monitor, so text is mostly unreadable; these notes describe the structure).

| Area | Reference | Ours |
|---|---|---|
| Top bar | Day clock, speed buttons, revenue / orders / products / agents active | Five think-tank KPIs; no clock or speed buttons until agents run on their own |
| Left sidebar | Agent list with coloured markers and one-line status; click for details | Same, plus a mini funnel |
| Main area | Pixel-art room per department with characters, status bubbles, progress bars and levels | Plain cards per department with status and two KPIs |
| Chat / activity panel | Agents' messages and a message box | Activity feed now; chat in stage 3 |
| Ticker | Recent sales | Milestones: pitches, kills, balance alerts, your decisions |
| Bottom toolbar | Other views, badges, alerts | Pipeline, Quality Lab, Market & Portfolio, Review Queue, Ops |

What we keep from it: one room per agent so you see who is busy or stuck at a glance, click-to-inspect so the main view stays calm, and one shared feed so the team visibly works together.

---

## 6. Build order

1. **Pipeline first.** Run at least one game through all stages so there's real data.
2. **Read-only dashboard (v1).** Agent Network (with Learn mode and replay), Studio Floor, Pipeline, Game page and Review Queue first; Quality Lab, Market & Portfolio and Ops once a few games exist.
3. **Interactive.** Recording your decisions, sending games back with notes, starting agent runs, chat.
4. **Theme.** The themed think-tank look, characters and animation.

## 7. Agents: setup and customisation

Each agent is one file in `.claude/agents/`. The part between the `---` lines is its configuration; the rest is its instructions.

- `name` - the ID the Director uses to call it
- `description` - when the Director should use it; this matters most for correct routing
- `tools` - what it may do. Keep it minimal: the designer doesn't need the web, the researcher doesn't need to run code.
- `model` (optional) - a cheaper model for simple agents, a stronger one for design and critique

To change behaviour, edit the instructions: the researcher's rubric, the designer's principles, the playtester's thresholds and the critic's verdict rules. Studio rules (revision limit, 18/30 cut-off, KPI targets) live in `CLAUDE.md`. When the Quality Lab shows a recurring problem, fix it in the relevant agent's instructions.

Display settings stay separate from behaviour, in `dashboard/agents.json`:

```json
{
  "manager":           { "room": "Director's Office", "color": "#d9d4c7" },
  "market-researcher": { "room": "Market Intel",      "color": "#c9a227" },
  "game-designer":     { "room": "Design Studio",     "color": "#8f6fc4" },
  "playtester":        { "room": "Playtest Lab",      "color": "#d0603f" },
  "critic":            { "room": "Review Board",      "color": "#4a9bb0" }
}
```

Agents to add later, each with its own room: an **artist** (card layouts and print-and-play PDFs), a **rules editor** (rulebooks for new players), a **production planner** (component sourcing and unit cost estimates), and a **trend watcher** (scheduled weekly market check).

## 8. Running agents from the UI

1. **No runner.** You run the agents in Claude Code; the dashboard only watches the files. No extra cost beyond your subscription. Start here.
2. **Buttons that send commands.** A small local server starts Claude Code in non-interactive mode on your computer and the activity log streams progress back. Check Anthropic's current docs on whether this counts against your subscription or needs API billing.
3. **Fully autonomous.** Agents run on a server on a schedule using the Claude Agent SDK and API, billed per use plus a small server. Only worth it once the pipeline reliably produces good games.

Safety rules for every setup: agents never publish, buy or contact anyone; caps on revision loops and runs per day; a spend limit on any API key.

## 9. Suggested tech

- **Front end:** React + Vite, or plain HTML for the very first version.
- **Local server:** small Node or Python server that serves the repository's files (and, from stage 3, starts agent runs).
- **Live updates:** watch the JSON and `activity.jsonl` files and push changes to the browser.
- **Charts:** a standard charting library (funnel, bars, distributions, radar for critic scores).
