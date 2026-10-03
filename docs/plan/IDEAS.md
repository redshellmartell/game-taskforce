# Ideas parking lot

Ideas that aren't ready to become tasks yet. Discuss in the planning chat; when one is ready, it becomes a task brief.

## Open decisions

- **Duel Flip: revise or archive?** The pitch recommends one short rules pass (fix the bait wording contradiction, add the 1-card-river rule, delete dead text, cut the untested 3-4 player variant), then try a bigger bait payoff and species bonus, re-simulate, and only then print a paper prototype. The alternative is archiving it as a successful pipeline test, since the critic sees it as close to Port Royal.

## Lessons from the first run (possible agent improvements)

- **Thin originality checks.** Both the researcher and the critic couldn't open BoardGameGeek pages, so originality and market-gap evidence was weak. Idea: give them a better way to check BGG (its public XML API, or the browser), and make "searched BGG for the core mechanic" a required step.
- **Twists that do nothing.** Three of Duel Flip's features turned out to be inert in simulation. Idea: the playtester should measure each "twist" from the design notes directly (how often it fires, how often it changes the winner) and flag any below a threshold; the designer should state in advance what each twist is supposed to do.
- **Rules contradictions slipped through.** The bait wording contradicted itself between sections. Idea: a short "rules consistency" check by the designer before handing off, or a dedicated rules editor agent.
- **Messy simulation folders.** The sim folder kept old versions and experiments side by side. Idea: playtester keeps one current `sim/` and moves old versions to `sim/archive/`.

## Future directions

- Second game in a different space (more players, a small board, cooperative, or a party game) to test the pipeline's range.
- Print-and-play PDF generation for pitched games (artist agent).
- Owner's own game ideas via "+ New idea".
