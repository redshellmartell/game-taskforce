// Replay helpers: a game's journey through the network, one activity line at a time.
// Handoff arrows between the four specialists (NetworkView draws exactly these).
export const FORWARD = [
  ['market-researcher', 'game-designer', 'brief.md'],
  ['game-designer', 'playtester', 'rules.md'],
  ['playtester', 'critic', 'playtest-report.md'],
];
export const REVISIONS = [
  ['playtester', 'game-designer', 'playtest-report.md', 'bt'],
  ['critic', 'game-designer', 'critique.md', 'bt2'],
];
export const PITCH = ['manager', 'owner', 'pitch.md']; // Director -> You

// Activity lines for one game, oldest first.
export function replayEvents(state, slug) {
  return state.activity.filter((e) => e.game === slug).slice().reverse();
}

// Which line should a dot travel along between two agents? Returns { edgeId, reverse } or null.
// `reverse` means the dot runs against the line's drawn direction (an agent reporting up to the Director).
export function edgeBetween(from, to) {
  if (FORWARD.some(([s, t]) => s === from && t === to)) return { edgeId: `${from}>${to}`, reverse: false };
  if (REVISIONS.some(([s, t]) => s === from && t === to)) return { edgeId: `rev:${from}>${to}`, reverse: false };
  if (from === PITCH[0] && to === PITCH[1]) return { edgeId: `${from}>${to}`, reverse: false };
  if (to === 'manager' && from !== 'owner') return { edgeId: `org:${from}`, reverse: true };
  if (from === 'manager' && to !== 'owner') return { edgeId: `org:${to}`, reverse: false };
  return null;
}

// What the diagram shows at step `index`: the active agent and (maybe) a travelling dot.
export function replayFrame(events, index, gameTitle, slug) {
  const e = events[index];
  if (!e) return null;
  const prev = index > 0 ? events[index - 1] : null;
  const hop = prev && prev.agent !== e.agent ? edgeBetween(prev.agent, e.agent) : null;
  const agent = String(e.agent).startsWith('panel:') ? 'test-panel' : e.agent;
  return { event: e, agent, dot: hop ? { ...hop, key: `${slug}-${index}`, label: gameTitle } : null };
}
