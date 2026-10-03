import { Gate } from './Gate.jsx';
import { Help } from './Help.jsx';
import { DailyStack } from './charts.jsx';
import { ago } from '../util.js';

const DOT = { done: 'var(--good)', error: 'var(--bad)', start: '#7aa2f7', step: 'var(--muted)' };

// How the team is running: activity, failures and simulated games.
export function OpsView({ state }) {
  const o = state.ops;
  const f = o.failureRate;
  return (
    <div className="view">
      <div className="plist-head"><h2>Ops</h2><span className="muted">How the team is running.</span></div>
      <div className="tiles">
        <div className="kpi tile none"><span className="num">{state.kpis.agentsActive.value} / {state.kpis.agentsActive.total}</span><span className="lbl">Agents active <Help topic="agent" /></span><span className="tgt">&nbsp;</span></div>
        <div className={`kpi tile ${f.value === null ? 'none' : f.status}`}><span className="num">{f.value === null ? '—' : `${f.value}%`}</span><span className="lbl">Failure rate, 7 days <Help topic="kpi" /></span><span className="tgt">{f.value === null ? 'no runs yet' : 'target under 10%'}</span></div>
        <div className="kpi tile none"><span className="num">{o.simulated.total.toLocaleString('en-US')}</span><span className="lbl">Simulated games, total</span><span className="tgt">{o.simulated.last24h.toLocaleString('en-US')} in the last 24 h</span></div>
        <div className="kpi tile none"><span className="num">{'—'}</span><span className="lbl">Usage per pitch</span><span className="tgt">tracked once runs are automated</span></div>
      </div>
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
