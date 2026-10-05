// Task 014, stage 2 (task 011 Step A): a click writes its whole effect, so nobody has to type "continue with approved work".
//   - an approval-gate click appends an entry to games/decisions.json and a line to the game's history in games/status.json
//   - a pitch send-back also raises the revision request it needs (pending: the owner approves it with one more click)
// Atomic writes. Never starts an agent.
import fs from 'node:fs';

const readJson = (f, dflt) => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return dflt; } };
function writeAtomic(file, data) { const tmp = `${file}.tmp`; fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n'); fs.renameSync(tmp, file); }

// After decideApproval() succeeded for request `id`.
export function recordApprovalEffects({ approvalsFile, decisionsFile, statusFile }, id, now = Date.now()) {
  const req = (readJson(approvalsFile, {}).requests || []).find((r) => r && r.id === id);
  if (!req) return null;
  const time = new Date(now).toISOString();
  const decisions = readJson(decisionsFile, { decisions: [] });
  if (!Array.isArray(decisions.decisions)) decisions.decisions = [];
  const entry = { slug: req.game || null, time, decision: req.decision, notes: `${id} (${req.gate} gate): owner decided in the dashboard${req.owner_notes ? `: ${req.owner_notes}` : ''}` };
  decisions.decisions.push(entry);
  writeAtomic(decisionsFile, decisions);
  const status = readJson(statusFile, null);
  const game = status && (status.games || []).find((g) => g.slug === req.game);
  if (game) {
    (game.history = game.history || []).push({ stage: game.stage, time, verdict: null, note: req.status === 'approved' ? `${id} approved by the owner (dashboard); queued` : `${id}: ${req.decision} chosen by the owner (dashboard)` });
    writeAtomic(statusFile, status);
  }
  return entry;
}

// After decidePitch() recorded a send-back to the designer: raise the revision request (pending), with the owner's notes as the brief.
export function raiseRevisionForSendBack({ approvalsFile, statusFile }, slug, notes, target, now = Date.now()) {
  if (target && target !== 'game-designer') return null;      // other departments are routed by the Director
  const data = readJson(approvalsFile, { requests: [] });
  if (!Array.isArray(data.requests)) data.requests = [];
  const status = readJson(statusFile, { games: [] });
  const game = (status.games || []).find((g) => g.slug === slug);
  const n = data.requests.filter((r) => r && r.game === slug && r.gate === 'revision').length + 1;
  const id = `${slug}-revision-${n}`;
  if (data.requests.some((r) => r && r.id === id)) return null;
  const time = new Date(now).toISOString();
  const req = {
    id, gate: 'revision', game: slug, time, status: 'pending',
    summary: `You sent ${game ? game.title : slug} back to the designer from the Review Queue.${notes && !/^decided in the dashboard/.test(notes) ? ` Your note: ${notes}` : ''}`,
    why_needed: 'Your send-back is the brief. The Director adds the latest playtest and critic findings before the designer starts.',
    expected_outcome: 'The designer addresses your note and the open findings; the playtester and critic then re-check the targeted numbers.',
    usage_estimate: 'M', recommendation: 'approve',
    options: [{ key: 'approve', label: 'Run the revision (designer, playtester, critic)' }, { key: 'park', label: 'Park the game; no further work for now' }, { key: 'kill', label: 'Kill it and record why' }],
    decision: null, decided_at: null, owner_notes: null,
  };
  data.requests.push(req);
  writeAtomic(approvalsFile, data);
  if (game) { (game.history = game.history || []).push({ stage: game.stage, time, verdict: null, note: `owner sent it back; waiting for approval: revision (${id})` }); writeAtomic(statusFile, status); }
  return req;
}
