import { CopyBox } from './IdeaForm.jsx';
import { Help } from './Help.jsx';
import { ago } from '../util.js';

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

// Pitches waiting for the owner, past decisions and your real-world playtests. Read-only.
export function ReviewQueueView({ state, onOpen }) {
  const r = state.review;
  const sessions = state.games.flatMap((g) => g.humanPlaytests.map((s) => ({ ...s, title: g.title, slug: g.slug })));
  return (
    <div className="view">
      <div className="plist-head"><h2>Review queue</h2><span className="muted">Pitches waiting for your decision, oldest first.</span></div>
      <p className="notice info">This screen is read-only. To record a decision, tell Claude Code, for example <span className="mono">approve {r.queue[0]?.slug || 'game-name'}</span>, and it updates the files this page reads.</p>
      <div className="tiles">
        <Tile label="Waiting for you" k={state.kpis.reviewQueue} />
        <Tile label="Approval rate" k={r.approvalRate} suffix="%" note="rising is better" />
        <Tile label="Prototypes built" k={r.prototypes} />
        <Tile label="Human playtest score" k={r.humanScore} suffix={r.humanScore.value != null ? ' / 5' : ''} note={`${r.humanScore.sessions} session${r.humanScore.sessions === 1 ? '' : 's'}`} />
        <Tile label="Agent-vs-human gap" k={r.gap} suffix={r.gap.value != null ? ' pts' : ''} />
      </div>

      {r.queue.length === 0 && <div className="card"><p className="empty" style={{ margin: 0 }}>Nothing waiting. Pitches the Director finishes appear here.</p></div>}
      {r.queue.map((q) => (
        <section className="card pitch" key={q.slug}>
          <div className="pitch-head">
            <div>
              <h3 style={{ margin: 0, textTransform: 'none', letterSpacing: 0, fontSize: 18, color: 'var(--text)' }}>{q.title}</h3>
              {q.hook && <p className="hook" style={{ margin: '4px 0' }}>{q.hook}</p>}
              <div className="muted">{[q.players, q.minutes && `${q.minutes} min`].filter(Boolean).join(' · ')}</div>
            </div>
            <div className="gp-chips">
              <span className={`chip big ${q.days != null && q.days > 7 ? 'v-bad' : 'v-warn'}`}>{q.days != null ? `waiting ${q.days} day${q.days === 1 ? '' : 's'}` : 'waiting'}</span>
              {q.critic != null && <span className={`chip big ${q.critic >= 3.5 ? 'v-good' : 'v-warn'}`}>critic {q.critic}/5</span>}
              {q.scored > 0 && <span className="chip big">{q.passing} of {q.scored} KPIs on target</span>}
            </div>
          </div>
          <div className="pitch-cols">
            <div>
              <h4>How it plays</h4>
              <p style={{ marginTop: 0 }}>{q.howItPlays || <span className="empty">Not in the pitch file yet.</span>}</p>
            </div>
            <div>
              <h4>Components and cost</h4>
              {q.components.length ? <table className="score"><tbody>{q.components.map((c) => <tr key={c.item}><td>{c.item}</td><td className="mono">{c.count}</td></tr>)}</tbody></table> : <p className="empty" style={{ marginTop: 0 }}>No component list yet.</p>}
              <p>Estimated prototype cost: <b className="mono">{q.cost != null ? `$${q.cost}` : '—'}</b></p>
            </div>
          </div>
          <div className="pitch-actions">
            <button className="link" onClick={() => onOpen(q.slug)}>Open the full overview</button>
            <div className="muted small">Tell Claude Code:</div>
            <CopyBox text={`approve ${q.slug}`} />
            <CopyBox text={`reject ${q.slug}`} />
            <CopyBox text={`send ${q.slug} back with notes: ...`} />
          </div>
        </section>
      ))}

      <div className="gp-grid" style={{ marginTop: 12 }}>
        <section className="card">
          <h3>Your past decisions</h3>
          {state.decisions.length === 0 && <p className="empty">No decisions recorded yet.</p>}
          {state.decisions.map((d, i) => <div className="item" key={i}><b>{d.decision}</b> {d.slug}<div className="meta">{d.notes} {d.time ? `· ${ago(d.time)}` : ''}</div></div>)}
        </section>
        <section className="card">
          <h3>Your playtests</h3>
          {sessions.length === 0 && <p className="empty">No real playtests recorded yet. After you play a prototype, tell Claude Code how it went, for example "we played lantern-heist, fun 4, replay 4, clarity 3".</p>}
          {sessions.length > 0 && <table className="score"><thead><tr className="muted"><td>Game</td><td>Fun</td><td>Replay</td><td>Clarity</td></tr></thead><tbody>{sessions.map((s, i) => <tr key={i}><td>{s.title}<div className="muted small">{s.date}</div></td><td className="mono">{s.fun}</td><td className="mono">{s.replay}</td><td className="mono">{s.clarity}</td></tr>)}</tbody></table>}
        </section>
        <section className="card">
          <h3>Do the agents agree with you? <Help topic="kpi" /></h3>
          {r.gapRows.length === 0 && <p className="empty">Needs a critique and at least one real playtest of the same game.</p>}
          {r.gapRows.map((g) => <div className="item" key={g.slug}><b>{g.title}</b>: critic fun {g.criticFun}, you {g.humanFun}<div className="meta">gap {g.gap > 0 ? '+' : ''}{g.gap} {Math.abs(g.gap) > 1 ? ' · the critic may need recalibrating' : ''}</div></div>)}
        </section>
      </div>
    </div>
  );
}
