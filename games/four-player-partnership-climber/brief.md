# Brief: Ladder Pairs

- **Working title / slug:** Ladder Pairs / `four-player-partnership-climber`
- **Idea-bank id:** `four-player-partnership-climber` (scan of 2026-10-03; brief written 2026-10-06 from the bank, 2 searches)

## Target
- **Players:** 4 only (partnerships need exactly four)
- **Play time:** about 25 minutes (accepted 20-30), a short match of several hands
- **Audience:** card-game groups who like Tichu, Big Two or trick-takers but want a shorter, lighter game; teens and adults (12+)
- **Complexity:** 2 / 5

## Core mechanics and theme
- A **climbing and shedding** game: on your turn beat the current play with a higher combination of the same type, or pass; empty your hand first.
- **Hidden per-hand partnerships:** teams are not fixed at the table. Each hand, partners are decided by cards dealt, so nobody knows at the start who is on their side. Players infer partners from play, which makes it a read-the-table game.
- Suggested direction for the designer (not mandatory): the holder of a specific card (or a matching pair of "pact" cards) is your partner, as in called-card partnership games such as Sheepshead. Revealing happens automatically when that card is played, never by voluntary announcement.
- Theme: mountain hut relay, climbers handing over the rope. Tone light.

## Market gap (evidence and honesty)
- Partnership card play is strong in 2026 (The Crew, LOTR Fellowship, Gamefound trick-taking bundle; see banked sources). Tichu holds BGG average 7.6, rank about #243 and takes about 60 minutes (search snippet, boardgamematcher.com): proven demand, but long and heavy.
- Haggis was designed to bring Tichu's feel to fewer players (meeplemountain, donteatthemeeples), showing the climbing family is served by a few classics, and almost entirely by older games. I found no recent climbing release with hidden changing partners; this is a gap but a thin one (search snippets only, no sales data).
- Hidden partners themselves are NOT new: called-partner games (Sheepshead, Skat family) use them. The novelty is combining them with a climbing hand in 25 minutes.

## Comparables
1. **Tichu** (BGG average about 7.6, rank about #243; 4 players, about 60 min): fixed partners across the table, card passing, special cards, calls (Tichu / Grand Tichu), and a long scoring game.
2. **Haggis** (rating not found; 2-3 players): Tichu-like feel for fewer players. Shows the market likes this feel in other sizes.
3. **The Crew** (BGG 7.8): partnership-style play with strong demand, but trick-taking co-op, not competitive shedding.

### Tichu similarity and what must differ
Closeness: **medium-high** by family (climb, beat same-type combination, pass, win the trick, empty your hand, team scoring). Rules that MUST differ from Tichu so this is not a clone: (a) no fixed partners, (b) no Tichu / Grand Tichu calls, (c) no Dragon / Phoenix / Dog / Mah Jong specials copied one for one, (d) no card passing at the start, (e) no 1-2 finish scoring copied unchanged, (f) a different, shorter match structure (a few short hands). The one-page rule limit forces most of this anyway.

## Rubric scores (23/30, down from 24)
Demand 3, Gap 3, Originality 3 (honest risk of 2 if the partner rule is only Sheepshead plus Big Two), Producibility 5, Simulatability 4 (down from 5: partner inference needs a belief model in the bot), Owner fit 5. Above the 18 cut-off.

## Constraints for the designer
- **Cards only**, 4 players, about 25 minutes. No board, dice or tokens beyond a pencil tally. Standard deck or at most about 60 cards.
- **Rules fit one page, at most 3 special rules.** Count them and cut one per revision (lesson L7).
- **Comeback mechanism stated in the rules** and tied to the score gap, not to luck (lesson L3): for example the trailing team picks the lead, or a bonus on the final hand.
- **Partner reveal timing** must be deterministic and bot-simulatable: reveal through a defined game event (the pact card is played, or a player empties their hand), never an optional announcement. Players may not communicate except through legal plays; no free-form table talk. Define a "code attack" check: a bot that uses card-play patterns as agreed signals must not beat an honest bot by more than a few points (lesson from Silent Duo).
- **Zero dead cards.** Every card has a use in a combination and a timing role (lesson L1: test each special rule by ablation).
- Avoid rules that block cheating but create forced dead turns (L11); report forced-pass rate.
- Balance must hold across all four seats, and at every partner configuration, including hands where the partner is also the lead player.

## KPI targets (from CLAUDE.md)
Seat balance gap <= 5 points; strategic vs random win gap >= 20 points; simulated length within +/-20% of 25 minutes (20-30); runaway leader <= 65%; at least 2 lead changes per game on average; zero dead cards and zero rule ambiguities at pitch; critic average >= 3.5. Test with at least two bots of different strength (L2): greedy and one with partner inference.

## Main risks
1. **Partner timing:** reveal too early and it is a fixed-partner game; too late and play is noise. Bots cannot model bluffing well, so the reveal must come from events.
2. **Originality:** called-partner and Tichu are both established; the twist (re-chosen hidden partners in a short climbing hand) must change best play, proven by ablation.
3. **Shedding luck and runaway leaders:** the first player out can snowball over several hands (L3).
4. **Skill gap:** pure luck in the deal gives a small strategic-vs-random gap (L6).

## What simulation cannot test
Whether guessing partners is fun or frustrating, table talk and bluffing between humans, real partner-reading skill versus bot inference, atmosphere of the hut-relay theme, and whether teaching it in under five minutes works. Panel numbers are advisory only; human playtests are the final check.

## Sources
- https://boardgamematcher.com/game/tichu
- https://meeplemountain.com/reviews/haggis
- https://donteatthemeeples.substack.com/p/why-haggis-is-the-greatest-modern
- https://www.boardgamequest.com/crowdfunding-campaigns-of-the-week-8-10-26/
- https://boardgamematcher.com/game/skull-king
