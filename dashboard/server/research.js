// The dashboard's fifth allowed write: asking the Market Intel agent for research.
// Clicking "Run this" in the popup is the owner's explicit approval, so it records an ALREADY-APPROVED request in
// games/approvals.json. Nothing runs: the Director carries it out on "continue with approved work" (see CLAUDE.md).
import fs from 'node:fs';

export const KINDS = {
  'game-research': { gate: 'scan', label: 'Game research (market scan)', usage: 'XL',
    summary: 'Run a market scan to fill the idea bank (owner request from the dashboard).',
    why: 'Fill the idea bank with scored, focus-aware ideas (card games, card-heavy games with a few small components, tabletop RPGs) so new games start from a cheap brief.',
    outcome: 'New scored ideas in research/idea-bank.json (target: 8-12) and an updated research/market-scan.md.' },
  'persona-research': { gate: 'panel-research', label: 'Persona research', usage: 'XL',
    summary: 'Refresh the evidence behind the test-panel personas and re-run calibration (owner request from the dashboard).',
    why: 'Build stronger playtesting profiles: current evidence is thin (search summaries only) and the trust flags are provisional.',
    outcome: 'Refreshed panel/evidence/<persona>.md files and an updated panel/calibration.json.' },
  reanalyze: { gate: 'deep-research', label: 'Reanalyze pipeline games', usage: null,
    summary: 'Deeper research on selected pipeline games (owner request from the dashboard).',
    why: 'Re-check the nearest comparable games, originality and market fit for each selected game, and look for new insights.',
    outcome: 'games/<slug>/research-update.md (and research-update.json) for each selected game.' },
};
const MAX_GAMES = 12;
function fail(status, message) { const e = new Error(message); e.status = status; throw e; }
const usageFor = (n) => (n <= 2 ? 'M' : n <= 5 ? 'L' : 'XL');

// Games that can be reanalysed: in the pipeline, not killed or archived.
export function pipelineGames(statusFile) {
  let st; try { st = JSON.parse(fs.readFileSync(statusFile, 'utf8')); } catch { return []; }
  return (st.games || []).filter((g) => g && g.slug && !['killed', 'archived'].includes(g.stage)).map((g) => ({ slug: g.slug, title: g.title || g.slug, stage: g.stage }));
}

export function requestResearch(approvalsFile, decisionsFile, statusFile, { kind, games, note }, now = Date.now()) {
  const k = KINDS[kind];
  if (!k) fail(400, 'Pick one of the three research buttons.');
  const notes = note == null ? '' : String(note).trim();
  if (notes.length > 2000) fail(400, 'The note is too long (max 2000 characters).');
  let targets = null;
  if (kind === 'reanalyze') {
    const ok = new Set(pipelineGames(statusFile).map((g) => g.slug));
    targets = [...new Set(Array.isArray(games) ? games.map(String) : [])];
    if (targets.length === 0) fail(400, 'Tick at least one game.');
    if (targets.length > MAX_GAMES) fail(400, `Pick at most ${MAX_GAMES} games at a time.`);
    if (targets.some((s) => !ok.has(s))) fail(400, 'One of those games is not in the pipeline.');
  } else if (games && games.length) fail(400, 'This research does not take a list of games.');
  let data = { requests: [] };
  try { data = JSON.parse(fs.readFileSync(approvalsFile, 'utf8')); if (!Array.isArray(data.requests)) data.requests = []; } catch { /* no file yet */ }
  let recorded = '';
  try { recorded = (JSON.parse(fs.readFileSync(decisionsFile, 'utf8')).decisions || []).map((d) => String(d.notes || '')).join(' '); } catch { /* none yet */ }
  const open = data.requests.find((r) => r && r.research_kind === kind && (r.status === 'pending' || (r.status === 'approved' && !recorded.includes(r.id))) && (kind !== 'reanalyze' || JSON.stringify([...(r.targets || [])].sort()) === JSON.stringify([...targets].sort())));
  if (open) fail(409, 'The same research is already waiting to be run. Say "continue with approved work" to the Director.');
  const when = new Date(now).toISOString();
  const id = `research-${kind}-${when.replace(/[-:]/g, '').replace(/\.\d+Z$/, 'Z').toLowerCase()}`;
  const usage = k.usage || usageFor(targets.length);
  const req = {
    id, gate: k.gate, game: null, research_kind: kind, ...(targets ? { targets } : {}), time: when, status: 'approved',
    summary: kind === 'reanalyze' ? `${k.summary} Games: ${targets.join(', ')}.` : k.summary, why_needed: k.why, expected_outcome: k.outcome,
    usage_estimate: usage, recommendation: 'approve', options: [{ key: 'approve', label: 'Run it' }],
    decision: 'approve', decided_at: when, owner_notes: notes || 'requested and approved from the dashboard',
  };
  data.requests.push(req);
  const tmp = `${approvalsFile}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n');
  fs.renameSync(tmp, approvalsFile);
  return { id, gate: k.gate, usage_estimate: usage, targets };
}

// What looks due, shown as hints (never run automatically).
export function researchHints({ bank, calibrated, games, now = Date.now(), fileTimes = {} }) {
  const DAY = 86400000;
  const days = (iso) => { const t = Date.parse(iso); return Number.isNaN(t) ? null : Math.floor((now - t) / DAY); };
  return {
    scan: bank ? { lastScan: bank.lastScan, days: bank.scanAgeDays, strongBanked: bank.strongBanked, due: !!bank.needsScan, reasons: bank.scanReasons } : null,
    personas: { updated: calibrated || null, days: days(calibrated), due: calibrated ? (days(calibrated) ?? 0) > 30 : true },
    games: (games || []).filter((g) => !['killed', 'archived'].includes(g.stage)).map((g) => {
      const t = fileTimes[g.slug] ?? null;
      return { slug: g.slug, title: g.title, stage: g.stage, revision: g.revision || 0, lastResearch: t ? new Date(t).toISOString() : null, days: t ? Math.floor((now - t) / DAY) : null };
    }),
  };
}
