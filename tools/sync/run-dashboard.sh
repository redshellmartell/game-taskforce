#!/bin/bash
# One command to run the dashboard live on your Mac, with the files kept up to date.
#   bash tools/sync/run-dashboard.sh
# It checks Node, gets the latest files, installs and builds the dashboard, starts it, opens it in your browser,
# and keeps pulling new work from GitHub every 20 seconds while it runs. Press Ctrl+C to stop everything.
# Set PORT=4180 to use a different port. Set NO_SYNC=1 to skip the background pulling.
cd "$(git rev-parse --show-toplevel)" || { echo "Run this from inside the game-taskforce folder."; exit 1; }
PORT="${PORT:-4173}"
URL="http://localhost:$PORT"
say() { echo; echo "== $1"; }

say "1/5 Checking Node.js"
if ! command -v node >/dev/null || ! command -v npm >/dev/null; then
  echo "Node.js is not installed (or Terminal can't see it). Install it from https://nodejs.org, then close and reopen Terminal and run this again."; exit 1
fi
echo "node $(node --version), npm $(npm --version)"

say "2/5 Getting the latest files"
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if git status --porcelain | grep -q '^UU'; then
  echo "A previous pull left a conflict. Fix it first with:"
  echo "  git fetch origin && git show origin/$BRANCH:tools/sync/repair.py > /tmp/repair.py && python3 /tmp/repair.py"
  exit 1
fi
GIT_TERMINAL_PROMPT=0 git pull --rebase --autostash -q origin "$BRANCH" 2>/tmp/run-dashboard-pull.txt && echo "up to date ($(git log -1 --format=%s | cut -c1-60))" || { echo "Could not pull (continuing with the files you have):"; tail -3 /tmp/run-dashboard-pull.txt; }

say "3/5 Installing and building the dashboard (the first time takes a minute)"
cd dashboard || exit 1
npm install --no-audit --no-fund --loglevel=error || { echo "npm install failed (see above)."; exit 1; }
npx vite build --logLevel=error || { echo "The build failed (see above)."; exit 1; }

say "4/5 Checking the port"
if lsof -ti ":$PORT" >/dev/null 2>&1; then
  echo "Something is already using port $PORT (probably an older copy of the dashboard). Stopping it."
  kill $(lsof -ti ":$PORT") 2>/dev/null; sleep 1
fi

ROOT="$(git rev-parse --show-toplevel)"
SYNC_PID=""
if [ -z "$NO_SYNC" ]; then
  ( cd "$ROOT" && exec bash tools/sync/sync.sh 20 ) &
  SYNC_PID=$!
fi
trap '[ -n "$SYNC_PID" ] && kill $SYNC_PID 2>/dev/null; kill $SERVER_PID 2>/dev/null; echo; echo "Stopped."; exit 0' INT TERM

say "5/5 Starting the dashboard"
PORT="$PORT" node server/index.js &
SERVER_PID=$!
for i in $(seq 1 20); do
  if curl -fs "$URL/api/state" >/dev/null 2>&1; then
    echo; echo "READY: $URL"
    command -v open >/dev/null && open "$URL"
    echo "Leave this window open. New work from the cloud appears here by itself. Press Ctrl+C to stop."
    break
  fi
  sleep 1
done
if ! curl -fs "$URL/api/state" >/dev/null 2>&1; then echo "The dashboard did not start (see any error above)."; fi
wait $SERVER_PID
