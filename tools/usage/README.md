# Usage meter and guard

Counts what the studio uses, in **tokens**, and can stop scheduled work before your plan's limit.

```
python3 tools/usage/usage.py                          # usage by agent, model and game
python3 tools/usage/usage.py --record                 # save a summary to usage/sessions.jsonl (run at the end of each task)
python3 tools/usage/usage.py --check                  # the guard: exit 0 go, 1 warn, 2 STOP, 3 not calibrated
python3 tools/usage/usage.py --calibrate 5h=63 7d=41  # tell it your plan usage % from the Claude app
python3 tools/usage/usage.py --cost                   # also show an API-equivalent dollar estimate (optional)
```

**Usage tokens** = input + output + cache writes + cache reads at 0.1 weight. The stop and warn percentages and the weight live in `studio-settings.json` under `usage_guard` (defaults: stop at 80%, warn at 60%).

**How the percentage works.** Claude Code's logs do not include your plan's usage percentage, so you give it a reading: open the Claude app, read the 5-hour and weekly usage, and run `--calibrate`. It divides the tokens used in that window by your percentage to estimate what 100% is. The estimate is only as good as the reading: if the percentage also includes usage outside the studio (your own chats), the budget comes out too small and the guard stops early, which is the safe direction. Recalibrate now and then.

**Where it works.** It reads this project's Claude Code session logs (cloud sessions keep them inside the session; local ones are in `~/.claude/projects/`). `--record` copies counts into `usage/sessions.jsonl` so cloud sessions are kept in the repository. Usage from sessions that were never recorded, including your interactive sessions on other machines, is not counted unless you record it.

Only counts, names and times are stored, never prompts or content. Tests: `python3 -m unittest discover tools/usage`.
