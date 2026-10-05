import { Help } from './Help.jsx';
import { TaskforceSwitch } from './TaskforceSwitch.jsx';

// The five headline KPIs. All numbers are computed on the server (server/kpis.js).
function Kpi({ label, k, suffix = '', extra }) {
  const none = !k || k.value === null || k.value === undefined;
  return (
    <div className={`kpi ${none ? 'none' : k.status}`}>
      <span className="num">{none ? '—' : `${k.value}${suffix}`}{extra}</span>
      <span className="lbl">{label} <Help topic="kpi" /></span>
      <span className="tgt">{none ? 'no data yet' : k.target ? `target ${k.target}` : ' '}</span>
    </div>
  );
}

export function TopBar({ state, learn, setLearn, onWaiting }) {
  const k = state.kpis;
  return (
    <div className="topbar">
      <span className="brand">Game Think Tank</span>
      {state.sample && <span className="badge" title="No real games yet, or started with npm run demo">Sample data</span>}
      {state.approvals?.pending > 0 && <button className="waiting-badge" onClick={onWaiting} title="The Director is waiting for your decision">Waiting for you <b>{state.approvals.pending}</b></button>}
      <TaskforceSwitch state={state} />
      <Kpi label="Concepts in development" k={k.concepts} />
      <Kpi label="Pitch rate" k={k.pitchRate} suffix="%" />
      <Kpi label="Avg critic score" k={k.avgCritic} suffix={k.avgCritic?.value != null ? ' / 5' : ''} />
      <Kpi label="Review queue" k={k.reviewQueue} />
      <label className="learn-toggle" title="Show ? markers that explain the concepts on screen"><input type="checkbox" checked={learn} onChange={(e) => setLearn(e.target.checked)} /> Learn mode</label>
      <Kpi label="Agents active" k={k.agentsActive} extra={<span className="muted" style={{ fontSize: 14 }}>{` / ${k.agentsActive.total}`}</span>} />
    </div>
  );
}
