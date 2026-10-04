import { useEffect, useState } from 'react';
import { FileView, Markdown } from './Markdown.jsx';
import { Help } from './Help.jsx';
import { IdeaForm, CopyBox, stageForAgent } from './IdeaForm.jsx';
import { PanelTab } from './PanelTab.jsx';
import { ResearchTab } from './ResearchTab.jsx';
import { GATE_LABEL } from './ApprovalsView.jsx';
import { ago, STATE_LABEL } from '../util.js';

const summaries = import.meta.glob('../content/agents/*.md', { query: '?raw', import: 'default', eager: true });
const summaryFor = (id) => summaries[`../content/agents/${id}.md`] || '';

function Shell({ title, help, color, onClose, tabs, tab, setTab, children }) {
  return (
    <aside className="panel" style={{ '--accent': color }}>
      <header><h2>{title} {help}</h2><button className="close" onClick={onClose} aria-label="Close">×</button></header>
      {tabs && <div className="tabs">{tabs.map(([id, label]) => <button key={id} className={`tab ${tab === id ? 'on' : ''}`} onClick={() => setTab(id)}>{label}</button>)}</div>}
      <div className="body">{children}</div>
    </aside>
  );
}

function Viewing({ path, version, onBack }) {
  return <><button className="link back" onClick={onBack}>← Back</button><FileView path={path} version={version} /></>;
}

// "Talk to it": leave a note for this agent, or start one of your own ideas at its stage.
function TalkTab({ agent, state }) {
  const [game, setGame] = useState('');
  const [note, setNote] = useState('');
  const where = game || 'a new game';
  const prompt = `Ask the ${agent.id} agent to work on ${game ? `games/${game}` : 'a new game'}: ${note.trim() || '(write your note above)'}`;
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState(null);
  const mine = (state.notes || []).filter((n) => n.agent === agent.id);
  const send = async () => {
    setBusy(true); setMsg(null);
    try {
      const r = await fetch('/api/notes', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ agent: agent.id, game: game || null, note }) });
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || 'Could not save the note');
      setMsg({ ok: true, text: `Saved (${body.file}). The Director reads it at the start of the next session.` }); setNote('');
    } catch (e) { setMsg({ ok: false, text: e.message }); }
    setBusy(false);
  };
  return (
    <>
      <h4 style={{ marginTop: 0 }}>Leave a note for {agent.room}</h4>
      <p className="muted" style={{ marginTop: 0 }}>The dashboard cannot run agents. Write your note, copy the prompt and paste it into Claude Code; the Director will hand it to this agent.</p>
      <div className="ideaform">
        <label>About which game?
          <select value={game} onChange={(e) => setGame(e.target.value)}>
            <option value="">A new game</option>
            {state.games.map((g) => <option key={g.slug} value={g.slug}>{g.title}</option>)}
          </select>
        </label>
        <label>Your note<textarea rows={3} value={note} onChange={(e) => setNote(e.target.value)} placeholder={`e.g. Focus on 2-player games for ${where}`} /></label>
        <button type="button" className="primary" disabled={busy || !note.trim()} onClick={send}>{busy ? 'Saving…' : `Send note to ${agent.room}`}</button>
        {!note.trim() && <p className="muted small" style={{ margin: 0 }}>Write a note to enable the button.</p>}
        {msg && <p className={msg.ok ? 'saved-ok' : 'saved-err'} role="status" style={{ margin: 0 }}>{msg.text}</p>}
        <details><summary className="muted small">Or copy a prompt to paste into Claude Code yourself</summary><CopyBox text={prompt} /></details>
      </div>
      {mine.length > 0 && <>
        <h4>Your notes to {agent.room}</h4>
        {mine.slice(0, 6).map((n) => (
          <div className="item" key={n.file}>
            <div>{n.text}</div>
            <div className="meta">{n.game ? `${n.game} · ` : ''}{n.done ? 'answered' : 'waiting for the Director'}</div>
            {n.reply && <div className="small" style={{ color: agent.color }}><b>Reply:</b> {n.reply}</div>}
          </div>))}
      </>}
      <IdeaForm key={agent.id} state={state} fixedStage={stageForAgent(agent.id)} heading={`Or start my own idea at ${agent.room}`} />
    </>
  );
}

