// KPI maths for the dashboard. Every function returns { value, target, status }
// where status is "good", "warn", "bad" or "none" (no data, or no target).
// Targets come from docs/dashboard-notes.md, section 1.

const IN_DEVELOPMENT = ['brief', 'design', 'playtest', 'critique', 'pitch'];
const PITCHED = ['owner-review', 'approved', 'prototyped'];
const DAY = 24 * 3600 * 1000;

const none = (value = null, target = null) => ({ value, target, status: 'none' });

// KPI: "Concepts in development" (games not yet pitched, killed or archived). Target 1-3.
export function conceptsInDevelopment(games) {
  const n = games.filter((g) => IN_DEVELOPMENT.includes(g.stage)).length;
  const status = n === 0 ? 'none' : n <= 3 ? 'good' : n <= 5 ? 'warn' : 'bad';
  return { value: n, target: '1-3', status };
}

// Did this game ever reach the pitch stage? (used by "Pitch rate")
function wasPitched(g) {
  return PITCHED.includes(g.stage) || (g.history || []).some((h) => h.stage === 'pitch' || h.stage === 'owner-review');
}

// KPI: "Pitch rate" (pitches / briefs started). Target 20-40%.
export function pitchRate(games) {
  if (games.length === 0) return none();
  const pct = Math.round((games.filter(wasPitched).length / games.length) * 100);
  const status = pct >= 20 && pct <= 40 ? 'good' : pct >= 10 && pct <= 60 ? 'warn' : 'bad';
  return { value: pct, target: '20-40%', status };
}

// Average of the six critic scores, using the stored average when there is one.
export function criticAverage(critique) {
  if (!critique) return null;
  if (typeof critique.average === 'number') return critique.average;
  const vals = Object.values(critique.scores || {}).filter((v) => typeof v === 'number');
  return vals.length ? vals.reduce((a, b) => a + b, 0) / vals.length : null;
}

// KPI: "Critic scores" (average at pitch). Target >= 3.5.
export function avgCriticAtPitch(games) {
  const pitched = games.filter(wasPitched).map((g) => criticAverage(g.critique)).filter((v) => v !== null);
  if (pitched.length === 0) return none();
  const avg = Math.round((pitched.reduce((a, b) => a + b, 0) / pitched.length) * 10) / 10;
  const status = avg >= 3.5 ? 'good' : avg >= 3 ? 'warn' : 'bad';
  return { value: avg, target: '3.5+', status };
}

// KPI: "Review queue" (pitches waiting for the owner, and how long). Target: cleared weekly.
export function reviewQueue(games, now = Date.now()) {
  const waiting = games.filter((g) => g.stage === 'owner-review');
  if (waiting.length === 0) return { value: 0, target: 'cleared weekly', status: 'good' };
  const oldest = Math.min(...waiting.map((g) => {
    const h = [...(g.history || [])].reverse().find((e) => e.stage === 'owner-review');
    const ts = h ? Date.parse(h.time) : NaN;
    return Number.isNaN(ts) ? now : ts;
  }));
  return { value: waiting.length, target: 'cleared weekly', status: now - oldest > 7 * DAY ? 'bad' : 'warn', oldest_days: Math.floor((now - oldest) / DAY) };
}

// KPI: "Agents active" (agents working now, out of the total). No target.
export function agentsActive(agents) {
  const working = agents.filter((a) => a.state === 'working').length;
  return { value: working, total: agents.length, target: null, status: 'none' };
}

// All headline KPIs for the top bar.
export function computeKpis(games, agents, now = Date.now()) {
  return {
    concepts: conceptsInDevelopment(games),
    pitchRate: pitchRate(games),
    avgCritic: avgCriticAtPitch(games),
    reviewQueue: reviewQueue(games, now),
    agentsActive: agentsActive(agents),
  };
}

