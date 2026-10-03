# Critique: Split the Take (rules v1, revision 0)

**Verdict: REVISE-MAJOR**

Average 3.0 (KPI at pitch is 3.5 or higher). Originality was judged from the comparables in the brief; no web searches were run, since the core mechanic is well known.

| Area | Score |
|---|---|
| Originality | 3 |
| Rules clarity | 3 |
| Fun | 2 |
| Balance | 2 |
| Market fit | 3 |
| Production | 5 |

## Originality (3)
The exact-count contract is the core of Oh Hell, Wizard and Spades-style exact bidding, and Skull King uses it too. Closest existing game: **Oh Hell / Wizard** (similarity: medium). What is new here is the shared crew contract with a spoiler who profits when it is missed, plus rotating roles built for 3 players. That is a real twist, but the part that makes it work (exactness) is the part that fails in testing. No rules or text have been copied.

## Rules clarity (3)
One page, and the phases are clear. Problems:
- The revoke rule contradicts itself ("0 tricks" vs "tricks as played").
- Heat on a player with no bonus is undefined.
- The direction of the role pass can be read two ways.
- Tiebreaker 1 is unclear when Heat reduced the bonus.
- "No table talk about hands" is hard to enforce between the crew, who are partners and rivals at once.
- Rules simplicity scores 0.41 with the panel personas, and every persona hit a rulebook-weight pet peeve.

## Fun (2)
The playtest notes read as flat. The Double-Crosser cashes top cards for an easy +4, and the Target is "a guess no one can steer". The duck-or-win question that the design notes promise is "rarely live". Tension lasts for two tricks and then goes dead. Panel predicted fun is 3.58 on average. The competitor persona rates it 4.08 and the story persona 3.20, but that comes from bot proxies and does not offset the narrated play.

## Balance (2)
Against the KPI targets:
- **Seat gap:** 4.3 points, passes but borderline.
- **Skill gap:** 53 points, passes. Most of that is greedy play beating random, not the intended strategy.
- **Length:** about 18 minutes, passes.
- **Lead changes:** 1.27, fails (target 2 or more).
- **Runaway leader rate:** 64.4%, borderline.
- **Contract success rate:** 19.7% against an aim of 40-60%, a major failure.
- **Dominant strategy:** greedy trick-grabbing wins 68% against the intended exact-count strategy at 27%.
- **Roles:** Double-Crosser earns 4.8 points per round and Safecracker 2.7.
- **Dead options:** Heat (73% held, about 0.45 points of effect) and No Trump (0% chosen) do almost nothing.

## Market fit (3)
It still matches the brief: exactly 3 players, about 20 minutes, rotating roles, 40 cards. It drifted from the brief in one way. The brief asked for roles that fix the 2-vs-1 gang-up problem, but the crew shares one contract, and it only rarely succeeds. Two of the three roles therefore mostly feel like losing to the third. The family persona's bot wins 55% by playing greedy, which suggests the family audience will not see the contract at all.

## Production (5)
A 40-card standard-size deck and a score pad. About $10-15 as a prototype. Nothing hard to make.

## Biggest strength
The 3-player-only shared-contract structure with rotating roles is a clear and cheap hook. Seat balance is already near target.

## Biggest weakness
The central exact-Target mechanic succeeds only about 1 round in 5. The Double-Crosser's bonus is nearly free, and plain trick-grabbing beats the intended strategy.

## Required changes
1. **Make the Target reachable.** Score the crew bonus on an exact hit and a reduced bonus for +/-1 (for example +3 exact, +1 within one), or cut the Double-Crosser bonus to +2 and raise the crew bonus. Aim: contract success 40-60%, the greedy-vs-strategic gap closed, and Double-Crosser and Safecracker points per round within about 1 point of each other.
2. **Rebalance the roles.** Give the Safecracker a stronger Swap (keep 3, or a loot bonus). Aim: the Safecracker flag (win correlation -0.52) clears.
3. **Make Heat bite or cut it.** Heat of -2 or a loot penalty, or remove it and save a special rule slot. Aim: lead changes of 2 or more, runaway leader rate at or under 65%.
4. **Resolve the No Trump option.** Remove it, or give it a real payoff such as a lower Target requirement. Aim: zero dead options.
5. **Fix the rule ambiguities.** Revoke, Heat on no bonus, pass direction, and tiebreaker 1. Aim: zero ambiguities at pitch.
6. **Re-run a larger seat balance check** (4,000 games or more) after the changes. Aim: gap of 5 points or less.

## Is another revision worth it?
**Yes.** The diagnosis is clear (the exact-hit rate), and the fixes are cheap changes to the scoring rules. The untested fixes (tolerance band, DC bonus 2) have not been simulated, so a first revision round is a reasonable bet. Treat this as one loop only: if the contract rate stays below 35%, kill the game.
