// The owner's idea inbox. The dashboard's only write: it saves one Markdown file per idea
// into games/_inbox/. It never starts an agent; the Director picks the file up when asked.
import fs from 'node:fs';
import path from 'node:path';

// Where the idea enters the pipeline. Earlier stages are skipped; the owner's material stands in for them.
export const ENTRY_STAGES = ['research', 'design', 'playtest', 'critique', 'pitch'];
const MAX_TITLE = 120;
const MAX_NOTES = 60000;

export function slugify(text) {
  return String(text).toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 50).replace(/-+$/, '');
}

function fail(status, message) { const e = new Error(message); e.status = status; throw e; }

export function saveIdea(gamesDir, { title, notes, stage }) {
  const cleanTitle = String(title || '').replace(/[\r\n]+/g, ' ').trim();
  const cleanNotes = String(notes || '').trim();
  if (!cleanTitle) fail(400, 'Please give the idea a title.');
  if (cleanTitle.length > MAX_TITLE) fail(400, `Title is too long (max ${MAX_TITLE} characters).`);
  if (cleanNotes.length > MAX_NOTES) fail(400, 'Notes are too long.');
  if (!ENTRY_STAGES.includes(stage)) fail(400, 'Unknown starting stage.');
  const base = slugify(cleanTitle);
  if (!base) fail(400, 'The title needs some letters or numbers.');

  const dir = path.join(gamesDir, '_inbox');
  fs.mkdirSync(dir, { recursive: true });
  const body = `---\ntitle: ${cleanTitle}\nenter_at: ${stage}\nsubmitted: ${new Date().toISOString()}\n---\n\n${cleanNotes}\n`;
  for (let n = 1; n < 100; n++) {
    const slug = n === 1 ? base : `${base}-${n}`;
    try {
      fs.writeFileSync(path.join(dir, `${slug}.md`), body, { flag: 'wx' }); // never overwrite
      return { slug, file: `games/_inbox/${slug}.md`, stage };
    } catch (e) { if (e.code !== 'EEXIST') throw e; }
  }
  fail(409, 'Too many ideas with that name.');
}

export function listInbox(gamesDir) {
  const dir = path.join(gamesDir, '_inbox');
  let names = [];
  try { names = fs.readdirSync(dir).filter((f) => f.endsWith('.md')); } catch { return []; }
  const out = [];
  for (const f of names) {
    try {
      const text = fs.readFileSync(path.join(dir, f), 'utf8');
      const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
      const fm = {};
      if (m) for (const line of m[1].split(/\r?\n/)) { const i = line.indexOf(':'); if (i > 0) fm[line.slice(0, i).trim()] = line.slice(i + 1).trim(); }
      const slug = f.replace(/\.md$/, '');
      out.push({ slug, title: fm.title || slug, stage: ENTRY_STAGES.includes(fm.enter_at) ? fm.enter_at : 'research', submitted: fm.submitted || null, notes: (m ? m[2] : text).trim().slice(0, 400), file: `games/_inbox/${f}` });
    } catch { /* unreadable idea file: skip */ }
  }
  return out.sort((a, b) => String(b.submitted).localeCompare(String(a.submitted)));
}
