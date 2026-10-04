# The player test panel

A small group of **player personas** that give a game a "public test" on top of the bot playtest. Each persona is modelled on a real type of tabletop player:

| Persona | Cares about |
|---|---|
| The Strategist | Deep decisions, planning ahead, skill over luck |
| The Casual Social | Quick to learn, laughs, short games, low downtime |
| The Competitor | The best strategy, exploits, fair and tight endings |
| The Story Lover | Theme, atmosphere, the game telling a story |
| The Family Player | Simple rules, nobody left behind, gentle interaction |

The panel's opinions are **advisory**. Your own playtests with real people stay the final check.

## What is in this folder

| Path | What it is |
|---|---|
| `personas/<id>.md` | One profile per persona: who they are, loves, pet peeves, how they play, patience for rules, rating anchors and voice. The top of the file (between the `---` lines) holds settings the dashboard and scoring code read: colour, initials, how their simulation bot plays, and **weights** (how much each simulation measurement drives their fun; they add up to 1). |
| `evidence/<id>.md` | What real players of that type say, gathered from review sites and communities: recurring themes (with how often and which sources), reactions to ten well-known games, and a "Gaps" section that says what could not be found. Every profile links to its evidence file. |
| `calibration.json` | The trust check: how well each persona's predicted ratings match how that type of player really received well-known games. |
| `calibrate.py` | Recomputes the errors and `trusted` flags in `calibration.json`. |
| `activity.jsonl` | A log of panel work, in the same format as the games' activity logs. |

## How calibration works

Before a persona is trusted, it is checked against reality:

1. Eight well-known games with very different receptions were chosen: Twilight Imperium (4th edition), Gloomhaven, Terraforming Mars, Catan, Codenames, Dixit, Exploding Kittens and Ticket to Ride. The profiles never mention them, so they stay a fair test.
2. The researcher found how each player type really received each game (a 1-5 rating, a reason, and sources). That is the "actual".
3. A fresh agent was shown **only the persona's profile** and asked what the persona would rate each game. That is the "predicted".
4. `calibrate.py` works out the mean difference between the two. A persona is **trusted** when it has at least six rated games and a mean error of **1.0 or less**.

If a persona misses, adjust its profile (loves, peeves or anchors), re-run the predictions and the script. After two tries, leave it untrusted and note why.

**Read the results with care.** The numbers in `calibration.json` come from a first, thin research pass (see `baseline_quality` in that file), so a "trusted" flag is provisional. Refresh the research when you can (see below) before relying on it.

## Common tasks

**Add a persona.** Tell the Director: *"Add a persona: a solo player who mostly plays alone, hates waiting for others, loves puzzles."* It will:
1. Copy the structure of an existing persona into `personas/<new-id>.md`, filling the settings at the top (the weights must add up to 1).
2. Ask the market researcher to gather evidence into `evidence/<new-id>.md`.
3. Calibrate the new persona and record the result.

You can also do step 1 yourself: copy a file in `personas/`, change the settings and text, then ask the Director to research and calibrate it.

**Refresh the research.** Tell the Director: *"Refresh the panel research"* (or name a persona). The market researcher re-gathers the evidence, then calibration is re-run for the affected personas.

**Edit a persona.** Change its profile file. If you change the loves, peeves or anchors, ask the Director to re-run its calibration so the trust flag stays honest. The weights are a starting guess and can be tuned the same way.

## Limits to know about

- This panel was built in a cloud session where **BoardGameGeek, Reddit, Wikipedia, Meeple Mountain and Dice Tower were blocked** (BoardGameGeek stays off limits by the owner's decision: see "Research rules" in `CLAUDE.md`) and web searches were capped at 200 for the whole session. Every evidence file says it rests on search-result summaries, and the calibration baseline is thin. To improve it, allow those sites under the environment's *Network access* settings and raise the web-search limit, then ask for a refresh.
- The personas are language-model roleplay anchored on that evidence. They can be consistent and useful, but they are not real people.

## The Bar Raiser (sixth persona)

`barraiser` is a veteran-designer persona that joins the panel as its hardest judge and the only one that can **veto** a game (a recorded "do not pitch as it stands" the owner must decide on). Its profile sets the veto limits. It starts untrusted: it needs panel research (`panel/evidence/barraiser.md`) and calibration like the others.

## Scoring and rotation (task 006)

After each playtest the game's `sim/panel_run.py` plays every pair of personas' bots in both seats (200 games per seating) and `python3 panel/scoring.py <slug>` turns the results into `games/<slug>/panel.json`: each persona's predicted fun, replay, would-buy (with a price) and pet peeves hit, plus every matchup. This is free (no AI). The AI part, `panel-player` reviews in `games/<slug>/panel/<persona>.md`, sits behind the `panel-reviews` approval gate. Tests: `python3 -m unittest panel/test_scoring.py`.
