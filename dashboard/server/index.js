// Read-only server for the Think Tank dashboard.
//   GET /api/state   one JSON object with agents, games, activity and KPIs
//   GET /api/file    the text of one Markdown report (games/ and .claude/agents/ only)
//   GET /api/events  Server-Sent Events: a "changed" message when a watched file changes
import express from 'express';
import chokidar from 'chokidar';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildState } from './state.js';
import { saveIdea } from './ideas.js';
import { decideApproval } from './approvals.js';
import { decidePitch } from './pitch.js';

const dashboardDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = path.resolve(dashboardDir, '..');
const demoFlag = process.argv.includes('--demo');
const PORT = Number(process.env.PORT) || 4173;

function hasRealGames() {
  try { return fs.readdirSync(path.join(repoRoot, 'games'), { withFileTypes: true }).some((d) => d.isDirectory() && !d.name.startsWith('_')); }
  catch { return false; }
}
const useSample = () => demoFlag || !hasRealGames();

const app = express();
app.use(express.json({ limit: '200kb' }));

// Save one of the owner's own ideas into games/_inbox/ (the dashboard's only write; it never starts an agent).
app.post('/api/ideas', (req, res) => {
  const origin = req.get('origin');
  if (origin && new URL(origin).host !== req.get('host')) return res.status(403).json({ error: 'Not allowed' }); // only this page may save ideas
  if (useSample()) return res.status(409).json({ error: 'The dashboard is showing sample data, so ideas are not saved. Run npm start (not npm run demo) in a copy of the repository that has a games/ folder.' });
  try { res.json(saveIdea(path.join(repoRoot, 'games'), req.body || {})); }
  catch (e) { res.status(e.status || 500).json({ error: e.status ? e.message : 'Could not save the idea.' }); }
});

app.get('/api/state', (req, res) => {
  try { res.json(buildState({ repoRoot, dashboardDir, sample: useSample() })); }
  catch (e) { console.warn('[dashboard] state error:', e.message); res.status(500).json({ error: 'Could not build state' }); }
});

// Record the owner's decision on one approval request (the dashboard's second write; it never starts an agent).
app.post('/api/approvals/:id', (req, res) => {
  const origin = req.get('origin');
  if (origin && new URL(origin).host !== req.get('host')) return res.status(403).json({ error: 'Not allowed' });
  if (useSample()) return res.status(409).json({ error: 'The dashboard is showing sample data, so decisions are not saved. Run npm start in a copy of the repository that has real games.' });
  try { res.json(decideApproval(path.join(repoRoot, 'games', 'approvals.json'), req.params.id, (req.body || {}).decision, (req.body || {}).notes)); }
  catch (e) { res.status(e.status || 500).json({ error: e.status ? e.message : 'Could not record the decision.' }); }
});

// Record the owner's decision on a pitch in the Review Queue (appends to games/decisions.json only; never starts an agent).
app.post('/api/pitch/:slug', (req, res) => {
  const origin = req.get('origin');
  if (origin && new URL(origin).host !== req.get('host')) return res.status(403).json({ error: 'Not allowed' });
  if (useSample()) return res.status(409).json({ error: 'The dashboard is showing sample data, so decisions are not saved. Run npm start in a copy of the repository that has real games.' });
  try { res.json(decidePitch(path.join(repoRoot, 'games', 'decisions.json'), path.join(repoRoot, 'games', 'status.json'), req.params.slug, (req.body || {}).decision, (req.body || {}).notes)); }
  catch (e) { res.status(e.status || 500).json({ error: e.status ? e.message : 'Could not record the decision.' }); }
});

// Only Markdown files inside games/ (or sample-data/games/) and .claude/agents/ may be read.
app.get('/api/file', (req, res) => {
  const rel = String(req.query.path || '').replace(/\\/g, '/');
  const isAgent = rel.startsWith('.claude/agents/');
  const isPanel = /^panel\/(personas|evidence)\//.test(rel);   // persona profiles and their research evidence (not game data, so never sample)
  const isGame = rel.startsWith('games/');
  if ((!isAgent && !isGame && !isPanel) || !rel.endsWith('.md') || rel.includes('..')) return res.status(400).json({ error: 'Not allowed' });
  const base = isAgent || isPanel || !useSample() ? repoRoot : path.join(dashboardDir, 'sample-data');
  const full = path.resolve(base, rel);
  const allowedRoot = path.resolve(base, isAgent ? '.claude/agents' : isPanel ? rel.split('/').slice(0, 2).join('/') : 'games');
  if (!full.startsWith(allowedRoot + path.sep)) return res.status(400).json({ error: 'Not allowed' });
  try { res.json({ path: rel, text: fs.readFileSync(full, 'utf8') }); }
  catch { res.status(404).json({ error: 'No such file yet' }); }
});

const clients = new Set();
app.get('/api/events', (req, res) => {
  res.set({ 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
  res.write('retry: 2000\n\n');
  clients.add(res);
  req.on('close', () => clients.delete(res));
});

let timer = null;
function notifyChanged() {
  clearTimeout(timer);
  timer = setTimeout(() => { for (const c of clients) c.write('event: changed\ndata: {}\n\n'); }, 300);
}
const watchPaths = [path.join(repoRoot, 'games'), path.join(repoRoot, '.claude', 'agents'), path.join(dashboardDir, 'agents.json'), path.join(dashboardDir, 'sample-data'), path.join(repoRoot, 'research'), path.join(repoRoot, 'usage'), path.join(repoRoot, 'panel')];
chokidar.watch(watchPaths, { ignoreInitial: true, ignored: /(__pycache__|\.pyc$|\/sim\/)/, awaitWriteFinish: { stabilityThreshold: 150, pollInterval: 50 } })
  .on('all', notifyChanged).on('error', (e) => console.warn('[dashboard] watcher:', e.message));
setInterval(() => { for (const c of clients) c.write(': ping\n\n'); }, 25000); // keep connections open

if (!process.argv.includes('--dev')) {
  const dist = path.join(dashboardDir, 'dist');
  app.use(express.static(dist));
  app.get('*', (req, res) => res.sendFile(path.join(dist, 'index.html')));
}

app.listen(PORT, () => {
  console.log(`\nThink Tank dashboard: http://localhost:${PORT}  (${useSample() ? 'sample data' : 'real games'})\n`);
});
