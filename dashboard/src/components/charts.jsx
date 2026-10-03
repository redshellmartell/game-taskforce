// All charts (Recharts). One accent colour per department, used only for that department's charts:
// critic charts use the Review Board colour, balance charts the Playtest Lab colour,
// pipeline charts the Director's Office colour. Every chart shows "no data yet" instead of an empty box.
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell, ReferenceLine, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, LabelList } from 'recharts';

const AXIS = '#8a8f9b';
const GRID = '#272a32';
const BAD = '#e0574f';
const tip = { contentStyle: { background: '#1b1e25', border: '1px solid #272a32', borderRadius: 6, fontSize: 12 }, labelStyle: { color: '#d8dae0' }, itemStyle: { color: '#d8dae0' }, cursor: { fill: 'rgba(255,255,255,0.04)' } };
const axis = { stroke: AXIS, fontSize: 11, tickLine: false };

export const colorOf = (state, id, fallback = '#8a8f9b') => state.agents.find((a) => a.id === id)?.color || fallback;

function Frame({ height = 180, empty, children }) {
  if (empty) return <div className="nodata" style={{ height }}>no data yet</div>;
  return <div style={{ height }}><ResponsiveContainer width="100%" height="100%">{children}</ResponsiveContainer></div>;
}

// Critic's six scores (1-5).
export function CriticRadar({ scores, color }) {
  const data = Object.entries(scores || {}).map(([k, v]) => ({ k: k.replace('_', ' '), v }));
  return (
    <Frame height={230} empty={data.length === 0}>
      <RadarChart data={data} outerRadius="72%">
        <PolarGrid stroke={GRID} />
        <PolarAngleAxis dataKey="k" tick={{ fill: AXIS, fontSize: 11 }} />
        <PolarRadiusAxis domain={[0, 5]} tickCount={6} tick={false} axisLine={false} />
        <Radar dataKey="v" stroke={color} fill={color} fillOpacity={0.3} />
        <Tooltip {...tip} />
      </RadarChart>
    </Frame>
  );
}

// Win rates (0-1) as percent bars, with an optional "fair share" reference line.
export function RateBars({ rates, color, fair, height = 150, prefix = '' }) {
  const data = Object.entries(rates || {}).map(([k, v]) => ({ name: `${prefix}${k}`, pct: Math.round(v * 1000) / 10 }));
  return (
    <Frame height={height} empty={data.length === 0}>
      <BarChart data={data} margin={{ top: 14, right: 8, bottom: 0, left: -18 }}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey="name" {...axis} />
        <YAxis domain={[0, 100]} unit="%" {...axis} />
        <Tooltip {...tip} formatter={(v) => [`${v}%`, 'win rate']} />
        {fair != null && <ReferenceLine y={fair} stroke={AXIS} strokeDasharray="4 4" label={{ value: 'fair', fill: AXIS, fontSize: 10, position: 'insideTopRight' }} />}
        <Bar dataKey="pct" fill={color} radius={[3, 3, 0, 0]}><LabelList dataKey="pct" position="top" fill={AXIS} fontSize={11} formatter={(v) => `${v}%`} /></Bar>
      </BarChart>
    </Frame>
  );
}

// Card/action win correlation. Flagged cards are drawn in red.
export function CardCorrelation({ cards }) {
  const data = (cards || []).map((c) => ({ name: c.name, corr: c.win_correlation, flag: c.flag, played: c.played_rate }));
  return (
    <Frame height={Math.max(120, data.length * 34 + 30)} empty={data.length === 0}>
      <BarChart data={data} layout="vertical" margin={{ top: 4, right: 24, bottom: 0, left: 10 }}>
        <CartesianGrid stroke={GRID} horizontal={false} />
        <XAxis type="number" domain={[-0.3, 0.3]} {...axis} />
        <YAxis type="category" dataKey="name" width={90} {...axis} />
        <Tooltip {...tip} formatter={(v, n, p) => [v, p.payload.flag ? `win correlation (${p.payload.flag})` : 'win correlation']} />
        <ReferenceLine x={0} stroke={AXIS} />
        <Bar dataKey="corr" radius={3}>{data.map((d, i) => <Cell key={i} fill={d.flag ? BAD : '#d0603f'} />)}</Bar>
      </BarChart>
    </Frame>
  );
}

