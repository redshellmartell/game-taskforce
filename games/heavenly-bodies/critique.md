# Heavenly Bodies: Critique (revision 0)

**Verdict: REVISE-MAJOR** (owner-supplied game; Rules v2 is locked, so the studio can only revise the card set. Most of the big findings need owner decisions first.)

Fun and Market fit are judged from `panel.json` (free bot-predicted scores) and the playtest only. There is no `panel-report.md` because the AI persona reviews were not approved. Bot-predicted fun is not human fun, and the bots are variants of one strategic bot, so treat those scores as weak evidence.

## Scores (1-5)

| Area | Score | Why |
|---|---|---|
| Originality | 4 | See below. No close match found. |
| Rules clarity | 2 | Restatement is tidy, but 40 listed gaps mean the game cannot be played or taught from the text alone. |
| Fun | 3 | Strong skill gap and a few real "aha" moments, but dead hands and no answer to a countdown. Unproven with humans. |
| Balance | 2 | Fails seat gap, win-path parity, and Star parity. |
| Market fit | 3 | No researcher brief, so there is no gap to check against. A 2-player-first card duel with a 12-minute game suits a crowded market; free-for-all identity is undermined by the path flip. |
| Production | 3 | 108 cards, all unique text, 12 Stars needing names and art, HP and Critical Mass trackers. Not hard, but a text-heavy unique-card set is costly to proof and print. |
| **Average** | **2.83** | Below the 3.5 pitch KPI. |

## Originality

Searched BoardGameGeek and web sources (2 searches, as the game has no brief or idea-bank comparables). Nearest hits were Orbita (2025, 2p card game where planet markers move on an orbital track), ORBIT (planet-race game with reversible orbits) and Planetarium (1998, marble planets on a board). None combines a per-player rotating four-slot ring, Stability and Size collision resolution, and a dual Star Destruction / Critical Mass win. Closest in feel is a collectible-card-game duel (HP-based Star, creatures with stats, spells) with a rotating-board twist. Similarity: low to medium. No copied rules or text found. The search was shallow; the owner should do a BGG check before any public step.

## Biggest strength

The orbit-as-clock idea is genuinely fresh. Per-player rotation makes "where do I put this" a real puzzle, and skill expression is very high (strategic bot beats random 88.9%, gap 77.7 points). The game also runs cleanly: no ties, no stuck games, no turn-cap hits.

## Biggest weakness

The two win conditions are not co-equal, and which one dominates depends on player count (2p 72/28 Star, 4p 39/61 CM, 6p 25/75). The owner's own stated aim was parity, and the "free-for-all is first-class" claim does not hold. This comes from the locked rules and cannot be fixed by cards alone.

## Problems split by who can fix them

### Owner decisions (locked rules or the Star roster)

1. Seat advantage 7.4 points at 2p (KPI 5). Cause is the playtester's reading of gap G4. Skipping the first player's turn-1 draw gives 50.2%. This is the sole trigger of the Bar Raiser veto, so the veto is an artefact of one interpretation, not a design flaw. It still stands until the owner decides G4.
2. Win-path split flips with player count; 2p and 4p+ cannot both be fixed by one card-count change (tested, see playtest). Needs a rule-level choice.
3. HP outweighs ability: HP 9 Star wins 70.6%, HP 5 Stars 33% to 45%; ST01 beats HP 5 Stars 70% to 82%. In 4.6-own-turn games HP is the whole trade. The roster is the owner's; the studio can only recommend.
4. 40 rule gaps. The playtester coded 41 interpretations. One matters for trust in every number: G29, where the locked rule says LIFO stack but the simulation resolves triggers immediately, so results reflect a different rule. G8, G10 and G27 are flagged as result-moving too.

### Studio-fixable (card set and design)

