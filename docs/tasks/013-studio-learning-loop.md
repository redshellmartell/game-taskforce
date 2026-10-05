---
status: draft
priority: high
depends_on: []
---
# 013: Make the studio learn (lessons, playbook, retrospectives, scoreboard)

**Draft written 2026-10-04 at the owner's request. Not `open` yet:** the owner and the planning chat should review it first, and decide where it sits in the order (the owner wants it **before** 011 and 012; renumber or set `depends_on` on those when promoting it to `open`).

## Goal
The point of the studio is to **grow and promote better and better games**, not to churn out games. Today each game is judged and then forgotten, and the same faults recur (see "Evidence"). Build a small learning loop so the **first-pass failure rate falls over time**, and so the owner's real playtests become the ground truth that keeps the bots honest.

**Owner policy (2026-10-05):** many revisions and tests are good, because that is how the studio learns. So the loop runs **automatically up to a cap per game**; at the cap the owner decides, through an action gate, whether to continue or kill. The cap, and how the loop stops early, are Stage 3b below.

**The one number that says it works:** share of games whose first playtest is PASS. Baseline (2026-10-04): **0 of 10** (all 10 first playtests were NEEDS-FIXES; first-pass critic average about 3.2).

## Conditions this must work in (design around them, do not fight them)
- **Usage is limited and billed in cloud credits.** Do free work (scripts, reading JSON) first. One agent call at a time. No new research or web searches. Never fetch boardgamegeek.com, rpggeek.com or videogamegeek.com.
- **Agents have no memory between sessions.** Anything learned must live in short files in the repo, and every agent must be told to read them. Keep them small (lessons at most about 40 lines, playbook at most one page) or they cost usage on every call.
- **The designer, critic and market researcher have no shell.** The Director (main session) writes the files and the activity lines for them.
- **The auto-mode safety classifier has blocked the Director from editing control files and committing** (reasons "Instruction Poisoning", "Self-Modification") until `.claude/settings.json` allow rules were added. Editing `.claude/agents/*.md` and `CLAUDE.md` is the most likely thing to be blocked again. If it is, **stop and tell the owner**; do not work around it. Prefer putting new rules in `studio/*.md` (plain notes the agents are told to read) and keep edits to agent files to one short line each.
- **The bots are weak and unvalidated.** No human playtest exists yet. Every lesson drawn from a simulation must say so. Do not tune a game to a bot (Nine Lives: the same rules gave 19% with one bot and 81% with another).
- **The owner is new to coding.** Plain language. Exact steps. Stop after each stage for review.
- **The owner's Mac follows `main`** and syncs every 20 seconds. Everything here is plain files, so no dashboard code is needed; do not touch `dashboard/`. A "Learning" dashboard page belongs to task 011 (Step B).
- Work on the session's branch, one stage per session if the session is long, and tell the owner when to merge.

## Evidence (verify each from the files; do not trust this list)
Seen across the first 10 games, from `games/*/critique.json`, `playtest.json` and `playtest-report.md`:
1. **Inert twists.** The advertised twist does not change the best play: Duel Flip bait claimed 99% of the time; Dead Reckoning Sonar (never pinging wins exactly 50%); Fifty-Two Workshop engine suits (Hearts win, Spades lose). Needs an *ablation test*: a bot that ignores the twist should lose clearly.
2. **Weak or single reference bots mislead** (Nine Lives 19% vs 81%; Fifty-Two "strategic beats greedy by 3 points").
3. **Early luck and runaway leaders** (Duel Flip 74.8%, Dead Reckoning 0.79, Tug of Crowns lead changes 1.15): designs ship without a comeback mechanism.
4. **Dead cards and rule ambiguities in every first draft** (6 to 11 per game against a target of zero).
5. **Solo and co-op win lines tuned blind** (Fifty-Two solo 98.6%, Silent Duo 73%): no target band or tuning knob checked in design.
6. **Stalls and loops** (Fifty-Two gather/discard loop hit the 600-turn cap) and games shorter or longer than the brief's time.
7. **Low skill gap in luck-heavy designs** (Last Bid Standing: 17.5 points, 0.8 to 2.3 at mixed tables).
8. **Rule weight above the "one page" promise.**
9. **Process:** every revision waits on one owner click, so 10 of 11 games sit at critique.

