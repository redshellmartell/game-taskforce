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

// ---- Milestone 4 ----
test('how-it-plays paragraph is pulled out of pitch.md', () => {
  const g = state.games.find((x) => x.slug === 'lantern-heist');
  assert.match(g.howItPlays, /secretly bids one card/);
  assert.doesNotMatch(g.howItPlays, /Components/);
});
test('review queue: one pitch with cost, components and passing KPIs', () => {
  const q = state.review.queue;
  assert.equal(q.length, 1); assert.equal(q[0].slug, 'lantern-heist');
  assert.equal(q[0].cost, 18); assert.equal(q[0].components.length, 2);
  assert.ok(q[0].days >= 6); assert.ok(q[0].passing >= 8);
});
test('owner stats: 0% approval (one rejection), human score 3.7, no gap between critic and human fun', () => {
  const r = state.review;
  assert.equal(r.approvalRate.value, 0);
  assert.equal(r.humanScore.value, 3.7); assert.equal(r.humanScore.sessions, 1);
  assert.equal(r.gap.value, 0); assert.equal(r.gap.status, 'good');
  assert.equal(r.prototypes.value, 0);
});
test('owner stats with no decisions or playtests are "none", not a crash', () => {
  const r = ownerStats([], []);
  assert.equal(r.approvalRate.status, 'none'); assert.equal(r.gap.status, 'none'); assert.equal(r.humanScore.value, null);
});
test('quality lab: recurring problem types and first-pass trend', () => {
  const q = state.quality;
  const types = Object.fromEntries(q.recurring.map((r) => [r.type, r.games]));
  assert.equal(types['Runaway leader'], 1); assert.equal(types['Rules ambiguity'], 1); assert.equal(types['Overpowered content'], 1);
  assert.equal(q.firstPass.length, 3); assert.equal(q.firstPass[q.firstPass.length - 1].rate, 33);
  assert.equal(q.criticByRevision.length >= 1, true);
});
test('portfolio: mechanics, brief count, comparables and unexplored mechanics', () => {
  const m = state.market;
  assert.equal(m.briefs, 3);
  assert.equal(m.opportunity[0].title, 'Lantern Heist');
  assert.ok(m.mechanics.some((x) => x.name === 'push-your-luck'));
  assert.ok(m.unexplored.includes('worker placement') && !m.unexplored.includes('push-your-luck'));
  assert.equal(m.comparables.find((c) => c.slug === 'lantern-heist').status, 'good');
  assert.equal(m.comparables.find((c) => c.slug === 'ember-market').status, 'warn'); // only 1 comparable
  assert.equal(m.topMechanic.status, 'good'); // 1 of 3 = 33%
});
test('ops: runs per agent, no failures, simulated games', () => {
  const o = state.ops;
  assert.equal(o.perAgent.length, 5);
  assert.equal(o.perAgent.find((a) => a.id === 'game-designer').runs, 2);
  assert.equal(o.perAgent.reduce((a, x) => a + x.runs, 0), 8);
  assert.ok(o.perAgent.every((x) => x.errors === 0));
  assert.equal(o.simulated.total, 8000);
  assert.equal(o.daily.length, 7);
  assert.equal(o.failureRate.status === 'good' || o.failureRate.status === 'none', true);
  assert.equal(o.usagePerPitch, null);
});
test('ops: a failed run shows up in the failure rate', () => {
  const now = Date.now();
  const iso = (m) => new Date(now - m * 60000).toISOString();
  const act = [{ time: iso(5), agent: 'critic', game: 'x', event: 'error', message: 'boom' }, { time: iso(10), agent: 'critic', game: 'x', event: 'done', message: 'ok' }];
  const o = opsStats([], [{ id: 'critic', room: 'Review Board', color: '#000', state: 'error' }], act, now);
  assert.equal(o.perAgent[0].failureRate, 50); assert.equal(o.failureRate.status, 'bad');
});
test('portfolio of no games does not crash', () => {
  const m = portfolio([]);
  assert.equal(m.briefs, 0); assert.equal(m.topMechanic, null);
});
import { ownerStats, portfolio, opsStats, ideaBankStats, usageStats } from './kpis.js';

// ---- Idea bank ----
test('idea bank (sample): counts by status and a scan is needed (only 3 strong banked ideas, scan 21+ days old but under 30 is fine)', () => {
  const b = state.market.ideaBank;
  assert.equal(b.total, 8); assert.equal(b.inPipeline, 2); assert.equal(b.rejected, 2); assert.equal(b.banked, 4);
  assert.equal(b.strongBanked, 4);
  assert.equal(b.needsScan, false);
});
test('idea bank rule: fewer than 3 strong banked ideas, or a scan over 30 days old, means a scan is needed', () => {
  const now = Date.parse('2026-10-03T00:00:00Z');
  const few = ideaBankStats({ last_scan: '2026-10-01', ideas: [{ status: 'banked', score: 22 }, { status: 'banked', score: 17 }] }, now);
  assert.equal(few.needsScan, true); assert.match(few.scanReasons[0], /only 1 banked idea/);
  const old = ideaBankStats({ last_scan: '2026-08-01', ideas: [1, 2, 3].map(() => ({ status: 'banked', score: 20 })) }, now);
  assert.equal(old.needsScan, true); assert.equal(old.scanAgeDays, 63);
  const fine = ideaBankStats({ last_scan: '2026-09-20', ideas: [1, 2, 3].map(() => ({ status: 'banked', score: 18 })) }, now);
  assert.equal(fine.needsScan, false);
});
test('idea bank: missing or broken file gives null, not a crash', () => {
  assert.equal(ideaBankStats(null), null); assert.equal(ideaBankStats({}), null);
});
test('Market Intel room card shows briefs written and ideas banked', () => {
  const r = state.pipeline.rooms['market-researcher'];
  assert.equal(r[0].label, 'Briefs written'); assert.equal(r[1].label, 'Ideas banked'); assert.equal(r[1].value, 4);
});

// ---- Usage ----
test('usage (sample): totals by agent, game and week, and usage per pitched game in tokens', () => {
  const u = state.ops.usage;
  assert.equal(u.total, 5060000 + 3400000);
  assert.equal(u.byAgent[0].name, 'director'); assert.equal(u.byAgent[0].tokens, 5600000);
  assert.equal(u.byGame.find((g) => g.name === 'lantern-heist').tokens, 2900000);
  assert.equal(u.perPitched.pitched, 1); assert.equal(u.perPitched.value, u.total);   // one pitched game (lantern-heist)
  assert.ok(u.byWeek.length >= 2);
});
test('usage: nothing recorded gives null, and a game count of zero gives no per-pitch number', () => {
  assert.equal(usageStats([], []), null); assert.equal(usageStats(null, []), null);
  const u = usageStats([{ by_day: [{ name: '2026-10-01', weighted_tokens: 100 }] }], [], Date.parse('2026-10-03T00:00:00Z'));
  assert.equal(u.perPitched.value, null); assert.equal(u.total, 100); assert.equal(u.last7days, 100);
});
test('usage guard status from guard.json reaches the Ops data', () => {
  assert.equal(state.ops.guard.status, 'warn'); assert.equal(state.ops.guard.windows[0].percent, 68);
});
