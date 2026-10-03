---
status: open
priority: high
depends_on: [001, 008, 010]
---
# 005: Test panel, part 1: player personas grounded in real reviews

## Goal
Create a "public test group" of player personas, each modelled on a real type of tabletop player. Their opinions must come from what real players of that type say in reviews and forums, not from an AI imagining them, and each persona is checked against how real players rated well-known games before we trust it.

This task builds the personas and their evidence. Task 006 makes them play and judge games; task 007 brings them to life in the dashboard.

## Scope
New `panel/` folder at the repository root, plus an extension of the market researcher's instructions. No game or dashboard changes in this task.

### 1. Persona profiles: `panel/personas/<id>.md`

Start with five:

| id | Name | Archetype | Cares about |
|---|---|---|---|
| `strategist` | The Strategist | Heavy, thinky gamer | Deep decisions, planning ahead, skill over luck |
| `casual` | The Casual Social | Light, social player | Quick to learn, laughs, short games, low downtime |
| `competitor` | The Competitor | Win-focused optimiser | Finding the best strategy, exploits, fair and tight endings |
| `story` | The Story Lover | Thematic player | Theme, atmosphere, the game telling a story |
| `family` | The Family Player | New or occasional player, plays with kids | Simple rules, nobody left hopelessly behind, gentle interaction |

Each file has YAML frontmatter, which the dashboard and scoring code read:

```yaml
---
id: strategist
name: The Strategist
archetype: Heavy, thinky gamer
tagline: "If luck decides it, why are we playing?"
color: "#4a6fa5"
initials: ST
bot_style: planner          # how their simulation bot plays (see task 006)
weights:                    # how much each simulation metric drives their fun (sum to 1)
  skill_expression: 0.35
  decisions_per_turn: 0.25
  lead_changes: 0.10
  length_fit: 0.05
  rules_simplicity: 0.00
  catch_up: 0.05
  interaction: 0.10
  dominant_strategy_absent: 0.10
preferred_minutes: [45, 120]
price_tolerance_usd: [25, 60]
---
```

Followed by these sections, written in plain language:
- **Who they are** - a short character sketch (age range, how often they play, who with, a name if you like)
- **What they love** - with real example games
- **Pet peeves** - specific things that ruin a game for them; these must be checked in every review they write
- **How they play** - their decision style, used for their bot in task 006
- **Patience for rules** - how much rulebook they'll put up with
- **Rating anchors** - what a 5, 3 and 1 out of 5 feel like to them, each with a real game example
- **Voice** - how they talk when giving feedback (a couple of example sentences, in your own words)

The weights are a starting guess; they're tuned by calibration (step 3).

### 2. Research evidence: `panel/evidence/<id>.md`

Extend `.claude/agents/market-researcher.md` with a **Panel research** mode. For each persona, gather evidence of what that type of player actually says, from BoardGameGeek reviews and forums, Reddit (r/boardgames and similar) and review sites:
- What they praise and complain about, as recurring themes, with how often each comes up
- How they reacted to 8-12 well-known games across weights and genres, including the comparables from existing briefs (Flip 7, Port Royal, Sea Salt & Paper, etc.)
- Sources listed for every theme

Write in your own words. No long quotes: at most one short quote (under 15 words) per source. Add a "Last refreshed" date at the top. Each persona profile links to its evidence file, and the evidence should shape the profile's love, peeves and anchors.

### 3. Calibration: `panel/calibration.json`

Check each persona against reality before trusting it:
1. Choose 6-10 well-known games with clearly different receptions (some loved by heavy gamers and disliked by casual players, and the reverse).
2. Record how each player type actually received them (from the evidence), as a 1-5 rating with sources.
3. Have each persona rate the same games from its profile alone, without seeing the real ratings.
4. Store both and compute each persona's average error:

```json
{ "updated": "2026-10-03",
  "personas": { "strategist": {
      "games": [ { "game": "Twilight Imperium", "predicted": 5, "actual": 4.5, "sources": [""] } ],
      "mean_abs_error": 0.6, "trusted": true } } }
```

A persona is `trusted` when its mean error is 1.0 or less. If not, adjust its profile (love, peeves, anchors) and re-run, up to two times; if still not trusted, leave it `false` and say why in `PROGRESS.md`.

### 4. Index and docs
- `panel/README.md`: what the panel is, how to add or edit a persona, how to refresh evidence ("Refresh the panel research"), and how calibration works.
- Add to `CLAUDE.md` that the Director can be asked to "refresh the panel research" or "add a persona: …", which runs the researcher in Panel research mode and re-runs calibration for affected personas.

## Done when
- Five persona files with complete frontmatter and sections, each linked to an evidence file with sources.
- `panel/calibration.json` exists with at least 6 games per persona and a trusted flag for each.
- `panel/README.md` explains how to add a persona in plain language.
- An entry in `docs/plan/PROGRESS.md` with each persona's calibration error and anything that surprised you.

## Notes for the builder
- Copyright: summarise reviews in your own words, never copy them.
- **Budget (lean mode):** at most 10 searches and 10 page reads per persona, reusing sources across personas where one thread covers several player types. Calibration uses the evidence you already gathered, not new searches.
- If BoardGameGeek pages can't be fetched directly, try its public XML API (`boardgamegeek.com/xmlapi2/`) and note what worked in `PROGRESS.md`; thin originality research was a problem in the first run.
