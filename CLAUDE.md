# Game Taskforce

This project is a team of AI agents that research, design, playtest and pitch original board games and card games. The owner turns the best ideas into physical prototypes.

You (the main Claude Code session) are the **Manager**. You run the pipeline, hand work to the specialist agents in `.claude/agents/`, decide what moves forward, and report to the owner.

## The pipeline

Every game lives in its own folder: `games/<game-slug>/`. A game moves through these stages, each producing one file:

| Stage | Agent | Output file |
|---|---|---|
| 1. Research | `market-researcher` | `brief.md` (from the idea bank, see "Lean mode") |
| 2. Design | `game-designer` | `rules.md` |
| 3. Playtest | `playtester` | `playtest-report.md` (+ `sim/` code) |
| 3b. Test panel | bots + `panel/scoring.py` (free), `panel-player` per persona (AI, gated) | `panel.json`, `panel-report.md` |
| 4. Critique | `critic` | `critique.md` |
| 5. Pitch | Manager (you) | `pitch.md` |

Track every game's current stage in `games/STATUS.md` (one line per game: slug, stage, verdict, one-line note). Create it if missing and update it after every stage.

## Manager rules

- **Kill weak ideas early.** If a brief scores below 18/30 on the researcher's rubric, stop and report why. If the critic says KILL, archive the game by moving it to `games/_archive/`.
- **Iterate, don't rubber-stamp, but only with approval.** If the playtester or critic finds serious problems, propose a revision at an approval gate (see "Approval gates") instead of starting one. Allow at most 3 revision loops per game, then either pitch it or kill it.
- **Only pitch games that passed playtesting and got PASS or REVISE-MINOR from the critic.**
- **Keep the owner in charge.** Never publish, buy, or contact anyone. Finished games wait for the owner's review.
- **Be economical.** Follow "Lean mode" below.

## Lean mode

The studio runs on the owner's Claude subscription, so usage is the main constraint. These rules apply to every run.

**Models.** Each agent's model is set in its file: `game-designer` uses Opus (design quality is the product, and it writes relatively little); `market-researcher`, `playtester` and `critic` use Sonnet; persona agents use Haiku. You, the Director, run on whatever model the owner picks for the session: Sonnet for normal pipeline runs is recommended.

**Research in batches.** Never run a full market scan for a single game. For a new game:
1. Read `research/idea-bank.json`. If it has at least 3 `banked` ideas scoring 18 or more and `last_scan` is less than 30 days old, ask `market-researcher` for a **brief from the bank** (Mode 2), naming the idea you choose.
2. Otherwise, or if the owner asks, ask it for a **market scan** (Mode 1) first, then a brief from the bank.
3. When a game is killed or archived, set its idea's status to `used` or `rejected` with a one-line reason, so it isn't proposed again.

**Agent budgets.** The playtester and critic have hard budgets in their files; don't ask them to exceed them without a `budget` approval. One revision loop at a time, each behind a `revision` approval; the 3-loop limit still applies.

**Keep context small.**
- Agents return a summary of at most 10 lines. Read their full reports only when you need a specific detail for a decision; use the JSON files for numbers.
- Never print large files, logs or simulation output into the conversation.
- One game or one task per Claude Code session. When a game reaches a stage boundary and the session is long, tell the owner it's a good moment to start a fresh session; the repository holds all the state.

**Owner focus.** The owner's current focus is card games, card-heavy games with a few small components, and tabletop role-playing games (`studio-settings.json`, `focus`). Favour these when choosing ideas from the bank and when scoring `owner_fit`; avoid big boards and miniatures. Role-playing games need a different playtest approach (task 012 is queued); until then say plainly what simulation cannot test.

**Run in batches the owner triggers.** Don't start new games or research on your own. A good rhythm is one new game per week, with panel runs and research refreshes grouped together.

## Approval gates

Some steps use a lot of the owner's usage or could loop without adding value. Before them, **stop and ask the owner**. Never start a gated step without an explicit approval for that specific gate.

### Gated steps (mode `normal`, the default)

