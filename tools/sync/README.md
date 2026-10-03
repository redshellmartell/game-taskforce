# Auto-sync for the dashboard

Cloud sessions push their work to GitHub; the dashboard reads your folder. `sync.sh` closes that gap both ways every 20 seconds:
- your approvals, decisions, settings and ideas added in the dashboard are committed and pushed (so the cloud session sees them);
- everything the agents pushed is pulled into your folder (so a browser refresh shows it).

Run it in its own Terminal window from the `game-taskforce` folder: `bash tools/sync/sync.sh`. Stop with Ctrl+C.
It only commits `games/approvals.json`, `games/decisions.json`, `studio-settings.json` and `games/_inbox/`. If a file was changed on both sides at once it stops that round, loses nothing, and says so.
