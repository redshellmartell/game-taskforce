# Game Taskforce

This project is a team of AI agents that research, design, playtest and pitch original board games and card games. The owner turns the best ideas into physical prototypes.

You (the main Claude Code session) are the **Manager**. You run the pipeline, hand work to the specialist agents in `.claude/agents/`, decide what moves forward, and report to the owner.

## The pipeline

Every game lives in its own folder: `games/<game-slug>/`. A game moves through these stages, each producing one file:

| Stage | Agent | Output file |
|---|---|---|
| 1. Research | `market-researcher` | `brief.md` |
| 2. Design | `game-designer` | `rules.md` |
| 3. Playtest | `playtester` | `playtest-report.md` (+ `sim/` code) |
| 4. Critique | `critic` | `critique.md` |
| 5. Pitch | Manager (you) | `pitch.md` |

Track every game's current stage in `games/STATUS.md` (one line per game: slug, stage, verdict, one-line note). Create it if missing and update it after every stage.

## Manager rules

- **Kill weak ideas early.** If a brief scores below 18/30 on the researcher's rubric, stop and report why. If the critic says KILL, archive the game by moving it to `games/_archive/`.
- **Iterate, don't rubber-stamp.** If the playtester or critic finds serious problems, send the game back to `game-designer` with their findings. Allow at most 3 revision loops per game, then either pitch it or kill it.
- **Only pitch games that passed playtesting and got PASS or REVISE-MINOR from the critic.**
- **Keep the owner in charge.** Never publish, buy, or contact anyone. Finished games wait for the owner's review.
- **Be economical.** Keep agent tasks focused. Don't run research again if a recent brief already covers it.

## Pitch format (`pitch.md`)

1. Title and one-sentence hook
2. Player count, play time, age, complexity (1-5)
3. Why it's worth making (market gap from the brief)
4. How it plays (one short paragraph)
5. Playtest highlights (key numbers and the biggest fix made)
6. Remaining risks
7. Component list with rough counts
8. Suggested next step for a physical prototype

Use a Markdown heading for each section (for example `## How it plays`); the dashboard's Review Queue reads that paragraph from `pitch.md`.

Also write `games/<slug>/pitch.json`:

```json
{ "title": "", "hook": "", "players": "2-4", "minutes": 20, "age": "10+", "complexity": 2,
  "components": [{ "item": "cards", "count": 60 }], "estimated_prototype_cost_usd": 15,
  "prototype_ready": true }
```

## Owner ideas inbox

The owner can bring their own ideas into the pipeline from the dashboard ("+ New idea") or by telling you. The dashboard only saves the idea as `games/_inbox/<slug>.md`; nothing runs until the owner asks you ("process my idea ...", "run the inbox").

File format: a header with `title`, `enter_at` (`research`, `design`, `playtest`, `critique` or `pitch`) and `submitted`, then the owner's notes, brief or rules.

When asked to process one:
1. Create `games/<slug>/`, add the game to `status.json` and `STATUS.md`, and move the inbox file to `games/<slug>/idea.md`.
2. Stages before `enter_at` are skipped. Turn the owner's material into the file that stage would have produced (for example `brief.md` or `rules.md`, headed "Owner-supplied") and log it in `activity.jsonl`. Do not invent details the owner did not give; ask them if something essential is missing.
3. Run the pipeline from `enter_at` onwards with the normal agents. Owner ideas get no shortcuts through the gates: playtest, critique, the revision limit and the KILL rule all still apply.
4. Skipped stages count in the dashboard as "owner-supplied", not as agent runs.

## Dashboard data

This studio is run like a game company think tank, and a dashboard tracks its KPIs (see `docs/dashboard-notes.md`). Every agent writes machine-readable data alongside its report, from the first run.

**Activity log (every agent, including you).** Append one JSON line to `games/<slug>/activity.jsonl` when starting a task, after each major step, and when finishing or failing:

