// Checks that recording a decision changes only the decision fields, and refuses bad requests. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { decideApproval } from './approvals.js';

const NOW = Date.parse('2026-10-03T12:00:00Z');
const base = () => ({ requests: [
  { id: 'r1', gate: 'revision', game: 'g', time: '2026-10-02T09:00:00Z', status: 'pending', summary: 'S', why_needed: 'W', expected_outcome: 'E', usage_estimate: 'M', recommendation: 'approve',
    options: [{ key: 'approve', label: 'Run it' }, { key: 'park', label: 'Park it' }], decision: null, decided_at: null, owner_notes: null, extra: { keep: 1 } },
  { id: 'old', gate: 'scan', game: null, time: '2026-09-01T09:00:00Z', status: 'pending', options: [{ key: 'approve', label: 'x' }], decision: null, decided_at: null, owner_notes: null },
  { id: 'done', gate: 'scan', game: null, time: '2026-10-01T09:00:00Z', status: 'approved', options: [{ key: 'approve', label: 'x' }], decision: 'approve', decided_at: '2026-10-01T10:00:00Z', owner_notes: null }] });
const setup = () => { const f = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'appr-')), 'approvals.json'); fs.writeFileSync(f, JSON.stringify(base())); return f; };
const read = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));
const code = (fn) => { try { fn(); return null; } catch (e) { return e.status; } };

test('approve: only status, decision, decided_at and owner_notes change; everything else is kept', () => {
  const f = setup(); const before = read(f);
  const r = decideApproval(f, 'r1', 'approve', '  Go ahead  ', NOW);
  assert.deepEqual(r, { id: 'r1', status: 'approved', decision: 'approve', decided_at: '2026-10-03T12:00:00.000Z' });
  const after = read(f);
  const strip = (x) => { const { status, decision, decided_at, owner_notes, ...rest } = x; return rest; };
  assert.deepEqual(strip(after.requests[0]), strip(before.requests[0]));            // nothing else about that request changed
  assert.equal(after.requests[0].owner_notes, 'Go ahead');
  assert.deepEqual(after.requests.slice(1), before.requests.slice(1));              // other requests untouched
});
test('any other option records a declined step with that decision', () => {
  const f = setup(); decideApproval(f, 'r1', 'park', '', NOW);
  const r = read(f).requests[0]; assert.equal(r.status, 'declined'); assert.equal(r.decision, 'park'); assert.equal(r.owner_notes, null);
});
test('review-cap: continue counts as approved, park and kill do not', () => {
  const f = setup(); const d = read(f);
  d.requests.push({ id: 'cap', gate: 'review-cap', game: 'g', time: '2026-10-03T09:00:00Z', status: 'pending', options: [{ key: 'continue', label: 'More cycles' }, { key: 'kill', label: 'Kill' }], decision: null, decided_at: null, owner_notes: null });
  fs.writeFileSync(f, JSON.stringify(d));
  assert.equal(decideApproval(f, 'cap', 'continue', '', NOW).status, 'approved');
  assert.equal(decideApproval(f, 'r1', 'park', '', NOW).status, 'declined');
});
test('refusals: unknown id 404, unknown option 400, already decided 409, expired 409, notes too long 400, no file 404', () => {
  const f = setup();
  assert.equal(code(() => decideApproval(f, 'nope', 'approve', '', NOW)), 404);
  assert.equal(code(() => decideApproval(f, 'r1', 'delete-everything', '', NOW)), 400);
  assert.equal(code(() => decideApproval(f, 'done', 'approve', '', NOW)), 409);
  assert.equal(code(() => decideApproval(f, 'old', 'approve', '', NOW)), 409);
  assert.equal(code(() => decideApproval(f, 'r1', 'approve', 'x'.repeat(2001), NOW)), 400);
  assert.equal(code(() => decideApproval('/definitely/not/here.json', 'r1', 'approve', '', NOW)), 404);
  assert.equal(read(f).requests[0].status, 'pending');                              // none of the refused calls changed anything
});
test('a request cannot be decided twice', () => {
  const f = setup(); decideApproval(f, 'r1', 'approve', '', NOW);
  assert.equal(code(() => decideApproval(f, 'r1', 'park', '', NOW)), 409);
});
