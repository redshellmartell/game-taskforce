# Auto-sync for the dashboard

Cloud sessions push their work to GitHub; the dashboard reads your folder. `sync.sh` closes that gap both ways every 20 seconds:
- your approvals, decisions, settings and ideas added in the dashboard are committed and pushed (so the cloud session sees them);
- everything the agents pushed is pulled into your folder (so a browser refresh shows it).

Run it in its own Terminal window from the `game-taskforce` folder: `bash tools/sync/sync.sh`. Stop with Ctrl+C.
It only commits `games/approvals.json`, `games/decisions.json`, `studio-settings.json` and `games/_inbox/`. If a file was changed on both sides at once it stops that round, loses nothing, and says so.

## Run it automatically (Mac)

`bash tools/sync/install-mac.sh` installs two background jobs (macOS LaunchAgents) that start when you log in and restart if they stop: the sync script and the dashboard at http://localhost:4173. `status`, `restart` and `uninstall` are the other commands. Logs are in `~/Library/Logs/game-taskforce/`. Written without access to a Mac, so the first run is its test.
