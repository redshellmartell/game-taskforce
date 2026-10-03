# Decisions

Short log of decisions and why, newest first, so nobody re-argues them.

## 2026-10-03

- **Planning and building are split.** Strategy happens in a claude.ai planning chat; Claude Code builds from task briefs in `docs/tasks/`. The repository is the shared memory. See `WORKFLOW.md`.
- **Dashboard starts minimalist and read-only.** Same layout ideas as the reference UI (rooms per agent, click to inspect, shared feed) without pixel art. It never starts agents. Exception approved by the owner: saving new ideas to `games/_inbox/`.
- **The home screen is an Agent Network diagram with Learn mode.** The owner is new to agents and wants to see how they work together, not just KPIs.
- **The dashboard is framed as a game studio think tank** with KPIs for pipeline health, design quality, market and portfolio, production, owner decisions and team operations (`docs/dashboard-notes.md`).
- **Real-world testing is the final judge.** The owner's human playtest scores are tracked and compared with the critic's, to check whether the agents' sense of "fun" matches reality.
- **Low cost first.** Everything runs inside the Claude subscription; no servers or API billing until the pipeline reliably produces good games.
- **Duel Flip was pushed to pitch after one revision** at the owner's request, as a test of the whole pipeline. The usual "only pitch games that passed playtesting" rule was knowingly waived for it.
