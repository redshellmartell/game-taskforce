import { useMemo } from 'react';
import { ReactFlow, Handle, Position, MarkerType, BaseEdge, getBezierPath, getSmoothStepPath } from '@xyflow/react';
import { ago } from '../util.js';
import { FORWARD, REVISIONS, PITCH } from '../replay.js';
import { Help } from './Help.jsx';
import { GATE_LABEL } from './ApprovalsView.jsx';

const STEP = 320; // distance between the four specialists
const GREY = '#8a8f9b';
const ORG = '#4a4f5c';
const HELP_TOPIC = { playtester: 'simulation', critic: 'verdict' }; // every other node explains "agent"

// Org-chart layout: You at the top, the Director's Office below, the specialists in a row under it.
const Y = { owner: 0, manager: 150, row: 320 };

function AgentNode({ data }) {
  const { id, label, sub, color, state, selected, active, isOwner } = data;
  const mid = { left: '50%' };
  return (
    <div className={`node ${state} ${selected ? 'selected' : ''} ${active ? 'active' : ''} ${isOwner ? 'owner' : ''}`} style={{ '--accent': color }}>
      <Handle type="target" position={Position.Left} />
      <Handle type="source" position={Position.Right} />
      <Handle id="tt" type="target" position={Position.Top} style={mid} />
      <Handle id="tc" type="source" position={Position.Top} style={mid} />
      <Handle id="bs" type="source" position={Position.Bottom} style={mid} />
      <Handle id="bc" type="target" position={Position.Bottom} style={mid} />
      <Handle id="bt" type="target" position={Position.Bottom} style={{ left: '30%' }} />
      <Handle id="bt2" type="target" position={Position.Bottom} style={{ left: '70%' }} />
      <div className="room" style={{ color }}>{label}{!isOwner && <Help topic={HELP_TOPIC[id] || 'agent'} />}</div>
      <div className="sub">{sub}</div>
      <div className="state"><span className="dot" />{state === 'waiting' ? 'waiting for owner' : state}</div>
    </div>
  );
}

// A small labelled dot that travels along a line (used by Replay). `reverse` runs it backwards.
function Dot({ path, dot }) {
  if (!dot) return null;
  return (
    <g key={dot.key} className="replay-dot">
      {dot.reverse ? <animateMotion dur="1.3s" path={path} keyPoints="1;0" keyTimes="0;1" calcMode="linear" fill="freeze" /> : <animateMotion dur="1.3s" path={path} fill="freeze" />}
      <circle r="6" fill="#fff" />
      <text y="-12" textAnchor="middle">{dot.label}</text>
    </g>
  );
}

const labelProps = { labelStyle: { fill: GREY, fontSize: 11, fontFamily: 'monospace' }, labelBgStyle: { fill: '#0e0f12' }, labelBgPadding: [6, 3] };

function HandoffEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, markerEnd, style, label, data }) {
  const [path, lx, ly] = getBezierPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition });
  const flat = Math.abs(targetY - sourceY) < 6 && Math.abs(targetX - sourceX) > Math.abs(targetY - sourceY);
  return (<><BaseEdge id={id} path={path} markerEnd={markerEnd} style={style} label={label} labelX={lx} labelY={flat ? ly - 13 : ly} {...labelProps} /><Dot path={path} dot={data?.dot} /></>);
}

// Reporting line: an elbow connector from the Director down to a specialist, like an org chart.
function OrgEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, style, data }) {
  const [path] = getSmoothStepPath({ sourceX, sourceY, sourcePosition, targetX, targetY, targetPosition, borderRadius: 10 });
  return (<><BaseEdge id={id} path={path} style={style} /><Dot path={path} dot={data?.dot} /></>);
}

// A dashed loop that dips below the nodes and comes back up to the Design Studio.
// (React Flow's built-in curve goes flat when both ends face downwards.)
function RevisionEdge({ id, sourceX, sourceY, targetX, targetY, markerEnd, style, label, data }) {
  const dip = data?.dip ?? 70;
  const path = `M ${sourceX},${sourceY} C ${sourceX},${sourceY + dip} ${targetX},${targetY + dip} ${targetX},${targetY}`;
  return (<><BaseEdge id={id} path={path} markerEnd={markerEnd} style={style} label={label} labelX={(sourceX + targetX) / 2} labelY={(sourceY + targetY) / 2 + dip * 0.75} {...labelProps} /><Dot path={path} dot={data?.dot} /></>);
}

// An invisible node under the chart so "fit to screen" leaves room for the revision loops.
function GhostNode() { return <div style={{ width: 1, height: 1 }} />; }
const nodeTypes = { agent: AgentNode, ghost: GhostNode };
const edgeTypes = { handoff: HandoffEdge, revision: RevisionEdge, org: OrgEdge };