// Scorecard for one game (Game page): each design-quality KPI from docs/dashboard-notes.md section 1
// compared with its target. Rows with no data get status "none" and a null value.
export function gameScorecard(game) {
  const pt = game.playtest, cr = game.critique, br = game.brief;
  const num = (v) => (typeof v === 'number' && !Number.isNaN(v) ? v : null);
  const row = (id, label, value, target, status, unit = '') => ({ id, label, value: value === null ? null : value, unit, target, status: value === null ? 'none' : status });
  const band = (v, good, warnLimit, higherIsBetter) => (higherIsBetter ? (v >= good ? 'good' : v >= warnLimit ? 'warn' : 'bad') : (v <= good ? 'good' : v <= warnLimit ? 'warn' : 'bad'));

  // KPI: "Opportunity score" (brief rubric, target 18+ to proceed)
  const opp = num(br?.opportunity_score);
  // KPI: "Critic scores" (average of six, target 3.5+) and "Originality score" (target 3+)
  const avg = criticAverage(cr);
  const orig = num(cr?.scores?.originality);
  // KPI: "Seat balance" (largest gap from a fair share, points, target 5 or less)
  const gap = num(pt?.seat_balance_gap);
  // KPI: "Skill expression" (strategic minus random win rate, points, target 20+)
  const skill = num(pt?.skill_expression);
  // KPI: "Game length vs target" (simulated minutes vs the brief's target, within 20%)
  const est = num(pt?.length?.estimated_minutes), tgt = num(pt?.length?.target_minutes);
  const lenPct = est !== null && tgt ? Math.round(((est - tgt) / tgt) * 100) : null;
  // KPI: "Lead changes" (average per game, target 2+)
  const lead = num(pt?.lead_changes_mean);
  // KPI: "Runaway leader rate" (share of games won by the halfway leader, target 65% or less)
  const run = num(pt?.runaway_leader_rate);
  const runPct = run === null ? null : Math.round(run * 100);
  // KPI: "Rules ambiguities" (target 0) and "Dead or broken content" (flagged cards, target 0)
  const amb = Array.isArray(pt?.ambiguities) ? pt.ambiguities.length : null;
  const flagged = Array.isArray(pt?.cards) ? pt.cards.filter((c) => c.flag).length : null;

  return [
    row('opportunity', 'Opportunity score', opp, '18+ of 30', opp !== null && band(opp, 18, 15, true), '/30'),
    row('critic', 'Critic average', avg === null ? null : Math.round(avg * 10) / 10, '3.5+', avg !== null && band(avg, 3.5, 3, true), '/5'),
    row('originality', 'Originality', orig, '3+', orig !== null && (orig >= 3 ? 'good' : orig >= 2.5 ? 'warn' : 'bad'), '/5'),
    row('seat', 'Seat balance gap', gap, '5 points or less', gap !== null && band(gap, 5, 8, false), ' pts'),
    row('skill', 'Skill expression', skill, '20+ points', skill !== null && band(skill, 20, 10, true), ' pts'),
    row('length', 'Length vs target', lenPct, 'within 20%', lenPct !== null && (Math.abs(lenPct) <= 20 ? 'good' : Math.abs(lenPct) <= 35 ? 'warn' : 'bad'), '%'),
    row('lead', 'Lead changes', lead, '2+ per game', lead !== null && band(lead, 2, 1, true)),
    row('runaway', 'Runaway leader rate', runPct, '65% or less', runPct !== null && band(runPct, 65, 75, false), '%'),
    row('ambiguities', 'Rules ambiguities', amb, '0', amb !== null && (amb === 0 ? 'good' : amb <= 2 ? 'warn' : 'bad')),
    row('dead', 'Flagged cards', flagged, '0', flagged !== null && (flagged === 0 ? 'good' : 'warn')),
  ];
}

