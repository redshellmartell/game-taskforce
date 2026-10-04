import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { saveNote, listNotes } from './notes.js';

const tmpGames = () => fs.mkdtempSync(path.join(os.tmpdir(), 'notes-'));

test('saveNote writes one file in games/_notes with a header and your text', () => {
  const g = tmpGames();
  const r = saveNote(g, { agent: 'game-designer', game: 'duelflip', note: '  Please try a 3-card hand.  ' }, Date.parse('2026-10-04T12:00:00Z'));
  assert.match(r.file, /^games\/_notes\/20261004T120000Z-game-designer\.md$/);
  const text = fs.readFileSync(path.join(g, '_notes', '20261004T120000Z-game-designer.md'), 'utf8');
  assert.match(text, /agent: game-designer/); assert.match(text, /game: duelflip/); assert.match(text, /Please try a 3-card hand\./);
  assert.deepEqual(fs.readdirSync(path.join(g, '_notes')), ['20261004T120000Z-game-designer.md']);   // no temp file left behind
});
test('two notes in the same second never overwrite each other', () => {
  const g = tmpGames(); const t = Date.parse('2026-10-04T12:00:00Z');
  saveNote(g, { agent: 'critic', note: 'one' }, t); saveNote(g, { agent: 'critic', note: 'two' }, t);
  assert.equal(fs.readdirSync(path.join(g, '_notes')).length, 2);
});
test('bad input is refused: unknown agent, empty or huge note, bad game name', () => {
  const g = tmpGames();
  for (const bad of [{ agent: 'hacker', note: 'x' }, { agent: 'critic', note: '   ' }, { agent: 'critic', note: 'x'.repeat(4001) }, { agent: 'critic', note: 'x', game: '../etc' }, { agent: '../x', note: 'x' }])
    assert.throws(() => saveNote(g, bad), (e) => e.status === 400);
  assert.equal(fs.existsSync(path.join(g, '_notes')), false);
});
test('listNotes shows pending notes and answered ones with the Director\'s reply', () => {
  const g = tmpGames(); saveNote(g, { agent: 'playtester', game: 'g1', note: 'Test 3 players too.' }, Date.parse('2026-10-04T12:00:00Z'));
  fs.mkdirSync(path.join(g, '_notes', '_done'));
  fs.writeFileSync(path.join(g, '_notes', '_done', 'a.md'), '---\nagent: critic\ngame:\nsubmitted: 2026-10-03T10:00:00Z\n---\n\nIs it original?\n\n## Director\'s reply\n\nYes, medium similarity to Wizard.\n');
  const l = listNotes(g);
  assert.equal(l.length, 2); assert.equal(l[0].done, false); assert.equal(l[0].text, 'Test 3 players too.'); assert.equal(l[0].reply, null);
  assert.equal(l[1].done, true); assert.equal(l[1].reply, 'Yes, medium similarity to Wizard.'); assert.equal(l[1].text, 'Is it original?');
  assert.deepEqual(listNotes(tmpGames()), []);
});
