// Checks the KPI calculations against the sample data. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildState } from './state.js';
import { conceptsInDevelopment, pitchRate, avgCriticAtPitch, reviewQueue, agentsActive } from './kpis.js';

const dashboardDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(dashboardDir, '..');
const state = buildState({ repoRoot, dashboardDir, sample: true });

test('sample data has three games and five agents', () => {
  assert.equal(state.games.length, 3);
  assert.equal(state.agents.length, 5);
});
test('concepts in development: only ember-market is still in progress', () => {
  const k = conceptsInDevelopment(state.games);
  assert.equal(k.value, 1); assert.equal(k.status, 'good');
});
test('pitch rate: 1 of 3 games was pitched = 33%', () => {
  const k = pitchRate(state.games);
  assert.equal(k.value, 33); assert.equal(k.status, 'good');
});
test('average critic score at pitch: lantern-heist scored 4.2', () => {
  const k = avgCriticAtPitch(state.games);
  assert.equal(k.value, 4.2); assert.equal(k.status, 'good');
});
test('review queue: one pitch waiting', () => {
  const k = reviewQueue(state.games);
  assert.equal(k.value, 1);
});
test('agents active: the designer is working on ember-market', () => {
  const k = agentsActive(state.agents);
  assert.equal(k.value, 1); assert.equal(k.total, 5);
  assert.equal(state.agents.find((a) => a.id === 'game-designer').currentGame, 'ember-market');
});
test('no data gives status "none", not a crash', () => {
  assert.equal(pitchRate([]).status, 'none');
  assert.equal(avgCriticAtPitch([]).status, 'none');
  assert.equal(conceptsInDevelopment([]).status, 'none');
});
test('real games folder (no JSON files yet) still builds', () => {
  const real = buildState({ repoRoot, dashboardDir, sample: false });
  assert.ok(Array.isArray(real.games));
});

// ---- Game page scorecard ----
import { gameScorecard } from './kpis.js';
const byId = (rows) => Object.fromEntries(rows.map((r) => [r.id, r]));

test('scorecard: lantern-heist (a good game) is green with one flagged card', () => {
  const s = byId(state.games.find((g) => g.slug === 'lantern-heist').scorecard);
  assert.equal(s.opportunity.value, 24); assert.equal(s.opportunity.status, 'good');
  assert.equal(s.critic.value, 4.2); assert.equal(s.seat.status, 'good');
  assert.equal(s.length.value, -5); assert.equal(s.length.status, 'good');
  assert.equal(s.runaway.value, 58);
  assert.equal(s.dead.value, 1); assert.equal(s.dead.status, 'warn');
});
test('scorecard: ember-market shows its runaway-leader problem in red', () => {
  const s = byId(state.games.find((g) => g.slug === 'ember-market').scorecard);
  assert.equal(s.runaway.value, 78); assert.equal(s.runaway.status, 'bad');
  assert.equal(s.seat.status, 'warn');
  assert.equal(s.critic.status, 'none'); // no critique yet
});
test('scorecard: a game with no data gives all "none" rows, not a crash', () => {
  const rows = gameScorecard({});
  assert.ok(rows.length > 5);
  assert.ok(rows.every((r) => r.status === 'none' && r.value === null));
});

// ---- Pipeline KPIs ----
test('stage funnel: 3 briefs, 2 reached critique, 1 reached pitch, none approved', () => {
  assert.deepEqual(state.pipeline.funnel.map((f) => f.count), [3, 3, 3, 2, 1, 0, 0]);
});
test('kill rate by stage: tide-lords was killed at critique, 1 of 2 = 50%', () => {
  const k = state.pipeline.killRate.find((s) => s.id === 'critique');
  assert.equal(k.entered, 2); assert.equal(k.killed, 1); assert.equal(k.pct, 50);
  assert.equal(state.pipeline.killRate.find((s) => s.id === 'brief').killed, 0);
});
test('cycle time: lantern-heist took 5.5 hours from brief to pitch', () => {
  const c = state.pipeline.cycleTimes.find((x) => x.slug === 'lantern-heist');
  assert.equal(c.hours, 5.5);
});
test('average revision loops: lantern-heist had 1', () => {
  assert.equal(state.pipeline.avgRevisions.value, 1); assert.equal(state.pipeline.avgRevisions.status, 'good');
});
test('first-pass playtest rate: only tide-lords passed first time = 33%', () => {
  assert.equal(state.pipeline.firstPass.value, 33);
});
test('stuck games: lantern-heist is waiting for the owner; ember-market is not stuck', () => {
  assert.deepEqual(state.pipeline.stuck.map((s) => s.slug), ['lantern-heist']);
});
test('room cards have two numbers each', () => {
  for (const a of state.agents) assert.equal(state.pipeline.rooms[a.id].length, 2, a.id);
  assert.equal(state.pipeline.rooms.playtester[0].value, '8,000');
  assert.equal(state.pipeline.rooms.critic[1].value, 1);
});
test('milestone ticker lists pitch, kill, balance problem and decision', () => {
  const kinds = new Set(state.pipeline.milestones.map((m) => m.kind));
  for (const k of ['pitch', 'kill', 'balance', 'decision']) assert.ok(kinds.has(k), k);
});
test('pipeline numbers with no games do not crash', () => {
  assert.equal(avgRevisionLoops([]).status, 'none');
  assert.equal(stageFunnel([]).every((f) => f.count === 0), true);
});
import { avgRevisionLoops, stageFunnel } from './kpis.js';
