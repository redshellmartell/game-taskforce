import { useState } from 'react';
import { ApprovalCard, GATE_LABEL } from './ApprovalsView.jsx';
import { verdictClass } from './ProjectsView.jsx';
import { OwnerMark } from './OwnerMark.jsx';
import { CopyBox } from './IdeaForm.jsx';

// Which agent works on a game in each stage.
const STAGE_AGENT = { brief: 'market-researcher', design: 'game-designer', playtest: 'playtester', critique: 'critic', pitch: 'manager', 'owner-review': 'manager' };
const STAGE_NAME = { brief: 'brief', design: 'design', playtest: 'playtest', critique: 'critique', pitch: 'pitch', 'owner-review': 'waiting for you' };

// A short note to this agent, saved for the Director to read (same endpoint as the Talk tab).
export function QuickNote({ agent, game }) {
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState(null);
  const send = async () => {
    setBusy(true); setMsg(null);
    try {
      const r = await fetch('/api/notes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ agent: agent.id, game: game || null, note }) });
      const body = await r.json(); if (!r.ok) throw new Error(body.error || 'Could not save the note');
      setMsg({ ok: true, text: 'Saved. The Director reads it at the start of the next session.' }); setNote('');
    } catch (e) { setMsg({ ok: false, text: e.message }); }
    setBusy(false);
  };
  return (
    <div className="quicknote">
      <textarea rows={2} value={note} onChange={(e) => setNote(e.target.value)} placeholder={`A short note for ${agent.room}…`} style={{ width: '100%' }} />
      <div className="pitch-buttons"><button className="primary" disabled={busy || !note.trim()} onClick={send}>{busy ? 'Saving…' : 'Send note'}</button>{msg && <span className={msg.ok ? 'saved-ok small' : 'saved-err small'} role="status">{msg.text}</span>}</div>
    </div>
  );
}

// Everything you can do with one agent without leaving the org map.
export function AgentActions({ agent, state, onOpenGame, onNavigate }) {
  const [last, setLast] = useState(null);
  const mine = state.approvals.requests.filter((r) => r.state === 'pending' && r.agentId === agent.id);
  const here = state.games.filter((g) => STAGE_AGENT[g.stage] === agent.id);
  const pendingNotes = (state.notes || []).filter((n) => n.agent === agent.id && !n.done).length;
  return (
    <div className="agent-actions">
      {agent.id === 'manager' && (
        <div className="action-tiles">
          <button className="action-tile" onClick={() => onNavigate('approvals')}><span className="at-title">Approvals waiting for you <span className="chip v-warn">{state.approvals.pending}</span></span><span className="at-blurb">Revision loops, greenlights, scans and budget requests.</span><span className="at-foot"><span className="at-go">Open →</span></span></button>
          <button className="action-tile" onClick={() => onNavigate('review')}><span className="at-title">Pitches waiting for you <span className="chip v-warn">{state.waitingPitches.length}</span></span><span className="at-blurb">Approve, send back or reject.</span><span className="at-foot"><span className="at-go">Open →</span></span></button>
          <div className="action-tile static"><span className="at-title">Carry out what you approved</span><span className="at-blurb">Tell the Director in a Claude Code session:</span><CopyBox text="Continue with approved work" /></div>
        </div>
      )}
      {mine.length > 0 && (
        <>
          <h4>Waiting for you here ({mine.length})</h4>
          {last && <p className="saved-ok small">Recorded: {last.label}. Tell the Director: <span className="mono">continue with approved work</span></p>}
          {mine.map((r) => <ApprovalCard key={r.id} r={r} onOpen={onOpenGame} sample={state.sample} onDecided={setLast} />)}
        </>
      )}
      <h4>Games with {agent.room} now ({here.length})</h4>
      {here.length === 0 && <p className="empty">None right now.</p>}
      {here.map((g) => (
        <button key={g.slug} className="game-row" onClick={() => onOpenGame(g.slug)}>
          <span><OwnerMark game={g} /> <b>{g.title}</b></span>
          <span className="muted small">{STAGE_NAME[g.stage]}</span>
          {g.verdicts?.critic && <span className={`chip v-${verdictClass(g.verdicts.critic)}`}>{g.verdicts.critic}</span>}
          {!g.verdicts?.critic && g.verdicts?.playtest && <span className={`chip v-${verdictClass(g.verdicts.playtest)}`}>{g.verdicts.playtest}</span>}
        </button>))}
      <h4>Send a note to {agent.room}{pendingNotes ? ` (${pendingNotes} waiting)` : ''}</h4>
      <QuickNote agent={agent} />
    </div>
  );
}
