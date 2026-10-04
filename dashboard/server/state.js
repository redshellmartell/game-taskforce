// Reads the repository (games/, .claude/agents/, agents.json) and builds the one
// JSON object the front end needs. Missing or half-written files are skipped.
import fs from 'node:fs';
import path from 'node:path';
import { computeKpis, gameScorecard, stageFunnel, killRateByStage, cycleTimes, avgRevisionLoops, firstPassRate, stuckGames, roomStats, panelStats, milestones, ownerStats, reviewQueueItems, qualityLab, portfolio, opsStats, ideaBankStats, usageStats, approvalStats } from './kpis.js';
import { listInbox } from './ideas.js';
import { loadPanel } from './panel.js';
import { pitchDecisionFor } from './pitch.js';
import { listNotes } from './notes.js';
import { researchHints } from './research.js';

const AGENT_ORDER = ['market-researcher', 'game-designer', 'playtester', 'critic', 'test-panel', 'manager'];
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

function readText(file) {
  try { return fs.readFileSync(file, 'utf8'); } catch { return null; }
}

function readJsonl(file, needsTime = true) {
  let text;
  try { text = fs.readFileSync(file, 'utf8'); } catch (e) { if (e.code !== 'ENOENT') warn(`could not read ${file}`); return []; }
  const out = [];
  for (const line of text.split('\n')) {
    if (!line.trim()) continue;
    try { const o = JSON.parse(line); if (o && (!needsTime || o.time)) out.push(o); } catch { /* half-written line: skip */ }
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

const PANEL_AGENTS = new Set(['panel-player']);

function loadAgents(repoRoot, agentsJson) {
  const dir = path.join(repoRoot, '.claude', 'agents');
  const found = {};
  try {
    for (const f of fs.readdirSync(dir)) {
      if (!f.endsWith('.md')) continue;
      try {
        const fm = parseFrontmatter(fs.readFileSync(path.join(dir, f), 'utf8'));
        const id = fm.name || f.replace(/\.md$/, '');
        if (PANEL_AGENTS.has(id)) continue;   // persona agents live inside the Playtest Lab's Test panel, not as org-chart boxes
        found[id] = { id, description: fm.description || '', tools: (fm.tools || '').split(',').map((s) => s.trim()).filter(Boolean), file: `.claude/agents/${f}` };
      } catch (e) { warn(`bad agent file ${f}: ${e.message}`); }
    }
  } catch { warn('no .claude/agents folder found'); }
  found.manager = { id: 'manager', description: 'The main Claude Code session. Runs the pipeline, decides what moves forward and reports to the owner.', tools: [], file: null };
  found['test-panel'] = { id: 'test-panel', description: 'The player test panel: five persona bots and reviewers that give each game a public test. Part of the Playtest Lab.', tools: [], file: 'panel/README.md' };
  const ids = [...AGENT_ORDER.filter((id) => found[id]), ...Object.keys(found).filter((id) => !AGENT_ORDER.includes(id))];
  return ids.map((id) => ({ ...found[id], room: agentsJson[id]?.room || id, color: agentsJson[id]?.color || '#888', reportsTo: agentsJson[id]?.reportsTo || (id === 'manager' ? 'owner' : id === 'test-panel' ? 'playtester' : 'manager') }));
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

// The "How it plays" paragraph of a pitch.md, whichever heading style it uses (e.g. "## 4. How it plays").
function extractSection(text, name) {
  if (!text) return null;
  const m = text.match(new RegExp('^#{1,6}\\s*(?:\\d+\\.\\s*)?' + name + '[^\\n]*\\n+([\\s\\S]*?)(?=^#{1,6}\\s|$(?![\\s\\S]))', 'im'));
  const t = m ? m[1].trim() : '';
  return t || null;
}

function titleFromSlug(slug) { return slug.split('-').map((w) => w[0]?.toUpperCase() + w.slice(1)).join(' '); }

// Which agent would run the gated step (a request may name one in an optional `agent` field).
const GATE_AGENT = { scan: 'market-researcher', greenlight: 'game-designer', revision: 'game-designer', 'panel-research': 'market-researcher', 'deep-research': 'market-researcher', 'panel-reviews': 'playtester', budget: 'playtester', 'free-api': 'playtester' };
const EXPIRE_DAYS = 14;
const DAY_MS = 24 * 3600 * 1000;
// Requests the Director wrote to games/approvals.json (see "Approval gates" in CLAUDE.md), with what the owner needs to decide.
function buildApprovals(requests, games, shiftTime, now) {
  if (!Array.isArray(requests)) return { requests: [], pending: 0 };
  const bySlug = Object.fromEntries(games.map((g) => [g.slug, g]));
  const list = requests.filter((r) => r && r.id && r.gate).map((r) => {
    const time = r.time ? shiftTime(r.time) : null;
    const age = time ? Math.max(0, Math.floor((now - Date.parse(time)) / DAY_MS)) : null;
    const state = r.status === 'pending' && age !== null && age > EXPIRE_DAYS ? 'expired' : r.status;
    const g = r.game ? bySlug[r.game] : null;
    const rows = g ? g.scorecard.filter((x) => x.status !== 'none') : [];
    return {
      ...r, time, decided_at: r.decided_at ? shiftTime(r.decided_at) : null, state, ageDays: age, gameTitle: g?.title || r.game || null, agentId: r.agent || GATE_AGENT[r.gate] || null, ownerIdea: !!g?.ownerIdea, verdicts: g?.verdicts || null,
      revision: r.gate === 'revision' && g ? { worthIt: g.critique?.revision_worth_it ?? null, reason: g.critique?.revision_reason || null, scorecard: rows, revisionsDone: g.revision || 0 } : null,
    };
  });
  const pending = list.filter((r) => r.state === 'pending').sort((a, b) => Date.parse(a.time) - Date.parse(b.time));
  const decided = list.filter((r) => r.state !== 'pending').sort((a, b) => Date.parse(b.decided_at || b.time) - Date.parse(a.decided_at || a.time));
  return { requests: [...pending, ...decided], pending: pending.length };
}

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
    const files = listGameFiles(dir, slug).concat(listGameFiles(path.join(dir, 'panel'), `${slug}/panel`).map((f) => ({ ...f, name: `panel/${f.name}`, agent: null })));
    const st = statusBySlug[slug];
    let events = readJsonl(path.join(dir, 'activity.jsonl')).map((e) => ({ ...e, time: shiftTime(e.time), game: e.game || slug }));
    if (events.length === 0) {
      // No activity log yet: show the files that exist as finished steps (marked synthetic).
      events = files.filter((f) => f.agent).map((f) => ({ time: new Date(f.mtime).toISOString(), agent: f.agent, game: slug, event: 'done', message: `${f.name} written`, synthetic: true }));
    }
    // an agent without a clock may guess a time in the future: never show one (clamp to now and mark it approximate)
    events = events.map((e) => (Date.parse(e.time) > now + 60000 ? { ...e, time: new Date(now).toISOString(), time_estimated: true } : e));
    events = events.map((e, i) => ({ ...e, _seq: activity.length + i }));
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
      panel: readJson(path.join(dir, 'panel.json')), conversations: readJsonl(path.join(dir, 'panel', 'conversations.jsonl')).map((c) => ({ ...c, time: shiftTime(c.time) })),
      files, howItPlays: extractSection(readText(path.join(dir, 'pitch.md')), 'How it plays'),
      ownerIdea: st?.source === 'owner' || files.some((f) => f.name === 'idea.md'),   // came from the owner's inbox (see "Owner ideas inbox")
      derived: !st,
    });
  }
  for (const g of games) g.scorecard = gameScorecard(g);
  // newest first; lines with the same time (agents without a clock, clamped times) keep file order, so the LAST line written counts as the latest
  activity.sort((a, b) => (Date.parse(b.time) - Date.parse(a.time)) || ((b._seq ?? 0) - (a._seq ?? 0)));

  // Agent states from the newest activity line of each agent.
  for (const a of agents) {
    const mine = activity.filter((e) => (a.id === 'test-panel' ? String(e.agent).startsWith('panel:') : e.agent === a.id));
    const last = mine[0] || null;
    a.lastEvent = last;
    a.recent = mine.slice(0, 8);
    a.state = 'idle';
    if (last && last.event === 'error') a.state = 'error';
    else if (last && (last.event === 'start' || last.event === 'step') && now - Date.parse(last.time) < WORKING_WINDOW) a.state = 'working';
    a.currentGame = a.state === 'working' ? last.game : null;
    a.reports = games.flatMap((g) => g.files.filter((f) => f.agent === a.id).map((f) => ({ ...f, game: g.slug, gameTitle: g.title }))).sort((x, y) => y.mtime - x.mtime);
  }
  const decisionsEarly = (readJson(path.join(gamesDir, 'decisions.json'))?.decisions || []).map((d) => ({ ...d, time: shiftTime(d.time) }));
  for (const g of games.filter((x) => x.stage === 'owner-review')) {     // a pitch you decided in the dashboard that the Director has not acted on yet
    const h = [...(g.history || [])].reverse().find((e) => e.stage === 'owner-review');
    const since = h ? Date.parse(shiftTime(h.time)) || 0 : 0;
    const d = pitchDecisionFor(g.slug, since, decisionsEarly);
    g.pitchDecision = d ? { decision: d.decision, time: d.time, notes: d.notes || null } : null;
  }
  const waitingPitches = games.filter((g) => g.stage === 'owner-review' && !g.pitchDecision);
  const manager = agents.find((a) => a.id === 'manager');
  if (manager && waitingPitches.length && manager.state === 'idle') manager.state = 'waiting';

  const decisions = (readJson(path.join(gamesDir, 'decisions.json'))?.decisions || []).map((d) => ({ ...d, time: shiftTime(d.time) }));
  const approvals = buildApprovals(readJson(path.join(gamesDir, 'approvals.json'))?.requests, games, shiftTime, now);
  for (const r of approvals.requests.filter((x) => x.state === 'pending')) {       // an agent waiting at a gate shows "waiting for you"
    const a = agents.find((x) => x.id === (r.agent || GATE_AGENT[r.gate]));
    if (a && !a.waitingGate) { a.waitingGate = { id: r.id, gate: r.gate, game: r.game, gameTitle: r.gameTitle }; if (a.state === 'idle' || a.state === 'waiting') a.state = 'waiting'; }
  }
  const settingsFile = readJson(path.join(repoRoot, 'studio-settings.json')) || {};
  const settings = { approval_mode: settingsFile.approval_mode || 'normal' };
  const kpis = computeKpis(games, agents, now);
  const bankFile = readJson(path.join(sample ? path.join(dashboardDir, 'sample-data') : repoRoot, 'research', 'idea-bank.json'));
  const bankStats = ideaBankStats(bankFile, now);
  const usageDir = path.join(sample ? path.join(dashboardDir, 'sample-data') : repoRoot, 'usage');
  const usageSessions = readJsonl(path.join(usageDir, 'sessions.jsonl'), false).map((x) => ({ ...x, by_day: (x.by_day || []).map((b) => ({ ...b, name: sample ? shiftTime(`${b.name}T12:00:00Z`).slice(0, 10) : b.name })) }));
  const guard = readJson(path.join(usageDir, 'guard.json'));
  const panel = loadPanel(repoRoot);
  const panelData = panelStats(panel, games, activity);
  const stuck = stuckGames(games, activity, now);
  const pipeline = {
    funnel: stageFunnel(games), killRate: killRateByStage(games), cycleTimes: cycleTimes(games),
    avgRevisions: avgRevisionLoops(games), firstPass: firstPassRate(games), stuck,
    rooms: roomStats(games, agents, stuck, bankStats, panelData), milestones: milestones(games, decisions),
  };
  const review = { ...ownerStats(games, decisions), queue: reviewQueueItems(games, now) };

  return { sample, generatedAt: new Date(now).toISOString(), agents, games, activity: activity.slice(0, 500), decisions, approvals, settings, inbox: listInbox(gamesDir), notes: listNotes(gamesDir), research: researchHints({ bank: bankStats, calibrated: panel?.calibrated || null, games, now, fileTimes: Object.fromEntries(games.map((g) => { const f = g.files.find((x) => x.name === 'research-update.md'); return [g.slug, f ? f.mtime : null]; })) }), panel: panel && { ...panel, stats: panelData }, kpis, pipeline, review, quality: qualityLab(games), market: { ...portfolio(games), ideaBank: bankFile && bankStats ? { ...bankStats, updated: bankFile.updated || null, ideas: bankFile.ideas } : null }, ops: { ...opsStats(games, agents, activity, now), usage: usageStats(usageSessions, games, now), guard, approvals: approvalStats(approvals.requests) }, waitingPitches: waitingPitches.map((g) => g.slug) };
}