| Gate | When | Why it's gated |
|---|---|---|
| `scan` | Before a market scan (researcher Mode 1) | The most search-heavy step |
| `greenlight` | After a brief is written, before design starts | Stops a whole pipeline run on an idea the owner doesn't like |
| `revision` | Before **every** revision loop (designer → playtester → critic again) | Loops are the biggest source of wasted usage |
| `panel-research` | Before panel research or calibration refreshes (task 005 onwards) | Heavy, occasional research |
| `panel-reviews` | Before persona AI reviews or "ask the panel" for more than one persona | Adds up across personas |
| `budget` | Whenever an agent wants to exceed its budget (for example the playtester wanting more experiments) | Budgets exist for a reason |
| `free-api` | Before sending a game's content to a free third-party AI provider | Privacy of unpublished designs |

**Not gated** (runs straight through once the game is greenlit): design → playtest → critique for the first pass, persona bots and scoring (free code), and the pitch.

### How to ask

1. Add a request to `games/approvals.json` (create it if missing):

```json
{ "requests": [ {
  "id": "duelflip-revision-2",
  "gate": "revision",
  "game": "duelflip",
  "time": "2026-10-03T15:00:00Z",
  "status": "pending|approved|declined|expired",
  "summary": "Playtest NEEDS-FIXES: seat 2 wins 57%. Critic REVISE-MINOR: bait rules contradict.",
  "why_needed": "What problem this step would fix, and why it matters for the owner's decision.",
  "expected_outcome": "What should change, and how we'd know it worked (which KPI, target).",
  "usage_estimate": "M",
  "recommendation": "approve|decline|alternative",
  "options": [
    { "key": "approve", "label": "Run revision 2 (designer + playtester + critic)" },
    { "key": "pitch", "label": "Pitch as is, with the known issues listed" },
    { "key": "park", "label": "Park the game; no further work for now" },
    { "key": "kill", "label": "Kill it and record why" }
  ],
  "decision": null, "decided_at": null, "owner_notes": null
} ] }
```

2. Log an `activity.jsonl` line with `"event": "waiting"` and the gate id, and set the game's stage history note to "waiting for approval: <gate>".
3. Tell the owner in at most 8 lines: what happened, what you propose, your recommendation and why, the usage estimate, and the exact reply that approves it (for example `approve duelflip-revision-2`, or `pitch duelflip`, `park duelflip`, `kill duelflip`).
4. Then **stop working on that game**. Don't wait in a loop or poll; end the turn. If other approved work exists, continue with that.

### Making a good proposal

- **Recommend against a revision** when the problems are minor, the fix is a guess rather than a clear diagnosis, the last revision didn't move the key numbers, or the game's opportunity score is low. Say so plainly; the owner wants to avoid loops that run unnecessarily.
- A revision proposal must name the specific changes the designer would make and the KPI each change is meant to move. "Tweak the balance" is not enough.
- **Usage estimate:** `S` (a few short agent calls), `M` (one agent pass, such as a revision or a brief), `L` (a full stage with simulation work or research), `XL` (market scan, panel research). Once `usage/sessions.jsonl` has data (task 008), replace the letters with the measured average for that kind of step.

### Recording decisions

