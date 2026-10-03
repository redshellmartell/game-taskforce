import { useState } from 'react';
import { FileView } from './Markdown.jsx';
import { CopyBox } from './IdeaForm.jsx';
import { Help } from './Help.jsx';
import { STAGE_LABEL, verdictClass } from './ProjectsView.jsx';
import { ago, clock } from '../util.js';
import { CriticRadar, RateBars, CardCorrelation, LengthHistogram, colorOf } from './charts.jsx';

const DOCS = [['brief.md', 'Brief'], ['rules.md', 'Rules'], ['playtest-report.md', 'Playtest report'], ['critique.md', 'Critique'], ['pitch.md', 'Pitch']];

// What the owner can do next, as a prompt to paste into Claude Code.
function nextStep(g) {
  switch (g.stage) {
    case 'owner-review': return { text: 'This pitch is waiting for your decision.', prompt: `approve ${g.slug}`, alt: [`reject ${g.slug}`, `send ${g.slug} back with notes: ...`] };
    case 'killed': case 'archived': return { text: g.kill_reason ? `Stopped: ${g.kill_reason}` : 'This game was stopped.' };
    case 'approved': return { text: 'Approved. Build a prototype, then tell Claude Code how it went.', prompt: `I built a prototype of ${g.slug}` };
    default: return { text: `In progress at ${STAGE_LABEL[g.stage] || g.stage}.`, prompt: `Show me the status of ${g.slug}` };
  }
}

export function GamePage({ game: g, state, onBack }) {
  const [doc, setDoc] = useState(() => (DOCS.find(([f]) => g.files.some((x) => x.name === f)) || DOCS[0])[0]);
  const cr = g.critique, pt = g.playtest, step = nextStep(g);
  const events = state.activity.filter((e) => e.game === g.slug).slice().reverse();
  const hasDoc = (f) => g.files.some((x) => x.name === f);
  const meta = [g.pitch?.players || g.brief?.players, (g.pitch?.minutes || g.brief?.minutes) && `${g.pitch?.minutes || g.brief?.minutes} min`, g.pitch?.age, (g.pitch?.complexity || g.brief?.complexity) != null && `complexity ${g.pitch?.complexity ?? g.brief?.complexity}/5`].filter(Boolean).join(' · ');

  return (
    <div className="gamepage">
      <button className="link back" onClick={onBack}>← All projects</button>
      <header className="gp-head">
        <div>
          <h2>{g.title}</h2>
          {g.pitch?.hook && <p className="hook">{g.pitch.hook}</p>}
          <div className="muted">{meta || 'No details recorded yet.'}</div>
        </div>
        <div className="gp-chips">
          <span className="chip big">{STAGE_LABEL[g.stage] || g.stage}</span>
          {g.verdicts?.playtest && <span className={`chip big v-${verdictClass(g.verdicts.playtest)}`}>playtest: {g.verdicts.playtest} <Help topic="verdict" /></span>}
          {g.verdicts?.critic && <span className={`chip big v-${verdictClass(g.verdicts.critic)}`}>critic: {g.verdicts.critic}</span>}
          {g.revision > 0 && <span className="chip big">revision {g.revision} of 3</span>}
        </div>
      </header>
      {g.derived && <p className="notice">The agents have not written status.json or the JSON data files for this game yet, so its stage is worked out from the files that exist and scores show "no data yet". They fill these in from the next run.</p>}

      <div className="gp-grid">
        <section className="card">
          <h3>Scorecard <Help topic="kpi" /></h3>
          <table className="score"><tbody>
            {g.scorecard.map((r) => (
              <tr key={r.id} className={r.status}><td>{r.label}</td><td className="mono val">{r.value === null ? 'no data yet' : `${r.value}${r.unit || ''}`}</td><td className="muted">target {r.target}</td><td><i className="mark" title={r.status} /></td></tr>
            ))}
          </tbody></table>
        </section>
        <section className="card">
          <h3>Critic scores</h3>
          <CriticRadar scores={cr?.scores} color={colorOf(state, 'critic')} />
          {cr?.strength && <p><b>Strength:</b> {cr.strength}</p>}
          {cr?.weakness && <p><b>Weakness:</b> {cr.weakness}</p>}
          {cr?.closest_existing_game?.name && <p className="muted">Closest existing game: {cr.closest_existing_game.name} ({cr.closest_existing_game.similarity} similarity)</p>}
        </section>
        <section className="card">
          <h3>Balance <span className="muted" style={{ fontWeight: 400 }}>{pt?.games_simulated ? `${pt.games_simulated.toLocaleString()} simulated games` : ''}</span></h3>
          <h4>Win rate by seat</h4>
          <RateBars rates={pt?.seat_win_rates} color={colorOf(state, 'playtester')} fair={pt ? 100 / Math.max(1, Object.keys(pt.seat_win_rates || {}).length) : null} prefix="seat " />
          <h4>Win rate by bot</h4>
          <RateBars rates={pt?.bot_win_rates} color={colorOf(state, 'playtester')} />
          <h4>Game length (turns)</h4>
          <LengthHistogram length={pt?.length} histogram={pt?.length_histogram} color={colorOf(state, 'playtester')} />
          <h4>Card win correlation</h4>
          <CardCorrelation cards={pt?.cards} />
          {pt?.problems?.length > 0 && <><h4>Problems found</h4>{pt.problems.map((p, i) => <div className="item" key={i}><span className={`chip sev-${p.severity}`}>{p.severity}</span> {p.problem}<div className="meta">{p.fix}</div></div>)}</>}
        </section>
        <section className="card">
          <h3>What happens next</h3>
          <p style={{ marginTop: 0 }}>{step.text}</p>
          {step.prompt && <><div className="muted small">Tell Claude Code:</div><CopyBox text={step.prompt} />{step.alt?.map((a) => <CopyBox key={a} text={a} />)}</>}
          {g.humanPlaytests.length > 0 && <><h4>Your playtests</h4>{g.humanPlaytests.map((s, i) => <div className="item" key={i}>{s.date}: fun {s.fun}/5, replay {s.replay}/5, clarity {s.clarity}/5<div className="meta">{s.notes}</div></div>)}</>}
        </section>
      </div>

      <section className="card">
        <h3>History</h3>
        {g.history.length > 0
          ? <ol className="timeline">{g.history.map((h, i) => <li key={i}><b>{STAGE_LABEL[h.stage] || h.stage}</b>{h.verdict && <span className={`chip v-${verdictClass(h.verdict)}`}>{h.verdict}</span>} <span className="muted">{h.note} · {ago(h.time)}</span></li>)}</ol>
          : events.length > 0
            ? <ol className="timeline">{events.map((e, i) => <li key={i}><span className="mono muted">{clock(e.time)}</span> <b>{state.agents.find((a) => a.id === e.agent)?.room || e.agent}</b> <span className="muted">{e.message}{e.synthetic ? ' (inferred from file)' : ''}</span></li>)}</ol>
            : <p className="empty">No history yet.</p>}
      </section>

      <section className="card">
        <h3>Documents</h3>
        <div className="tabs doc-tabs">{DOCS.map(([f, label]) => <button key={f} className={`tab ${doc === f ? 'on' : ''}`} disabled={!hasDoc(f)} onClick={() => setDoc(f)}>{label}</button>)}</div>
        <div className="doc-body"><FileView path={`games/${g.slug}/${doc}`} version={state.generatedAt} /></div>
      </section>
    </div>
  );
}