export function NetworkView({ state, selection, onSelect, compact, frame }) {
  const { nodes, edges } = useMemo(() => {
    const byId = Object.fromEntries(state.agents.map((a) => [a.id, a]));
    const ownerWaiting = state.waitingPitches.length > 0;
    const ideas = state.inbox?.length || 0;
    const inReplay = !!frame;

    const specialists = state.agents.filter((a) => a.id !== 'manager');
    const centre = ((specialists.length - 1) * STEP) / 2;
    const place = (a) => (a.id === 'manager' ? { x: centre, y: Y.manager } : { x: specialists.indexOf(a) * STEP, y: Y.row });

    const agentNodes = state.agents.map((a) => {
      const active = inReplay && frame.agent === a.id;
      let sub;
      if (inReplay) sub = active ? frame.event.message : '';
      else if (a.state === 'waiting' && a.waitingGate) sub = `waiting: ${GATE_LABEL[a.waitingGate.gate] || a.waitingGate.gate}`;
      else if (a.state === 'working') sub = state.games.find((g) => g.slug === a.currentGame)?.title || a.currentGame;
      else sub = a.lastEvent ? `last: ${ago(a.lastEvent.time)}` : 'no activity yet';
      const live = a.state === 'waiting' && !a.waitingGate ? 'idle' : a.state;   // the Director's "waiting" for pitches is shown on the owner node; a waiting gate gets the amber ring here
      return {
        id: a.id, type: 'agent', position: place(a), draggable: false,
        data: { id: a.id, label: a.room, sub, color: a.color, state: inReplay ? (active ? 'working' : 'idle') : live, selected: selection?.id === a.id, active },
      };
    });
    const ownerSub = [ownerWaiting && `${state.waitingPitches.length} pitch${state.waitingPitches.length > 1 ? 'es' : ''} to review`, ideas && `${ideas} idea${ideas > 1 ? 's' : ''} in inbox`].filter(Boolean).join(' · ') || 'decides what gets built';
    const ownerNode = {
      id: 'owner', type: 'agent', position: { x: centre, y: Y.owner }, draggable: false,
      data: { id: 'owner', label: 'You', sub: ownerSub, color: '#d9d4c7', state: ownerWaiting ? 'waiting' : 'idle', selected: selection?.id === 'owner', isOwner: true },
    };

    const present = new Set([...state.agents.map((a) => a.id), 'owner']);
    const label = (id) => (id === 'owner' ? 'You' : byId[id]?.room);
    const dotFor = (edgeId) => (frame?.dot?.edgeId === edgeId ? frame.dot : null);
    const arrow = { type: MarkerType.ArrowClosed, color: GREY };

    // Director -> You: the pitch goes up to the owner.
    const [ps, pt, pfile] = PITCH;
    const pitch = present.has(ps) ? [{
      id: `${ps}>${pt}`, source: ps, sourceHandle: 'tc', target: pt, targetHandle: 'bc', label: pfile, type: 'handoff', markerEnd: arrow, style: { stroke: GREY },
      data: { file: pfile, targetLabel: 'You', dot: dotFor(`${ps}>${pt}`) }, selected: selection?.id === `${ps}>${pt}`,
    }] : [];
    // Reporting lines: every specialist reports to the Director's Office.
    const reporting = specialists.filter((a) => (a.reportsTo || 'manager') === 'manager' && present.has('manager')).map((a) => ({
      id: `org:${a.id}`, source: 'manager', sourceHandle: 'bs', target: a.id, targetHandle: 'tt', type: 'org',
      style: { stroke: ORG, strokeWidth: 1.5 }, data: { org: true, agent: a.id, dot: dotFor(`org:${a.id}`) }, selected: false,
    }));
    // Handoff arrows between the specialists.
    const forward = FORWARD.filter(([s, t]) => present.has(s) && present.has(t)).map(([s, t, file]) => ({
      id: `${s}>${t}`, source: s, target: t, label: file, type: 'handoff', markerEnd: arrow, style: { stroke: GREY },
      data: { file, targetLabel: label(t), dot: dotFor(`${s}>${t}`) }, selected: selection?.id === `${s}>${t}`,
    }));
    const revisions = REVISIONS.filter(([s, t]) => present.has(s) && present.has(t)).map(([s, t, file, handle]) => ({
      id: `rev:${s}>${t}`, source: s, sourceHandle: 'bs', target: t, targetHandle: handle, label: 'revision', type: 'revision', markerEnd: arrow,
      style: { stroke: GREY, strokeDasharray: '6 5' },
      data: { file, targetLabel: label(t), revision: true, dip: handle === 'bt' ? 45 : 75, dot: dotFor(`rev:${s}>${t}`) }, selected: selection?.id === `rev:${s}>${t}`,
    }));

    const pad = { id: '__pad', type: 'ghost', position: { x: centre, y: Y.row + 190 }, draggable: false, selectable: false, focusable: false, data: {} };
    return { nodes: [ownerNode, ...agentNodes, pad], edges: [...reporting, ...forward, ...revisions, ...pitch] };
  }, [state, selection, frame]);

  return (
    <div className="net">
      <div className="hint">
        Click an agent to inspect it or leave it a note. Grey org lines show who reports to whom; arrows show the files handed over.
        <span className="legend"><span>handoff file <Help topic="handoff" /></span><span>revision loop <Help topic="revision-loop" /></span></span>
      </div>
      <ReactFlow key={compact ? 'compact' : 'full'} nodes={nodes} edges={edges} nodeTypes={nodeTypes} edgeTypes={edgeTypes}
        fitView fitViewOptions={{ padding: 0.12 }} nodesDraggable={false} nodesConnectable={false} elementsSelectable
        panOnDrag zoomOnScroll={false} minZoom={0.4}
        onNodeClick={(_, n) => onSelect({ type: n.id === 'owner' ? 'owner' : 'agent', id: n.id })}
        onEdgeClick={(_, e) => onSelect(e.data?.org ? { type: 'agent', id: e.data.agent } : { type: 'edge', id: e.id, edge: e.data })}
        onPaneClick={() => onSelect(null)} proOptions={{ hideAttribution: true }} />
    </div>
  );
}
