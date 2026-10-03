#!/bin/bash
# Installs two background jobs on your Mac (macOS "LaunchAgents") that start when you log in and restart if they stop:
#   1. com.gametaskforce.sync       runs tools/sync/sync.sh (keeps this folder in step with GitHub, both ways)
#   2. com.gametaskforce.dashboard  runs the dashboard at http://localhost:4173
# Usage, from the game-taskforce folder:
#   bash tools/sync/install-mac.sh            install and start both
#   bash tools/sync/install-mac.sh status     show whether they are running and the last log lines
#   bash tools/sync/install-mac.sh restart    restart both (do this after the dashboard code changes)
#   bash tools/sync/install-mac.sh uninstall  stop and remove both
set -e
ROOT="$(git rev-parse --show-toplevel)"
UIDN="$(id -u)"
AGENTS="$HOME/Library/LaunchAgents"
LOGS="$HOME/Library/Logs/game-taskforce"
SYNC=com.gametaskforce.sync
DASH=com.gametaskforce.dashboard

plist() { # label, working dir, command
cat > "$AGENTS/$1.plist" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$1</string>
  <key>WorkingDirectory</key><string>$2</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>-lc</string><string>$3</string></array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>$LOGS/$1.log</string>
  <key>StandardErrorPath</key><string>$LOGS/$1.log</string>
</dict></plist>
PL
}
load()   { launchctl bootout "gui/$UIDN/$1" 2>/dev/null || true; launchctl bootstrap "gui/$UIDN" "$AGENTS/$1.plist"; }
unload() { launchctl bootout "gui/$UIDN/$1" 2>/dev/null || true; }

case "${1:-install}" in
  install)
    command -v node >/dev/null || { echo "Node.js is not installed (nodejs.org). Install it, then run this again."; exit 1; }
    mkdir -p "$AGENTS" "$LOGS"
    ( cd "$ROOT/dashboard" && npm install --no-audit --no-fund >/dev/null )
    plist $SYNC "$ROOT" "bash tools/sync/sync.sh 20"
    plist $DASH "$ROOT/dashboard" "npm start"
    load $SYNC; load $DASH
    echo "Installed. Open http://localhost:4173 in about 30 seconds (the dashboard builds first)."
    echo "Check any time with:  bash tools/sync/install-mac.sh status" ;;
  status)
    for j in $SYNC $DASH; do
      if launchctl print "gui/$UIDN/$j" >/dev/null 2>&1; then echo "== $j: installed"; else echo "== $j: NOT installed"; fi
      tail -4 "$LOGS/$j.log" 2>/dev/null | sed 's/^/   /'
    done ;;
  restart) kickstart() { launchctl kickstart -k "gui/$UIDN/$1"; }; kickstart $SYNC; kickstart $DASH; echo restarted ;;
  uninstall) unload $SYNC; unload $DASH; rm -f "$AGENTS/$SYNC.plist" "$AGENTS/$DASH.plist"; echo "Removed both background jobs." ;;
  *) echo "Use: install | status | restart | uninstall"; exit 2 ;;
esac