// ---------------------------------------------------------------------------
// Pipeline KPIs (Pipeline screen, Studio Floor). See docs/dashboard-notes.md section 1.
// ---------------------------------------------------------------------------
export const FUNNEL_STAGES = [
  { id: 'brief', label: 'Brief' }, { id: 'design', label: 'Design' }, { id: 'playtest', label: 'Playtest' },
  { id: 'critique', label: 'Critique' }, { id: 'pitch', label: 'Pitch' },
  { id: 'approved', label: 'Owner-approved' }, { id: 'prototyped', label: 'Prototyped' },
];
const STAGE_INDEX = { brief: 0, design: 1, playtest: 2, critique: 3, pitch: 4, 'owner-review': 4, approved: 5, prototyped: 6 };

// How far a game got (index into FUNNEL_STAGES), from its stage history and current stage.
export function reachedIndex(g) {
  let m = -1;
  for (const h of g.history || []) if (h.stage in STAGE_INDEX) m = Math.max(m, STAGE_INDEX[h.stage]);
  if (g.stage in STAGE_INDEX) m = Math.max(m, STAGE_INDEX[g.stage]);
  if (m < 0 && (g.stage === 'killed' || g.stage === 'archived')) m = g.verdicts?.critic === 'KILL' ? 3 : g.playtest ? 2 : 0;
  return Math.max(m, 0);
}

// KPI: "Stage funnel" (count of games that reached each stage).
export function stageFunnel(games) {
  return FUNNEL_STAGES.map((s, i) => ({ ...s, count: games.filter((g) => reachedIndex(g) >= i).length }));
}

// KPI: "Kill rate by stage" (killed at a stage, as a % of games entering it). Target: most kills early.
export function killRateByStage(games) {
  return FUNNEL_STAGES.slice(0, 5).map((s, i) => {
    const entered = games.filter((g) => reachedIndex(g) >= i).length;
    const killed = games.filter((g) => (g.stage === 'killed' || g.stage === 'archived') && reachedIndex(g) === i).length;
    return { ...s, entered, killed, pct: entered ? Math.round((killed / entered) * 100) : null };
  });
}

// KPI: "Cycle time" (hours from brief to pitch), one row per pitched game.
export function cycleTimes(games) {
  const out = [];
  for (const g of games) {
    const h = g.history || [];
    const start = h.find((e) => e.stage === 'brief') || h[0];
    const end = h.find((e) => e.stage === 'pitch' || e.stage === 'owner-review');
    const a = start ? Date.parse(start.time) : NaN, b = end ? Date.parse(end.time) : NaN;
    if (!Number.isNaN(a) && !Number.isNaN(b) && b >= a) out.push({ slug: g.slug, title: g.title, hours: Math.round(((b - a) / 3600000) * 10) / 10 });
  }
  return out;
}

// KPI: "Average revision loops" (per pitched game). Target <= 2.
export function avgRevisionLoops(games) {
  const pitched = games.filter(wasPitched);
  if (pitched.length === 0) return none();
  const avg = Math.round((pitched.reduce((a, g) => a + (g.revision || 0), 0) / pitched.length) * 10) / 10;
  return { value: avg, target: '2 or fewer', status: avg <= 2 ? 'good' : avg <= 3 ? 'warn' : 'bad' };
}

// KPI: "First-pass playtest rate" (% of new designs that get PASS on their first playtest).
export function firstPassRate(games) {
  const firsts = games.map((g) => {
    const entry = (g.history || []).find((h) => h.stage === 'playtest' && h.verdict);
    if (entry) return entry.verdict;
    return !(g.history || []).length || g.revision === 0 ? g.playtest?.verdict ?? null : null;
  }).filter(Boolean);
  if (firsts.length === 0) return none();
  return { value: Math.round((firsts.filter((v) => v === 'PASS').length / firsts.length) * 100), target: 'rising over time', status: 'none' };
}