// Game length distribution (simulated games per number of turns), with the mean marked.
export function LengthHistogram({ length, histogram, color }) {
  const data = (histogram || []).map((h) => ({ turns: h.turns, games: h.games }));
  const mean = length?.mean_turns;
  const nearest = mean != null && data.length ? data.reduce((a, b) => (Math.abs(b.turns - mean) < Math.abs(a.turns - mean) ? b : a)).turns : null;
  return (
    <>
      <Frame height={150} empty={data.length === 0}>
        <BarChart data={data} margin={{ top: 14, right: 8, bottom: 0, left: -18 }}>
          <CartesianGrid stroke={GRID} vertical={false} />
          <XAxis dataKey="turns" {...axis} />
          <YAxis {...axis} />
          <Tooltip {...tip} formatter={(v) => [v, 'games']} labelFormatter={(t) => `${t} turns`} />
          {nearest != null && <ReferenceLine x={nearest} stroke="#fff" strokeDasharray="3 3" label={{ value: `mean ${mean}`, fill: '#d8dae0', fontSize: 10, position: 'top' }} />}
          <Bar dataKey="games" fill={color} radius={[3, 3, 0, 0]} />
        </BarChart>
      </Frame>
      {length && <div className="muted small">{mean != null && `Average ${mean} turns`}{length.stdev != null && ` (±${length.stdev})`}{length.estimated_minutes != null && `, about ${length.estimated_minutes} min`}{length.target_minutes != null && ` vs target ${length.target_minutes} min`}.{data.length === 0 && ' The full distribution was not recorded.'}</div>}
    </>
  );
}

// Stage funnel: games that reached each stage.
export function FunnelChart({ funnel, color }) {
  const data = funnel || [];
  return (
    <Frame height={230} empty={data.every((d) => d.count === 0)}>
      <BarChart data={data} layout="vertical" margin={{ top: 4, right: 30, bottom: 0, left: 20 }}>
        <XAxis type="number" hide allowDecimals={false} />
        <YAxis type="category" dataKey="label" width={100} {...axis} />
        <Tooltip {...tip} formatter={(v) => [v, 'games reached']} />
        <Bar dataKey="count" fill={color} radius={3}><LabelList dataKey="count" position="right" fill="#d8dae0" fontSize={12} /></Bar>
      </BarChart>
    </Frame>
  );
}

// Kill rate by stage (% of games entering the stage that were killed there).
export function KillRateChart({ killRate, color }) {
  const data = (killRate || []).map((k) => ({ ...k, pct: k.pct ?? 0 }));
  return (
    <Frame height={200} empty={data.every((d) => d.entered === 0)}>
      <BarChart data={data} margin={{ top: 14, right: 8, bottom: 0, left: -18 }}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey="label" {...axis} />
        <YAxis domain={[0, 100]} unit="%" {...axis} />
        <Tooltip {...tip} formatter={(v, n, p) => [`${v}% (${p.payload.killed} of ${p.payload.entered})`, 'killed here']} />
        <Bar dataKey="pct" fill={color} radius={[3, 3, 0, 0]}><LabelList dataKey="pct" position="top" fill={AXIS} fontSize={11} formatter={(v) => (v ? `${v}%` : '')} /></Bar>
      </BarChart>
    </Frame>
  );
}

