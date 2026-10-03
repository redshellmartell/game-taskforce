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
