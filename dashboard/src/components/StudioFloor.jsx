import { useState } from 'react';
import { AgentPanel } from './SidePanel.jsx';
import { ActivityFeed } from './ActivityFeed.jsx';
import { GATE_LABEL } from './ApprovalsView.jsx';
import { ago, STATE_LABEL } from '../util.js';

// A room card: who is in it, what they are doing, and the department's two key numbers.
function RoomCard({ a, stats, state, selected, onSelect }) {
  const game = state.games.find((g) => g.slug === a.currentGame);
  const panelStats = a.id === 'test-panel' ? state.panel?.stats : null;
  const line = panelStats && a.state !== 'working' ? `${panelStats.gamesWithPanel} game${panelStats.gamesWithPanel === 1 ? '' : 's'} scored${panelStats.room.lastGame ? `; last: ${panelStats.room.lastGame}` : ''}`
    : a.state === 'working' ? `${game?.title || a.currentGame}: ${a.lastEvent.message}`
    : a.waitingGate ? `Waiting for you: ${GATE_LABEL[a.waitingGate.gate] || a.waitingGate.gate}${a.waitingGate.gameTitle ? ` (${a.waitingGate.gameTitle})` : ''}`
    : a.state === 'waiting' ? `${state.waitingPitches.length} pitch${state.waitingPitches.length === 1 ? '' : 'es'} for your review`
    : a.lastEvent ? `Last: ${a.lastEvent.message} (${ago(a.lastEvent.time)})` : 'No activity yet';
  return (
    <button className={`room ${a.state} ${selected ? 'selected' : ''}`} style={{ '--accent': a.color }} onClick={() => onSelect(a.id)}>
      <div className="room-head"><b style={{ color: a.color }}>{a.room}</b><span className="status"><i className="dot" />{STATE_LABEL[a.state]}</span></div>
      <div className="room-line">{line}</div>
      <div className="room-stats">
        {(stats || []).map((s) => <div key={s.label}><span className="mono big">{s.value}{s.unit || ''}</span><span className="lbl">{s.label}</span></div>)}
      </div>
    </button>
  );
}

// The KPI screen: room cards, sidebar with a mini funnel, shared feed and a milestone ticker.
export function StudioFloor({ state }) {
  const [sel, setSel] = useState(null);
  const agent = state.agents.find((a) => a.id === sel);
  const maxCount = Math.max(1, ...state.pipeline.funnel.map((f) => f.count));
  return (
    <div className="floor-wrap">
      <div className={`floor ${agent ? 'open' : ''}`}>
        <aside className="sidebar">
          <h3>Agents</h3>
          {state.agents.map((a) => (
            <button key={a.id} className={`side-agent ${sel === a.id ? 'on' : ''}`} onClick={() => setSel(sel === a.id ? null : a.id)}>
              <i className={`dot ${a.state}`} style={{ '--accent': a.color }} /><span><b>{a.room}</b><small>{a.state === 'working' ? `working on ${state.games.find((g) => g.slug === a.currentGame)?.title || a.currentGame}` : STATE_LABEL[a.state]}</small></span>
            </button>
          ))}
          <h3 style={{ marginTop: 18 }}>Funnel</h3>
          {state.pipeline.funnel.map((f) => (
            <div className="mini" key={f.id}><span>{f.label}</span><i style={{ width: `${(f.count / maxCount) * 100}%` }} /><b className="mono">{f.count}</b></div>
          ))}
        </aside>
        <main className="floor-main">
          <div className="rooms">
            {state.agents.map((a) => <RoomCard key={a.id} a={a} stats={state.pipeline.rooms[a.id]} state={state} selected={sel === a.id} onSelect={(id) => setSel(sel === id ? null : id)} />)}
          </div>
          <ActivityFeed state={state} filterable />
        </main>
        {agent && <AgentPanel agent={agent} state={state} onClose={() => setSel(null)} />}
      </div>
      <div className="ticker" aria-label="Milestones">
        <b>Milestones</b>
        {state.pipeline.milestones.length === 0 && <span className="muted">Nothing yet. Pitches, kills, balance problems and your decisions appear here.</span>}
        {state.pipeline.milestones.map((m, i) => <span key={i} className={`tick k-${m.kind}`}>{'▸'} {m.text}</span>)}
      </div>
    </div>
  );
}
