import { useEffect, useState } from 'react';
import { FileView, Markdown } from './Markdown.jsx';
import { ago, STATE_LABEL } from '../util.js';

const summaries = import.meta.glob('../content/agents/*.md', { query: '?raw', import: 'default', eager: true });
const summaryFor = (id) => summaries[`../content/agents/${id}.md`] || '';

function Shell({ title, color, onClose, tabs, tab, setTab, children }) {
  return (
    <aside className="panel" style={{ '--accent': color }}>
      <header><h2>{title}</h2><button className="close" onClick={onClose} aria-label="Close">×</button></header>
      {tabs && <div className="tabs">{tabs.map(([id, label]) => <button key={id} className={`tab ${tab === id ? 'on' : ''}`} onClick={() => setTab(id)}>{label}</button>)}</div>}
      <div className="body">{children}</div>
    </aside>
  );
}

function Viewing({ path, version, onBack }) {
  return <><button className="link back" onClick={onBack}>← Back</button><FileView path={path} version={version} /></>;
}

// Click a node -> three tabs: what it's doing, how it works, its work.
export function AgentPanel({ agent, state, onClose }) {
  const [tab, setTab] = useState('doing');
  const [viewing, setViewing] = useState(null);
  useEffect(() => { setTab('doing'); setViewing(null); }, [agent.id]);
  const version = state.generatedAt;
  const open = (path) => setViewing(path);
  const last = agent.lastEvent;
  const gameTitle = (slug) => state.games.find((g) => g.slug === slug)?.title || slug;

  let content;
  if (viewing) content = <Viewing path={viewing} version={version} onBack={() => setViewing(null)} />;
  else if (tab === 'doing') content = (
    <>
      <p style={{ marginTop: 0 }}>
        {agent.state === 'working' && <>Working on <b>{gameTitle(agent.currentGame)}</b>: {last.message}</>}
        {agent.state === 'idle' && (last ? <>Idle. Last finished: {last.message} ({gameTitle(last.game)}, {ago(last.time)}).</> : <>Idle. This agent has not logged any activity yet.</>)}
        {agent.state === 'waiting' && <>Waiting for you to review {state.waitingPitches.length} pitch{state.waitingPitches.length === 1 ? '' : 'es'}.</>}
        {agent.state === 'error' && <>Something went wrong: {last.message}</>}
      </p>
      <h4>Recent steps</h4>
      {agent.recent.length === 0 && <p className="empty">No steps logged yet.</p>}
      {agent.recent.map((e, i) => (
        <div className="item" key={i}>{e.message}<div className="meta">{gameTitle(e.game)} · {e.event} · {ago(e.time)}{e.synthetic ? ' · inferred from file' : ''}</div></div>
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
      {agent.file ? <button className="link" onClick={() => open(agent.file)}>{agent.file}</button> : <span className="mono muted">CLAUDE.md (repository root)</span>}
    </>
  );
  else content = (
    <>
      <h4 style={{ marginTop: 0 }}>Reports written, newest first</h4>
      {agent.reports.length === 0 && <p className="empty">No reports yet.</p>}
      {agent.reports.map((r) => (
        <div className="item" key={r.path}><button className="link" onClick={() => open(r.path)}>{r.name}</button><div className="meta">{r.gameTitle} · {ago(new Date(r.mtime).toISOString())}</div></div>
      ))}
    </>
  );

  return (
    <Shell title={`${agent.room} · ${STATE_LABEL[agent.state]}`} color={agent.color} onClose={onClose}
      tabs={[['doing', "What it's doing"], ['how', 'How it works'], ['work', 'Its work']]} tab={tab} setTab={(t) => { setViewing(null); setTab(t); }}>
      {content}
    </Shell>
  );
}

// You (the owner) node.
export function OwnerPanel({ state, onClose }) {
  const [viewing, setViewing] = useState(null);
  const waiting = state.games.filter((g) => g.stage === 'owner-review');
  return (
    <Shell title="You · the owner" color="#d9d4c7" onClose={onClose}>
      {viewing ? <Viewing path={viewing} version={state.generatedAt} onBack={() => setViewing(null)} /> : (
        <>
          <Markdown text={summaryFor('owner')} />
          <h4>Pitches waiting for you</h4>
          {waiting.length === 0 && <p className="empty">Nothing waiting.</p>}
          {waiting.map((g) => <div className="item" key={g.slug}><button className="link" onClick={() => setViewing(`games/${g.slug}/pitch.md`)}>{g.title}</button><div className="meta">read pitch.md</div></div>)}
          <h4>Your past decisions</h4>
          {state.decisions.length === 0 && <p className="empty">No decisions recorded yet.</p>}
          {state.decisions.map((d, i) => <div className="item" key={i}><b>{d.decision}</b> {d.slug}<div className="meta">{d.notes}</div></div>)}
        </>
      )}
    </Shell>
  );
}

// Click a line -> the real file that was handed over, for the most recent game that passed along it.
export function EdgePanel({ edge, state, onClose }) {
  const candidates = state.games.map((g) => ({ g, f: g.files.find((f) => f.name === edge.file) })).filter((x) => x.f).sort((a, b) => b.f.mtime - a.f.mtime);
  const latest = candidates[0];
  return (
    <Shell title={`${edge.file} → ${edge.targetLabel}`} color="#8a8f9b" onClose={onClose}>
      {edge.revision && <p className="muted" style={{ marginTop: 0 }}>This is a <b>revision</b> handoff: the report goes back to the Design Studio when problems are found.</p>}
      {latest ? <><p style={{ marginTop: 0 }}>Most recent game: <b>{latest.g.title}</b></p><FileView path={latest.f.path} version={state.generatedAt} /></>
        : <p className="empty">No game has passed along this line yet.</p>}
    </Shell>
  );
}
