---
status: open
priority: normal
depends_on: [006]
---
# 012: Handle tabletop role-playing games properly in the pipeline

Queued by the owner for later. The owner's current focus is **card games, card-heavy games with a few small components, and tabletop role-playing games**. The studio is built around simulating card and board games; role-playing games (RPGs) need their own approach. First case: the owner's idea `archetypes` (a questionnaire-driven RPG, `games/archetypes/`).

## Goal
RPG ideas should go through research, design, testing, critique and pitch honestly, instead of being forced through a simulation that cannot judge whether play is fun.

## Scope (propose first, then build with the owner's go-ahead)
1. **A game "kind" in the data:** `kind: card | card-heavy | rpg | other` in `status.json` and `brief.json`, shown in the dashboard (Pipeline cards, game page). Add the owner's focus list as a filter on the idea bank and Market page.
2. **Research and scoring:** the market researcher's rubric weights `simulatability` for card games; for RPGs replace it with a measure that fits (for example "can it be tested with a scripted session or a human table"). Make the idea bank and scans prefer the owner's focus (already noted in `studio-settings.json` and `CLAUDE.md`).
3. **Design output for RPGs:** a structured design (character-creation flow, questionnaire and outcome map, archetype or ability cards, scene and reward rules, GM or GM-less procedure, a one-page quickstart) instead of the card-game `rules.md` sections.
4. **Playtest for RPGs:** what code can test (questionnaire reachability and outcome balance, card/token economy, option and ability balance, pacing tables) plus a **scripted solo session** by an agent playing every seat from a session script, and a **human playtest kit** (a printable session script and feedback form) so the owner's real sessions are the main test. Record the results with `player_type` as for other games.
5. **Critic and panel for RPGs:** an RPG rubric (clarity of the first session, how much the system supports roleplay, GM load, replayability of characters) and a Story-lover-weighted panel view; the Bar Raiser judges originality against known RPGs.
6. **Pitch and prototype for RPGs:** components usually a booklet plus cards; update the pitch format and the prototype next step.

## Done when
- A short design proposal has been reviewed by the owner before any building.
- The Archetypes game can be run through the RPG path end to end, with the limits stated honestly.
- `npm test` and the other test suites pass; `docs/plan/PROGRESS.md` updated.
