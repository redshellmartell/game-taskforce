// Replay helpers: a game's journey through the network, one activity line at a time.
// Handoff lines that exist in the diagram (NetworkView draws exactly these).
export const FORWARD = [
  ['market-researcher', 'game-designer', 'brief.md'],
  ['game-designer', 'playtester', 'rules.md'],
  ['playtester', 'critic', 'playtest-report.md'],
  ['critic', 'manager', 'critique.md'],
  ['manager', 'owner', 'pitch.md'],
];
export const REVISIONS = [
  ['playtester', 'game-designer', 'playtest-report.md', 'bt'],
  ['critic', 'game-designer', 'critique.md', 'bt2'],
];

// Activity lines for one game, oldest first.
export function replayEvents(state, slug) {
  return state.activity.filter((e) => e.game === slug).slice().reverse();
}

// Which handoff line should a dot travel along between two agents? Returns an edge id or null.
export function edgeBetween(from, to) {
  if (FORWARD.some(([s, t]) => s === from && t === to)) return `${from}>${to}`;
  if (REVISIONS.some(([s, t]) => s === from && t === to)) return `rev:${from}>${to}`;
  return null;
}

// What the diagram shows at step `index`: the active agent and (maybe) a travelling dot.
export function replayFrame(events, index, gameTitle, slug) {
  const e = events[index];
  if (!e) return null;
  const prev = index > 0 ? events[index - 1] : null;
  const edgeId = prev && prev.agent !== e.agent ? edgeBetween(prev.agent, e.agent) : null;
  return { event: e, agent: e.agent, dot: edgeId ? { edgeId, key: `${slug}-${index}`, label: gameTitle } : null };
}
