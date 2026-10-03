// Learn mode texts live in src/content/learn/*.md so they are easy to edit.
// Each file: a small header (title, link = a file in the repository) and 2-3 sentences of explanation.
const raw = import.meta.glob('./content/learn/*.md', { query: '?raw', import: 'default', eager: true });

export const REPO_URL = 'https://github.com/redshellmartell/game-taskforce/blob/main/';

export const topics = Object.fromEntries(Object.entries(raw).map(([file, text]) => {
  const id = file.split('/').pop().replace(/\.md$/, '');
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/);
  const fm = {};
  (m ? m[1] : '').split(/\r?\n/).forEach((line) => { const i = line.indexOf(':'); if (i > 0) fm[line.slice(0, i).trim()] = line.slice(i + 1).trim(); });
  return [id, { id, title: fm.title || id, link: fm.link || null, body: (m ? m[2] : text).trim() }];
}));
