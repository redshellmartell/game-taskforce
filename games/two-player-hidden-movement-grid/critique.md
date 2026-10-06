# Critique: Dead Reckoning (revision 1, cycle 1; rules v2.1, playtested at v2)

**Verdict: REVISE-MAJOR (recommend park at the review-cap gate)**

Average 3.00 (was 3.33; target 3.5 at pitch). All numbers are bots only, unvalidated. The revision fixed the cooling-read layer, but the failure I flagged as the stop condition got worse: runaway leader is 0.831 (rev 0 was 0.795; target 0.65; my own park line was 0.70). Lead changes are unchanged at 1.50. **The problem is structural.**

## Scores (1-5)
| Area | Score | Note |
|---|---|---|
| Originality | 3 | Core mechanic unchanged, not re-checked. Closest remains Creep in Silent (medium). Creep in Silent was still never compared (designer had no search access), so that check is open. |
| Rules clarity | 3 | The 6 ambiguities are closed in v2.1, which is good. But about 100 lines of teach text, six sub-steps per step, and the Reef bounce conflict is still the likeliest rule to be played wrongly. The one-page promise is unmet (L7). |
| Fun | 2 | The cooling-hand read is a real pleasure (narrated round 3), but the narrated game became two solitaire races, then three rounds of walking home with nothing to decide. 71% of strategic games end on the cap, so most games are decided and then coast. |
| Balance | 2 | Seat 1.8, skill gap 88.7, length 17.1 min (+14%) pass. Runaway 0.831 and lead changes 1.50 fail, and the Sonar is still a dead card. |
| Market fit | 3 | Still a cheap, no-downtime two-player duel. But the brief sold "outguess your rival" and delivers "race to a finite pile". Family fit (2.91 at rev 0) was not addressed. |
| Production | 5 | 25 grid cards, 18 helm cards, 2 tokens, no board; about $15. |

Average: (3+3+2+2+3+5)/6 = 3.00.

## Playbook checks
- **Comeback (L3):** the stated mechanisms were mirrored home waters, trailer-only ping, and the torpedo steal of the highest card. The data shows none working. Runaway rose to 0.831 and is 0.76-0.92 in every bot pairing. The zoned deal is no better than the old one (0.794 vs 0.78). The 3-step ping gives 0.76 and the 8-round cap gives 0.78. The round-1 leader wins only 58.2%, so round 1 is not the cause; the lead sets in the middle of the game, with no catch-up tied to the score gap. This repeats L3 for the third time in this studio.
- **Ablations (L1):** they were run and are informative. Cooling-blind 41.4% passes (reading worth about 17 points, up from about 5; real progress). No-torpedo 29.9% and no-middle-row 29.2% pass. **No-ping 49.4% fails** (52% even with a 3-step ping), so the Sonar is a dead card for the second revision running. The ping is also used by trailers only, and the ping spent correlates -0.17 with winning, so it mostly marks a loss. Repeats L1.
- **Two or more bots (L2):** met. Random, greedy, mid and strategic were used. The spread is real (greedy to mid is the skill step; extra depth adds nothing), and runaway is flat across every pairing, so this is not a bot artefact.
- **Dead cards:** Sonar only.
- **Bundled changes (L10):** v2 changed the deal, the card mix, the ping and the cap together. The playtester's single-change runs did isolate them, and they show those changes did not help runaway.
- **Wording:** the designer's v2.1 pass is clean and added no mechanics.

## Why it is structural
This is a race to take a finite pile of 27 points, with a mid-game leader who simply keeps what they have. The only interaction that moves points is the torpedo (hits link to winning at +0.35), and it needs the subs to meet; but they play a mirrored solitaire race for the first rounds. Three different fixes (zoned deal, ping reach, cap length) each left runaway at 0.76-0.83. The playtester's untried ideas (a two-card steal, a leader-only Mine penalty, a scoring change that keeps moving) are real changes to the scoring model, not tuning. A scoring-model rework would be a new design (for example, points that are re-contested every round), not a revision, and nothing in the data says which would work (L9: structural problems do not move with mechanical fixes).

## Rules clarity: remaining issues
- Phase 1 ping asks the rival to plot first and show two cards; this is a unique, easily forgotten sub-procedure for a card that is a dead rule anyway. Cutting the Sonar would remove it (rules shorter, zero dead cards).
- Reef bounce conflict, torpedoes on 8 neighbours, Harbour immunity, Mine cancellation and ordered steps A-E: too many edge cases for a 10+ family game.
- The Known gaps section is honest and lists the unmet rule-budget and family-fit items (the playbook asks for this).

## Fun
The hand-reading puzzle is a genuine hook and now measurably matters. The no-downtime simultaneous play is good. But a game that is effectively decided by round 6 in 83% of cases, then runs to round 12, is not good, and the casual and family personas will feel it more than the bots do.

## Production
About 45 cards and 2 tokens. Two distinct card backs for Harbours; zone marks on the Sea cards (a corner mark, easy). Sort time about a minute.

## Biggest strength
The cooling row now carries real skill (cooling-blind bot 41.4%, torpedo and middle row clearly valuable), in a very cheap, no-downtime, well-seat-balanced two-player package.

## Biggest weakness
Runaway leader 0.831 with 1.50 lead changes, flat across every bot pairing and untouched by three separate fixes: a structural lack of comeback (repeats L3), plus a Sonar that is still a dead card after a rework (repeats L1).

## Required changes (only if the owner chooses to continue)
These are new design, not tuning, so treat them as a different game variant.
1. **Score-gap catch-up** (runaway 0.83 to 0.65 or below, lead changes to 2 or more): for example the torpedo steals two cards, or the leader's Mine penalty takes the highest card instead of the lowest, or Salvage regrows. Test one change at a time with the playtester's single-change runs (L10).
2. **Cut the Sonar** unless a version beats the no-ping ablation by 5 points (target no-ping at most 45%). Cutting it also removes the ping sub-procedure from the rules.
3. **End decided games early** (71% reach the cap): for instance end when the lead exceeds the remaining Salvage in play. Target length within +-20% of 15 minutes.
4. **Compare with Creep in Silent** in one search before any prototype is shown to others.

## Is another revision worth it?
**No.** My rev-0 stop rule (park if runaway stays above 0.70) is triggered: it rose to 0.831 despite three targeted changes, it is flat across every bot, and the remaining fixes are guesses at a rework of the scoring model rather than a diagnosed tweak. Recommend **park** (keep the cooling-row-plus-torpedo kernel, which tested well, for reuse in another design). Kill is also defensible; I do not recommend a pitch.
