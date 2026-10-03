# Game Taskforce

A team of Claude Code agents that research the tabletop market, design original board and card games, playtest them with simulations, and hand you finished pitches to prototype.

## The team

| Agent | Job |
|---|---|
| Manager (`CLAUDE.md`) | Runs the pipeline, decides what moves forward, reports to you |
| `market-researcher` | Finds market gaps and writes a design brief |
| `game-designer` | Designs the game and writes exact rules |
| `playtester` | Codes the game, runs thousands of bot games, plays narrated games |
| `critic` | Checks originality, clarity, fun and balance; can kill a game |

## How to use it

1. Put these files in a GitHub repository (keep the `.claude/agents/` folder as is).
2. Open the repository in Claude Code.
3. Say: **"Run the pipeline."**

You can also steer it:

- "Research 2-player card games under 20 minutes and pick the best idea."
- "Design a game from the brief in `games/<slug>`."
- "Playtest `games/<slug>` again after the last revision."
- "Show me the status of all games."

Results land in `games/<slug>/`, and `games/STATUS.md` tracks everything. Finished games end with a `pitch.md` for you to review.
