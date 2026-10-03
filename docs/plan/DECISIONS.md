# Decisions

Short log of decisions and why, newest first, so nobody re-argues them.

## 2026-10-03

- **Lean mode.** The studio runs on the owner's subscription, with no paid extras. Models per agent: designer on Opus (highest-value, low-volume), researcher, playtester and critic on Sonnet, personas on Haiku, and the Director on the session model (Sonnet recommended). The playtester has hard caps (one 2,000-game headline run, at most 5 experiments and 3 debugging attempts per pass, one compact narrated game) and the critic a search budget.
- **Research happens in batches.** A market scan (at most every ~30 days, or when fewer than 3 good ideas are left) fills `research/idea-bank.json` with 8-12 scored ideas; each new game takes a brief from the bank with at most 3 searches. Used and rejected ideas stay in the bank so they're never researched twice.
- **Measure before optimising further.** A usage meter reads Claude Code's session logs and reports usage per agent and per game.
- **Free models are an experiment, not a switch.** Persona work and research summaries will be tested on a local model (Ollama on the owner's Mac) or a free API against Haiku; design, simulation code and critique stay on Claude. Unpublished designs aren't sent to a free API without checking its data-use terms and the owner agreeing.
- **There's no free way to run capable agents continuously.** The studio runs in batches the owner triggers (about one game a week), with all number-crunching in free code.
- **The test panel plays in rotation.** When a game seats fewer players than there are personas, every combination of personas plays, with every persona in every seat equally often, so each persona gives feedback on every game and we see who dominates or enjoys playing with whom. Spare seats in bigger games are filled with standard bots.
- **A test panel of player personas** sits under the Playtest Lab: a strategist, a casual social player, a competitor, a story lover and a family player. Their opinions are grounded in research on what real players of each type say in reviews and forums, and each persona is calibrated against real receptions of well-known games before it's trusted. Real human playtests remain the final check, compared per player type.
- **Panel cost is kept low by doing most of the work in free code.** Each persona has a simulation bot and a scoring formula, so every game gets a free "fun profile" per persona. The AI only writes in-character reviews, only for games that passed the bot playtest (or on request), using the smaller Haiku model. Running everything off the subscription is possible later but costs money or quality.
- **Personas are personified in the dashboard** with their own pages, track record, statistics and a way to talk to them.
- **Each persona is a profile file, not a separate agent.** One `panel-player` agent plays any persona, because Claude Code agents can't start their own sub-agents and this makes adding a persona as simple as writing a file.
- **Planning and building are split.** Strategy happens in a claude.ai planning chat; Claude Code builds from task briefs in `docs/tasks/`. The repository is the shared memory. See `WORKFLOW.md`.
- **Dashboard starts minimalist and read-only.** Same layout ideas as the reference UI (rooms per agent, click to inspect, shared feed) without pixel art. It never starts agents. Exception approved by the owner: saving new ideas to `games/_inbox/`.
- **The home screen is an Agent Network diagram with Learn mode.** The owner is new to agents and wants to see how they work together, not just KPIs.
- **The dashboard is framed as a game studio think tank** with KPIs for pipeline health, design quality, market and portfolio, production, owner decisions and team operations (`docs/dashboard-notes.md`).
- **Real-world testing is the final judge.** The owner's human playtest scores are tracked and compared with the critic's, to check whether the agents' sense of "fun" matches reality.
- **Low cost first.** Everything runs inside the Claude subscription; no servers or API billing until the pipeline reliably produces good games.
- **Duel Flip was pushed to pitch after one revision** at the owner's request, as a test of the whole pipeline. The usual "only pitch games that passed playtesting" rule was knowingly waived for it.