// KPI: "Stuck games" (no activity for over 24h, or waiting for the owner). Target 0.
export function stuckGames(games, activity, now = Date.now()) {
  const out = [];
  for (const g of games) {
    if (!IN_DEVELOPMENT.includes(g.stage) && g.stage !== 'owner-review') continue;
    const times = activity.filter((e) => e.game === g.slug).map((e) => Date.parse(e.time)).filter((n) => !Number.isNaN(n));
    const last = times.length ? Math.max(...times) : NaN;
    const hours = Number.isNaN(last) ? null : Math.round(((now - last) / 3600000) * 10) / 10;
    if (g.stage === 'owner-review') out.push({ slug: g.slug, title: g.title, reason: 'waiting for the owner', hours });
    else if (hours !== null && hours > 24) out.push({ slug: g.slug, title: g.title, reason: 'no activity for over 24h', hours });
  }
  return out;
}

// Two key numbers for each agent's room card on the Studio Floor.
export function roomStats(games, agents, stuck) {
  const all = (fn) => games.map(fn).filter((v) => v !== null && v !== undefined);
  const avg = (xs) => (xs.length ? Math.round((xs.reduce((a, b) => a + b, 0) / xs.length) * 10) / 10 : null);
  const designer = agents.find((a) => a.id === 'game-designer');
  const designing = games.find((g) => g.slug === designer?.currentGame) || games.filter((g) => g.stage === 'design').sort((a, b) => (b.revision || 0) - (a.revision || 0))[0];
  const critiqued = all((g) => criticAverage(g.critique));
  const kills = games.filter((g) => g.verdicts?.critic === 'KILL' || g.critique?.verdict === 'KILL').length;
  const first = firstPassRate(games);
  const sims = games.reduce((a, g) => a + (g.playtest?.games_simulated || 0), 0);
  const dash = '—';
  return {
    'market-researcher': [{ label: 'Briefs written', value: all((g) => g.brief).length }, { label: 'Avg opportunity', value: avg(all((g) => g.brief?.opportunity_score)) ?? dash, unit: avg(all((g) => g.brief?.opportunity_score)) === null ? '' : '/30' }],
    'game-designer': [{ label: 'Current game', value: designing?.title || dash }, { label: 'Revision', value: designing ? `${designing.revision || 0} of 3` : dash }],
    playtester: [{ label: 'Games simulated', value: sims.toLocaleString('en-US') }, { label: 'First-pass rate', value: first.value === null ? dash : first.value, unit: first.value === null ? '' : '%' }],
    critic: [{ label: 'Avg critic score', value: avg(critiqued) ?? dash, unit: avg(critiqued) === null ? '' : '/5' }, { label: 'Kills', value: kills }],
    manager: [{ label: 'Pitches for you', value: games.filter((g) => g.stage === 'owner-review').length }, { label: 'Stuck games', value: stuck.length }],
  };
}

// Milestone ticker: pitch ready, game killed, balance problem found, owner decision recorded.
export function milestones(games, decisions) {
  const t = (iso) => { const n = Date.parse(iso); return Number.isNaN(n) ? 0 : n; };
  const items = [];
  for (const g of games) {
    const pitchEntry = (g.history || []).find((h) => h.stage === 'owner-review') || (g.history || []).find((h) => h.stage === 'pitch');
    if (pitchEntry) items.push({ time: t(pitchEntry.time), kind: 'pitch', text: `PITCH READY: ${g.title}` });
    const killEntry = (g.history || []).find((h) => h.stage === 'killed' || h.stage === 'archived');
    if (killEntry || g.stage === 'killed') items.push({ time: t(killEntry?.time), kind: 'kill', text: `KILLED: ${g.title}${g.kill_reason ? ` (${g.kill_reason})` : ''}` });
    const big = (g.playtest?.problems || []).find((p) => p.severity === 'high');
    if (big) {
      const e = [...(g.history || [])].reverse().find((h) => h.stage === 'playtest');
      items.push({ time: t(e?.time), kind: 'balance', text: `BALANCE PROBLEM: ${g.title}: ${big.problem}` });
    }
  }
  for (const d of decisions || []) items.push({ time: t(d.time), kind: 'decision', text: `OWNER DECISION: ${d.decision} ${d.slug}` });
  return items.sort((a, b) => b.time - a.time).slice(0, 20);
}
