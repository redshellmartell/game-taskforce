// The dashboard's fourth allowed write: a short note from the owner to one agent, saved as games/_notes/<time>-<agent>.md.
// Nothing runs: the Director reads pending notes at the start of a session (see CLAUDE.md), routes or answers them,
// and moves each to games/_notes/_done/ with a reply, which the dashboard then shows.
import fs from 'node:fs';
import path from 'node:path';

export const NOTE_AGENTS = ['manager', 'market-researcher', 'game-designer', 'playtester', 'critic', 'test-panel'];
const MAX_NOTE = 4000;
function fail(status, message) { const e = new Error(message); e.status = status; throw e; }

export function saveNote(gamesDir, { agent, game, note }, now = Date.now()) {
  if (!NOTE_AGENTS.includes(agent)) fail(400, 'Pick one of the agents.');
  const text = String(note ?? '').trim();
  if (!text) fail(400, 'Write a note first.');
  if (text.length > MAX_NOTE) fail(400, `The note is too long (max ${MAX_NOTE} characters).`);
  const slug = game == null || game === '' ? null : String(game);
  if (slug && !/^[a-z0-9][a-z0-9-]{0,80}$/.test(slug)) fail(400, 'That game name is not valid.');
  const dir = path.join(gamesDir, '_notes');
  fs.mkdirSync(dir, { recursive: true });
  const stamp = new Date(now).toISOString().replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z');
  let name = `${stamp}-${agent}.md`, n = 1;
  while (fs.existsSync(path.join(dir, name))) name = `${stamp}-${agent}-${++n}.md`;
  const body = `---\nagent: ${agent}\ngame: ${slug || ''}\nsubmitted: ${new Date(now).toISOString()}\n---\n\n${text}\n`;
  const tmp = path.join(dir, `.${name}.tmp`);
  fs.writeFileSync(tmp, body);
  fs.renameSync(tmp, path.join(dir, name));
  return { file: `games/_notes/${name}`, agent, game: slug };
}

function parseNote(file, text, done) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  const fm = {}; (m ? m[1] : '').split(/\r?\n/).forEach((l) => { const i = l.indexOf(':'); if (i > 0) fm[l.slice(0, i).trim()] = l.slice(i + 1).trim(); });
  const rest = (m ? m[2] : text).trim();
  const r = rest.split(/\n+## Director's reply\s*\n+/i);
  return { file, agent: fm.agent || null, game: fm.game || null, submitted: fm.submitted || null, text: r[0].trim(), reply: r[1] ? r[1].trim() : null, done };
}

export function listNotes(gamesDir) {
  const out = [];
  for (const [sub, done] of [['', false], ['_done', true]]) {
    const dir = path.join(gamesDir, '_notes', sub);
    let files = [];
    try { files = fs.readdirSync(dir).filter((f) => f.endsWith('.md') && !f.startsWith('.')); } catch { continue; }
    for (const f of files) {
      try { out.push(parseNote(`games/_notes/${sub ? `${sub}/` : ''}${f}`, fs.readFileSync(path.join(dir, f), 'utf8'), done)); } catch { /* unreadable note: skip */ }
    }
  }
  return out.sort((a, b) => (b.submitted || '').localeCompare(a.submitted || ''));
}
