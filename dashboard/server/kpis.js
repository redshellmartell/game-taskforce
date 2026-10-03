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
export function roomStats(games, agents, stuck, bank = null) {
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
    'market-researcher': [{ label: 'Briefs written', value: all((g) => g.brief).length }, { label: 'Ideas banked', value: bank ? bank.banked : dash }],
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

// ---------------------------------------------------------------------------
// Milestone 4: Review Queue, Quality Lab, Market & Portfolio, Ops.
// ---------------------------------------------------------------------------
const isNum = (v) => typeof v === 'number' && !Number.isNaN(v);
const round1 = (n) => Math.round(n * 10) / 10;
const avgOf = (xs) => { const v = xs.filter(isNum); return v.length ? round1(v.reduce((a, b) => a + b, 0) / v.length) : null; };

// KPIs: "Owner approval rate", "Prototypes built", "Human playtest score", "Agent-vs-human gap".
export function ownerStats(games, decisions) {
  const count = (d) => decisions.filter((x) => x.decision === d).length;
  const approved = count('approve');
  const decided = approved + count('reject') + count('send-back');
  const sessions = games.flatMap((g) => g.humanPlaytests || []);
  const human = avgOf(sessions.map((s) => avgOf([s.fun, s.replay, s.clarity])));
  const gapRows = games.map((g) => {
    const criticFun = isNum(g.critique?.scores?.fun) ? g.critique.scores.fun : null;
    const humanFun = avgOf((g.humanPlaytests || []).map((s) => s.fun));
    return criticFun !== null && humanFun !== null ? { slug: g.slug, title: g.title, criticFun, humanFun, gap: round1(criticFun - humanFun) } : null;
  }).filter(Boolean);
  const gap = gapRows.length ? round1(gapRows.reduce((a, r) => a + r.gap, 0) / gapRows.length) : null;
  return {
    approvalRate: decided ? { value: Math.round((approved / decided) * 100), target: 'rising over time', status: 'none' } : none(),
    prototypes: { value: count('prototyped'), target: null, status: 'none' },
    humanScore: { value: human, target: null, status: 'none', sessions: sessions.length },
    gap: gap === null ? none(null, 'close to 0') : { value: gap, target: 'close to 0', status: Math.abs(gap) <= 0.5 ? 'good' : Math.abs(gap) <= 1 ? 'warn' : 'bad' },
    gapRows,
  };
}

// Pitches waiting for the owner, oldest first.
export function reviewQueueItems(games, now = Date.now()) {
  return games.filter((g) => g.stage === 'owner-review').map((g) => {
    const h = [...(g.history || [])].reverse().find((e) => e.stage === 'owner-review');
    const since = h ? Date.parse(h.time) : NaN;
    const passing = g.scorecard.filter((r) => r.status === 'good').length;
    const scored = g.scorecard.filter((r) => r.status !== 'none').length;
    return { slug: g.slug, title: g.title, hook: g.pitch?.hook || null, howItPlays: g.howItPlays || null, components: g.pitch?.components || [], cost: g.pitch?.estimated_prototype_cost_usd ?? null,
      players: g.pitch?.players || g.brief?.players || null, minutes: g.pitch?.minutes || g.brief?.minutes || null, since: Number.isNaN(since) ? null : new Date(since).toISOString(),
      days: Number.isNaN(since) ? null : Math.floor((now - since) / DAY), passing, scored, critic: criticAverage(g.critique) };
  }).sort((a, b) => (a.since || '').localeCompare(b.since || ''));
}

// What kind of problem is this? (for "recurring problem types" in the Quality Lab)
const PROBLEM_TYPES = [
  ['Runaway leader', /runaway|snowball|halfway leader/],
  ['Seat imbalance', /seat|first.?player|second.?player|turn order/],
  ['Dead or useless content', /dead|useless|inert|decides only|never (worth|played)|unused/],
  ['Overpowered content', /outsized|overpowered|too strong|slightly strong|dominant/],
  ['Wrong game length', /game length|too long|too short|length vs/],
  ['Too few real decisions', /no (real )?decisions|automatic|same every turn|skill expression|dominated|solved/],
  ['Rules ambiguity', /ambigu|unclear rule/],
];
export function problemTypes(g) {
  const found = new Set();
  const pt = g.playtest;
  if (!pt) return found;
  const texts = (pt.problems || []).map((p) => `${p.problem} ${p.evidence || ''}`.toLowerCase());
  if ((pt.ambiguities || []).length) found.add('Rules ambiguity');
  // A flagged card or design element is filed by what its flag says ("outsized" = overpowered, "inert" = dead, ...).
  for (const c of pt.cards || []) {
    if (!c.flag) continue;
    const t = String(c.flag).toLowerCase();
    let hit = false;
    for (const [name, re] of PROBLEM_TYPES) if (re.test(t)) { found.add(name); hit = true; }
    if (!hit) found.add('Dead or useless content');
  }
  for (const t of texts) { for (const [name, re] of PROBLEM_TYPES) if (re.test(t)) found.add(name); }
  return found;
}

// Quality Lab: trends across all games.
export function qualityLab(games) {
  const ordered = [...games].sort((a, b) => Date.parse(a.history?.[0]?.time || 0) - Date.parse(b.history?.[0]?.time || 0));
  let pass = 0, seen = 0;
  const firstPass = [];
  for (const g of ordered) {
    const v = firstPass_verdict(g);
    if (!v) continue;
    seen += 1; if (v === 'PASS') pass += 1;
    firstPass.push({ slug: g.slug, title: g.title, passed: v === 'PASS', rate: Math.round((pass / seen) * 100) });
  }
  const byRev = {};
  for (const g of games) { const a = criticAverage(g.critique); if (a !== null) (byRev[g.critique.revision ?? g.revision ?? 0] ||= []).push(a); }
  const criticByRevision = Object.entries(byRev).map(([rev, xs]) => ({ revision: Number(rev), label: `Revision ${rev}`, avg: avgOf(xs), games: xs.length })).sort((a, b) => a.revision - b.revision);
  const tested = games.filter((g) => g.playtest);
  const counts = {};
  for (const g of tested) for (const t of problemTypes(g)) counts[t] = (counts[t] || 0) + 1;
  const recurring = Object.entries(counts).map(([type, n]) => ({ type, games: n, of: tested.length })).sort((a, b) => b.games - a.games);
  return { firstPass, criticByRevision, recurring };
}
function firstPass_verdict(g) {
  const entry = (g.history || []).find((h) => h.stage === 'playtest' && h.verdict);
  if (entry) return entry.verdict;
  return !(g.history || []).length || g.revision === 0 ? g.playtest?.verdict ?? null : null;
}

// Market & Portfolio: what are we making, and is it varied?
const COMMON_MECHANICS = ['push-your-luck', 'set collection', 'hidden bidding', 'engine building', 'market drafting', 'deck building', 'worker placement', 'area control', 'trick-taking', 'co-operative', 'deduction', 'tile placement', 'dice rolling', 'roll and write', 'negotiation', 'solo play', 'bluffing', 'real-time'];
export function portfolio(games) {
  const briefs = games.filter((g) => g.brief);
  const tally = (keyFn) => {
    const m = {};
    for (const g of briefs) for (const k of [].concat(keyFn(g.brief) ?? [])) if (k !== null && k !== undefined && k !== '') m[k] = (m[k] || 0) + 1;
    return Object.entries(m).map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count);
  };
  const minutes = (b) => (!isNum(b.minutes) ? null : b.minutes <= 15 ? '15 min or less' : b.minutes <= 30 ? '16-30 min' : b.minutes <= 60 ? '31-60 min' : 'over 60 min');
  const complexity = (b) => (!isNum(b.complexity) ? null : b.complexity <= 2 ? 'light (up to 2)' : b.complexity <= 3 ? 'medium (2.5-3)' : 'heavy (3.5+)');
  const mechanics = tally((b) => (b.mechanics || []).map((m) => String(m).toLowerCase()));
  const top = mechanics[0];
  const share = top && briefs.length ? Math.round((top.count / briefs.length) * 100) : null;
  const used = new Set(mechanics.map((m) => m.name));
  return {
    briefs: briefs.length,
    players: tally((b) => (b.players == null ? null : String(b.players))), minutes: tally(minutes), complexity: tally(complexity),
    mechanics, themes: tally((b) => (b.theme ? String(b.theme).toLowerCase() : null)),
    topMechanic: top ? { name: top.name, share, status: briefs.length < 3 ? 'none' : share > 40 ? 'warn' : 'good', target: 'no mechanic over 40%' } : null,
    opportunity: briefs.map((g) => ({ slug: g.slug, title: g.title, score: g.brief.opportunity_score ?? null, rubric: g.brief.rubric || null })).filter((o) => o.score !== null).sort((a, b) => b.score - a.score),
    comparables: briefs.map((g) => ({ slug: g.slug, title: g.title, items: g.brief.comparables || [], status: (g.brief.comparables || []).length >= 2 ? 'good' : 'warn' })),
    unexplored: COMMON_MECHANICS.filter((m) => ![...used].some((u) => u.includes(m) || m.includes(u))),
  };
}

