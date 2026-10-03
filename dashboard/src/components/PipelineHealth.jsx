import { Help } from './Help.jsx';
import { FunnelChart, KillRateChart, CycleChart, colorOf } from './charts.jsx';

function Tile({ label, k, suffix = '', note }) {
  const none = !k || k.value === null || k.value === undefined;
  return (
    <div className={`kpi tile ${none ? 'none' : k.status}`}>
      <span className="num">{none ? '—' : `${k.value}${suffix}`}</span>
      <span className="lbl">{label} <Help topic="kpi" /></span>
      <span className="tgt">{none ? 'no data yet' : note || (k.target ? `target ${k.target}` : ' ')}</span>
    </div>
  );
}

// Pipeline health: is the idea pipeline working? Funnel, where games die, how long they take, what is stuck.
export function PipelineHealth({ state, onOpen }) {
  const pl = state.pipeline;
  const color = colorOf(state, 'manager');
  const stuckKpi = { value: pl.stuck.length, target: '0', status: pl.stuck.length === 0 ? 'good' : 'warn' };
  return (
    <section className="health">
      <div className="tiles">
        <Tile label="Concepts in development" k={state.kpis.concepts} />
        <Tile label="Pitch rate" k={state.kpis.pitchRate} suffix="%" />
        <Tile label="Avg revision loops" k={pl.avgRevisions} />
        <Tile label="First-pass playtest" k={pl.firstPass} suffix="%" note="rising is better" />
        <Tile label="Stuck games" k={stuckKpi} />
      </div>
      <div className="charts3">
        <div className="card"><h3>Stage funnel</h3><FunnelChart funnel={pl.funnel} color={color} /></div>
        <div className="card"><h3>Kill rate by stage <span className="muted" style={{ fontWeight: 400 }}>(most should die early)</span></h3><KillRateChart killRate={pl.killRate} color={color} /></div>
        <div className="card"><h3>Cycle time, brief to pitch</h3><CycleChart times={pl.cycleTimes} color={color} /></div>
      </div>
      {pl.stuck.length > 0 && (
        <div className="card"><h3>Stuck games</h3>
          {pl.stuck.map((s) => <div className="item" key={s.slug}><button className="link" onClick={() => onOpen(s.slug)}>{s.title}</button> <span className="muted">{s.reason}{s.hours != null && ` (${s.hours < 48 ? `${s.hours} h` : `${Math.round(s.hours / 24)} days`} since last activity)`}</span></div>)}
        </div>
      )}
    </section>
  );
}
