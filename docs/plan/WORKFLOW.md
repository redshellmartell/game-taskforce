# How planning and building work together

Two Claude sessions work on this project, and they never talk to each other directly. This repository is their shared memory.

| | Planning chat (claude.ai) | Claude Code |
|---|---|---|
| Role | Strategy, ideas, priorities, specs | Building, running the pipeline, testing |
| Writes | `docs/plan/ROADMAP.md`, `DECISIONS.md`, `IDEAS.md`, `docs/tasks/*.md` | Code, games, `docs/plan/PROGRESS.md`, the `status` line of task files |
| Branch | Commits planning files to `main` | Works on its own branch, merges `main` in before starting a task |

## The loop

1. The owner and the planning chat decide what's next and write a **task brief** in `docs/tasks/`.
2. The owner tells Claude Code: **"Check for new tasks."**
3. Claude Code pulls `main`, picks the lowest-numbered task with `status: open`, sets it to `in-progress`, builds it, checks the "Done when" list, sets it to `done` (or `blocked`) and adds an entry to `PROGRESS.md`.
4. Back in the planning chat, the owner says something like **"Check the repo."** The planning chat reads `PROGRESS.md`, the task statuses and recent commits on all branches, then updates the roadmap with the owner.

## Task brief format

File name: `docs/tasks/NNN-short-name.md` (three-digit number, in the order they should be done).

```markdown
---
status: open            # open | in-progress | done | blocked
priority: high          # high | normal | low
depends_on: []          # task numbers that must be done first
---
# NNN: Title

## Goal
Why this matters, in one or two sentences.

## Scope
What to build or change. What NOT to touch.

## Steps
Numbered steps, or a pointer to an existing spec.

## Done when
- Checkable statements the owner can verify by opening or clicking something.

## Notes for the builder
Anything else: links to specs, decisions, gotchas.
```

## Rules for Claude Code

- Before starting any task: `git fetch origin` and merge `origin/main` into your working branch, so you have the latest plans.
- Only change a task file's `status:` line. If the brief is wrong, unclear or impossible, set `status: blocked` and explain why in `PROGRESS.md` instead of rewriting the brief.
- Never edit `ROADMAP.md`, `DECISIONS.md` or `IDEAS.md`. Put questions for the owner in `PROGRESS.md` under "Questions for the owner".
- One task at a time. Commit and push at the end of each task.

## PROGRESS.md entry format

```markdown
## 2026-10-03 — Task 002: Backfill Duel Flip data — done
- What was built or changed (2-5 bullets, plain language)
- What differs from the brief, and why
- How the owner can see it ("open the dashboard, click …")
- Questions for the owner (if any)
```

Newest entries go at the top.
