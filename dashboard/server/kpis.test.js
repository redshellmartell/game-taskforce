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
