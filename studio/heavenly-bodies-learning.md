# Heavenly Bodies project: learning log (v1 and v2)

Every agent call in this project reads this file, `studio/lessons.md`, `studio/design-rules.md`, `studio/mechanics.md` and `studio/checklists.md` first. The Manager appends a short entry after each cycle of either version. Keep it under about 60 lines; merge duplicates.

## Standing method
- **Designer, before each revision:** read the last critique, playtest and this log. Write 3 different candidate fixes for the main problem (at least one bold or unconventional), pick one, and say in `rules.md` changelog why the others lost. State the KPI each change should move.
- **Designer, after each revision:** one line "what I would try next if this works" and one line "what I suspect is still wrong".
- **Cross-pollination:** ideas that worked in one version are offered to the other (for example v2's kinetic card movement may fix v1's thin rotation play; v1's tested balance fixes apply to v2).
- **Playtester, each cycle:** use `tools/sim-kit/`. Add at least one new test it did not run last cycle (new bot style, a stress case, a player count), and note any sim-kit improvement. Test the previous cycle's weakest point first. Stay inside the budget.
- **Critic:** compare against the previous cycle's scores and say which required changes were met.
- **Manager:** after each cycle, record in the table below what moved, and promote durable lessons to `studio/lessons.md`. Say when a lesson comes from simulation only.

## Cycle table
| Version | Cycle | Targeted | Result | Lesson |
|---|---|---|---|---|
| v2 | 1 | win timing, length, churn | critic 3.17 to 3.00 (fell); playtest BROKEN (overshoot): Long Night 0%, but 3-8 turns and first seat wins 62-67%; win-at-end-of-turn was the real fix, shield was the length lever (too strong); no opening bodies is the best next arm | fixing one failure by a bundle overshoots; set the knob with a sweep before the designer commits |
| v1 | 1 | seat gap, path split, rotation cards, Star/HP, CM answers, 40 gaps | critic 2.83 to 3.17; seat gap 7.4 to 0.1; ambiguities 41 to 8; rotation direction still inert | L12, L13; bundled changes needed single-change ablations (worked) |

## Lessons