5. 3-damage hard-cost cards dominate: AE28 winning link +0.42, AE25 +0.26. Costs barely hurt.
6. Thin answers to Critical Mass: about 12 of 60 AEs can knock out or shrink a CO, while 41% of announcements are cancelled. Holding no answer means a lost game (narrated play). Also leaves the Denial/control gap open.
7. Dead early draws: 3.4 of a 7-card hand has no legal play, 3.4% of hands have no CO, and the narrated game had three CO-less turns. Mostly by design but the "zero dead cards" KPI is breached if read literally.
8. Cards the bots never play (13 under 5%, AE55 and AE57 near 0%). Part of this is bot blindness. The headline rotation mechanic may be underused; rotation Collisions are only 0.48 per game against 0.76 from placement. Needs human check.
9. Fun risks in the narrated play: clogged hands (9 cards by turn 4), runaway outcome (63.4% runaway leader, close to the 65% limit). Lead changes 3.1 pass.

## KPI check

| KPI | Result | Status |
|---|---|---|
| Seat gap <= 5 | 7.4 (50.2% if G4 skipped) | FAIL (owner decision) |
| Strategic vs random >= 20 | 77.7 | pass |
| Length within +-20% of target | 12 min vs owner's flexible 10-20; no locked target | not judged |
| Runaway leader <= 65% | 63.4% | pass, narrowly |
| Lead changes >= 2 | 3.1 | pass |
| Dead cards, rule ambiguities zero | 47 AEs dead on turn 1; 40 gaps | FAIL |
| Critic average >= 3.5 | 2.83 | FAIL |

Caution on the numbers: all rest on one family of heuristic bots, 5-6p used only 300 games, and strategic barely beats greedy (53.5%). Directions are credible, exact percentages are not.

## Required changes (studio side, for the revision)

1. Replace or re-cost AE28 and AE25 (for example 2 damage, or a cost that hurts) and re-run. Target: winning link under 0.2, 2p Star share closer to 60%.
2. Add 4 to 6 cheap knockout or Size-reduction AEs in place of weak or dead cards; add at least 1 Denial-themed card. Target: CM cancel share 45-55%, fewer lost-without-an-answer games, CM share at 2p up from 28%.
3. Rebalance weak cards the bots ignore (AE41, AE43, AE45, AE55, AE57, AE60, CO14, CO24) so rotation tricks have easy-to-see payoffs. Target: each played in at least 5% of games.
4. After the owner answers the G-items, re-run with the locked rule readings (especially G29 LIFO and G4). Target: seat gap 5 or less, all KPIs re-measured on the real rules.
5. Replace 2 or 3 always-dead AEs with cards that have a legal play on an empty board. Target: dead cards per 7-card hand under 3.

## Decisions for the owner (rules-level, with my recommendation)

1. **G4, first-turn draw:** rule that the first player skips the turn-1 draw. Recommend yes; it fixes the seat gap at no cost and clears the veto.
2. **Primary mode and win-path parity:** declare 2p the primary mode and tune for it, then add a player-count-scaled Critical Mass threshold for 4+ players. Note the playtester's untested idea looks reversed for 2p: Critical Mass is too rare at 2p (28%), so lower the threshold there, or raise it at 4-6p (for example 17) to cut CM's 61-75% share. Recommend testing the 4-6p raise first.
3. **HP versus ability:** either flatten the curve (for example HP 9 down to 8, HP 5 up to 6) or strengthen ST08, ST10 and ST11. Recommend buffing the abilities first and keeping the HP curve, since the owner chose the curve for pacing.
4. **Mulligan:** allow a free redraw of an opening hand with no CO. Recommend yes; it addresses dead starts without touching the card list.
5. **The 40 gaps:** rule on the 8 that move results and block teaching (G1, G4, G7, G8, G10, G12/G13, G27, G29) and leave the rest as errata. Confirm G29: should the simulation use the LIFO stack the rules lock? Recommend yes.
6. **Zero dead cards KPI:** decide whether a held Augmentation counts as dead. Recommend no (it is by design); the KPI wording should say "unplayable all game".

## Is another revision worth it?

**Yes, conditional on the owner answering decisions 1, 2 and 5 first.** The card-set fixes are cheap, the diagnosis is clear (the same bots already measured each lever), and a revision without those answers would only re-measure a rule set the owner has not settled.
