import { clock } from '../util.js';

// One stream of every agent's updates, newest first.
export function ActivityFeed({ state }) {
  const byId = Object.fromEntries(state.agents.map((a) => [a.id, a]));
  const rows = state.activity.slice(0, 40);
  return (
    <div className="feed">
      <h3>Activity feed</h3>
      {rows.length === 0 && <div className="empty">No activity yet. Agents add lines to games/&lt;game&gt;/activity.jsonl as they work.</div>}
      {rows.map((e, i) => {
        const a = byId[e.agent];
        return (
          <div className="row" key={i}>
            <span className="time">{clock(e.time)}</span>
            <span className="who" style={{ color: a?.color }}>{a?.room || e.agent}</span>
            <span className="game">{e.game}</span>
            <span className={e.event === 'error' ? 'err' : ''}>{e.message}</span>
          </div>
        );
      })}
    </div>
  );
}
