import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { requestResearch, pipelineGames, researchHints, KINDS } from './research.js';

function setup() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'research-'));
  const f = { approvals: path.join(dir, 'approvals.json'), decisions: path.join(dir, 'decisions.json'), status: path.join(dir, 'status.json'), dir };
  fs.writeFileSync(f.status, JSON.stringify({ games: [{ slug: 'a', title: 'A', stage: 'design' }, { slug: 'b', title: 'B', stage: 'critique' }, { slug: 'dead', title: 'Dead', stage: 'killed' }] }));
  fs.writeFileSync(f.approvals, JSON.stringify({ requests: [{ id: 'old', gate: 'revision', status: 'pending' }] }));
  return f;
}
const read = (f) => JSON.parse(fs.readFileSync(f, 'utf8'));
const run = (f, body, now) => requestResearch(f.approvals, f.decisions, f.status, body, now);

test('game research records an already-approved scan request and keeps the others', () => {
  const f = setup(); const r = run(f, { kind: 'game-research' }, Date.parse('2026-10-04T12:00:00Z'));
  assert.equal(r.gate, 'scan'); assert.equal(r.usage_estimate, 'XL');
  const reqs = read(f.approvals).requests; assert.equal(reqs.length, 2); assert.equal(reqs[0].id, 'old');
  assert.equal(reqs[1].status, 'approved'); assert.equal(reqs[1].decision, 'approve'); assert.equal(reqs[1].decided_at, '2026-10-04T12:00:00.000Z');
  assert.equal(reqs[1].id, 'research-game-research-20261004t120000z');
  assert.equal(fs.existsSync(f.approvals + '.tmp'), false);               // no temp file left behind
});
test('persona research uses the panel-research gate', () => {
  const f = setup(); assert.equal(run(f, { kind: 'persona-research' }).gate, 'panel-research');
});
test('reanalyze needs ticked games from the pipeline; usage grows with the number of games', () => {
  const f = setup();
  assert.throws(() => run(f, { kind: 'reanalyze', games: [] }), (e) => e.status === 400);
  assert.throws(() => run(f, { kind: 'reanalyze', games: ['dead'] }), (e) => e.status === 400);
  assert.throws(() => run(f, { kind: 'reanalyze', games: ['nope'] }), (e) => e.status === 400);
  const r = run(f, { kind: 'reanalyze', games: ['a', 'b', 'a'] });
  assert.equal(r.gate, 'deep-research'); assert.deepEqual(r.targets, ['a', 'b']); assert.equal(r.usage_estimate, 'M');
  assert.equal(read(f.approvals).requests.at(-1).targets.length, 2);
});
test('bad input: unknown kind, games on a non-game request, long note', () => {
  const f = setup();
  assert.throws(() => run(f, { kind: 'hack' }), (e) => e.status === 400);
  assert.throws(() => run(f, { kind: 'game-research', games: ['a'] }), (e) => e.status === 400);
  assert.throws(() => run(f, { kind: 'game-research', note: 'x'.repeat(2001) }), (e) => e.status === 400);
  assert.equal(read(f.approvals).requests.length, 1);
});
test('the same research cannot be queued twice until the Director has run it', () => {
  const f = setup(); const first = run(f, { kind: 'game-research' }, 1000);
  assert.throws(() => run(f, { kind: 'game-research' }, 2000), (e) => e.status === 409);
  fs.writeFileSync(f.decisions, JSON.stringify({ decisions: [{ notes: `${first.id}: Director ran it` }] }));
  assert.doesNotThrow(() => run(f, { kind: 'game-research' }, 3000));
  run(f, { kind: 'reanalyze', games: ['a'] }, 4000);
  assert.throws(() => run(f, { kind: 'reanalyze', games: ['a'] }, 5000), (e) => e.status === 409);
  assert.doesNotThrow(() => run(f, { kind: 'reanalyze', games: ['b'] }, 6000));      // a different selection is a different request
});
test('pipelineGames skips killed and archived; hints say what looks due', () => {
  const f = setup(); assert.deepEqual(pipelineGames(f.status).map((g) => g.slug), ['a', 'b']);
  const now = Date.parse('2026-10-04T00:00:00Z');
  const h = researchHints({ bank: { lastScan: '2026-08-01', scanAgeDays: 64, strongBanked: 2, needsScan: true, scanReasons: ['x'] }, calibrated: '2026-10-01', games: [{ slug: 'a', title: 'A', stage: 'design' }, { slug: 'dead', stage: 'killed' }], now, fileTimes: { a: now - 3 * 86400000 } });
  assert.equal(h.scan.due, true); assert.equal(h.personas.due, false); assert.equal(h.games.length, 1); assert.equal(h.games[0].days, 3);
  assert.equal(researchHints({ bank: null, calibrated: null, games: [], now }).personas.due, true);
  assert.deepEqual(Object.keys(KINDS), ['game-research', 'persona-research', 'reanalyze']);
});