// Ops: runs, failures, simulated games and each agent's recent activity.
export function opsStats(games, agents, activity, now = Date.now()) {
  const week = now - 7 * DAY, day = now - DAY;
  const inWeek = activity.filter((e) => Date.parse(e.time) >= week);
  const perAgent = agents.map((a) => {
    const mine = inWeek.filter((e) => e.agent === a.id);
    const runs = mine.filter((e) => e.event === 'done').length, errors = mine.filter((e) => e.event === 'error').length;
    const all = activity.filter((e) => e.agent === a.id);
    return { id: a.id, room: a.room, color: a.color, state: a.state, runs, errors, failureRate: runs + errors ? Math.round((errors / (runs + errors)) * 100) : null,
      last: all[0]?.time || null, history: all.slice(0, 14).reverse().map((e) => ({ time: e.time, event: e.event, game: e.game, message: e.message })) };
  });
  const totalRuns = perAgent.reduce((a, x) => a + x.runs, 0), totalErrors = perAgent.reduce((a, x) => a + x.errors, 0);
  const failure = totalRuns + totalErrors ? Math.round((totalErrors / (totalRuns + totalErrors)) * 100) : null;
  const days = [];
  for (let i = 6; i >= 0; i--) {
    const start = new Date(now - i * DAY); start.setUTCHours(0, 0, 0, 0);
    const row = { day: start.toISOString().slice(5, 10) };
    for (const a of agents) row[a.id] = activity.filter((e) => e.agent === a.id && e.time.slice(0, 10) === start.toISOString().slice(0, 10)).length;
    days.push(row);
  }
  const simsTotal = games.reduce((a, g) => a + (g.playtest?.games_simulated || 0), 0);
  const simsDay = games.reduce((a, g) => {
    const last = activity.find((e) => e.game === g.slug && e.agent === 'playtester' && e.event === 'done');
    return a + (g.playtest?.games_simulated && last && Date.parse(last.time) >= day ? g.playtest.games_simulated : 0);
  }, 0);
  return {
    perAgent, daily: days,
    failureRate: failure === null ? none(null, 'under 10%') : { value: failure, target: 'under 10%', status: failure < 10 ? 'good' : 'bad' },
    simulated: { total: simsTotal, last24h: simsDay }, usagePerPitch: null,
  };
}

