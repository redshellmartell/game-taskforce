---
status: done
priority: high
depends_on: [005]
---
# 006: Test panel, part 2: personas play and judge games

## Goal
Every game gets feedback from each persona, cheaply. Most of it is free (code bots and maths); the AI only writes the personas' opinions, only for games that passed the bot playtest, and on the small, cheap model.

## Scope
Changes to the playtester, a new panel agent, new shared code in `panel/`, and new pipeline steps in `CLAUDE.md`. Then run it on Duel Flip as the first real test.

### 1. Persona bots (free, every game)

Extend `.claude/agents/playtester.md`: for every game, also write one bot per persona `bot_style` in `games/<slug>/sim/bots.py`, following the persona's "How they play" section. Starting styles:
- `planner` (Strategist) - looks ahead, plays for the long game
- `instinct` (Casual) - plays on gut feel: decent but noisy choices, some randomness
- `optimiser` (Competitor) - searches for and plays the strongest line, probes for exploits
- `flavour` (Story Lover) - prefers moves that feel thematic or dramatic, even if slightly worse
- `cautious` (Family) - simple, safe, sometimes suboptimal moves

`run.py` runs a **panel rotation** and records, per persona bot: win rate, decisions per turn, how often it fell hopelessly behind, and downtime.

#### Panel rotation

Most games seat fewer players than there are personas, so the panel plays in rotation until everyone has played with everyone, in every seat:

1. **Tables:** for a game played at N seats (use the brief's main player count, and also each other supported count if it's up to 5), build every combination of N personas from the trusted panel. With 5 personas: 10 tables at 2 players, 10 at 3, 5 at 4, 1 at 5.
2. **Seats:** at each table, rotate seating so every persona sits in every seat equally often.
3. **Games:** play the same number of games per table and seating (default: 200 per seating), with fixed seeds. Every persona ends up with the same number of games, against every other persona, in every seat.
4. **More seats than personas:** fill the remaining seats with the standard bots (random, greedy, strategic), rotated the same way, and note it.
5. **Matchups:** record results per pairing as well as per persona: each persona's win rate against each other persona, and how the experience changed with the opponent (for example, the Family player falling behind much more often against the Competitor).

Each persona's fun profile (step 2) uses all of its rotation games, and also shows its best and worst table ("most fun with: casual; least fun with: competitor").

For the AI reviews (step 3), save two sample logs per persona from **different** tables: one from the table where it scored highest and one where it scored lowest, so the review can say who it enjoyed playing with and why.

### 2. Fun profile scoring (free, every game): `panel/scoring.py`

A small shared Python module (standard library only) that reads `playtest.json`, the persona-bot results and the persona weights, and computes each persona's predicted ratings:

- `fun` (1-5): weighted metrics from the persona's `weights`, each metric normalised to 0-1
- `replay` (1-5) and `would_buy` (yes, maybe or no, plus a price from `price_tolerance_usd` and the game's `minutes`)
- `pet_peeves_hit`: which of the persona's pet peeves the numbers suggest were triggered

Write the results to `games/<slug>/panel.json`:

```json
{ "revision": 1, "stage": "scores",
  "personas": { "strategist": {
      "fun": 2.6, "replay": 2.2, "would_buy": "no", "price_usd": null,
      "metrics": { "skill_expression": 0.7 }, "pet_peeves_hit": ["luck decides close games"],
      "bot": { "win_rate": 0.41, "fell_behind_rate": 0.12, "games": 4000,
               "seat_win_rates": { "1": 0.43, "2": 0.39 } },
      "best_table": ["strategist", "competitor"], "worst_table": ["strategist", "casual"],
      "review": null } },
  "rotation": { "player_counts": [2], "tables": 10, "seatings_per_table": 2,
                "games_per_seating": 200, "filler_bots": [] },
  "matchups": [ { "a": "strategist", "b": "casual", "games": 400,
                  "a_win_rate": 0.62, "a_fun": 2.3, "b_fun": 3.4, "note": "" } ],
  "summary": { "average_fun": 3.1, "spread": 1.4, "best_fit": "casual", "worst_fit": "strategist" } }
```

Include unit tests for the scoring maths.

### 3. Persona reviews (AI, finalists only)

New agent `.claude/agents/panel-player.md`:
- `model: haiku`, tools: Read, Write, Glob only.
- Input: one persona id and one game slug. It reads the persona profile and evidence, `rules.md`, its own scores in `panel.json`, and two short sample game logs played by its persona bot (the playtester saves these as `games/<slug>/sim/logs/<persona>-1.txt` and `-2.txt`).
- Output: `games/<slug>/panel/<persona>.md`, written in character: first impression, best moment, worst moment, confusing rules, which pet peeves were hit, fun / replay / would-buy with a price, the one change they'd make, and "who I'd recommend this to". It also fills in the `review` field of its entry in `panel.json` with those fields.
- Honesty rules in its instructions: judge independently (don't read other personas' reviews or the designer's notes), use the rating anchors, name at least one real frustration, and explain any rating that differs from the scored prediction by more than 1 point.

### 4. Pipeline changes (`CLAUDE.md`)

- New stage **3b. Test panel** between Playtest and Critique.
- After every playtest: the playtester's persona bots and `panel/scoring.py` run automatically (free).
- Only when the playtest verdict is PASS (or the owner asks): the Director runs `panel-player` once per trusted persona, in parallel, then writes `games/<slug>/panel-report.md`: who the game is for, where the personas agree and disagree, recurring complaints, and suggested changes.
- The critic reads `panel-report.md` and uses it for its Fun and Market fit scores.
- Add a `panel` entry to `status.json` history, and `start` / `done` lines to `activity.jsonl` with `"agent": "panel:<persona>"`.

### 5. Talking to personas

Add to `CLAUDE.md`: when the owner says "Ask <persona> about <game>: <question>", the Director runs `panel-player` for that persona in conversation mode. It answers in character, grounded in its review and the game's data, and appends the question and answer to `games/<slug>/panel/conversations.jsonl` (`{"time", "persona", "question", "answer"}`) so the dashboard can show them. Same for "Ask the panel …" (all trusted personas, one short answer each).

### 6. Human calibration

Add an optional `player_type` field (a persona id) to each session in `human-playtests.json`, and tell the Director to ask the owner for it when recording a real playtest. This lets the dashboard compare each persona's predictions with real players of that type.

### 7. First run: Duel Flip
Run the panel on Duel Flip (bots, scores and all five reviews, regardless of its playtest verdict, as a test) and add the panel report.

## Done when
- Duel Flip's rotation covers all 10 two-player pairings, with each persona in both seats and the same number of games per persona.
- Duel Flip has `panel.json` with all five personas' scores, matchups and reviews, five review files, sample logs from different tables and `panel-report.md`.
- The scoring tests pass.
- The persona reviews read like five different people and each names a real frustration.
- `PROGRESS.md` entry: how the personas rated Duel Flip, whether that matches the critic, and how much of the run used the AI versus free code.
