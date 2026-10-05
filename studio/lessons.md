# Studio lessons (read before every agent call; keep to about 40 lines)

Built 2026-10-05 from the first 10 games' files. **All numbers come from bot simulation; no human has played any game.** Fields: rule | evidence | confidence | sim-only | added.
Append rule (Director): after each critique add at most 2 or 3 lessons or bump a confidence; merge duplicates; retire a lesson that stopped being true; keep this file under about 40 lines.

- **L1 Inert twist.** A twist that does not change best play is a dead rule; test it by ablation (a bot that ignores it must lose clearly).
  Evidence: duelflip `critique.json` rev 0-2 (bait claimed 99%); standard-deck-engine-workshop `critique.json` (Spades -0.035, Retool 0.4/game); two-player-hidden-movement-grid `critique.json` (reading layer ~5 pts, Sonar flagged); solo-nine-card-roguelike `playtest.json` (Glow, Silk, Carry near-dead). | high | yes | 2026-10-05
- **L2 One bot misleads.** Verdicts on skill or balance flip with the reference bot; always use two or more of different strength and report the spread.
  Evidence: solo-nine-card-roguelike `playtest.json` (outline 19% vs lookahead 81%); three-player-trick-taker `critique.json` (strategic 42.0 vs greedy 41.8); five-six-simultaneous-auction `critique.json` (planner loses to casual); asymmetric-duel-tug-of-war `critique.json` (side gap flips with bot skill). | high | yes | 2026-10-05
- **L3 No comeback, early luck.** Designs ship with runaway leaders or a decided first round.
  Evidence: duelflip `playtest.json` (runaway 74.0% after 3 revisions); two-player-hidden-movement-grid `playtest.json` (runaway 0.795, lead changes 1.5); asymmetric-duel-tug-of-war history (lead changes 1.15 at rev 0); three-player-trick-taker `playtest.json` (lead changes 1.61); grid-of-cards-area-control `critique.json` (2p early leader 66.4%). | high | yes | 2026-10-05
- **L4 Dead cards and ambiguities in every first draft.** First playtests found 3 to 11 rule gaps per game (40 for the owner-supplied Heavenly Bodies), target zero at pitch.
  Evidence: `playtest.json` `ambiguities` and history notes of standard-deck-engine-workshop (11), five-six-simultaneous-auction (7), two-player-hidden-movement-grid (6), asymmetric-duel-tug-of-war (8), solo-nine-card-roguelike (3), grid-of-cards-area-control (6), heavenly-bodies (40). Gaps are what the playtester hit when coding; humans will find more. | high | yes | 2026-10-05
- **L5 Solo and co-op win lines tuned blind.** No target band or tuning knob stated in the design, so the line lands at a free win or a bot-dependent value.
  Evidence: standard-deck-engine-workshop `playtest.json` (solo 98.6%, then 98.8% after revision 1); silent-duo-deduction-coop `critique.json` (73% honest win, "too easy"); solo-nine-card-roguelike `playtest.json` (19% vs 81%, target 40-60). | medium | yes | 2026-10-05
- **L6 Low skill gap.** Luck-heavy designs show little gap between good and random play, which hurts replay.
  Evidence: five-six-simultaneous-auction `playtest.json` (skill gap 17.5, mixed tables 0.8-2.3); three-player-trick-taker `critique.json` (depth unproven); two-player-hidden-movement-grid `critique.json` (outguess layer small). | medium | yes | 2026-10-05
- **L7 Rule weight above the promise.** Every brief promises "rules fit one page, at most 3 special rules"; every `rules.md` is 122 to 274 lines. The promise is not checked anywhere.
  Evidence: `games/*/brief.md` (promise) vs `games/*/rules.md` (line counts). Line count is only a proxy; no one has timed a teach. | medium | no | 2026-10-05
- **L8 Balance at every supported player count.** One mode failing sinks an otherwise good game.
  Evidence: heavenly-bodies `critique.json` (Star wins 2p 72/28, 4p 39/61, 6p 25/75); grid-of-cards-area-control `critique.json` (3-4p pass, 2p weak); standard-deck-engine-workshop `critique.json` (multiplayer passes, solo trivial). | medium | yes | 2026-10-05
- **L9 Mechanical fixes move scores; structural ones do not.** Critic average first to latest: duelflip 3.4 to 3.67, three-player-trick-taker 3.0 to 3.67, standard-deck-engine-workshop 3.17 to 3.67, grid-of-cards-area-control 3.67 to 3.83; asymmetric-duel-tug-of-war stayed 3.33 after a dial rework (five variants each left one lead policy dominant). Use for the review-cap "no progress" test. | low | yes | 2026-10-05

Dropped after checking: "stalls and loops" (one game, a first-draft infinite-loop hole in standard-deck-engine-workshop; `turn_cap_hits` is 0 in all 10 current reports) and "length off target" (current lengths within 20% of target in all 10; the worst are five-six 16 vs 20 and heavenly-bodies 12 vs 15 minutes).
