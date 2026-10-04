// Checks the Review Queue decision write. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { decidePitch, pitchDecisionFor } from './pitch.js';

function setup(extra = []) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pitch-'));
  const status = path.join(dir, 'status.json'), decisions = path.join(dir, 'decisions.json');
  fs.writeFileSync(status, JSON.stringify({ games: [
    { slug: 'g1', stage: 'owner-review', history: [{ stage: 'owner-review', time: '2026-10-01T10:00:00Z' }] },
    { slug: 'g2', stage: 'design', history: [] }] }));
  fs.writeFileSync(decisions, JSON.stringify({ decisions: extra }));
  return { dir, status, decisions };
}
const read = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));

test('approve: appends one decision, touches nothing else, writes atomically', () => {
  const { status, decisions, dir } = setup([{ slug: 'old', decision: 'approve', time: '2026-09-01T00:00:00Z', notes: 'x' }]);
  const before = fs.readFileSync(status, 'utf8');
  const e = decidePitch(decisions, status, 'g1', 'approve', ' looks good ', Date.parse('2026-10-02T09:00:00Z'));
  assert.equal(e.decision, 'approve'); assert.equal(e.notes, 'looks good'); assert.equal(e.time, '2026-10-02T09:00:00.000Z');
  const d = read(decisions).decisions; assert.equal(d.length, 2); assert.equal(d[0].slug, 'old');
  assert.equal(fs.readFileSync(status, 'utf8'), before);          // status.json is never edited by the dashboard
  assert.deepEqual(fs.readdirSync(dir).sort(), ['decisions.json', 'status.json']);   // no temp file left behind
});
test('reject and send-back are accepted; anything else is refused', () => {
  for (const k of ['reject', 'send-back']) { const { status, decisions } = setup(); assert.equal(decidePitch(decisions, status, 'g1', k, 'n').decision, k); }
  const { status, decisions } = setup();
  for (const bad of ['prototyped', 'park', '', undefined, 'APPROVE']) assert.throws(() => decidePitch(decisions, status, 'g1', bad, ''), (e) => e.status === 400);
  assert.equal(read(decisions).decisions.length, 0);
});
test('refusals: not waiting 404, already decided 409, notes too long 400', () => {
  const { status, decisions } = setup();
  assert.throws(() => decidePitch(decisions, status, 'g2', 'approve', ''), (e) => e.status === 404);
  assert.throws(() => decidePitch(decisions, status, 'nope', 'approve', ''), (e) => e.status === 404);
  assert.throws(() => decidePitch(decisions, status, 'g1', 'approve', 'x'.repeat(2001)), (e) => e.status === 400);
  decidePitch(decisions, status, 'g1', 'approve', '');
  assert.throws(() => decidePitch(decisions, status, 'g1', 'reject', ''), (e) => e.status === 409);
  assert.equal(read(decisions).decisions.length, 1);
});
test('an old decision from before the game entered owner-review does not count', () => {
  const { status, decisions } = setup([{ slug: 'g1', kind: 'pitch', decision: 'send-back', time: '2026-09-20T00:00:00Z', notes: 'earlier round' }]);
  assert.equal(pitchDecisionFor('g1', Date.parse('2026-10-01T10:00:00Z'), read(decisions).decisions), null);
  assert.equal(decidePitch(decisions, status, 'g1', 'approve', '').decision, 'approve');
});
test('a missing decisions file is created', () => {
  const { dir, status } = setup(); const f = path.join(dir, 'new-decisions.json');
  decidePitch(f, status, 'g1', 'approve', ''); assert.equal(read(f).decisions.length, 1);
});

test('the server file itself loads (catches a broken import before it reaches the owner)', async () => {
  const { spawnSync } = await import('node:child_process');
  const r = spawnSync(process.execPath, ['--check', new URL('./index.js', import.meta.url).pathname], { encoding: 'utf8' });
  assert.equal(r.status, 0, r.stderr);
});

test('an approval-gate decision for the same game is NOT mistaken for a pitch decision', () => {
  const gate = { slug: 'g1', time: '2026-10-02T00:00:00Z', decision: 'approve', notes: 'g1-revision-1 (revision gate): owner approved' };
  assert.equal(pitchDecisionFor('g1', Date.parse('2026-10-01T10:00:00Z'), [gate]), null);
  const { status, decisions } = setup([gate]);
  const e = decidePitch(decisions, status, 'g1', 'approve', 'ok');            // so the pitch can still be decided
  assert.equal(e.kind, 'pitch');
});

test('send-back records the department it goes to (design by default); other decisions refuse a target', () => {
  let { status, decisions } = setup();
  assert.equal(decidePitch(decisions, status, 'g1', 'send-back', 'n').target, 'game-designer');
  ({ status, decisions } = setup());
  assert.equal(decidePitch(decisions, status, 'g1', 'send-back', 'check the market again', Date.now(), 'market-researcher').target, 'market-researcher');
  ({ status, decisions } = setup());
  assert.throws(() => decidePitch(decisions, status, 'g1', 'send-back', '', Date.now(), 'owner'), (e) => e.status === 400);
  assert.throws(() => decidePitch(decisions, status, 'g1', 'approve', '', Date.now(), 'critic'), (e) => e.status === 400);
  assert.equal(JSON.parse(fs.readFileSync(decisions, 'utf8')).decisions.length, 0);
  assert.equal(decidePitch(decisions, status, 'g1', 'approve', '').target, undefined);
});
