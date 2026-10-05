# Pitch: Duel Flip (`duelflip`)

## 1. Title and hook
**Duel Flip.** Two tide-pool scavengers flip cards into one shared, visible river. Push for a bigger haul, but flip a value already in the river and the pile you flipped washes over to your rival. When you bank, you must leave a card behind as bait, and your rival can only claim it if their pile is at least twice its value.

## 2. Stats
- Players: 2
- Play time: about 12 minutes
- Age: 8+
- Complexity: 1.5 / 5

## 3. Why it's worth making
Push-your-luck card games are at peak demand (Flip 7, Sea Salt & Paper). Reviewers of Flip 7 complain about no dedicated 2-player mode, heavy luck and take-that swings. Duel Flip is 2-player-first, uses fully public information and has no take-that. It costs almost nothing to prototype (60 index cards and two coins). Brief score 26/30; the market-gap evidence is thin (moderate 3/5). The critic is clear that the base loop is close to Port Royal plus Flip 7, so the pitch does not call the river new.

## 4. How it plays
Players alternate turns flipping cards from a 60-card deck into a shared river. The first flip is a safe scout; a second flip is mandatory; then you choose to keep flipping or bank. Flipping a value already in the river is a clash: you bust and your rival takes the pile you flipped, unless you spend your single Lifebuoy. When you bank you take your pile, but you must leave one of your own cards in the river as bait. Your rival claims the bait only if their pile total at banking is at least twice its value; if they cannot, the bait goes back to you and they leave no new bait. High baits are therefore a real decision. The game ends when the deck runs out. Score is card values, plus 3 for the second player.

## 5. Playtest highlights
- Three revisions. Revision 3: 72,000 bot games across the bot pairings, plus leave-strategy matchups.
- Biggest fix (revision 3): the 2x bait hurdle. Bait claim rates for 8, 9 and 10 baits fell from 99% to 65%, 39% and 17%. "Leave lowest" (44.7%) and "leave highest" (46.5%) both score under 60% against a smart leaver, and a non-lowest card is left in 27.9% of choices.
- Seat gap 2.0 points; strategic beats random by 38 points; about 12 minutes; 2.8 lead changes; no dead cards; no rule ambiguities found.
- Critic: PASS (narrow), average 3.67 (originality 3, clarity 4, fun 3.5, balance 3, market fit 3.5, production 5). Panel predicted fun 3.60; no Bar Raiser veto.

## 6. Remaining risks
- **Runaway leader 74.0%** against a 65% target. It was unchanged over three revisions and is a known, unfixed weakness.
- **Bait payoff is modest** (the leave choice is worth only a few points) and was measured only against a one-step bot, so humans may claim 9-10 baits more often, which would favour leaving the lowest card again.
- **Originality is thin:** the critic scores 3/5, closest game Port Royal (medium similarity); one plain web search found no "leave a bait the rival must double" game, which is a weak signal, not proof. BoardGameGeek was not checked.
- **Family players:** panel fun 3.60 overall but weakest for the Family persona.
- **Untested with humans:** the 2x arithmetic may not be fun or readable, and a trailing player may feel out of the game.
- The 3-4 player variant was removed.

## 7. Components
- 60 species cards (6 species x values 1-10; species are art only)
- 2 Lifebuoy tokens
- 1 rules sheet
- Target retail about $10-15

## 8. Suggested next step for a physical prototype
Print or write 60 index cards (6 species x 1-10) and use two coins as Lifebuoys. Play at least five 2-player games and record each session in `human-playtests.json` (fun, replay, clarity, player type). Watch whether players read the 2x bait rule easily and whether the leader runs away. Rules and sim code are in `games/duelflip/`.