// Cycle time: hours from brief to pitch, per game.
export function CycleChart({ times, color }) {
  const data = times || [];
  return (
    <Frame height={200} empty={data.length === 0}>
      <BarChart data={data} margin={{ top: 14, right: 8, bottom: 0, left: -18 }}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey="title" {...axis} />
        <YAxis unit="h" {...axis} />
        <Tooltip {...tip} formatter={(v) => [`${v} hours`, 'brief to pitch']} />
        <Bar dataKey="hours" fill={color} radius={[3, 3, 0, 0]}><LabelList dataKey="hours" position="top" fill={AXIS} fontSize={11} /></Bar>
      </BarChart>
    </Frame>
  );
}

// ---- Milestone 4 charts ----
import { LineChart, Line, Legend } from 'recharts';

// Generic bars: one value per category, optional reference line (e.g. a target).
export function ValueBars({ data, xKey, yKey, color, height = 180, domain, ticks, unit = '', refLine, refText, horizontal = false, label = '', labelWidth = 130 }) {
  const rows = data || [];
  const common = { stroke: AXIS, fontSize: 11, tickLine: false };
  return (
    <>
    <Frame height={horizontal ? Math.max(120, rows.length * 30 + 30) : height} empty={rows.length === 0}>
      <BarChart data={rows} layout={horizontal ? 'vertical' : 'horizontal'} margin={horizontal ? { top: 4, right: 30, bottom: 0, left: 10 } : { top: 16, right: 8, bottom: 0, left: -12 }}>
        <CartesianGrid stroke={GRID} vertical={horizontal} horizontal={!horizontal} />
        {horizontal
          ? <><XAxis type="number" allowDecimals={false} {...common} /><YAxis type="category" dataKey={xKey} width={labelWidth} {...common} /></>
          : <><XAxis dataKey={xKey} {...common} /><YAxis domain={domain} ticks={ticks} unit={unit} allowDecimals={false} {...common} /></>}
        <Tooltip {...tip} formatter={(v) => [`${v}${unit}`, label || yKey]} />
        {refLine != null && <ReferenceLine {...(horizontal ? { x: refLine } : { y: refLine })} stroke="#fff" strokeDasharray="4 4" />}
        <Bar dataKey={yKey} fill={color} radius={horizontal ? 3 : [3, 3, 0, 0]}><LabelList dataKey={yKey} position={horizontal ? 'right' : 'top'} fill={AXIS} fontSize={11} /></Bar>
      </BarChart>
    </Frame>
    {refLine != null && rows.length > 0 && <div className="muted small">Dashed line: {refText || 'target'}.</div>}
    </>
  );
}

// A line over time (for example the running first-pass playtest rate).
export function TrendLine({ data, xKey, yKey, color, domain, unit = '', height = 180 }) {
  return (
    <Frame height={height} empty={!data || data.length === 0}>
      <LineChart data={data} margin={{ top: 16, right: 12, bottom: 0, left: -12 }}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey={xKey} {...axis} />
        <YAxis domain={domain} unit={unit} {...axis} />
        <Tooltip {...tip} formatter={(v) => [`${v}${unit}`, 'rate so far']} />
        <Line type="monotone" dataKey={yKey} stroke={color} strokeWidth={2} dot={{ r: 4, fill: color }} />
      </LineChart>
    </Frame>
  );
}

// Agent activity per day, stacked by agent, in each agent's own colour.
export function DailyStack({ daily, agents }) {
  const empty = !daily || daily.every((d) => agents.every((a) => !d[a.id]));
  return (
    <Frame height={220} empty={empty}>
      <BarChart data={daily} margin={{ top: 8, right: 8, bottom: 0, left: -18 }}>
        <CartesianGrid stroke={GRID} vertical={false} />
        <XAxis dataKey="day" {...axis} />
        <YAxis allowDecimals={false} {...axis} />
        <Tooltip {...tip} />
        <Legend wrapperStyle={{ fontSize: 11 }} />
        {agents.map((a) => <Bar key={a.id} dataKey={a.id} name={a.room} stackId="d" fill={a.color} />)}
      </BarChart>
    </Frame>
  );
}