// Click a node -> tabs: what it's doing, how it works, its work, talk to it.
export function AgentPanel({ agent, state, onClose, initialTab, onPersona }) {
  const [tab, setTab] = useState(initialTab || 'doing');
  const [viewing, setViewing] = useState(null);
  const [personaId, setPersonaId] = useState(null);   // kept here so "Back" from a file returns to the same persona
  useEffect(() => { setTab(initialTab || 'doing'); setViewing(null); setPersonaId(null); }, [agent.id, initialTab]);
  const version = state.generatedAt;
  const last = agent.lastEvent;
  const gameTitle = (slug) => state.games.find((g) => g.slug === slug)?.title || slug;

  let content;
  if (viewing) content = <Viewing path={viewing} version={version} onBack={() => setViewing(null)} />;
  else if (tab === 'doing') content = (
    <>
      <p style={{ marginTop: 0 }}>
        {agent.state === 'working' && <>Working on <b>{gameTitle(agent.currentGame)}</b>: {last.message}</>}
        {agent.state === 'idle' && (last ? <>Idle. Last finished: {last.message} ({gameTitle(last.game)}, {ago(last.time)}).</> : <>Idle. This agent has not logged any activity yet.</>)}
        {agent.waitingGate && <>Waiting for your approval: <b>{GATE_LABEL[agent.waitingGate.gate] || agent.waitingGate.gate}</b>{agent.waitingGate.gameTitle ? <> for {agent.waitingGate.gameTitle}</> : null}. Open the Approvals page to decide. </>}
        {agent.state === 'waiting' && !agent.waitingGate && <>Waiting for you to review {state.waitingPitches.length} pitch{state.waitingPitches.length === 1 ? '' : 'es'}.</>}
        {agent.state === 'error' && <>Something went wrong: {last.message}</>}
      </p>
      <h4>Recent steps</h4>
      {agent.recent.length === 0 && <p className="empty">No steps logged yet.</p>}
      {agent.recent.map((e, i) => (
        <div className="item" key={i}>{e.message}<div className="meta">{gameTitle(e.game)} · {e.event} · {ago(e.time)}{e.synthetic ? ' · inferred from file' : ''}{e.reconstructed ? ' · reconstructed from commits' : ''}</div></div>
      ))}
    </>
  );
  else if (tab === 'how') content = (
    <>
      <Markdown text={summaryFor(agent.id)} />
      <h4>Its job, in its own configuration</h4>
      <p style={{ marginTop: 0 }}>{agent.description || <span className="empty">No description found.</span>}</p>
      <h4>Tools it may use</h4>
      {agent.tools.length ? agent.tools.map((t) => <span className="chip" key={t}>{t}</span>) : <span className="muted">All the main session's tools</span>}
      <h4>Instruction file</h4>
      {agent.file ? <button className="link" onClick={() => setViewing(agent.file)}>{agent.file}</button> : <span className="mono muted">CLAUDE.md (repository root)</span>}
    </>
  );
  else if (tab === 'work') content = (
    <>
      <h4 style={{ marginTop: 0 }}>Reports written, newest first</h4>
      {agent.reports.length === 0 && <p className="empty">No reports yet.</p>}
      {agent.reports.map((r) => (
        <div className="item" key={r.path}><button className="link" onClick={() => setViewing(r.path)}>{r.name}</button><div className="meta">{r.gameTitle} · {ago(new Date(r.mtime).toISOString())}</div></div>
      ))}
    </>
  );
  else if (tab === 'research') content = <ResearchTab state={state} />;
  else if (tab === 'panel') content = <PanelTab state={state} onOpen={setViewing} id={personaId} setId={setPersonaId} onPersona={onPersona} />;
  else content = <TalkTab agent={agent} state={state} />;

  return (
    <Shell title={`${agent.room} · ${STATE_LABEL[agent.state]}`} color={agent.color} onClose={onClose}
      help={<><Help topic="agent" />{agent.id !== 'manager' && agent.id !== 'test-panel' && <Help topic="subagent" />}</>}
      tabs={[['doing', "What it's doing"], ['how', 'How it works'], ['work', 'Its work'], ...(agent.id === 'market-researcher' ? [['research', 'Research']] : []), ...(agent.id === 'playtester' || agent.id === 'test-panel' ? [['panel', 'Test panel']] : []), ['talk', 'Talk to it']]} tab={tab} setTab={(t) => { setViewing(null); setTab(t); }}>
      {content}
    </Shell>
  );
}

// You (the owner) node: inject your own ideas, and review what the agents pitched.
export function OwnerPanel({ state, onClose }) {
  const [tab, setTab] = useState('ideas');
  const [viewing, setViewing] = useState(null);
  const waiting = state.games.filter((g) => g.stage === 'owner-review');
  const stageName = { research: 'Market Intel', design: 'Design Studio', playtest: 'Playtest Lab', critique: 'Review Board', pitch: "Director's Office" };

  let content;
  if (viewing) content = <Viewing path={viewing} version={state.generatedAt} onBack={() => setViewing(null)} />;
  else if (tab === 'ideas') content = (
    <>
      <Markdown text={summaryFor('owner')} />
      <IdeaForm state={state} heading="Inject an idea of your own" />
      <h4>Ideas in your inbox</h4>
      {state.inbox.length === 0 && <p className="empty">No ideas waiting.</p>}
      {state.inbox.map((i) => (
        <div className="item" key={i.slug}>
          <button className="link" onClick={() => setViewing(i.file)}>{i.title}</button>
          <div className="meta">starts at {stageName[i.stage]} · {i.submitted ? ago(i.submitted) : ''}</div>
          <CopyBox text={`Process my idea "${i.title}" from ${i.file}. Start at the ${i.stage} stage.`} />
        </div>
      ))}
    </>
  );
  else content = (
    <>
      <h4 style={{ marginTop: 0 }}>Pitches waiting for you</h4>
      {waiting.length === 0 && <p className="empty">Nothing waiting.</p>}
      {waiting.map((g) => <div className="item" key={g.slug}><button className="link" onClick={() => setViewing(`games/${g.slug}/pitch.md`)}>{g.title}</button><div className="meta">read pitch.md</div></div>)}
      <h4>Your past decisions</h4>
      {state.decisions.length === 0 && <p className="empty">No decisions recorded yet.</p>}
      {state.decisions.map((d, i) => <div className="item" key={i}><b>{d.decision}</b> {d.slug}<div className="meta">{d.notes}</div></div>)}
    </>
  );
  return (
    <Shell title="You · the owner" color="#d9d4c7" onClose={onClose} tabs={[['ideas', 'Your ideas'], ['review', 'Review']]} tab={tab} setTab={(t) => { setViewing(null); setTab(t); }}>
      {content}
    </Shell>
  );
}

// Click a line -> the real file that was handed over, for the most recent game that passed along it.
export function EdgePanel({ edge, state, onClose }) {
  const candidates = state.games.map((g) => ({ g, f: g.files.find((f) => f.name === edge.file) })).filter((x) => x.f).sort((a, b) => b.f.mtime - a.f.mtime);
  const latest = candidates[0];
  return (
    <Shell title={`${edge.file} → ${edge.targetLabel}`} help={<Help topic={edge.revision ? 'revision-loop' : 'handoff'} />} color="#8a8f9b" onClose={onClose}>
      {edge.revision && <p className="muted" style={{ marginTop: 0 }}>This is a <b>revision</b> handoff: the report goes back to the Design Studio when problems are found.</p>}
      {latest ? <><p style={{ marginTop: 0 }}>Most recent game: <b>{latest.g.title}</b></p><FileView path={latest.f.path} version={state.generatedAt} /></>
        : <p className="empty">No game has passed along this line yet.</p>}
    </Shell>
  );
}
