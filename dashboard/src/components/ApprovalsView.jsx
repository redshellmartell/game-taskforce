import { CopyBox } from './IdeaForm.jsx';
import { Help } from './Help.jsx';
import { ago } from '../util.js';

export const GATE_LABEL = { scan: 'Market scan', greenlight: 'Start design', revision: 'Revision loop', 'panel-research': 'Panel research', 'panel-reviews': 'Persona reviews', budget: 'Over budget', 'free-api': 'Free AI provider' };
const USAGE = { S: ['S', 'a few short agent calls'], M: ['M', 'one agent pass, such as a revision or a brief'], L: ['L', 'a full stage with simulation work or research'], XL: ['XL', 'a market scan or panel research'] };
const STATE_CLASS = { approved: 'v-good', declined: 'v-warn', expired: 'v-bad', pending: 'v-warn' };

// What to tell Claude Code for one option (the Director's reply formats are in CLAUDE.md, "Approval gates").
const replyFor = (r, o) => (o.key === 'approve' ? `approve ${r.id}` : `${o.key} ${r.game || r.id}`);

function RevisionContext({ rev }) {
  return (
    <div className="rev-context">
      <h4>Is another revision worth it?</h4>
      {rev.worthIt === null ? <p className="muted small" style={{ marginTop: 0 }}>The critic has not answered this yet. Revisions done so far: {rev.revisionsDone}.</p>
        : <p style={{ marginTop: 0 }}><span className={`chip ${rev.worthIt ? 'v-good' : 'v-warn'}`}>critic: {rev.worthIt ? 'yes' : 'no'}</span> {rev.reason}</p>}
      <h4>Where the last playtest stands against the targets</h4>
      <table className="score"><tbody>{rev.scorecard.map((r) => (
        <tr key={r.id} className={r.status}><td>{r.label}</td><td className="mono val">{r.value}{r.unit || ''}</td><td className="muted">target {r.target}</td><td><i className="mark" title={r.status} /></td></tr>))}</tbody></table>
    </div>
  );
}

function Card({ r, onOpen, decided }) {
  const u = USAGE[r.usage_estimate];
  return (
    <section className={`card approval ${decided ? 'decided' : ''}`}>
      <div className="pitch-head">
        <div>
          <span className="chip big">{GATE_LABEL[r.gate] || r.gate}</span>{' '}
          {r.gameTitle && <button className="link" onClick={() => onOpen(r.game)}>{r.gameTitle}</button>}
          <div className="muted small">{r.id} · asked {r.ageDays === 0 ? 'today' : `${r.ageDays} day${r.ageDays === 1 ? '' : 's'} ago`}</div>
        </div>
        <div className="gp-chips">
          {r.state !== 'pending' && <span className={`chip big ${STATE_CLASS[r.state]}`}>{r.state}{r.decision && r.state !== 'expired' ? `: ${r.decision}` : ''}</span>}
          {u && <span className="chip big" title={`Usage estimate ${u[0]}: ${u[1]}`}>usage {u[0]}</span>}
          {r.recommendation && <span className="chip big v-good">Director recommends: {r.recommendation}</span>}
        </div>
      </div>
      <p style={{ marginBottom: 6 }}>{r.summary}</p>
      {!decided && (
        <>
          <div className="pitch-cols">
            <div><h4>Why it is needed</h4><p style={{ marginTop: 0 }}>{r.why_needed}</p></div>
            <div><h4>What should change</h4><p style={{ marginTop: 0 }}>{r.expected_outcome}</p></div>
          </div>
          {r.revision && <RevisionContext rev={r.revision} />}
          <div className="pitch-actions">
            <div className="muted small">Your options. For now, reply to Claude Code with the line next to the one you choose:</div>
            {r.options.map((o) => <div key={o.key} className="opt"><span>{o.label}</span><CopyBox text={replyFor(r, o)} /></div>)}
          </div>
        </>
      )}
      {decided && r.owner_notes && <p className="muted small" style={{ marginBottom: 0 }}>Your note: {r.owner_notes}{r.decided_at ? ` (${ago(r.decided_at)})` : ''}</p>}
    </section>
  );
}

// Requests the Director has stopped on, waiting for the owner. Decided and expired ones are listed below.
export function ApprovalsView({ state, onOpen }) {
  const all = state.approvals.requests;
  const pending = all.filter((r) => r.state === 'pending'), done = all.filter((r) => r.state !== 'pending');
  return (
    <div className="view">
      <div className="plist-head"><h2>Waiting for you <Help topic="kpi" /></h2><span className="muted">{pending.length} request{pending.length === 1 ? '' : 's'}, oldest first.</span></div>
      <p className="notice info">The Director stops before steps that use a lot of usage or could loop (see "Approval gates" in CLAUDE.md). Nothing here runs until you answer.</p>
      {pending.length === 0 && <div className="card"><p className="empty" style={{ margin: 0 }}>Nothing is waiting for you.</p></div>}
      {pending.map((r) => <Card key={r.id} r={r} onOpen={onOpen} />)}
      {done.length > 0 && <h3 className="sect">Decided and expired</h3>}
      {done.map((r) => <Card key={r.id} r={r} onOpen={onOpen} decided />)}
    </div>
  );
}
