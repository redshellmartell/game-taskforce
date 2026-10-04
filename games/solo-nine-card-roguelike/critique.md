# Critique: Nine Lives Dungeon (revision 0)

**Verdict: REVISE-MINOR**

| Area | Score |
|---|---|
| Originality | 3 |
| Rules clarity | 3 |
| Fun | 3 |
| Balance | 3 |
| Market fit | 3 |
| Production | 5 |
| **Average** | **3.33** (pitch bar is 3.5) |

**Biggest strength:** The hook is real. Nine known creatures in an unknown order, with Lighting spreading from cleared rooms, gives deduction, push-your-luck and reveal tension at once. The cost is nine cards and a tuckbox. Skill expression is huge (random 0%, greedy 5%, outline 19%, lookahead 81%), which is what a solo puzzle needs.

**Biggest weakness:** The persistence layer does not work as designed. Death should be the roguelike hook, but Ghost value is wildly uneven: Moth, Mouse and Spider give +0 to +1.4 points, while Owl, Fox and Crow give +38 to +44. Several tricks are also close to dead (Glow 0.5%, Silk 0.3%, Carry untested). So "every card matters every run" fails for about a third of the deck.

## Originality (3)
- 9-Bit Dungeon is a 9-card print-and-play solo roguelike. It shares the nine-card format but uses a different mechanism (rotated and flipped double-sided cards forming levels). Similarity is low to medium.
- Nine Lives: Rogue-and-Write (2020, Joe Hout) is a cat dungeon-crawler with nine lives. The theme and name overlap, but it is a dice roll-and-write. The mechanic is different, but the **title and theme collide**, which is a findability and trademark risk. Rename.
- Rogue Cards, Scoundrel and Card Crawl are 3x3-grid or dungeon-card games. They share the "grid of cards, fight the next one" feel, but none uses a fixed known set with Lit/Dark lighting and Shove-with-Anger.
- I found no copied rules or text. Closest existing game: 9-Bit Dungeon, similarity medium-low. The mechanic is distinct, but the brief's rubric rating of 3 stands.

## Rules clarity (3)
The rules are well structured, with a fixed order of resolution, an action table and edge cases. A new player still faces a lot:
- Four card states (Lit/Dark, Angry/calm), two trophy states (Ready/Spent), three roles for one number, seven different tricks with timing windows, two Room texts, and Ghost overrides. This breaks the brief's "at most 3 special rules" in spirit. The casual persona bot scores rules_simplicity 0.
- Ambiguities that must be closed before a prototype:
  1. "You know where the Hound is" (setup swap) is true only in the swapped case. Say so, or make it universal and re-test.
  2. Ghost "free trophy" in the design notes contradicts the rule that you must spend an action to fight it.
  3. Scavenge on a trick already used this turn.
  4. A Hound lit by a Shove is hunted in the same turn. This is fine but should be stated on the Cat card.
  5. Carry relighting a card is derived rather than stated.
- The strategic bot outline steps 5 and 6 are unclear. That is a simulation spec problem, not a player rule, but it should be fixed.

## Fun (3)
Cannot be judged from simulation. Evidence for: the narrated run had a real "oh no" moment (Spider lights the Crow, Thief takes the Moth), the Hound's Hunt clock is a good pressure source, and the lookahead bot's killer spread (8 cards over 5%) shows varied deaths. Evidence against: the opening is a grind in 36% to 91% of layouts (three Shoves before the first Fight), and the narrator called the early game "pure hidden-card luck". A strong player's session lasts only 2.3 runs with 72% scoring a perfect 9, so there is little ladder to climb. Panel fun is 2.69, but the panel is weak for solo games and is mostly measuring bots, so I weight it low (competitor 3.69, strategist 3.22 and Bar Raiser 3.47 are the only fits that matter; no veto).

