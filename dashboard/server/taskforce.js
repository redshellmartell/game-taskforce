// Task 014, stage 2: the taskforce switch and the checkpoint, as plain files in studio/ (the dashboard only writes the switch).
//   studio/taskforce.json  { active, pause_mode: "after-step" | "now", updated, by }   (written here)
//   studio/run-state.json  the checkpoint (written by the runner; read here)
// Mirrors tools/runner/state.py. Nothing here starts an agent.
import fs from 'node:fs';
import path from 'node:path';

const STALE_SECONDS = 120;   // a heartbeat older than this means the runner was interrupted (e.g. the Mac slept)
const MODES = ['after-step', 'now'];
function fail(status, message) { const e = new Error(message); e.status = status; throw e; }
const readJson = (f, dflt) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return dflt; } };

export function readTaskforce(studioDir, now = Date.now()) {
  const sw = readJson(path.join(studioDir, 'taskforce.json'), {});
  const run = { status: 'stopped', game: null, stage: null, step: null, agent: null, started: null, heartbeat: null, last_done: null, reason: null, queue: [], ...readJson(path.join(studioDir, 'run-state.json'), {}) };
  const hb = Date.parse(run.heartbeat);
  const stale = run.status === 'running' && !Number.isNaN(hb) && (now - hb) / 1000 > STALE_SECONDS;
  const stopFile = fs.existsSync(path.join(studioDir, 'STOP'));
  return {
    active: sw.active === true, pause_mode: MODES.includes(sw.pause_mode) ? sw.pause_mode : 'after-step', updated: sw.updated || null, by: sw.by || null,
    stopFile, run, displayStatus: stale ? 'interrupted' : run.status, lastHeartbeat: run.heartbeat || null,
  };
}

export function writeSwitch(studioDir, active, pauseMode, now = Date.now()) {
  if (typeof active !== 'boolean') fail(400, 'Say whether the taskforce should be on or off.');
  const mode = pauseMode == null ? 'after-step' : pauseMode;
  if (!MODES.includes(mode)) fail(400, 'Pause mode must be after-step or now.');
  fs.mkdirSync(studioDir, { recursive: true });
  const file = path.join(studioDir, 'taskforce.json');
  const data = { active, pause_mode: mode, updated: new Date(now).toISOString(), by: 'dashboard' };
  const tmp = `${file}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n');
  fs.renameSync(tmp, file);
  return data;
}
