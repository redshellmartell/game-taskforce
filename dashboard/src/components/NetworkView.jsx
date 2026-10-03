import { useMemo } from 'react';
import { ReactFlow, Handle, Position, MarkerType, BaseEdge, getBezierPath } from '@xyflow/react';
import { ago } from '../util.js';
import { FORWARD, REVISIONS } from '../replay.js';
import { Help } from './Help.jsx';

const STEP = 245;
const GREY = '#8a8f9b';
const HELP_TOPIC = { playtester: 'simulation', critic: 'verdict' }; // every other node explains "agent"

function AgentNode({ data }) {
  const { id, label, sub, color, state, selected, active, isOwner } = data;
  return (
    <div className={`node ${state} ${selected ? 'selected' : ''} ${active ? 'active' : ''} ${isOwner ? 'owner' : ''}`} style={{ '--accent': color }}>
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
      <Handle id="or" type="target" position={Position.Right} style={{ top: '30%' }} />
      <Handle id="bs" type="source" position={Position.Bottom} style={{ left: '50%' }} />
      <Handle id="bt" type="target" position={Position.Bottom} style={{ left: '30%' }} />
      <Handle id="bt2" type="target" position={Position.Bottom} style={{ left: '70%' }} />
      <Handle id="tt" type="target" position={Position.Top} style={{ left: '50%' }} />
      <Handle id="ts" type="source" position={Position.Top} style={{ left: '75%' }} />
      <div className="room" style={{ color }}>{label}{!isOwner && <Help topic={HELP_TOPIC[id] || 'agent'} />}</div>
      <div className="sub">{sub}</div>
      <div className="state"><span className="dot" />{state === 'waiting' ? 'waiting for owner' : state}</div>
    </div>
  );
}

// A small labelled dot that travels along a line (used by Replay).
function Dot({ path, dot }) {
  if (!dot) return null;
  return (
    <g key={dot.key} className="replay-dot">
      <animateMotion dur="1.3s" path={path} fill="freeze" />
      <circle r="6" fill="#fff" />
      <text y="-12" textAnchor="middle">{dot.label}</text>
    </g>
  );
}

const labelProps = { labelStyle: { fill: GREY, fontSize: 11, fontFamily: 'monospace' }, labelBgStyle: { fill: '#0e0f12' }, labelBgPadding: [6, 3] };

function HandoffEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, markerEnd, style, label, data }) {
  const [path, lx, ly] = getBezierPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition });
  return (<><BaseEdge id={id} path={path} markerEnd={markerEnd} style={style} label={label} labelX={lx} labelY={ly} {...labelProps} /><Dot path={path} dot={data?.dot} /></>);
}

// A dashed loop that dips below the nodes and comes back up to the Design Studio.
// (React Flow's built-in curve goes flat when both ends face downwards.)
function RevisionEdge({ id, sourceX, sourceY, targetX, targetY, markerEnd, style, label, data }) {
  const dip = data?.dip ?? 70;
  const path = `M ${sourceX},${sourceY} C ${sourceX},${sourceY + dip} ${targetX},${targetY + dip} ${targetX},${targetY}`;
  return (<><BaseEdge id={id} path={path} markerEnd={markerEnd} style={style} label={label} labelX={(sourceX + targetX) / 2} labelY={(sourceY + targetY) / 2 + dip * 0.75} {...labelProps} /><Dot path={path} dot={data?.dot} /></>);
}

const nodeTypes = { agent: AgentNode };
const edgeTypes = { handoff: HandoffEdge, revision: RevisionEdge };

