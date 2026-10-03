import { useEffect } from 'react';
import { replayEvents } from '../replay.js';
import { clock } from '../util.js';

const STEP_MS = 1800;

// Choose a game, then step through its activity log (or press play).
export function Replay({ state, replay, setReplay }) {
  const games = state.games.filter((g) => replayEvents(state, g.slug).length > 0);
  const events = replay ? replayEvents(state, replay.slug) : [];

  useEffect(() => {
    if (!replay?.playing) return undefined;
    const t = setTimeout(() => {
      setReplay((r) => (!r ? r : r.index >= events.length - 1 ? { ...r, playing: false } : { ...r, index: r.index + 1 }));
    }, STEP_MS);
    return () => clearTimeout(t);
  }, [replay, events.length, setReplay]);

  const start = (slug) => setReplay(slug ? { slug, index: 0, playing: false } : null);
  const go = (i) => setReplay((r) => ({ ...r, index: Math.max(0, Math.min(events.length - 1, i)), playing: false }));
  const cur = replay ? events[replay.index] : null;
  const agent = cur ? state.agents.find((a) => a.id === cur.agent) : null;

  return (
    <div className="replaybar">
      <label className="muted">Replay a game</label>
      <select value={replay?.slug || ''} onChange={(e) => start(e.target.value)}>
        <option value="">Choose a game…</option>
        {games.map((g) => <option key={g.slug} value={g.slug}>{g.title}</option>)}
      </select>
      {replay && cur && (
        <>
          <button onClick={() => go(0)} title="Back to the start" aria-label="First step">⏮</button>
          <button onClick={() => go(replay.index - 1)} disabled={replay.index === 0} aria-label="Previous step">◀</button>
          <button className="play" onClick={() => setReplay((r) => (r.index >= events.length - 1 ? { ...r, index: 0, playing: true } : { ...r, playing: !r.playing }))} aria-label={replay.playing ? 'Pause' : 'Play'}>{replay.playing ? '⏸' : '▶'}</button>
          <button onClick={() => go(replay.index + 1)} disabled={replay.index >= events.length - 1} aria-label="Next step">▶|</button>
          <span className="mono muted">{replay.index + 1}/{events.length}</span>
          <span className="rp-msg"><b style={{ color: agent?.color }}>{agent?.room || cur.agent}</b> · {cur.message} <span className="muted">({clock(cur.time)})</span></span>
          <button className="link" onClick={() => start('')}>Exit replay</button>
        </>
      )}
      {!replay && <span className="muted">Pick a game to watch how the team worked on it, step by step.</span>}
    </div>
  );
}
