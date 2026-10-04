import { useState } from 'react';
import { RateBars, CardCorrelation, LengthHistogram, colorOf } from './charts.jsx';

const TOP = 12;      // cards drawn in the chart unless "show all" is ticked

// The playtest results as one full-width card with three tabs, instead of one very long column.
export function PlaytestCard({ pt, state }) {
  const [tab, setTab] = useState('balance');
  const [all, setAll] = useState(false);
  if (!pt) return <section className="card"><h3>Playtest results</h3><p className="empty">No playtest data yet.</p></section>;
  const color = colorOf(state, 'playtester');
  const cards = (pt.cards || []);
  const measured = cards.filter((c) => typeof c.win_correlation === 'number').sort((a, b) => Math.abs(b.win_correlation) - Math.abs(a.win_correlation));
  const shown = all ? measured : measured.slice(0, TOP);
  const flagged = cards.filter((c) => c.flag);
  const problems = pt.problems || [];
  const sevCount = (s) => problems.filter((p) => p.severity === s).length;
  const tabs = [['balance', 'Balance'], ['cards', `Cards${flagged.length ? ` (${flagged.length} flagged)` : ''}`], ['problems', `Problems (${problems.length})`]];
  return (
    <section className="card playtest">
      <h3>Playtest results <span className="muted" style={{ fontWeight: 400 }}>{pt.games_simulated ? `${pt.games_simulated.toLocaleString()} simulated games` : ''}</span></h3>
      <div className="tabs" style={{ padding: 0, marginBottom: 10 }}>{tabs.map(([id, label]) => <button key={id} className={`tab ${tab === id ? 'on' : ''}`} onClick={() => setTab(id)}>{label}</button>)}</div>
      {tab === 'balance' && (
        <div className="pt-charts">
          <div><h4>Win rate by seat</h4><RateBars rates={pt.seat_win_rates} color={color} fair={100 / Math.max(1, Object.keys(pt.seat_win_rates || {}).length)} prefix="seat " /></div>
          <div><h4>Win rate by bot</h4><RateBars rates={pt.bot_win_rates} color={color} /></div>
          <div><h4>Game length (turns)</h4><LengthHistogram length={pt.length} histogram={pt.length_histogram} color={color} /></div>
        </div>
      )}
      {tab === 'cards' && (
        <div className="pt-cards">
          <div>
            <h4>Win correlation{measured.length > TOP ? ` (${all ? 'all' : `top ${TOP} of`} ${measured.length})` : ''}</h4>
            <div className="pt-scroll"><CardCorrelation cards={shown} /></div>
            {measured.length > TOP && <label className="small muted"><input type="checkbox" checked={all} onChange={(e) => setAll(e.target.checked)} /> show all {measured.length}</label>}
          </div>
          <div>
            <h4>Flagged by the playtester</h4>
            {flagged.length === 0 && <p className="empty">Nothing flagged.</p>}
            {flagged.map((c) => <div className="item" key={c.name}><b>{c.name}</b>: {c.flag}{typeof c.played_rate === 'number' && <div className="meta">comes into play in {Math.round(c.played_rate * 100)}% of games</div>}</div>)}
          </div>
        </div>
      )}
      {tab === 'problems' && (
        <div className="pt-problems">
          {problems.length === 0 && <p className="empty">No problems recorded.</p>}
          {problems.length > 0 && <p className="muted small" style={{ marginTop: 0 }}>{['high', 'medium', 'low'].map((s) => `${sevCount(s)} ${s}`).join(' · ')}</p>}
          {problems.map((p, i) => (
            <div className="pt-problem" key={i}>
              <span className={`chip sev-${p.severity}`}>{p.severity}</span>
              <div><b>{p.problem}</b>{p.evidence && <div className="small muted">{p.evidence}</div>}{p.fix && <div className="small"><span className="muted">Suggested fix:</span> {p.fix}</div>}</div>
            </div>))}
        </div>
      )}
    </section>
  );
}
