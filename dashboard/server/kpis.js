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
