import { useMemo } from 'react';
import { ReactFlow, Handle, Position, MarkerType, BaseEdge } from '@xyflow/react';
import { ago } from '../util.js';

const STEP = 245;

function AgentNode({ data }) {
  const { label, sub, color, state, selected } = data;
  return (
    <div className={`node ${state} ${selected ? 'selected' : ''}`} style={{ '--accent': color }}>
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
      <Handle id="bs" type="source" position={Position.Bottom} style={{ left: '50%' }} />
      <Handle id="bt" type="target" position={Position.Bottom} style={{ left: '30%' }} />
      <Handle id="bt2" type="target" position={Position.Bottom} style={{ left: '70%' }} />
      <div className="room" style={{ color }}>{label}</div>
      <div className="sub">{sub}</div>
      <div className="state"><span className="dot" />{state === 'waiting' ? 'waiting for owner' : state}</div>
    </div>
  );
}
const nodeTypes = { agent: AgentNode };

// A dashed loop that dips below the nodes and comes back up to the Design Studio.
// (React Flow's built-in curve goes flat when both ends face downwards.)
function RevisionEdge({ id, sourceX, sourceY, targetX, targetY, markerEnd, style, label, data }) {
  const dip = data?.dip ?? 70;
  const path = `M ${sourceX},${sourceY} C ${sourceX},${sourceY + dip} ${targetX},${targetY + dip} ${targetX},${targetY}`;
  const lx = (sourceX + targetX) / 2;
  const ly = (sourceY + targetY) / 2 + dip * 0.75;
  return <BaseEdge id={id} path={path} markerEnd={markerEnd} style={style} label={label} labelX={lx} labelY={ly}
    labelStyle={{ fill: '#8a8f9b', fontSize: 11, fontFamily: 'monospace' }} labelBgStyle={{ fill: '#0e0f12' }} labelBgPadding={[6, 3]} />;
}
const edgeTypes = { revision: RevisionEdge };

// The handoff files that travel between agents (spec section 2).
const FORWARD = [
  ['market-researcher', 'game-designer', 'brief.md'],
  ['game-designer', 'playtester', 'rules.md'],
  ['playtester', 'critic', 'playtest-report.md'],
  ['critic', 'manager', 'critique.md'],
  ['manager', 'owner', 'pitch.md'],
];
const REVISIONS = [
  ['playtester', 'game-designer', 'playtest-report.md', 'bt'],
  ['critic', 'game-designer', 'critique.md', 'bt2'],
];

export function NetworkView({ state, selection, onSelect, compact }) {
  const { nodes, edges } = useMemo(() => {
    const byId = Object.fromEntries(state.agents.map((a) => [a.id, a]));
    const ownerWaiting = state.waitingPitches.length > 0;
    const order = [...state.agents.map((a) => a.id), 'owner'];
    const nodes = order.map((id, i) => {
      const a = byId[id];
      const isOwner = id === 'owner';
      const sub = isOwner
        ? (ownerWaiting ? `${state.waitingPitches.length} pitch${state.waitingPitches.length > 1 ? 'es' : ''} to review` : 'no pitch waiting')
        : a.state === 'working' ? (state.games.find((g) => g.slug === a.currentGame)?.title || a.currentGame)
        : a.lastEvent ? `last: ${ago(a.lastEvent.time)}` : 'no activity yet';
      const nodeState = isOwner ? (ownerWaiting ? 'waiting' : 'idle') : a.state === 'waiting' ? 'idle' : a.state; // owner shows the amber ring
      return {
        id, type: 'agent', position: { x: i * STEP, y: i % 2 ? 110 : 20 }, draggable: false,
        data: { label: isOwner ? 'You' : a.room, sub, color: isOwner ? '#d9d4c7' : a.color, state: nodeState, selected: selection?.id === id },
      };
    });
    const present = new Set(order);
    const label = (id) => (id === 'owner' ? 'You' : byId[id]?.room);
    const edges = [
      ...FORWARD.filter(([s, t]) => present.has(s) && present.has(t)).map(([s, t, file]) => ({
        id: `${s}>${t}`, source: s, target: t, label: file, type: 'default',
        markerEnd: { type: MarkerType.ArrowClosed, color: '#8a8f9b' }, style: { stroke: '#8a8f9b' },
        data: { file, targetLabel: label(t) }, selected: selection?.id === `${s}>${t}`,
      })),
      ...REVISIONS.filter(([s, t]) => present.has(s) && present.has(t)).map(([s, t, file, handle]) => ({
        id: `rev:${s}>${t}`, source: s, sourceHandle: 'bs', target: t, targetHandle: handle, label: 'revision', type: 'revision',
        markerEnd: { type: MarkerType.ArrowClosed, color: '#8a8f9b' }, style: { stroke: '#8a8f9b', strokeDasharray: '6 5' },
        data: { file, targetLabel: label(t), revision: true, dip: handle === 'bt' ? 55 : 95 }, selected: selection?.id === `rev:${s}>${t}`,
      })),
    ];
    return { nodes, edges };
  }, [state, selection]);

  return (
    <div className="net">
      <div className="hint">Click an agent to inspect it, or a line to see the file handed over.</div>
      <ReactFlow key={compact ? 'compact' : 'full'} nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes} fitView fitViewOptions={{ padding: 0.08 }} defaultEdgeOptions={{ labelBgPadding: [6, 3], labelBgBorderRadius: 3 }}
        nodesDraggable={false} nodesConnectable={false} elementsSelectable panOnDrag zoomOnScroll={false} minZoom={0.4}
        onNodeClick={(_, n) => onSelect({ type: n.id === 'owner' ? 'owner' : 'agent', id: n.id })}
        onEdgeClick={(_, e) => onSelect({ type: 'edge', id: e.id, edge: e.data })}
        onPaneClick={() => onSelect(null)} proOptions={{ hideAttribution: true }} />
    </div>
  );
}
