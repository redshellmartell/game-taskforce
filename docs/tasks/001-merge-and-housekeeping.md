---
status: open
priority: high
depends_on: []
---
# 001: Merge the dashboard branch into main and tidy up

## Goal
Get all the work so far (dashboard milestones 1-2, Duel Flip, the ideas inbox) onto `main`, so `main` is the single up-to-date version of the project and the planning chat and Claude Code see the same thing.

## Scope
- Merge branch `claude/nice-allen-b9i0vi` into `main`.
- Remove committed Python cache files and stop them coming back.
- Don't change any game content, agent instructions or dashboard behaviour.

## Steps
1. Merge `origin/main` into `claude/nice-allen-b9i0vi`. It now contains the new `docs/plan/` and `docs/tasks/` folders and a short "Planning workflow" section at the end of `CLAUDE.md`. If `CLAUDE.md` conflicts, keep both sides (the branch's "Owner ideas inbox" section and main's "Planning workflow" section).
2. Add a root `.gitignore` with `__pycache__/`, `*.pyc`, `node_modules/`, `dist/` and `.DS_Store`, and remove the already-committed `__pycache__` folders from git (`git rm -r --cached`).
3. Run `npm test` in `dashboard/` and make sure it passes.
4. Open a pull request from the branch into `main`, with a plain-language summary, and merge it. The owner has approved this merge.
5. Continue future work from an up-to-date `main`.

## Done when
- `main` on GitHub contains `dashboard/`, `games/duelflip/` and `docs/plan/`.
- No `__pycache__` folders are in the repository.
- `npm test` passes.
- An entry is in `docs/plan/PROGRESS.md`.

## Notes for the builder
If anything in the merge looks risky, stop, set this task to `blocked` and explain in `PROGRESS.md`.
