#!/usr/bin/env python3
"""Fixes activity-log lines whose time is in the future (agents without a clock guessed them).
Every games/<slug>/activity.jsonl line later than now gets time = now and "time_estimated": true.
Usage: python3 tools/activity/fix_future_times.py [--dry-run]"""
import datetime, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse(t):
    try:
        return datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    except (TypeError, ValueError):
        return None


def fix_lines(lines, now):
    """Returns (new_lines, number_fixed)."""
    out, n = [], 0
    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    for line in lines:
        try:
            o = json.loads(line)
        except ValueError:
            out.append(line); continue
        t = parse(o.get("time"))
        if t and t > now + datetime.timedelta(seconds=60):
            o["time"] = stamp; o["time_estimated"] = True; n += 1
            line = json.dumps(o) + "\n"
        out.append(line)
    return out, n


if __name__ == "__main__":
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    total = 0
    for p in sorted(glob.glob(os.path.join(ROOT, "games", "*", "activity.jsonl"))):
        lines = open(p, encoding="utf-8").readlines()
        new, n = fix_lines(lines, now)
        if n and "--dry-run" not in sys.argv:
            open(p, "w", encoding="utf-8").writelines(new)
        if n: print("%s: %d future-dated line(s) fixed" % (os.path.relpath(p, ROOT), n))
        total += n
    print("fixed %d line(s)" % total)