## Balance (3): is the bot-strength gap a design problem or a bot problem?
Mostly a **bot problem, with one real design concern**.
- The outline bot is the designer's own sketch, and it loops by shoving into the cell where the known Hound sits. It is a weak solver, not a model of a human. A shove-target fix already moves it. The 19% figure is not evidence that the game is too hard.
- The 40-60% target was written for a "competent player" with no way of measuring one. The true human rate lies somewhere in a 19-81% range, so the sim cannot confirm or deny the target. Do not tune numbers against either bot.
- The real design concern: Claws is a knife edge. 1 gives 1.4% / 6.5%, 3 gives 48% / 98.6%. A game where one integer swings the strong player from 81% to 99%, and where Claws 3 makes even the weak bot reach 48%, has little tuning room, so it needs a softer lever (for example Ghosts and a starting trophy) rather than the headline stat. Keep Claws 2.
- Ghost lift (0 to +44) fails its 5-25 target. This is a clear design defect with a clear diagnosis.
- Dead and near-dead tricks (Moth, Spider, Carry) fail the "no dead cards" KPI. Carry was never tested by a bot that models it, so it is unknown rather than proven dead.
- KPIs that do not apply (seat balance, lead changes, runaway leader) are skipped. Length is fine: lookahead 8.3 min (-17%, in the band).

## Market fit (3)
The game still matches the brief: nine cards, one box, 10 minutes, solo, cosy-dark cat. It has not drifted, and the owner-fit is excellent. The gap stays at 3: the solo card space is crowded, and the "new rules to learn" burden is heavier than Friday or Onirim, which sell on being easy to start. The title clash (Nine Lives: Rogue-and-Write) weakens discoverability.

## Production (5)
10 cards and a tuckbox, a pencil for the tally. About $10 to $15 for a prototype. Sideways cards for Angry and Spent need a flat surface, which is an issue for the commuter audience the brief names (a plane tray or bus seat). That is a note, not a score deduction. Moth through Hound text density is high for a poker card, so check legibility.

## Required changes
1. **Rework Ghosts so every Ghost is worth about +5 to +25** (KPI: Ghost lift in range, balance 3 to 4). Give Moth, Mouse and Spider Ghosts a real effect (for example the Ghost's trophy starts Ready, or the Ghost counts as a free pick-up when it is Lit at setup), and cap Owl, Fox and Crow Ghosts (Ghost Danger 2, not 0). Re-run the single-Ghost lift.
2. **Revive Glow, Silk and Carry** (KPI: each trick used in at least 15% of runs where it is Ready; zero dead cards). Make Glow cheaper, let Silk also cover a Hound shove, and rework Carry. Test with a bot that actually models Carry.
3. **Close all five rule ambiguities** (KPI: zero ambiguities at pitch; clarity 3 to 4). Settle "you know where the Hound is" as universal or as swap-only, and fix the "free trophy" wording.
4. **Trim rules load** (KPI: clarity, and the casual persona's rules_simplicity). Remove or merge at least one rule or state. The candidate is dropping the Crow's Room text (Thief), since Thief is a pure tax and Carry is already dead.
5. **Rename the game** to avoid Nine Lives: Rogue-and-Write (market fit, originality).
6. **Fix the reference bot** (the shove-target loop and the unclear steps 5 and 6) and re-measure the outline bot exhaustively, so the playtester's solver gap becomes a skill ladder rather than an unexplained range (KPI: reference bot win rate in 25 to 60% band, median length at least 7). Do not change Claws.
7. **Soften the opening** with a free Peek or one starting trophy only if human sessions confirm the grind. This is a hedge, not an up-front change.

The playtester is right that human sessions should happen before anything else. Changes 1 to 6 do not wait on them, because each has a clear diagnosis from the data.

## Is another revision worth it?
**Yes.** One targeted revision (Ghosts, dead tricks, ambiguities, rename) has clear diagnoses and cheap tests. It should lift the average from 3.33 to at least 3.5. Do not tune Claws or chase the 40-60% band with bots. After that, human solo sessions decide fun.
