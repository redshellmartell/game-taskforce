#!/usr/bin/env python3
"""Recompute the calibration summary in panel/calibration.json.

For each persona: mean absolute error between predicted and actual ratings (1-5), over the games that have
both. A persona is `trusted` when it has at least MIN_GAMES rated games and its mean error is TRUST_LIMIT or less.

Usage:
  python3 panel/calibrate.py                 # recompute errors and trusted flags in place
  python3 panel/calibrate.py --merge DIR     # first merge DIR/predicted-<id>.json and DIR/actuals-<id>.json
                                             # (see panel/README.md), then recompute
"""
import json, sys, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, "calibration.json")
TRUST_LIMIT = 1.0
MIN_GAMES = 6

def load():
    try:
        with open(PATH) as f: return json.load(f)
    except FileNotFoundError:
        return {"updated": None, "trust_limit": TRUST_LIMIT, "personas": {}}

def summarise(entry):
    errs = [abs(g["predicted"] - g["actual"]) for g in entry["games"] if isinstance(g.get("predicted"), (int, float)) and isinstance(g.get("actual"), (int, float))]
    entry["rated_games"] = len(errs)
    entry["mean_abs_error"] = round(sum(errs) / len(errs), 2) if errs else None
    entry["trusted"] = bool(errs) and len(errs) >= MIN_GAMES and entry["mean_abs_error"] <= TRUST_LIMIT
    return entry

def merge(directory, data):
    for fn in sorted(os.listdir(directory)):
        if not fn.startswith("predicted-"): continue
        pid = fn[len("predicted-"):-len(".json")]
        with open(os.path.join(directory, fn)) as f: pred = json.load(f)
        with open(os.path.join(directory, f"actuals-{pid}.json")) as f: act = json.load(f)
        p = {g["game"]: g for g in pred["games"]}
        games = []
        for a in act["games"]:
            q = p.get(a["game"], {})
            games.append({"game": a["game"], "predicted": q.get("predicted"), "predicted_reason": q.get("reason"),
                          "actual": a.get("actual"), "actual_reason": a.get("reason"), "sources": a.get("sources", [])})
        old = data["personas"].get(pid, {})
        data["personas"][pid] = {"games": games, "evidence_basis": act.get("basis"), "attempts": old.get("attempts", 0) + 1, "notes": old.get("notes", "")}
    return data

if __name__ == "__main__":
    data = load()
    if "--merge" in sys.argv:
        data = merge(sys.argv[sys.argv.index("--merge") + 1], data)
    data["trust_limit"] = TRUST_LIMIT
    data["updated"] = datetime.date.today().isoformat()
    for pid, entry in data["personas"].items(): summarise(entry)
    with open(PATH, "w") as f: json.dump(data, f, indent=2, ensure_ascii=False); f.write("\n")
    for pid, e in data["personas"].items():
        print("%-11s mean error %s over %d games -> %s" % (pid, e["mean_abs_error"], e["rated_games"], "trusted" if e["trusted"] else "NOT trusted"))
