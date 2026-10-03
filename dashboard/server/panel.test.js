// Checks the test panel loader against the real panel/ folder and a few edge cases. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseFrontmatter, loadPanel } from './panel.js';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');

test('frontmatter: strings, numbers, arrays, trailing comments and the nested weights', () => {
  const fm = parseFrontmatter('---\nid: strategist\nname: The Strategist\ntagline: "If luck decides it, why are we playing?"\nbot_style: planner          # how their bot plays\nweights:                    # sum to 1\n  skill_expression: 0.35\n  lead_changes: 0.10\npreferred_minutes: [45, 120]\n---\nbody');
  assert.equal(fm.id, 'strategist'); assert.equal(fm.tagline, 'If luck decides it, why are we playing?'); assert.equal(fm.bot_style, 'planner');
  assert.deepEqual(fm.weights, { skill_expression: 0.35, lead_changes: 0.1 }); assert.deepEqual(fm.preferred_minutes, [45, 120]);
});
test('the real panel has five personas, each with a profile, evidence file and calibration', () => {
  const p = loadPanel(repoRoot);
  assert.equal(p.personas.length, 5);
  assert.deepEqual(p.personas.map((x) => x.id).sort(), ['casual', 'competitor', 'family', 'story', 'strategist']);
  for (const x of p.personas) {
    assert.ok(fs.existsSync(path.join(repoRoot, x.profile)), x.profile); assert.ok(fs.existsSync(path.join(repoRoot, x.evidence)), x.evidence);
    assert.equal(x.drivers.length, 3); assert.ok(x.calibration.ratedGames >= 6); assert.equal(x.calibration.confidence, 'low');
  }
  assert.equal(p.baselineQuality, 'low');
  const s = p.personas.find((x) => x.id === 'strategist');
  assert.equal(s.drivers[0].metric, 'skill_expression'); assert.equal(s.drivers[0].percent, 35);
});
test('no panel folder, or a broken persona file, does not crash', () => {
  assert.equal(loadPanel('/definitely/not/here'), null);
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'panel-'));
  fs.mkdirSync(path.join(tmp, 'panel', 'personas'), { recursive: true });
  fs.writeFileSync(path.join(tmp, 'panel', 'personas', 'bad.md'), 'no frontmatter at all');
  fs.writeFileSync(path.join(tmp, 'panel', 'personas', 'ok.md'), '---\nid: ok\nname: Okay\n---\n');
  const p = loadPanel(tmp);
  assert.deepEqual(p.personas.map((x) => x.id), ['ok']); assert.equal(p.personas[0].calibration, null);
});
