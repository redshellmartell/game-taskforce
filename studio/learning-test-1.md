# Learning test 1: does the first new game do better than the first ten?

Written 2026-10-06. Bots only, unvalidated; a single game is an anecdote, so the real answer needs 3 to 6 games.

**Game:** `four-player-partnership-climber` (Ladder Pairs), idea-bank score 24/30. Why this one: cards only, fits the owner's focus, and a new family for us (climbing and shedding with secret partners), so no game of ours has already taught the agents its traps. Simulation fits (clear skill, many bot styles). Alternatives if the owner prefers: Spy and Warden (2p deduction duel, but close to Silent Duo and the grid game), Haggle Duel and Cartographer's Memory (hard to judge with bots).

**Pipeline (gates stay the owner's):**
1. Brief from the bank (researcher Mode 2; no scan needed: the bank has 27 ideas, last scan 2026-10-03). Then the **greenlight gate**: wait for the owner's click.
2. Design (designer reads `studio/mechanics.md`, ends `rules.md` with the Playbook check block).
3. Playtest (kit from `tools/sim-kit`, 20-minute time box, ablations per twist).
4. Fix-before-critic pass, then critique. The review cap (4 automatic cycles in the learning period) applies after that.

**What we compare (first ten games, baseline in `studio/scoreboard.md`):**
| Measure | First ten games | A good sign for this game |
|---|---|---|
| First playtest verdict | 0 of 10 PASS | PASS, or only 1 to 2 KPIs failing |
| First critic average | 3.26 | 3.5 or more |
| Rule gaps (ambiguities) in the first draft | 3 to 11 | 2 or fewer |
| Dead cards in the first draft | several | 0 |
| Twists failing their ablation | most games | none |
| Playtest wall-clock time | 23 to 62 minutes | about 20 minutes |
| Checklist followed | not applicable | Playbook check block present; kit used; mechanics section named |

**How we'll judge it:** run `python3 tools/learning/scoreboard.py` after the first critique; write the comparison in the retro. If the agents ignore the files (no Playbook check block, kit unused), the fix is the agent instructions, not the game. Record every lesson from this game as usual.

**Cost and timing:** brief about M, design M, playtest L, critic S. Do not start while the usage guard reads STOP; at the time of writing the 5-hour window was at 78%, so wait for it to reset.
