# The idea bank

Game ideas are researched in **batches**, because research is the most expensive thing the studio does. One market scan fills this bank with many scored ideas. After that, a new game's brief is written *from the bank* with at most three searches.

- `idea-bank.json`: every idea, with a score out of 30 (the six-part rubric in `.claude/agents/market-researcher.md`), player count, length, mechanics, evidence and sources.
- `market-scan.md`: the latest market scan (trends, saturated areas, gaps). Created by the first scan. Older scans move to `archive/`.

## Statuses

| Status | Meaning |
|---|---|
| `banked` | Scored and available. The Director picks the highest-scoring one, or one you name. |
| `in-pipeline` | A game is being made from it (`game_slug` says which). |
| `used` | The game finished (pitched, approved or prototyped). |
| `rejected` | Not worth pursuing (score under 18, or the game was killed), with a one-line reason in `notes`. |

## When is a new scan needed?

The Director asks for a scan only when the bank has **fewer than 3 banked ideas scoring 18 or more**, or the last scan is **more than 30 days old**. Both are shown on the dashboard's *Market & Portfolio* page. A scan needs your approval first (it is the most search-heavy step).

## Add your own idea

Tell Claude Code: **"Add to the idea bank: <your idea>"**, for example *"Add to the idea bank: a cooperative game about running a small lighthouse, 2-4 players, 30 minutes."* The Director adds it with `source: "owner"`, scores it with the rubric from what is already known, and does not run any research. You can also add one yourself by copying an entry in `idea-bank.json`.

## What was seeded

The first three ideas come from the candidates table in Duel Flip's brief (`games/duelflip/brief.md`): Duel Flip itself (`in-pipeline`) and the two runners-up (`banked`). Their details are `null` where the brief did not record them. No new research was done.
