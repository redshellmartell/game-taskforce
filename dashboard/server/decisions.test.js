// Checks that recording a pitch verdict only appends to decisions.json and refuses bad input. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { recordDecision } from './decisions.js';

const NOW = Date.parse('2026-10-04T12:00:00Z');
const tmp = () => path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'dec-')), 'decisions.json');
const code = (fn) => { try { fn(); return null; } catch (e) { return e.status; } };

test('appends a verdict and keeps earlier decisions', () => {
  const f = tmp(); fs.writeFileSync(f, JSON.stringify({ decisions: [{ slug: 'a', decision: 'approve' }] }));
  const e = recordDecision(f, 'duelflip', 'send-back', 'fix the twists', NOW);
  assert.equal(e.decision, 'send-back'); assert.equal(e.time, '2026-10-04T12:00:00.000Z');
  const d = JSON.parse(fs.readFileSync(f, 'utf8')).decisions;
  assert.equal(d.length, 2); assert.equal(d[0].slug, 'a'); assert.match(d[1].notes, /fix the twists/);
});
test('creates the file when missing', () => {
  const f = tmp(); recordDecision(f, 'duelflip', 'reject', '', NOW);
  assert.equal(JSON.parse(fs.readFileSync(f, 'utf8')).decisions.length, 1);
});
test('refuses bad slug, bad verdict and long notes', () => {
  const f = tmp();
  assert.equal(code(() => recordDecision(f, '../x', 'approve', '', NOW)), 400);
  assert.equal(code(() => recordDecision(f, 'duelflip', 'delete', '', NOW)), 400);
  assert.equal(code(() => recordDecision(f, 'duelflip', 'approve', 'x'.repeat(2001), NOW)), 400);
});
