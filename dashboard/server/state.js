// Reads the repository (games/, .claude/agents/, agents.json) and builds the one
// JSON object the front end needs. Missing or half-written files are skipped.
import fs from 'node:fs';
import path from 'node:path';
import { computeKpis, gameScorecard } from './kpis.js';
import { listInbox } from './ideas.js';

const AGENT_ORDER = ['market-researcher', 'game-designer', 'playtester', 'critic', 'manager'];
// Which report each agent writes (used for "Its work" and for the handoff lines).
export const AGENT_FILES = {
  'market-researcher': 'brief.md',
  'game-designer': 'rules.md',
  playtester: 'playtest-report.md',
  critic: 'critique.md',
  manager: 'pitch.md',
};
const FILE_AGENT = Object.fromEntries(Object.entries(AGENT_FILES).map(([a, f]) => [f, a]));
const MD_FILES = Object.values(AGENT_FILES);
const WORKING_WINDOW = 60 * 60 * 1000; // an agent counts as working for 1h after its last start/step

function warn(msg) { console.warn(`[dashboard] ${msg}`); }

function readJson(file) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (e) { if (e.code !== 'ENOENT') warn(`could not read ${file}: ${e.message}`); return null; }
}

function readJsonl(file) {
  let text;
  try { text = fs.readFileSync(file, 'utf8'); } catch (e) { if (e.code !== 'ENOENT') warn(`could not read ${file}`); return []; }
  const out = [];
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    try { const o = JSON.parse(line); if (o && o.time) out.push(o); } catch { /* half-written line: skip */ }
  }
  return out;
}

// Pull name / description / tools out of an agent file's --- frontmatter.
function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const fm = {};
  if (m) for (const line of m[1].split(/\r?\n/)) {
    const i = line.indexOf(':');
    if (i > 0) fm[line.slice(0, i).trim()] = line.slice(i + 1).trim();
  }
  return fm;
}

function loadAgents(repoRoot, agentsJson) {
  const dir = path.join(repoRoot, '.claude', 'agents');
  const found = {};
  try {
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.md')) continue;
      try {
        const fm = parseFrontmatter(fs.readFileSync(path.join(dir, f), 'utf8'));
        const id = fm.name || f.replace(/\.md$/, '');
        found[id] = { id, description: fm.description || '', tools: (fm.tools || '').split(',').map((s) => s.trim()).filter(Boolean), file: `.claude/agents/${f}` };
      } catch (e) { warn(`bad agent file ${f}: ${e.message}`); }
    }
  } catch { warn('no .claude/agents folder found'); }
  found.manager = { id: 'manager', description: 'The main Claude Code session. Runs the pipeline, decides what moves forward and reports to the owner.', tools: [], file: null };
  const ids = [...AGENT_ORDER.filter((id) => found[id]), ...Object.keys(found).filter((id) => !AGENT_ORDER.includes(id))];
  return ids.map((id) => ({ ...found[id], room: agentsJson[id]?.room || id, color: agentsJson[id]?.color || '#888' }));
}

function listGameFiles(dir, slug) {
  const files = [];
  try {
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.md')) continue;
      try {
        const st = fs.statSync(path.join(dir, f));
        files.push({ name: f, path: `games/${slug}/${f}`, mtime: st.mtimeMs, agent: FILE_AGENT[f] || null });
      } catch { /* skip */ }
    }
  } catch { /* skip */ }
  return files;
}

// When status.json has no entry for a game (older runs), work out the stage from its files.
function deriveStage(files, jsons) {
  const has = (n) => files.some((f) => f.name === n);
  if (has('pitch.md') || jsons.pitch) return 'owner-review';
  if (has('critique.md') || jsons.critique) return 'pitch';
  if (has('playtest-report.md') || jsons.playtest) return 'critique';
  if (has('rules.md')) return 'playtest';
  if (has('brief.md') || jsons.brief) return 'design';
  return 'brief';
}

function titleFromSlug(slug) { return slug.split('-').map((w) => w[0]?.toUpperCase() + w.slice(1)).join(' '); }