## Stages (stop after each stage for the owner's review; do not start the next without a go-ahead)

### Stage 0: the scoreboard (free, scripts only)
- `tools/learning/scoreboard.py` reads `games/status.json`, `playtest.json`, `critique.json`, `approvals.json`, `decisions.json`, `human-playtests.json` and `usage/sessions.jsonl` and writes `studio/scoreboard.json` and a one-page `studio/scoreboard.md`.
- Metrics: first-pass playtest PASS rate; critic average at the first critique and at the latest; revisions per game; share of revision requests approved vs the Director's recommendation (Director calibration); owner decisions by kind; usage tokens per game where it can be attributed; human fun/replay/clarity averages (empty for now, shown as "no data").
- Backfill from the existing 11 games. Unit tests with sample files. No dashboard changes.
- **Done when:** running the script prints the baseline (0 of 10 first-pass PASS) and writes both files; `python3 -m unittest` passes.

### Stage 1: lessons (the memory)
- Create `studio/lessons.md` (at most about 40 lines): one entry per lesson: `id`, one-line rule, `evidence` (games and file names), `confidence` (low / medium / high), `from_simulation: yes/no`, `added`.
- Seed it from the Evidence list above, **after verifying each item in the files**; drop any that does not hold; add what you find that is not listed. Mark every simulation-only lesson low or medium confidence.
- Define the append rule for the Director: after each critique, add at most 2 or 3 lessons, or bump the confidence of an existing one; merge duplicates; retire lessons that stopped being true.
- **Done when:** the file exists, every entry cites at least one game and file, and the owner has read it.

### Stage 2: the design playbook (the distilled rules)
- Create `studio/design-rules.md` (one page): a checklist the designer must satisfy before handing over, built only from lessons seen in **three or more games**. Likely candidates: a stated comeback mechanism; an *ablation test* for each advertised twist (name the bot that ignores it and the win rate it must lose to); a termination argument and a turn cap; a target band and a tuning knob for any solo/co-op win rate; a self-check pass for dead cards and ambiguities; a rule-count budget.
- Add a short "bot rules" section for the playtester: at least two reference bots of different strength (for example a greedy and a lookahead bot), report the spread, and never tune a game to a single bot; say plainly what simulation cannot test.
- **Done when:** the file fits on one page, each rule links to its lessons, and the owner has agreed to it.

### Stage 3: wire it in
- Add one line to each of `.claude/agents/game-designer.md`, `playtester.md` and `critic.md`: "Before starting, read `studio/lessons.md` and `studio/design-rules.md`." (Critic: also check the ablation test and the comeback mechanism; designer: run the self-check pass.) **If the safety classifier blocks editing these files, stop and ask the owner.**
- Add to `CLAUDE.md` (Manager rules): after every critique append lessons; pass the playbook to every agent call; run the **fix-before-critic pass** (after the playtest, the designer gets one pass to fix only mechanical problems: dead cards, ambiguities, stalls, wording; never new mechanics) so the critic judges a cleaner draft. Approval gates change only as described in Stage 3b.
- **Done when:** the next game run (owner-approved) shows the agents citing the files, and the fix pass appears in its `activity.jsonl`.

