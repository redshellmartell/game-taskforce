# Critique: Silent Duo (rules v1, revision 0)

**Verdict: REVISE-MAJOR.** Average 3.5/5.

Caveats. This is a co-op game, so balance is judged on team win rates and the anti-code design. There is no `panel-report.md`, because AI persona reviews were not approved. Fun and Market fit rest on the free bot-predicted scores in `panel.json`, which are weak evidence. No shell was available, so the activity-log times are estimated, not from `date`.

## Scores

| Area | Score | Note |
|---|---|---|
| Originality | 3 | Skeleton is Hanabi-like (you see your partner's cards, not your own), with Crew-style silence. The double-lamp random-reveal Offer is a genuinely new device. |
| Rules clarity | 3 | Well written and learnable, but 9 listed ambiguities. `rules_simplicity` scores 0.0 for every persona. |
| Fun | 3 | Strong opening and Beacon moments. A third of turns are Trims, and Offer has a negative win correlation (-0.11). |
| Balance | 3 | Skill gap is excellent, but Standard is too easy and the anti-code claim fails at harder settings. |
| Market fit | 4 | Still matches the gap: cards only, tuckbox, 20 minutes, 2-3 players. |
| Production | 5 | 50 cards, 2 reference cards, 3 tokens. Very cheap. |

## Originality
- Closest: Hanabi (medium similarity; the hidden-own-info structure).
- Next: The Crew (silence), Bomb Busters, Sky Team (all already in the brief).
- The random-reveal pair offer is the differentiator, and no direct clone turned up in 2 searches. The core mechanic did not change, so no further re-check is needed on a revision.
- Not a KILL: no rules or text are copied.

## Rules clarity
New players could learn the turn structure from `rules.md`. Required fixes:
- Last Watch count.
- Beacon timing and Fog shortage.
- Deliberate hopeless Lights are legal, which is the miss-code loophole.
- Forced-bad-move Pass, and Offers that tell nothing.
- 3-player resolver role.
- Whether a miss draws.
- Trim with 1 card left.
- Whether the played card stays on a lit ship.
- Trust gap: the owner shuffles both face-down Offer cards and could peek at both. State a physical procedure, for example a face-down cup or card back-to-back.
- The rules call the Silence rule the communication model, yet pre-game discussion of codes is allowed. Decide which.

## Fun
- Opening: Offers on every ship.
- Middle: Trim runs of 3 to 5 turns, where both players wait. This is the pace killer.
- Ending: the Last Watch, a Beacon, a forced miss. Late wins are 74% and near-losses 77%, which is good for tension.
- Panel (bot-predicted): competitor 4.64, strategist 4.46, barraiser 4.42, story 3.68, casual 3.48, family 3.30. The game suits strategists, not families or casual players.
- A "couples and friends" brief with a family fun of 3.3 is a quiet drift.

## Balance and the code concern (Bar Raiser expert-grounds discussion)
- Random wins 0.6% against Honest 73%. Skill expression is excellent.
- Honest at Standard F=8 wins 73% against a 40-60% target (fail). F=12 gives 57.5% for 2 players.
- Greedy (81.6%) beats Honest, so caution is not rewarded.
- Length is 29.6 turns and about 21.9 minutes, inside ±20% (pass).
- Code attack beats Honest by +3.6 at F=8 (pass) and **+12.1 at F=16 (fail)**. F=12 is untested, and that is the setting the fix would adopt.
- The designer's claim that "codes lose to honest play over time" is contradicted by the sim. The core promise of the brief (the anti-code risk) is therefore unproven, and the fix would push the game toward the failing zone.
- Expert-grounds veto discussion: I do not veto, because the gap is bot-only. A human mod-10 Bayesian code is implausible at the table. I would still list it as a Remaining Risk. A human test should check whether pairs of players develop usable conventions. The designer should close the loophole structurally rather than rely on human clumsiness.
- Bots do not do pragmatic inference, so human win rates are likely lower than the 73%. Tune after a human test, not only from bot numbers.
- Seat balance, lead changes and runaway leader are not applicable (co-op).

## Market fit
The brief asked for a card-only 2-3 player limited-communication game, and this delivers one. The concern is audience: complexity 2.5 is stated, but the persona scores suggest a real 3.

## Production
Trivial. About 52 cards and 3 tokens, with no dice or board. The only wrinkle is the secret shuffle of two cards (see the clarity fixes).

## Biggest strength
A new, simple card-only Offer (two cards, chance picks one) that makes signalling cost the cards you need. Skill gap is 72 points, with tension late.

## Biggest weakness
The anti-code design is unproven and demonstrably failing at harder Fog. At the same time, a third of the turns are dull Trims.

## Required changes (REVISE-MAJOR)
1. **Close the code channel.** Show only the row (Low/High) to the owner, or limit offered pairs to adjacent values. Re-test Code attack at F=12 and F=16 (gap ≤ 10 points).
2. **Fix difficulty.** 2-player Standard at F=12 (or an equivalent cut to Beacons), re-check Honest at 40-60%, and aim for no more than 2 Beacons per game (Honest win rate).
3. **Make caution pay.** Two Reefs instead of three, or a miss costs a Fog card, so Greedy no longer beats Honest (Greedy ≤ Honest + 5).
4. **Give Trim an upside.** Draw 2 keep 1, or show the discarded card. Trim share should fall under 25% of turns, with no runs of 3+ (fun, pacing).
5. **Resolve all 9 ambiguities in the rulebook** and add a physical procedure for the secret shuffle (clarity to 4, zero ambiguities).
6. **Drop or redesign the Convention tier** so it adds value, or remove it from the rules notes.
7. Run a human playtest of 2 sessions before committing to the final Fog.

## Is another revision worth it?
Yes. The core loop works, the skill gap is huge, and the problems have named fixes. One revision is a good use of tokens provided the code-channel fix is tested at F=12.
