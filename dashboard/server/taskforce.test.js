// Checks the switch, the checkpoint display, and that clicks write their whole effect. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { readTaskforce, writeSwitch } from './taskforce.js';
import { decideApproval } from './approvals.js';
import { decidePitch } from './pitch.js';
import { recordApprovalEffects, raiseRevisionForSendBack } from './effects.js';

const NOW = Date.parse('2026-10-05T12:00:00Z');
const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'tf-'));
const code = (fn) => { try { fn(); return null; } catch (e) { return e.status; } };
const read = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));

test('switch: off by default; writing it records active, mode, time and who', () => {
  const d = tmp();
  assert.equal(readTaskforce(d, NOW).active, false);
  const w = writeSwitch(d, true, 'now', NOW);
  assert.deepEqual(w, { active: true, pause_mode: 'now', updated: '2026-10-05T12:00:00.000Z', by: 'dashboard' });
  assert.equal(readTaskforce(d, NOW).active, true);
  assert.deepEqual(fs.readdirSync(d).filter((f) => f.endsWith('.tmp')), []);
});
test('switch refuses bad input', () => {
  const d = tmp();
  assert.equal(code(() => writeSwitch(d, 'yes', 'now')), 400);
  assert.equal(code(() => writeSwitch(d, true, 'whenever')), 400);
  assert.equal(writeSwitch(d, false).pause_mode, 'after-step');
});
test('status: a running checkpoint with a stale heartbeat shows as interrupted; a fresh one as running', () => {
  const d = tmp();
  fs.writeFileSync(path.join(d, 'run-state.json'), JSON.stringify({ status: 'running', game: 'g', step: 's', heartbeat: '2026-10-05T11:59:30Z' }));
  assert.equal(readTaskforce(d, NOW).displayStatus, 'running');
  assert.equal(readTaskforce(d, NOW + 10 * 60 * 1000).displayStatus, 'interrupted');
  fs.writeFileSync(path.join(d, 'run-state.json'), JSON.stringify({ status: 'usage-stop', reason: 'guard' }));
  assert.equal(readTaskforce(d, NOW + 10 * 60 * 1000).displayStatus, 'usage-stop');
  fs.writeFileSync(path.join(d, 'STOP'), '');
  assert.equal(readTaskforce(d, NOW).stopFile, true);
});

function files() {
  const d = tmp();
  const f = { approvalsFile: path.join(d, 'approvals.json'), decisionsFile: path.join(d, 'decisions.json'), statusFile: path.join(d, 'status.json') };
  fs.writeFileSync(f.approvalsFile, JSON.stringify({ requests: [{ id: 'g-revision-1', gate: 'revision', game: 'g', time: '2026-10-05T09:00:00Z', status: 'pending', options: [{ key: 'approve', label: 'x' }, { key: 'park', label: 'y' }], decision: null, decided_at: null, owner_notes: null }] }));
  fs.writeFileSync(f.statusFile, JSON.stringify({ games: [{ slug: 'g', title: 'Game G', stage: 'critique', revision: 0, history: [] }, { slug: 'p', title: 'Pitch P', stage: 'owner-review', revision: 1, history: [{ stage: 'owner-review', time: '2026-10-05T08:00:00Z' }] }] }));
  return f;
}
test('an approval click also writes the decision entry and the game history line', () => {
  const f = files();
  decideApproval(f.approvalsFile, 'g-revision-1', 'approve', 'go', NOW);
  recordApprovalEffects(f, 'g-revision-1', NOW);
  const dec = read(f.decisionsFile).decisions;
  assert.equal(dec.length, 1);
  assert.equal(dec[0].slug, 'g'); assert.equal(dec[0].decision, 'approve'); assert.match(dec[0].notes, /g-revision-1 \(revision gate\)/);
  assert.equal(dec[0].kind, undefined);                                   // a gate answer has no "kind"
  const h = read(f.statusFile).games[0].history;
  assert.equal(h.length, 1); assert.match(h[0].note, /approved by the owner \(dashboard\); queued/);
});
test('a declined option records the choice, not "queued"', () => {
  const f = files();
  decideApproval(f.approvalsFile, 'g-revision-1', 'park', '', NOW);
  recordApprovalEffects(f, 'g-revision-1', NOW);
  assert.match(read(f.statusFile).games[0].history[0].note, /park chosen/);
});
test('a pitch send-back to the designer raises its own pending revision request; other targets and decisions do not', () => {
  const f = files();
  decidePitch(f.decisionsFile, f.statusFile, 'p', 'send-back', 'Make the bait matter', NOW, 'game-designer');
  const r = raiseRevisionForSendBack(f, 'p', 'Make the bait matter', 'game-designer', NOW);
  assert.equal(r.id, 'p-revision-1'); assert.equal(r.status, 'pending'); assert.match(r.summary, /Make the bait matter/);
  assert.equal(read(f.approvalsFile).requests.length, 2);
  assert.match(read(f.statusFile).games[1].history.at(-1).note, /waiting for approval: revision \(p-revision-1\)/);
  assert.equal(raiseRevisionForSendBack(f, 'p', 'x', 'critic', NOW), null);
});