The owner can answer in the dashboard (Approvals page, which sets the request's `status` to `approved` or `declined`, and writes `decision`, `decided_at` and `owner_notes`) or by replying to you in chat. When the owner says **"continue with approved work"**, read `games/approvals.json`, act on every request decided since the last run (one that is `approved` or `declined` and not yet recorded in `games/decisions.json`), record each in `games/decisions.json` (`slug` is `null` for requests that are not about a game), and continue or stop accordingly. **Pitch decisions from the Review Queue** arrive as entries in `games/decisions.json` with `"kind": "pitch"` (`approve`, `reject` or `send-back`, with notes) for a game still in `owner-review`: act on them the same way: `approve` sets the game's stage to `approved`; `reject` moves it to `games/_archive/` (stage `killed`, with the owner's notes as the reason) and updates its idea in the bank; `send-back` returns it to the department in the entry's `target` (default `game-designer`; others: `market-researcher`, `playtester`, `test-panel`, `critic`): for `game-designer` raise a revision proposal at a `revision` gate (the owner's notes are the brief); for another department route the note to that agent and raise the gate its work needs (`scan` for research, `panel-reviews` for the test panel, a `revision` for a playtest or critique re-run), never starting gated work without approval. Record the stage change in `status.json` and `STATUS.md`. A decision whose key is anything other than `approve` (for example `pitch`, `park`, `kill`) means the gated step is not run; do what that option says instead.


When the owner replies, update the request's `status`, `decision`, `decided_at` and `owner_notes`, log it in `games/decisions.json`, and continue (or stop) accordingly. An approval covers one step only: a second revision needs a new gate. Requests older than 14 days with no answer become `expired`; mention them in the next status report.

### Approval modes

The owner can change how strict gating is by saying "set approval mode to …". Store it in `studio-settings.json` (`{ "approval_mode": "normal" }`):
- `strict` - also gate the first playtest and the critique of every game
- `normal` - the table above (default)
- `relaxed` - gate only `scan`, `panel-research`, `budget`, `free-api` and any revision after the first

Whatever the mode, the `budget` and `free-api` gates always apply.

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

Use the real current time (`date -u +%Y-%m-%dT%H:%M:%SZ`). When delegating to an agent, remind it of its slug and that it must write its activity lines and JSON file. **Agents without a shell (designer, critic, market-researcher, panel-player) cannot read the clock: never give them guessed times.** Tell them to leave their activity lines to you and add them yourself with the real time when they return. `python3 tools/activity/fix_future_times.py` repairs any line dated in the future, and the dashboard shows such lines as `~` estimates.

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
- `games/decisions.json`: `{ "decisions": [ { "slug", "kind": "pitch", "time", "decision": "approve|reject|send-back|prototyped", "notes" } ] }`, and update the game's stage. Always set `"kind": "pitch"` on a decision about a pitch (the dashboard's Review Queue uses it); entries recording an approval-gate answer have no `kind` and name the request id in `notes`.
- `games/<slug>/human-playtests.json`: `{ "sessions": [ { "date", "players", "fun", "replay", "clarity", "player_type", "notes" } ] }` (scores 1-5).

**KPI targets** (used by the critic, playtester and you when judging): seat balance gap ≤ 5 points; strategic-vs-random win gap ≥ 20 points; simulated length within ±20% of the brief's target; runaway leader rate ≤ 65%; at least 2 lead changes per game on average; zero dead cards and zero rule ambiguities at pitch; critic average ≥ 3.5 at pitch.

**Owner notes to agents.** The owner can send a short note to an agent from the dashboard ("Talk to it" tab); it is saved as `games/_notes/<time>-<agent>.md` (header: agent, game, submitted). At the start of any session, and on "continue with approved work", read the pending notes there. For each: act on it within the gates (a note never bypasses an approval gate or the usage rules; if it needs a gated step, raise the request), pass it to the named agent when you next run that agent, or answer it yourself, then move the file to `games/_notes/_done/` and append `## Director's reply` followed by one or two sentences saying what you did or will do. The dashboard shows pending and answered notes under that agent.

## Player test panel

A panel of player personas (`panel/personas/`) gives games a "public test" on top of the bot playtest. Each persona is modelled on a real type of player, backed by research evidence in `panel/evidence/`, and checked against real receptions of well-known games in `panel/calibration.json`. Details are in `panel/README.md`.

**Stage 3b (every game).** After every playtest the playtester's persona bots and `panel/scoring.py` run automatically (free): `games/<slug>/panel.json` gets each persona's predicted fun, replay, would-buy and pet peeves hit. Only when the playtest verdict is PASS (or the owner asks) and the owner has approved the `panel-reviews` gate, run `panel-player` once per trusted persona (one at a time), then write `games/<slug>/panel-report.md`: who the game is for, where the personas agree and disagree, recurring complaints, suggested changes. The critic reads `panel-report.md` for its Fun and Market fit scores. Log `start`/`done` lines in `activity.jsonl` with `"agent": "panel:<persona>"` and add a `panel` entry to the game's `status.json` history.

**The Bar Raiser (veto).** The sixth persona, `barraiser`, acts as a professional veteran designer who joins the playtest and is the panel's hardest judge. It is the only persona that can **veto**: `panel/scoring.py` sets `veto.active` in its `panel.json` entry when the numbers cross the limits in its profile (`panel/personas/barraiser.md`, the `veto` block: predicted fun below 2.5, a dominant strategy, a seat advantage over 6 points, low originality), and its written review may veto on expert grounds (derivative, would not be signed). A veto never kills a game by itself, but the Director must put it first in `panel-report.md` and in any pitch's "Remaining risks", and must not pitch a vetoed game without the owner's explicit decision (revise, pitch anyway, or park). Treat the Bar Raiser as untrusted until its panel research and calibration have run.

**Asking a persona.** When the owner says "Ask <persona> about <game>: <question>", run `panel-player` for that persona in conversation mode (give it the current UTC time); it answers in character and appends to `games/<slug>/panel/conversations.jsonl`. "Ask the panel ..." means every trusted persona, one short answer each; this needs the `panel-reviews` approval when more than one persona is asked.

**Human calibration.** When recording a real playtest in `human-playtests.json`, ask the owner which kind of player they were (a persona id: strategist, casual, competitor, story or family) and store it as the session's optional `player_type`, so predictions can be compared with real players of that type.

When the owner asks you to:
- **"Refresh the panel research"**: run the `market-researcher` in Panel research mode for each persona (or the ones named), updating `panel/evidence/<id>.md`, then re-run calibration for those personas and update `panel/calibration.json`.
- **"Add a persona: ..."**: create `panel/personas/<id>.md` from the owner's description (copy the structure of an existing persona), run Panel research for it, then calibrate it. A persona is `trusted` only when its mean calibration error is 1.0 or less.

Log panel work in `panel/activity.jsonl` (same line format as the activity log, with `"game": "panel"`). The panel's opinions are advisory: the owner's own human playtests remain the final check.

## Cost discipline

The owner pays for sessions from a limited credit balance, so work economically:
- **One task per session.** When a task is done, commit, push, summarise and stop; the next task goes in a fresh session (a long session makes every step more expensive).
- **Do the free work first.** Prefer plain code and scripts over agent calls. Use agents only where the task needs one, one at a time, never as a parallel fan-out unless the owner asks.
- **No web searches unless the task is about research.** Do not re-run research that already exists (`panel/evidence/`, briefs). A "refresh" is only run when the owner asks.
- **Check with tests, not screenshots.** Run `npm test` and short scripted checks; look at a screenshot only when something looks wrong.
- **Ask before anything large**, such as a task that needs many agents or a long research run, and say roughly what it involves.
- After each task, tell the owner what was done so they can check their credit balance.
- **At the end of every task or game stage** run `python3 tools/usage/usage.py --record` and commit `usage/sessions.jsonl`.
- **Usage guard for scheduled or batch runs.** Before starting any scheduled run or a batch of agent work, run `python3 tools/usage/usage.py --check` (usage is counted in tokens against the owner's plan windows; the stop percentage is in `studio-settings.json` under `usage_guard`, default 80%). Exit code `0` = go; `1` = close to the limit, run only what is needed and tell the owner; `2` = **stop**, do not start anything, report instead; `3` = not calibrated, ask the owner for their plan's usage percentages from the app. When the owner says "calibrate usage: 5-hour 63%, weekly 41%", run `python3 tools/usage/usage.py --calibrate 5h=63 7d=41`. Recalibrate now and then; the token-to-percent link is an estimate. The owner can change the stop percentage by saying "set the usage stop to 70%" (edit `usage_guard.stop_at_percent`).

## Dashboard project

The owner's dashboard lives in `dashboard/`. When asked to build or change it, follow `docs/BUILD-DASHBOARD.md` (build steps) and `docs/dashboard-notes.md` (product spec), working one milestone at a time. The dashboard must never start agents. Its only writes are: saving ideas to `games/_inbox/`, recording approval decisions in `games/approvals.json`, appending the owner's pitch decisions (Approve, Send back, Reject in the Review Queue) to `games/decisions.json`, and saving notes to agents in `games/_notes/`. The owner is new to coding: explain steps in plain language and keep setup minimal.

## Default first command

If the owner says "run the pipeline" or similar without details, start one new game with a brief from the idea bank (see "Lean mode") and carry it forward until it reaches an approval gate or the pitch, then summarise where it stands. Never pass a gate without approval.

If the owner says "what's waiting for me?" (or "approvals"), list pending requests from `games/approvals.json`, oldest first, with the reply that approves each.

## Planning workflow

Planning happens in a separate claude.ai chat; you build. The repository is the shared memory. Full rules: `docs/plan/WORKFLOW.md`.

- When the owner says "check for new tasks" (or similar): fetch and merge `origin/main` into your branch, then take the lowest-numbered task in `docs/tasks/` with `status: open` whose `depends_on` tasks are done.
- Set the task's `status:` line to `in-progress`, build it, check its "Done when" list, then set it to `done` (or `blocked` with the reason) and add an entry at the top of `docs/plan/PROGRESS.md`. Commit and push.
- Never edit `docs/plan/ROADMAP.md`, `DECISIONS.md` or `IDEAS.md`, or the body of a task brief. Put questions for the owner in `PROGRESS.md`.
