# Mechanics reference (designer: read the one section for your game's family; about 50 lines in all)

Built 2026-10-06 from the first 11 games. **Every line is from bot simulation, not human play.** Each entry: what goes wrong | what moved it | KPI to watch. Add to it after a critique when a family teaches something new; keep it short.

**Race to a finite pile (Dead Reckoning, Duel Flip, area control)**
- Goes wrong: the early leader keeps the lead (runaway 0.79 to 0.83, lead changes 1.5). Zoned deals, extra pings and shorter caps changed nothing in Dead Reckoning; a comeback that depends on the score gap was never tried.
- Moved it: Duel Flip's 2x bait hurdle gave a real leave-or-take choice, but runaway stayed 74% over three revisions.
- Watch: runaway leader <= 65%, lead changes >= 2, round-1 leader's win rate, whether strategic games coast to a round cap.

**Auctions and simultaneous bidding (Last Bid Standing)**
- Goes wrong: a side score swamps skill (Hype 55 to 64% of points); a cap that fixes the share can make another lever inert (the crash); skill gap depends on the bot (greedy 15, sampling bot 31).
- Moved it: a per-lot ceiling (Hype 56/64 to 48/48%), passing draws 2, carrying unsold lots, wider bids; shown-income cards added only about 2.5 points.
- Watch: each side-score share, ablations at BOTH player counts, mixed-table skill gap, forced passes.

**Deduction and co-op (Silent Duo)**
- Goes wrong: players can signal by code; the win rate is a guess until a Fog-style knob is swept; Greedy beating Honest may be a bot artefact; legality rules can create forced waiting actions (Trim runs 54%).
- Moved it: requiring offers to be honest signals closed the code attack (+12 to +1); Fog sweep puts 2p in band at F10 and 3p at F8.
- Watch: win rate per player count and per bot, code-attack margin, share of forced actions, 3+ waiting actions in a row.

**Asymmetric roles (Tug of Crowns)**
- Goes wrong: the side gap flips with bot skill (Treasurer 60% vs random, 35% vs greedy), keyword abilities do not change best play, and a dial retuned five times stayed solved.
- Moved it: removing the lead choice fixed pacing (lead changes 1.15 to 2.22, early endings 31 to 18%) but not the twist.
- Watch: side win rate at EVERY bot skill (never the average), ablation per keyword, outlier cards (+20 points).

**Trick-taking and hands (Split the Take)**
- Goes wrong: the strategic bot only ties greedy (42.0 vs 41.8); lead changes depend on a single mechanism (Heat in 74% of rounds).
- Watch: strategic minus greedy gap, reliance of any one mechanism, audience fit (family 2.9).

**Solo and roguelike (Whiskerdark, Fifty-Two Workshop solo)**
- Goes wrong: win rate swings with the solver (19% vs 81%; 99% solo), tricks go dead (Carry 0.7%), Ghost-style persistence is uneven (+0 to +44 points).
- Moved it: lowering Ghost Danger and adding Drift moved the outline bot 19 to 57% but pushed the strong bot to 96%; Hunt-lethal narrowed the bot spread 39 to 21.
- Watch: win rate for TWO solver strengths, spread, trick use when Ready (>= 15%), single-element lift per persistent unit (+5 to +25).

**All families**
- Rules text: every brief promises one page; all 11 games are 100 to 275 lines. Count special rules and cut one per revision.
- Dead cards and ambiguities: 3 to 11 per first draft. The playbook's self-check pass is the fix.
- Re-run ablations after any lever change; do not trust a number a single bot produced.
