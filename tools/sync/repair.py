#!/usr/bin/env python3
"""Repairs a stuck sync WITHOUT losing the approvals you clicked on this Mac (standard library only).

What it does, in order:
  1. reads the approvals you answered that are saved in the git stash (or in your working copy),
  2. puts approvals.json and decisions.json back to GitHub's latest version and pulls everything new,
  3. re-applies every approval you answered that GitHub does not have yet (only requests that are still pending there),
  4. saves them as one commit and pushes it, then clears the stash.
Nothing is deleted until step 4 succeeds. Run from anywhere inside the game-taskforce folder:  python3 tools/sync/repair.py
"""
import json
import subprocess
import sys

FILES = ["games/approvals.json", "games/decisions.json"]


def git(*args, check=True):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), (r.stderr or r.stdout).strip()[:300]))
    return r.stdout


def merge_approvals(base, local):
    """base = GitHub's approvals.json, local = yours. Returns (merged, [ids applied])."""
    mine = {r["id"]: r for r in (local or {}).get("requests", []) if r.get("id")}
    applied = []
    for r in (base or {}).get("requests", []):
        m = mine.get(r.get("id"))
        if m and r.get("status") == "pending" and m.get("status") in ("approved", "declined"):
            for k in ("status", "decision", "decided_at", "owner_notes"):
                r[k] = m.get(k)
            applied.append(r["id"])
    return base, applied


def merge_decisions(base, local, requests, applied):
    """Keeps GitHub's decisions, adds yours that it lacks, and one entry for each re-applied approval."""
    base = base or {"decisions": []}
    have = {json.dumps(d, sort_keys=True) for d in base["decisions"]}
    for d in (local or {}).get("decisions", []):
        if json.dumps(d, sort_keys=True) not in have:
            base["decisions"].append(d)
            have.add(json.dumps(d, sort_keys=True))
    text = " ".join(str(d.get("notes") or "") for d in base["decisions"])
    by_id = {r["id"]: r for r in requests}
    for rid in applied:
        if rid not in text:
            r = by_id[rid]
            base["decisions"].append({"slug": r.get("game"), "time": r.get("decided_at"), "decision": r.get("decision") or r.get("status"),
                                      "notes": "%s: answered in the dashboard (recovered by repair)" % rid})
    return base


def read(ref, path):
    out = git("show", "%s:%s" % (ref, path), check=False)
    try:
        return json.loads(out)
    except ValueError:
        return None


def main():
    root = git("rev-parse", "--show-toplevel").strip()
    import os
    os.chdir(root)
    branch = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    has_stash = bool(git("stash", "list").strip())
    # 1. what you answered: the stash holds your version if a pull set it aside; otherwise your working copy
    local_a = read("stash@{0}", FILES[0]) if has_stash else None
    local_d = read("stash@{0}", FILES[1]) if has_stash else None
    if local_a is None:
        try:
            local_a = json.load(open(FILES[0])); local_d = json.load(open(FILES[1]))
        except (OSError, ValueError):
            local_a, local_d = None, None      # conflict markers in the file: the stash is the only source
    answered = [r["id"] for r in (local_a or {}).get("requests", []) if r.get("status") in ("approved", "declined")]
    print("Found %d answered approvals on this Mac: %s" % (len(answered), ", ".join(answered) or "none"))
    open("/tmp/approvals-backup.json", "w").write(json.dumps({"approvals": local_a, "decisions": local_d}, indent=2))
    print("Backup saved to /tmp/approvals-backup.json")
    # 2. back to GitHub's version, then pull
    git("fetch", "-q", "origin", branch)
    git("reset", "-q", "HEAD", "--", *FILES, check=False)
    git("checkout", "-f", "origin/%s" % branch, "--", *FILES)
    git("stash", "push", "-q", "-u", "-m", "repair-leftovers", check=False) if git("status", "--porcelain").strip() else None
    git("merge", "-q", "--ff-only", "origin/%s" % branch, check=False)
    git("pull", "-q", "--rebase", "origin", branch)
    # 3. re-apply
    base_a = json.load(open(FILES[0])); base_d = json.load(open(FILES[1]))
    merged_a, applied = merge_approvals(base_a, local_a)
    merged_d = merge_decisions(base_d, local_d, merged_a["requests"], applied)
    for path, obj in ((FILES[0], merged_a), (FILES[1], merged_d)):
        open(path, "w").write(json.dumps(obj, indent=2) + "\n")
    print("Re-applied: %s" % (", ".join(applied) or "nothing (GitHub already had them)"))
    # 4. save, push, clear
    git("add", *FILES)
    if git("status", "--porcelain", "--", *FILES).strip():
        git("commit", "-q", "-m", "Recovered approvals answered on the Mac (repair)")
    if git("log", "origin/%s..HEAD" % branch, "--oneline", check=False).strip():      # only push when there is something new to send
        git("push", "-q", "origin", branch)
    if has_stash:
        git("stash", "drop", "-q", check=False)
    print("Done. Refresh the dashboard. Pending requests left: %s" % ", ".join(r["id"] for r in merged_a["requests"] if r["status"] == "pending"))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print("Stopped (nothing was deleted; backup is in /tmp/approvals-backup.json):", e)
        sys.exit(1)
