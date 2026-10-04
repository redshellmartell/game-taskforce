// The dashboard's third allowed write: the owner's verdict on a pitched game (approve / reject / send-back) appended to games/decisions.json,
// and a helper that commits and pushes the two decision files so a Claude Code session in the cloud can see them. It never starts an agent.
import fs from 'node:fs';
import { execFile } from 'node:child_process';

const VERDICTS = ['approve', 'reject', 'send-back'];
const MAX_NOTES = 2000;
function fail(status, message) { const e = new Error(message); e.status = status; throw e; }

export function recordDecision(file, slug, decision, notes, now = Date.now()) {
  if (!/^[a-z0-9][a-z0-9-]*$/.test(String(slug || ''))) fail(400, 'Unknown game.');
  if (!VERDICTS.includes(decision)) fail(400, 'Decision must be approve, reject or send-back.');
  const clean = notes == null ? '' : String(notes).trim();
  if (clean.length > MAX_NOTES) fail(400, `Notes are too long (max ${MAX_NOTES} characters).`);
  let data = { decisions: [] };
  try { data = JSON.parse(fs.readFileSync(file, 'utf8')); } catch { /* first decision */ }
  if (!Array.isArray(data.decisions)) data.decisions = [];
  const entry = { slug, time: new Date(now).toISOString(), decision, notes: clean ? `${clean} (recorded from the dashboard)` : 'recorded from the dashboard' };
  data.decisions.push(entry);
  const tmp = `${file}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n');
  fs.renameSync(tmp, file);
  return entry;
}

const run = (cwd, args) => new Promise((resolve, reject) => execFile('git', args, { cwd, timeout: 60000 }, (err, out, errout) => err ? reject(new Error((errout || err.message).trim())) : resolve(out.trim())));

// Commit only the two decision files, then push the current branch.
export async function syncDecisions(repoRoot) {
  const files = ['games/approvals.json', 'games/decisions.json'];
  const changed = await run(repoRoot, ['status', '--porcelain', '--', ...files]);
  if (changed) {
    await run(repoRoot, ['add', '--', ...files]);
    await run(repoRoot, ['commit', '-m', 'Owner decisions from the dashboard', '--', ...files]);
  }
  const branch = await run(repoRoot, ['rev-parse', '--abbrev-ref', 'HEAD']);
  await run(repoRoot, ['push', '-u', 'origin', branch]);
  return { branch, committed: Boolean(changed) };
}
