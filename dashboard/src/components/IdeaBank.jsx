import { useMemo, useState } from 'react';
import { Help } from './Help.jsx';

const LENGTHS = [['', 'Any length'], ['short', '15 min or less'], ['medium', '16-30 min'], ['long', 'Over 30 min'], ['unknown', 'Length not recorded']];
const lengthOf = (m) => (typeof m !== 'number' ? 'unknown' : m <= 15 ? 'short' : m <= 30 ? 'medium' : 'long');
const STATUS_CLASS = { banked: 'v-good', 'in-pipeline': '', used: '', rejected: 'v-bad' };

// "2-4" fits a player filter of 3; unknown counts never match a specific number.
function fitsPlayers(players, n) {
  if (!n) return true;
  if (players == null) return false;
  const m = String(players).match(/^(\d+)(?:\s*-\s*(\d+))?/);
  if (!m) return false;
  const lo = Number(m[1]), hi = Number(m[2] || m[1]);
  return n >= lo && n <= hi;
}

// The idea bank (research/idea-bank.json): ideas by status and score, with filters. Read-only.
export function IdeaBank({ bank }) {
  const [status, setStatus] = useState('');
  const [players, setPlayers] = useState('');
  const [length, setLength] = useState('');
  const [mechanic, setMechanic] = useState('');
  const mechanics = useMemo(() => [...new Set((bank?.ideas || []).flatMap((i) => i.mechanics || []))].sort(), [bank]);
  if (!bank) {
    return <section className="card"><h3>Idea bank</h3><p className="empty">No idea bank yet (research/idea-bank.json). The first market scan creates it, or tell Claude Code "Add to the idea bank: ...".</p></section>;
  }
  const shown = bank.ideas
    .filter((i) => (!status || i.status === status) && fitsPlayers(i.players, Number(players)) && (!length || lengthOf(i.minutes) === length) && (!mechanic || (i.mechanics || []).includes(mechanic)))
    .sort((a, b) => (b.score ?? 0) - (a.score ?? 0));
  const tile = (label, value, cls = '') => <div className={`kpi tile ${cls}`} key={label}><span className="num">{value}</span><span className="lbl">{label}</span></div>;
  return (
    <section className="card" id="idea-bank">
      <h3>Idea bank <Help topic="kpi" /></h3>
      <div className="tiles" style={{ marginBottom: 8 }}>
        {tile('Banked', bank.banked, 'good')}{tile('In the pipeline', bank.inPipeline)}{tile('Used', bank.used)}{tile('Rejected', bank.rejected)}
        <div className={`kpi tile ${bank.needsScan ? 'warn' : 'good'}`}>
          <span className="num">{bank.needsScan ? 'Scan due' : 'No scan needed'}</span>
          <span className="lbl">Market scan</span>
          <span className="tgt">{bank.needsScan ? bank.scanReasons.join('; ') : `last scan ${bank.scanAgeDays} day${bank.scanAgeDays === 1 ? '' : 's'} ago, ${bank.strongBanked} strong banked ideas`}</span>
        </div>
      </div>
      <div className="ideaform" style={{ flexDirection: 'row', flexWrap: 'wrap', alignItems: 'end', gap: 10 }}>
        <label>Status<select value={status} onChange={(e) => setStatus(e.target.value)}><option value="">All</option>{['banked', 'in-pipeline', 'used', 'rejected'].map((s) => <option key={s}>{s}</option>)}</select></label>
        <label>Players<select value={players} onChange={(e) => setPlayers(e.target.value)}><option value="">Any</option>{[1, 2, 3, 4, 5, 6].map((n) => <option key={n} value={n}>{n}</option>)}</select></label>
        <label>Length<select value={length} onChange={(e) => setLength(e.target.value)}>{LENGTHS.map(([v, l]) => <option key={v} value={v}>{l}</option>)}</select></label>
        <label>Mechanic<select value={mechanic} onChange={(e) => setMechanic(e.target.value)}><option value="">Any</option>{mechanics.map((m) => <option key={m}>{m}</option>)}</select></label>
        <span className="muted small">{shown.length} of {bank.ideas.length} ideas</span>
      </div>
      <div style={{ overflowX: 'auto', marginTop: 8 }}>
        <table className="score matrix idea-table"><thead><tr className="muted"><td>Score</td><td>Idea</td><td>Status</td><td>Players</td><td>Length</td><td>Mechanics</td></tr></thead>
          <tbody>{shown.map((i) => (
            <tr key={i.id}>
              <td className={`mono cell ${i.score >= 18 ? 'good' : 'bad'}`}>{i.score ?? '—'}/30</td>
              <td style={{ whiteSpace: 'normal', minWidth: 260 }}><b>{i.title}</b>{i.source === 'owner' && <span className="chip" style={{ marginLeft: 6 }}>yours</span>}<div className="muted small">{i.pitch}</div></td>
              <td><span className={`chip ${STATUS_CLASS[i.status] || ''}`}>{i.status}</span>{i.game_slug && <div className="muted small mono">{i.game_slug}</div>}</td>
              <td className="mono">{i.players ?? '—'}</td><td className="mono">{i.minutes != null ? `${i.minutes} min` : '—'}</td>
              <td>{(i.mechanics || []).map((m) => <span className="chip" key={m}>{m}</span>)}</td>
            </tr>))}
            {shown.length === 0 && <tr><td colSpan={6} className="empty">No ideas match these filters.</td></tr>}
          </tbody></table>
      </div>
      <p className="muted small" style={{ marginBottom: 0 }}>Read-only. To add one, tell Claude Code "Add to the idea bank: ..." (see research/README.md). Scores are out of 30; 18 is the cut-off.</p>
    </section>
  );
}
