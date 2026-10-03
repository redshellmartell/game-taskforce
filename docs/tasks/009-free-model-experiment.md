---
status: blocked
priority: normal
depends_on: [006, 008]
---
# 009: Experiment: run persona work on free models

## Goal
Find out whether the high-volume, low-stakes AI work (persona reviews, persona conversations and summarising research pages) can run on a free model instead of the Claude subscription, without a noticeable drop in quality. Design, simulation code and critique stay on Claude.

This is an experiment. It ends with a recommendation for the owner, not a switch-over.

## Scope

### 1. Check the owner's Mac (needs Claude Code running on the Mac)
Report the chip (`sysctl -n machdep.cpu.brand_string`), memory (`sysctl -n hw.memsize`) and free disk space. Based on that, recommend which local models are realistic: roughly, 16 GB of memory is enough for small models (7-9B parameters), 32 GB or more for mid-size ones (14-32B). If this task runs in a cloud session, skip local models and test free APIs only, and tell the owner the commands to run on the Mac later.

### 2. A small model switch: `tools/llm/llm.py`
A tiny Python helper that sends a prompt to one of these and returns the text:
- **Claude Haiku** (baseline, via the Claude Code session or API key if one is configured)
- **Ollama** on the owner's Mac (`http://localhost:11434`)
- **One free API tier** (OpenRouter `:free` models or Google AI Studio), using a key from an environment variable, never committed to the repository

Settings live in `tools/llm/config.json`: which provider and model each job uses (`persona_review`, `persona_chat`, `research_summary`).

**Privacy:** unpublished game designs are the owner's ideas. Before sending anything to a free API, read and summarise that provider's data-use terms (whether prompts may be used for training) in `PROGRESS.md`, and only use it if the owner agrees. Local Ollama keeps everything on the Mac.

### 3. Blind comparison on Duel Flip
1. Generate all five persona reviews for Duel Flip with each available provider, using exactly the same inputs as task 006.
2. Have one neutral Claude pass (Sonnet) score every review blind (providers hidden) on: stays in character, grounded in the game data, specific and useful, names a real frustration. Score each 1-5.
3. Repeat with 3 research pages summarised by each provider.
4. Record the time each provider took.

### 4. Report
Write `docs/plan/free-model-experiment.md`: results table, examples of the best and worst output, cost and speed, privacy notes, and a recommendation per job (keep on Haiku, or move to which free option). Add the summary to `PROGRESS.md` and a question for the owner: "Switch persona work to X?"

## Done when
- The comparison has run for at least one free option (local or API) against Haiku.
- The report and recommendation are written.
- No API keys are committed (`git grep` for key patterns finds nothing).