// ---------------------------------------------------------------------------
// Idea bank (research/idea-bank.json). Lean-mode rule from CLAUDE.md: a market scan is only
// needed when fewer than 3 banked ideas score 18 or more, or the last scan is over 30 days old.
// ---------------------------------------------------------------------------
export function ideaBankStats(bank, now = Date.now()) {
  if (!bank || !Array.isArray(bank.ideas)) return null;
  const ideas = bank.ideas;
  const count = (s) => ideas.filter((i) => i.status === s).length;
  const strong = ideas.filter((i) => i.status === 'banked' && isNum(i.score) && i.score >= 18).length;
  const scan = Date.parse(bank.last_scan);
  const scanAgeDays = Number.isNaN(scan) ? null : Math.floor((now - scan) / DAY);
  const reasons = [];
  if (strong < 3) reasons.push(`only ${strong} banked idea${strong === 1 ? '' : 's'} scoring 18 or more (need 3)`);
  if (scanAgeDays === null) reasons.push('no scan date recorded');
  else if (scanAgeDays > 30) reasons.push(`last scan was ${scanAgeDays} days ago (limit 30)`);
  return { total: ideas.length, banked: count('banked'), inPipeline: count('in-pipeline'), used: count('used'), rejected: count('rejected'),
    strongBanked: strong, lastScan: bank.last_scan || null, scanAgeDays, needsScan: reasons.length > 0, scanReasons: reasons };
}

// ---------------------------------------------------------------------------
// Usage (from usage/sessions.jsonl, written by tools/usage/usage.py). Everything is in "usage tokens":
// input + output + cache writes + cache reads at a reduced weight, so it follows the owner's subscription, not dollars.
// ---------------------------------------------------------------------------
const weekStart = (day) => { const d = new Date(`${day}T00:00:00Z`); if (Number.isNaN(d.getTime())) return null; d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7)); return d.toISOString().slice(0, 10); };
export function usageStats(sessions, games, now = Date.now()) {
  if (!Array.isArray(sessions) || sessions.length === 0) return null;
  const sum = (key) => {
    const m = {};
    for (const s of sessions) for (const b of s[key] || []) m[b.name] = (m[b.name] || 0) + (b.weighted_tokens || 0);
    return Object.entries(m).map(([name, tokens]) => ({ name, tokens })).sort((a, b) => b.tokens - a.tokens);
  };
  const byDay = sum('by_day');
  const weeks = {};
  for (const d of byDay) { const w = weekStart(d.name); if (w) weeks[w] = (weeks[w] || 0) + d.tokens; }
  const total = byDay.reduce((a, d) => a + d.tokens, 0);
  const cut = new Date(now - 7 * DAY).toISOString().slice(0, 10);
  const last7 = byDay.filter((d) => d.name >= cut).reduce((a, d) => a + d.tokens, 0);
  const pitched = games.filter(wasPitched).length;
  return {
    total, last7days: last7, sessions: sessions.length,
    byAgent: sum('by_agent'), byGame: sum('by_category'),
    byWeek: Object.entries(weeks).sort().slice(-8).map(([week, tokens]) => ({ week, tokens })),
    perPitched: pitched ? { value: Math.round(total / pitched), target: 'falling over time', status: 'none', pitched } : none(null, 'falling over time'),
  };
}
