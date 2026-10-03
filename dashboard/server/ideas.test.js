// Checks the idea inbox: saving, never overwriting, and rejecting bad input. Run with: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { saveIdea, listInbox, slugify } from './ideas.js';

const tmp = () => fs.mkdtempSync(path.join(os.tmpdir(), 'inbox-'));

test('slugify makes safe folder names', () => {
  assert.equal(slugify('  Ember Market! '), 'ember-market');
  assert.equal(slugify('../../etc/passwd'), 'etc-passwd');
  assert.equal(slugify('!!!'), '');
});
test('saveIdea writes a file inside games/_inbox and listInbox reads it back', () => {
  const dir = tmp();
  const r = saveIdea(dir, { title: 'Moth Market', notes: 'Bluffing game about moths.', stage: 'design' });
  assert.equal(r.file, 'games/_inbox/moth-market.md');
  const list = listInbox(dir);
  assert.equal(list.length, 1);
  assert.equal(list[0].title, 'Moth Market');
  assert.equal(list[0].stage, 'design');
  assert.match(list[0].notes, /Bluffing/);
});
test('saving the same title twice never overwrites', () => {
  const dir = tmp();
  saveIdea(dir, { title: 'Same', notes: 'one', stage: 'research' });
  const second = saveIdea(dir, { title: 'Same', notes: 'two', stage: 'research' });
  assert.equal(second.slug, 'same-2');
  assert.match(fs.readFileSync(path.join(dir, '_inbox', 'same.md'), 'utf8'), /one/);
});
test('bad input is rejected with a 400', () => {
  const dir = tmp();
  for (const bad of [{ title: '', stage: 'design' }, { title: 'x', stage: 'nope' }, { title: '???', stage: 'design' }]) {
    assert.throws(() => saveIdea(dir, bad), (e) => e.status === 400);
  }
});
test('an empty or missing inbox lists nothing', () => {
  assert.deepEqual(listInbox(tmp()), []);
  assert.deepEqual(listInbox('/definitely/not/here'), []);
});