export function buildState({ repoRoot, dashboardDir, sample, now = Date.now() }) {
  const gamesDir = sample ? path.join(dashboardDir, 'sample-data', 'games') : path.join(repoRoot, 'games');
  const agentsJson = readJson(path.join(dashboardDir, 'agents.json')) || {};
  const agents = loadAgents(repoRoot, agentsJson);
  const statusFile = readJson(path.join(gamesDir, 'status.json'));
  const statusBySlug = Object.fromEntries((statusFile?.games || []).map((g) => [g.slug, g]));

  let slugs = [];
  try { slugs = fs.readdirSync(gamesDir, { withFileTypes: true }).filter((d) => d.isDirectory() && !d.name.startsWith('_')).map((d) => d.name); }
  catch { warn(`no games folder at ${gamesDir}`); }

  // Sample data has fixed dates; shift them so the newest event looks like "a minute ago".
  let shift = 0;
  if (sample) {
    const times = slugs.flatMap((s) => readJsonl(path.join(gamesDir, s, 'activity.jsonl')).map((e) => Date.parse(e.time))).filter((n) => !Number.isNaN(n));
    if (times.length) shift = now - 90 * 1000 - Math.max(...times);
  }
  const shiftTime = (iso) => { const n = Date.parse(iso); return Number.isNaN(n) ? iso : new Date(n + shift).toISOString(); };

  const games = [];
  let activity = [];
  for (const slug of slugs) {
    const dir = path.join(gamesDir, slug);
    const jsons = { brief: readJson(path.join(dir, 'brief.json')), playtest: readJson(path.join(dir, 'playtest.json')), critique: readJson(path.join(dir, 'critique.json')), pitch: readJson(path.join(dir, 'pitch.json')) };
    const files = listGameFiles(dir, slug);
    const st = statusBySlug[slug];
    let events = readJsonl(path.join(dir, 'activity.jsonl')).map((e) => ({ ...e, time: shiftTime(e.time), game: e.game || slug }));
    if (events.length === 0) {
      // No activity log yet: show the files that exist as finished steps (marked synthetic).
      events = files.filter((f) => f.agent).map((f) => ({ time: new Date(f.mtime).toISOString(), agent: f.agent, game: slug, event: 'done', message: `${f.name} written`, synthetic: true }));
    }
    activity = activity.concat(events);
    games.push({
      slug,
      title: st?.title || jsons.pitch?.title || jsons.brief?.title || titleFromSlug(slug),
      stage: st?.stage || deriveStage(files, jsons),
      revision: st?.revision ?? 0,
      history: (st?.history || []).map((h) => ({ ...h, time: shiftTime(h.time) })),
      verdicts: st?.verdicts || { playtest: jsons.playtest?.verdict ?? null, critic: jsons.critique?.verdict ?? null },
      kill_reason: st?.kill_reason ?? null,
      brief: jsons.brief, playtest: jsons.playtest, critique: jsons.critique, pitch: jsons.pitch,
      humanPlaytests: readJson(path.join(dir, 'human-playtests.json'))?.sessions || [],
      files,
      derived: !st,
    });
  }
  for (const g of games) g.scorecard = gameScorecard(g);
  activity.sort((a, b) => Date.parse(b.time) - Date.parse(a.time));

  // Agent states from the newest activity line of each agent.
  for (const a of agents) {
    const mine = activity.filter((e) => e.agent === a.id);
    const last = mine[0] || null;
    a.lastEvent = last;
    a.recent = mine.slice(0, 8);
    a.state = 'idle';
    if (last && last.event === 'error') a.state = 'error';
    else if (last && (last.event === 'start' || last.event === 'step') && now - Date.parse(last.time) < WORKING_WINDOW) a.state = 'working';
    a.currentGame = a.state === 'working' ? last.game : null;
    a.reports = games.flatMap((g) => g.files.filter((f) => f.agent === a.id).map((f) => ({ ...f, game: g.slug, gameTitle: g.title }))).sort((x, y) => y.mtime - x.mtime);
  }
  const waitingPitches = games.filter((g) => g.stage === 'owner-review');
  const manager = agents.find((a) => a.id === 'manager');
  if (manager && waitingPitches.length && manager.state === 'idle') manager.state = 'waiting';

  const decisions = readJson(path.join(gamesDir, 'decisions.json'))?.decisions || [];
  const kpis = computeKpis(games, agents, now);

  return { sample, generatedAt: new Date(now).toISOString(), agents, games, activity: activity.slice(0, 500), decisions, inbox: listInbox(gamesDir), kpis, waitingPitches: waitingPitches.map((g) => g.slug) };
}
