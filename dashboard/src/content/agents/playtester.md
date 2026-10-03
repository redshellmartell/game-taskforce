The **Playtester** turns the rules into code, plays thousands of bot games, and reads the statistics. Does the first player win too often? Is any card useless? Does a smart player beat a random one? Then it plays a few narrated games to judge how it *feels*.

- **Reads:** `rules.md`.
- **Writes:** `playtest-report.md`, plus the simulation code in the game's `sim/` folder.
- **Hands off to:** the Review Board, or back to the Design Studio as a "revision" if the numbers show real problems.
- **Tools:** it is the one agent allowed to run code, because the simulation is how it finds balance problems.
