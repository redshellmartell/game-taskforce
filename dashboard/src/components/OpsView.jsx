import { Gate } from './Gate.jsx';
import { Help } from './Help.jsx';
import { DailyStack, ValueBars, colorOf } from './charts.jsx';
import { ago } from '../util.js';

const DOT = { done: 'var(--good)', error: 'var(--bad)', start: '#7aa2f7', step: 'var(--muted)' };

// Usage is counted in tokens (input + output + cache writes + cache reads at a reduced weight), so it follows the
// owner's subscription. The guard compares recent usage with the plan windows the owner calibrated.
const DASH = '\u2014';
const tok = (n) => (n == null ? DASH : n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${Math.round(n / 1e3)}k` : String(n));
const millions = (rows) => rows.map((r) => ({ ...r, m: Math.round((r.tokens / 1e6) * 100) / 100 }));
const GUARD_CLASS = { ok: 'good', warn: 'warn', stop: 'bad', uncalibrated: 'none' };

// How the team is running: activity, failures, simulated games and usage.
export function OpsView({ state }) {
  const o = state.ops;
  const f = o.failureRate;
  const u = o.usage;
  return (
    <div className="view">
      <div className="plist-head"><h2>Ops</h2><span className="muted">How the team is running.</span></div>
      <div className="tiles">
        <div className="kpi tile none"><span className="num">{state.kpis.agentsActive.value} / {state.kpis.agentsActive.total}</span><span className="lbl">Agents active <Help topic="agent" /></span><span className="tgt">&nbsp;</span></div>
        <div className={`kpi tile ${f.value === null ? 'none' : f.status}`}><span className="num">{f.value === null ? '—' : `${f.value}%`}</span><span className="lbl">Failure rate, 7 days <Help topic="kpi" /></span><span className="tgt">{f.value === null ? 'no runs yet' : 'target under 10%'}</span></div>
        <div className="kpi tile none"><span className="num">{o.simulated.total.toLocaleString('en-US')}</span><span className="lbl">Simulated games, total</span><span className="tgt">{o.simulated.last24h.toLocaleString('en-US')} in the last 24 h</span></div>
        {o.guard && o.guard.windows.map((w) => (
          <div key={w.name} className={`kpi tile ${GUARD_CLASS[w.status]}`}>
            <span className="num">{w.percent == null ? 'not set' : `${w.percent}%`}</span>
            <span className="lbl">{w.name === '5h' ? '5-hour' : w.name === '7d' ? 'Weekly' : w.name} usage window <Help topic="kpi" /></span>
            <span className="tgt">{w.percent == null ? 'calibrate to see a percentage' : `stop at ${o.guard.stop_at_percent}% \u00b7 ${w.status.toUpperCase()}`}</span>
          </div>))}
        <div className="kpi tile none"><span className="num">{o.approvals.revision.proposed}</span><span className="lbl">Revision loops proposed <Help topic="approval-gate" /></span><span className="tgt">{o.approvals.revision.approved} approved \u00b7 {o.approvals.revision.declined} declined \u00b7 {o.approvals.revision.pending} waiting</span></div>
        <div className="kpi tile none" title={o.approvals.savedBasis}><span className="num">{tok(o.approvals.savedTokens)}</span><span className="lbl">Usage saved by declined loops <Help topic="usage-estimate" /></span><span className="tgt">estimate from request sizes</span></div>
        <div className="kpi tile none"><span className="num">{tok(u?.perPitched?.value)}</span><span className="lbl">Usage per pitched game <Help topic="kpi" /></span><span className="tgt">{u?.perPitched?.pitched ? `${u.perPitched.pitched} pitched \u00b7 usage tokens` : 'no pitched game yet'}</span></div>
      </div>
      {!u && !o.guard && <p className="notice info">No usage recorded yet. At the end of a task, run <span className="mono">python3 tools/usage/usage.py --record</span>; to set the stop percentage, run <span className="mono">--calibrate 5h=&lt;percent&gt; 7d=&lt;percent&gt;</span> with the usage percentages shown in the Claude app (see CLAUDE.md, "Cost discipline").</p>}
      {(!o.guard || o.guard.windows.some((w) => w.percent == null)) && u && <p className="notice">The usage guard is not calibrated yet, so there is no percentage. Read your plan usage in the Claude app (5-hour and weekly) and tell Claude Code: <span className="mono">calibrate usage: 5-hour 63%, weekly 41%</span>.</p>}
      {u && (
        <section className="card"><h3>Usage in tokens <Help topic="kpi" /> <span className="muted" style={{ fontWeight: 400 }}>{tok(u.total)} recorded over {u.sessions} session{u.sessions === 1 ? '' : 's'}, {tok(u.last7days)} in the last 7 days</span></h3>
          <div className="gp-grid">
            <div><h4>By agent (millions of tokens)</h4><ValueBars data={millions(u.byAgent)} xKey="name" yKey="m" horizontal color={colorOf(state, 'manager')} label="million usage tokens" /></div>
            <div><h4>By game or area (millions)</h4><ValueBars data={millions(u.byGame)} xKey="name" yKey="m" horizontal color={colorOf(state, 'manager')} label="million usage tokens" /></div>
            <div><h4>By week (millions)</h4><ValueBars data={millions(u.byWeek).map((w) => ({ ...w, name: w.week.slice(5) }))} xKey="name" yKey="m" color={colorOf(state, 'manager')} label="million usage tokens" /></div>
          </div>
          <p className="muted small" style={{ marginBottom: 0 }}>Usage tokens = input + output + cache writes + cache reads at a reduced weight. They follow your subscription, not dollars. Percentages depend on the calibration in <span className="mono">studio-settings.json</span>.</p>
        </section>
      )}
      <section className="card"><h3>Agent activity per day (last 7 days)</h3>
        <Gate games={state.games.length} what="This chart"><DailyStack daily={o.daily} agents={state.agents} /></Gate>
      </section>
      <section className="card"><h3>Agents</h3>
        <div style={{ overflowX: 'auto' }}><table className="score matrix"><thead><tr className="muted"><td>Agent</td><td>Status now</td><td>Runs, 7 days</td><td>Failures</td><td>Failure rate</td><td>Last active</td><td>Recent events <Help topic="activity-log" /></td></tr></thead>
          <tbody>{o.perAgent.map((a) => (
            <tr key={a.id}>
              <td><b style={{ color: a.color }}>{a.room}</b></td><td>{a.state}</td><td className="mono">{a.runs}</td><td className={`mono ${a.errors ? 'bad' : ''}`}>{a.errors}</td>
              <td className="mono">{a.failureRate === null ? '—' : `${a.failureRate}%`}</td><td className="muted">{a.last ? ago(a.last) : 'never'}</td>
              <td><span className="strip">{a.history.length === 0 && <span className="muted small">none</span>}{a.history.map((h, i) => <i key={i} title={`${h.event}: ${h.message} (${h.game})`} style={{ background: DOT[h.event] || 'var(--muted)' }} />)}</span></td>
            </tr>))}</tbody></table></div>
        <p className="muted small">Dots, oldest to newest: <span style={{ color: DOT.start }}>start</span>, <span>step</span>, <span style={{ color: DOT.done }}>done</span>, <span style={{ color: DOT.error }}>error</span>. Hover a dot for the message.</p>
      </section>
    </div>
  );
}