export function NetworkView({ state, selection, onSelect, compact, frame }) {
  const { nodes, edges } = useMemo(() => {
    const byId = Object.fromEntries(state.agents.map((a) => [a.id, a]));
    const ownerWaiting = state.waitingPitches.length > 0;
    const ideas = state.inbox?.length || 0;
    const inReplay = !!frame;

    const agentNodes = state.agents.map((a, i) => {
      const active = inReplay && frame.agent === a.id;
      let sub;
      if (inReplay) sub = active ? frame.event.message : '';
      else if (a.state === 'working') sub = state.games.find((g) => g.slug === a.currentGame)?.title || a.currentGame;
      else sub = a.lastEvent ? `last: ${ago(a.lastEvent.time)}` : 'no activity yet';
      const live = a.state === 'waiting' ? 'idle' : a.state; // the amber ring belongs to the owner node
      return {
        id: a.id, type: 'agent', position: { x: i * STEP, y: i % 2 ? 150 : 60 }, draggable: false,
        data: { id: a.id, label: a.room, sub, color: a.color, state: inReplay ? (active ? 'working' : 'idle') : live, selected: selection?.id === a.id, active },
      };
    });
    const ownerSub = [ownerWaiting && `${state.waitingPitches.length} pitch${state.waitingPitches.length > 1 ? 'es' : ''} to review`, ideas && `${ideas} idea${ideas > 1 ? 's' : ''} in inbox`].filter(Boolean).join(' · ') || 'decides what gets built';
    const ownerNode = {
      id: 'owner', type: 'agent', position: { x: (state.agents.length - 1) * STEP, y: -115 }, draggable: false,
      data: { id: 'owner', label: 'You', sub: ownerSub, color: '#d9d4c7', state: ownerWaiting ? 'waiting' : 'idle', selected: selection?.id === 'owner', isOwner: true },
    };

    const present = new Set([...state.agents.map((a) => a.id), 'owner']);
    const label = (id) => (id === 'owner' ? 'You' : byId[id]?.room);
    const dotFor = (edgeId) => (frame?.dot?.edgeId === edgeId ? frame.dot : null);
    const arrow = { type: MarkerType.ArrowClosed, color: GREY };

    const forward = FORWARD.filter(([s, t]) => present.has(s) && present.has(t)).map(([s, t, file]) => {
      const id = `${s}>${t}`;
      const toOwner = t === 'owner';
      return {
        id, source: s, target: t, label: file, type: 'handoff', markerEnd: arrow, style: { stroke: GREY },
        ...(toOwner ? { sourceHandle: 'ts', targetHandle: 'bt2' } : {}),
        data: { file, targetLabel: label(t), dot: dotFor(id) }, selected: selection?.id === id,
      };
    });
    const revisions = REVISIONS.filter(([s, t]) => present.has(s) && present.has(t)).map(([s, t, file, handle]) => {
      const id = `rev:${s}>${t}`;
      return {
        id, source: s, sourceHandle: 'bs', target: t, targetHandle: handle, label: 'revision', type: 'revision', markerEnd: arrow,
        style: { stroke: GREY, strokeDasharray: '6 5' },
        data: { file, targetLabel: label(t), revision: true, dip: handle === 'bt' ? 45 : 75, dot: dotFor(id) }, selected: selection?.id === id,
      };
    });
    return { nodes: [ownerNode, ...agentNodes], edges: [...forward, ...revisions] };
  }, [state, selection, frame]);

  return (
    <div className="net">
      <div className="hint">
        Click an agent to inspect it or leave it a note, or a line to see the file handed over.
        <span className="legend"><span>handoff file <Help topic="handoff" /></span><span>revision loop <Help topic="revision-loop" /></span></span>
      </div>
      <ReactFlow key={compact ? 'compact' : 'full'} nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes}
        fitView fitViewOptions={{ padding: 0.14 }} nodesDraggable={false} nodesConnectable={false} elementsSelectable
        panOnDrag zoomOnScroll={false} minZoom={0.4}
        onNodeClick={(_, n) => onSelect({ type: n.id === 'owner' ? 'owner' : 'agent', id: n.id })}
        onEdgeClick={(_, e) => onSelect({ type: 'edge', id: e.id, edge: e.data })}
        onPaneClick={() => onSelect(null)} proOptions={{ hideAttribution: true }} />
    </div>
  );
}
