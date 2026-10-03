import { Gate } from './Gate.jsx';
import { Help } from './Help.jsx';
import { TrendLine, ValueBars, colorOf } from './charts.jsx';
import { STAGE_LABEL } from './ProjectsView.jsx';

const COLS = [['seat', 'Seat gap'], ['skill', 'Skill expr.'], ['length', 'Length'], ['lead', 'Lead chg.'], ['runaway', 'Runaway'], ['ambiguities', 'Ambig.'], ['dead', 'Flagged']];

// Design quality across all games: are the designs getting better, and what keeps going wrong?
export function QualityLabView({ state, onOpen }) {
  const q = state.quality;
  const n = state.games.length;
  const tested = state.games.filter((g) => g.playtest);
  return (
    <div className="view">
      <div className="plist-head"><h2>Quality lab</h2><span className="muted">Are the designs getting better? Fix recurring problems in the agent instructions.</span></div>
      <div className="gp-grid">
        <section className="card"><h3>First-pass playtest rate over time <Help topic="verdict" /></h3>
          <Gate games={n} what="This chart"><TrendLine data={q.firstPass} xKey="title" yKey="rate" unit="%" domain={[0, 100]} color={colorOf(state, 'playtester')} /></Gate>
        </section>
        <section className="card"><h3>Critic score by revision</h3>
          <Gate games={n} what="This chart"><ValueBars data={q.criticByRevision} xKey="label" yKey="avg" domain={[0, 5]} refLine={3.5} refText="3.5 target at pitch" ticks={[0, 1, 2, 3, 4, 5]} color={colorOf(state, 'critic')} label="average critic score" /></Gate>
        </section>
        <section className="card"><h3>Recurring problem types</h3>
          <Gate games={n} what="This chart">
            {q.recurring.length === 0 ? <p className="empty">No problems recorded in any playtest.</p>
              : <><ValueBars data={q.recurring.map((r) => ({ ...r, name: `${r.type} (${r.games} of ${r.of})` }))} xKey="name" yKey="games" horizontal labelWidth={215} color={colorOf(state, 'playtester')} label="games affected" />
                <p className="muted small">A problem that shows up in several games belongs in the designer's or playtester's instructions, not in one game's fix.</p></>}
          </Gate>
        </section>
      </div>
      <section className="card">
        <h3>Every game against its targets</h3>
        {tested.length === 0 ? <p className="empty">No playtest data yet.</p> : (
          <div style={{ overflowX: 'auto' }}><table className="score matrix"><thead><tr className="muted"><td>Game</td><td>Stage</td>{COLS.map(([, l]) => <td key={l}>{l}</td>)}</tr></thead>
            <tbody>{tested.map((g) => {
              const rows = Object.fromEntries(g.scorecard.map((r) => [r.id, r]));
              return <tr key={g.slug}><td><button className="link" onClick={() => onOpen(g.slug)}>{g.title}</button></td><td className="muted">{STAGE_LABEL[g.stage] || g.stage}</td>
                {COLS.map(([id]) => <td key={id} className={`mono cell ${rows[id].status}`}>{rows[id].value === null ? '—' : `${rows[id].value}${rows[id].unit || ''}`}</td>)}</tr>;
            })}</tbody></table></div>
        )}
      </section>
    </div>
  );
}