### Stage 3b: the review cap (autonomous loops, then an owner gate)
This replaces the current rule "every revision needs an owner approval" in `CLAUDE.md` (Approval gates) for the **revision gate only**. All other gates stay (`scan`, `panel-research`, `panel-reviews`, `budget`, `deep-research`, `free-api`, `greenlight`).
- **A cycle** = one revision (designer), then playtest, then critique. The first design pass is cycle 0 and does not count.
- **Cap:** `studio-settings.json` gets `"review_cap": { "auto_cycles_per_game": 3, "learning_period_games": 6, "learning_period_cycles": 4 }`. During the learning period (the first 6 games that go through the loop after this task lands) the cap is 4 automatic cycles, afterwards 3. The owner can change the numbers by saying so ("set the review cap to 5"); the Director edits the file.
- **Inside the cap, no click is needed.** The Director runs the next cycle on its own, one agent at a time, and records the cycle in `status.json` history and `activity.jsonl`. Playtester budgets (5 configurations) and the usage guard (`python3 tools/usage/usage.py --check`; exit 2 stops everything) still apply, and a `budget` request is still gated.
- **Stop early, and go to the gate before the cap, when any of these is true:** the critic says PASS (go to pitch) or KILL (go to the gate with kill as the recommendation); the last cycle did not move the key numbers the revision targeted (no progress); the critic calls the problem structural; or the same failure appears two cycles in a row.
- **At the cap (or an early stop) the Director raises one `review-cap` request** in `games/approvals.json`: options `continue` (grants N more cycles, default 2), `pitch` (as is, with risks listed), `park`, `kill`. The request shows the numbers per cycle (a small table of the KPIs before and after each cycle), what each revision changed, and the Director's recommendation. Then the Director stops working on that game.
- **Every cycle must also feed learning:** the Director writes the lesson(s) (Stage 1 rule) and records, per cycle, which KPIs the revision targeted and whether they moved (`studio/scoreboard.md` gains "revision effectiveness": share of cycles that moved their target). This is how the studio learns which kinds of fix work.
- **Order and usage:** run games one at a time, highest opportunity score first. A long run across several games can burn the usage window: check the guard before every agent call and stop cleanly (state is in the files) when it says stop.
- **Dashboard:** until task 011, a `review-cap` request appears on the existing Approvals page like any other (its options come from the request). Make sure the request's `gate` value is one the page accepts, and add it to the gate labels in the dashboard (small change, with a test) if it is not; that is the only dashboard change in this task.
- **Done when:** a test game runs two automatic cycles with no approval requests in between, then stops at the cap with a `review-cap` request, and the owner's `continue` or `kill` click is acted on (and recorded) the same way as any other decision; `docs/plan/PROGRESS.md` and `CLAUDE.md` describe the rule.

### Stage 4: the retrospective routine
- Create `studio/retro-template.md` and the rule: after every **3 games** reach a verdict (or on the owner's request), the Director writes `studio/retros/YYYY-MM-DD.md` (one page): scoreboard now vs last time, what failed and why, proposed lesson and playbook changes, proposed agent-instruction changes, and which of the owner's decisions disagreed with the critic.
- Proposed changes to agent files or the playbook are **applied only after the owner's OK** (record it in `games/decisions.json` or as an approval request), consistent with the studio's gates.
- **Done when:** a first retro exists for the games run so far (use the 11 existing games), and the owner has responded.

### Stage 5: human ground truth (starts when a prototype exists)
- Ask the owner to prototype one game (their choice; the cheapest is the one needing only a standard deck or a few printed cards) and play it, then record each session in `games/<slug>/human-playtests.json` (`fun`, `replay`, `clarity`, `player_type`, notes) as `CLAUDE.md` describes.
- `tools/learning/calibrate_vs_human.py` (free) compares human scores with the panel's predicted fun and the bots' verdict, per game and per persona, and writes the gap to `studio/calibration-vs-human.md`. Until there are at least 3 human sessions it prints "not enough human data" and `studio/scoreboard.md` keeps the banner "bots unvalidated".
- Retro rule: where bots and humans disagree by more than 1.0, retune the bots, panel or critic and log it as a lesson with high confidence.
- **Done when:** the script runs on the sample data, and the owner knows exactly what to record and how.

## Out of scope
- Dashboard code beyond adding the `review-cap` gate label (a Learning page goes into task 011, Step B). Any gate other than `revision`. Market research or panel refreshes.
- Games already in the pipeline keep their pending `-revision-N` requests until the owner says whether to treat them as inside the cap (ask the owner; do not decide).

## Success measures (review at each retro; modest targets)
- First-pass playtest PASS rate: from 0 of 10 to **at least 2 of the next 6 games**.
- Mean critic average at first critique: from about 3.2 to **3.5 or more**.
- Revisions per game fall; Director recommendations match the owner's decisions more often.
- When human data exists: predicted vs human fun within 1.0.

## Notes for the builder
- Start by reading `CLAUDE.md`, `docs/plan/HANDOVER.md`, the 2026-10-04 evening entry in `docs/plan/PROGRESS.md`, and the ten games' `critique.json` and `playtest.json`. Use scripts for numbers; read full reports only for a specific lesson.
- Keep every new file short. A learning file that is too long to read each call defeats its purpose.
- Say plainly in each lesson what the simulation could not test.
- Questions for the owner go in `PROGRESS.md`, not in this brief.
