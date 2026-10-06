# sim-kit: shared simulation helpers for the playtester

Standard library only. Tests: `python3 -m unittest discover tools/sim-kit`. Checked against Duel Flip's real sim: it reproduced that game's runaway leader (0.74), lead changes (2.7), length (22 turns) and bot ranking.

## Use it (about 5 minutes)
1. Copy `tools/sim-kit/template/` to `games/<slug>/sim/` (or edit the existing sim; do not rewrite from scratch on a revision).
2. Replace `game.py` with the rules. Keep one adapter: `play(bots, seed) -> {winner, turns, capped, leaders}`; `winner` is a seat index or None; `leaders` is the leading seat after each turn (`simkit.leaders_from_diff(diffs)` for 2 players). Existing engines need a 5-line wrapper (see "Wrapping an existing sim").
3. Replace `bots.py`: makers are `seed -> bot`. At least **random, greedy, strategic**, plus **one ablated bot per advertised twist** (it ignores exactly one rule).
4. Set `TARGET_MINUTES` and `MINUTES_PER_TURN` in `run.py`, then `python3 run.py 2000 --json ../playtest.json`. It prints a PASS/FAIL table against the CLAUDE.md KPI targets and writes `playtest.json` with the keys the dashboard reads (adds `validation: "bots only, unvalidated"`).

## What it gives you
| Function | Use |
|---|---|
| `run_match(play, makers, n, seed)` | n games with seats rotated every game, so seat order cannot favour a bot |
| `summarize(rows, players)` | seat win rates, seat gap, ties, cap hits, length, lead changes, runaway leader rate |
| `round_robin(play, makers, n)` | each bot's average win rate and the **spread** (best minus worst). Report the spread; never judge from one bot (L2) |
| `ablation(play, full, ablated, n)` | margin in points, 95% interval, `passes` if the ablated bot loses by 5 or more (L1) |
| `wilson(k, n)` | 95% interval. A number within about 2 points of a target needs more games, or is unsettled |
| `evaluate(...)`, `to_playtest_json(...)` | KPI table and the JSON file |

## Wrapping an existing sim
```python
def play(bots, seed):
    r = old_play(cfg, bots, seed)                       # the game's own function
    return dict(winner=r["winner"], turns=r["turns"], capped=r["capped"], leaders=simkit.leaders_from_diff(r["st"].history))
```
Multi-player games: give `leaders` as the seat with the most points after each turn.

## Rules of use
- **Re-run every ablation after any cap, ceiling, legality or tie-break change** (the auction crash went inert after the Hype ceiling; silent-duo Trims became forced).
- Use 2,000 games per pairing; go higher only where a number is within 2 points of a target. Time-box the whole playtest to about 20 minutes.
- Say in the report what simulation cannot test: fun, teaching time, table talk, bluffing, readability. Every verdict is "bots only, unvalidated".
