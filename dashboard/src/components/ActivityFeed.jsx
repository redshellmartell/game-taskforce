import { useState } from 'react';
import { ownerPrefix } from './OwnerMark.jsx';
import { clock } from '../util.js';
import { Help } from './Help.jsx';

// One stream of every agent's updates, newest first. With `filterable`, narrow it by agent or game.
export function ActivityFeed({ state, filterable }) {
  const [agentF, setAgentF] = useState('');
  const [gameF, setGameF] = useState('');
  const byId = Object.fromEntries(state.agents.map((a) => [a.id, a]));
  const byGame = Object.fromEntries(state.games.map((g) => [g.slug, g]));
  const rows = state.activity.filter((e) => (!agentF || e.agent === agentF) && (!gameF || e.game === gameF)).slice(0, 40);
  return (
    <div className="feed">
      <h3>Activity feed <Help topic="activity-log" />
        {filterable && (
          <span className="filters">
            <select value={agentF} onChange={(e) => setAgentF(e.target.value)} aria-label="Filter by agent"><option value="">All agents</option>{state.agents.map((a) => <option key={a.id} value={a.id}>{a.room}</option>)}</select>
            <select value={gameF} onChange={(e) => setGameF(e.target.value)} aria-label="Filter by game"><option value="">All games</option>{state.games.map((g) => <option key={g.slug} value={g.slug}>{ownerPrefix(g)}{g.title}</option>)}</select>
          </span>
        )}
      </h3>
      {rows.length === 0 && <div className="empty">No activity yet. Agents add lines to games/&lt;game&gt;/activity.jsonl as they work.</div>}
      {rows.map((e, i) => {
        const a = byId[e.agent];
        return (
          <div className="row" key={i}>
            <span className="time" title={e.time_estimated ? 'time estimated by an agent without a clock' : undefined}>{e.time_estimated ? '~' : ''}{clock(e.time)}</span>
            <span className="who" style={{ color: a?.color }}>{a?.room || e.agent}</span>
            <span className="game">{ownerPrefix(byGame[e.game])}{e.game}</span>
            <span className={e.event === 'error' ? 'err' : ''}>{e.message}</span>
          </div>
        );
      })}
    </div>
  );
}
