#!/bin/bash
# Keeps this folder in step with GitHub so the dashboard is always current.
# Every 20 seconds it
#   1. saves and pushes YOUR changes (approvals you clicked, ideas you added in the dashboard), and
#   2. pulls everything the agents pushed from cloud sessions.
# It never touches anything else you have changed. Stop it with Ctrl+C.
# Usage (from the game-taskforce folder):  bash tools/sync/sync.sh        (add a number to change the seconds: bash tools/sync/sync.sh 10)
INTERVAL="${1:-20}"
OWNER_FILES=("games/approvals.json" "games/decisions.json" "studio-settings.json" "games/_inbox")
cd "$(git rev-parse --show-toplevel)" || exit 1
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "Syncing branch $BRANCH every ${INTERVAL}s. Press Ctrl+C to stop."
while true; do
  # 1. your decisions and ideas -> GitHub
  CHANGED=0
  for f in "${OWNER_FILES[@]}"; do
    if [ -e "$f" ] && [ -n "$(git status --porcelain -- "$f" 2>/dev/null)" ]; then git add -A -- "$f" 2>/dev/null && CHANGED=1; fi
  done
  if [ "$CHANGED" = 1 ] && ! git diff --cached --quiet; then
    git commit -q -m "Owner update from the dashboard (auto-sync)" 2>/dev/null && echo "$(date +%H:%M:%S) saved your changes"
  fi
  # 2. cloud work -> your folder (rebase keeps your commit on top; other uncommitted files are set aside and put back)
  if git fetch -q origin "$BRANCH" 2>/dev/null; then
    if ! git pull -q --rebase --autostash origin "$BRANCH" 2>/tmp/sync-error.txt; then
      git rebase --abort 2>/dev/null
      echo "$(date +%H:%M:%S) could not combine your changes with the cloud's (same file changed in both). Nothing was lost. Tell Claude: sync conflict."
      cat /tmp/sync-error.txt | tail -3
    fi
    if [ -n "$(git log '@{u}..HEAD' --oneline 2>/dev/null)" ]; then
      git push -q origin "$BRANCH" 2>/dev/null && echo "$(date +%H:%M:%S) sent your changes to GitHub"
    fi
  else
    echo "$(date +%H:%M:%S) no connection to GitHub; will retry"
  fi
  sleep "$INTERVAL"
done