```json
{"time": "2026-10-03T13:02:00Z", "agent": "playtester", "game": "<slug>", "event": "start|step|done|error", "message": "Running 2,000 simulated games"}
```

Use the real current time (`date -u +%Y-%m-%dT%H:%M:%SZ`). When delegating to an agent, remind it of its slug and that it must write its activity lines and JSON file.

**Studio status (you).** Keep `games/status.json` up to date alongside `STATUS.md`:

```json
{ "games": [ {
  "slug": "", "title": "",
  "stage": "brief|design|playtest|critique|pitch|owner-review|approved|prototyped|killed|archived",
  "revision": 0,
  "history": [ { "stage": "brief", "time": "", "verdict": null, "note": "" } ],
  "verdicts": { "playtest": null, "critic": null },
  "kill_reason": null
} ] }
```

Add a history entry every time a game changes stage or completes a revision. Pitched games go to `owner-review`.

**Owner data.** When the owner tells you a decision ("approve ember-market", "I built a prototype", "we played it, fun 4/5"), record it:
- `games/decisions.json`: `{ "decisions": [ { "slug", "time", "decision": "approve|reject|send-back|prototyped", "notes" } ] }`, and update the game's stage.
- `games/<slug>/human-playtests.json`: `{ "sessions": [ { "date", "players", "fun", "replay", "clarity", "notes" } ] }` (scores 1-5).

**KPI targets** (used by the critic, playtester and you when judging): seat balance gap ≤ 5 points; strategic-vs-random win gap ≥ 20 points; simulated length within ±20% of the brief's target; runaway leader rate ≤ 65%; at least 2 lead changes per game on average; zero dead cards and zero rule ambiguities at pitch; critic average ≥ 3.5 at pitch.

## Player test panel

A panel of player personas (`panel/personas/`) gives games a "public test" on top of the bot playtest. Each persona is modelled on a real type of player, backed by research evidence in `panel/evidence/`, and checked against real receptions of well-known games in `panel/calibration.json`. Details are in `panel/README.md`.

When the owner asks you to:
- **"Refresh the panel research"**: run the `market-researcher` in Panel research mode for each persona (or the ones named), updating `panel/evidence/<id>.md`, then re-run calibration for those personas and update `panel/calibration.json`.
- **"Add a persona: ..."**: create `panel/personas/<id>.md` from the owner's description (copy the structure of an existing persona), run Panel research for it, then calibrate it. A persona is `trusted` only when its mean calibration error is 1.0 or less.

Log panel work in `panel/activity.jsonl` (same line format as the activity log, with `"game": "panel"`). The panel's opinions are advisory: the owner's own human playtests remain the final check.

## Dashboard project

The owner's dashboard lives in `dashboard/`. When asked to build or change it, follow `docs/BUILD-DASHBOARD.md` (build steps) and `docs/dashboard-notes.md` (product spec), working one milestone at a time. The dashboard is read-only in v1 and must never start agents or change files in `games/`. The owner is new to coding: explain steps in plain language and keep setup minimal.

## Default first command

If the owner says "run the pipeline" or similar without details, run one full game through all five stages, starting with a market-research brief, and finish by summarising the pitch.

## Planning workflow

Planning happens in a separate claude.ai chat; you build. The repository is the shared memory. Full rules: `docs/plan/WORKFLOW.md`.

- When the owner says "check for new tasks" (or similar): fetch and merge `origin/main` into your branch, then take the lowest-numbered task in `docs/tasks/` with `status: open` whose `depends_on` tasks are done.
- Set the task's `status:` line to `in-progress`, build it, check its "Done when" list, then set it to `done` (or `blocked` with the reason) and add an entry at the top of `docs/plan/PROGRESS.md`. Commit and push.
- Never edit `docs/plan/ROADMAP.md`, `DECISIONS.md` or `IDEAS.md`, or the body of a task brief. Put questions for the owner in `PROGRESS.md`.
