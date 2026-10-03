# Pitch: Duel Flip (`duelflip`)

> **Feasibility-test pitch.** Per the owner's instruction, this was pushed to pitch after 1 revision loop (rules v2). The latest playtest verdict was NEEDS-FIXES (minor), not a clean pass, which is outside the usual "only pitch games that passed playtesting" rule. The critic's verdict is REVISE-MINOR.

## 1. Title and hook
**Duel Flip.** Two tide-pool scavengers flip cards into one shared, visible river. Push for a bigger haul, but flip a value already in the river and the pile you flipped washes over to your rival.

## 2. Stats
- Players: 2 (optional 3-4 variant, untested)
- Play time: 10-15 minutes
- Age: 8+
- Complexity: 1.5 / 5

## 3. Why it's worth making
Push-your-luck card games are at peak demand (Flip 7, Sea Salt & Paper). Reviewers of Flip 7 complain about no dedicated 2-player mode, heavy luck and take-that swings. Duel Flip is 2-player-first, uses fully public information and has no take-that. Caveat from the brief: gap evidence is thin (Gamefound and Rain City pages were blocked, BGG was not checked), so the market-gap score is a moderate 3/5. Brief score: 26/30.

## 4. How it plays
Players alternate turns flipping cards from a 60-card deck into a shared river. The first flip is a safe scout. A second flip is mandatory, then you choose to keep flipping or bank. Flipping a value already in the river is a clash: you bust and your opponent takes the pile you flipped, unless you spend your single Lifebuoy. When you bank, you take your pile but must leave one of your own cards in the river as bait. The game ends when the deck runs out. Score is card values, plus 8 per species where you hold a strict majority, plus 3 for the second player.

## 5. Playtest highlights
- About 100k bot games on v1 and thousands on v2 across 7 bots.
- v2 fixes that worked: seat 1 wins 50.6-51.9% (v1: second seat won about 57%), dead turns went from 9-12% to 0%, strategic bot averages 23.5 turns with no cap hits.
- Decisions matter: strategic beats random 82-85% and every other bot 58-63%. Bank-early does not dominate (36% vs strategic).
- Biggest fix: making the first flip a safe scout, plus equalising Lifebuoys and giving seat 2 +3 points.

## 6. Remaining risks
- **Inert twists:** "leave your lowest card" is still the dominant bait play, the species bonus decides only about 5% of games, and the Lifebuoy refund fires about 0.56 times per game. As written it plays like a generic shared-row duplicate-bust game and does not feel like the pitch.
- **Originality:** critic scores 2.5/5 and sees it as close to Port Royal. No copied text found, but the originality search was thin.
- **Rules contradiction:** bait wording differs between section 4 ("opponent takes the leftover") and the hook and section 5 ("leaver gets it back"). The 1-card-river banking case is undefined, and there is dead "other leftovers" text.
- **Untested:** the 3-4 player variant. Flag or cut it.
- **Deep pushing is not rewarded:** pusher targets of 4-20 all score 35-40%.
- Suggested untested fixes: bigger bait payoff, species bonus about 12 or by margin, drop or rework the refund (refund at 3 cards needs seat 2 +4).

## 7. Components
- 60 species cards (6 species x values 1-10)
- 2 Lifebuoy tokens
- 1 rules sheet
- Target retail about $10-15

## 8. Suggested next step
Do not prototype v2 as written. First do one short rules pass: fix the bait wording contradiction, add the 1-card-river rule, delete dead text and flag or cut the 3-4 player variant. Then try the bigger bait payoff and species bonus, re-simulate, and only then print a paper prototype (60 index cards plus 2 coins). Rules and sim code are in `games/duelflip/`.
