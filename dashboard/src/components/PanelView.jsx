import { useEffect, useState } from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, LabelList } from 'recharts';
import { Markdown, FileView } from './Markdown.jsx';
import { Help } from './Help.jsx';
import { CopyBox } from './IdeaForm.jsx';
import { Avatar, TrustChip } from './PanelTab.jsx';
import { fetchFile } from '../useStudioState.js';
import { ago } from '../util.js';

const WOULD = { yes: 'would buy', maybe: 'might buy', no: 'would not buy' };
const num = (x, unit = '') => (x === null || x === undefined ? '—' : `${x}${unit}`);

// Heatmap cell colour: low fun is warm, high fun is green-teal (single hue scale per theme would hide low scores).
function heat(v) {
  if (typeof v !== 'number') return { background: 'transparent', color: 'var(--muted)' };
  const t = Math.max(0, Math.min(1, (v - 1) / 4));
  return { background: `hsl(${Math.round(8 + t * 150)} ${40 + t * 10}% ${22 + t * 8}%)`, color: '#f2f3f5' };
}

export function HarshLabel({ h }) {
  if (h === null || h === undefined) return <span className="muted">not enough games yet</span>;
  if (Math.abs(h) < 0.15) return <span>as the panel average</span>;
  return <span>{h < 0 ? 'harsher' : 'more generous'} than the panel ({h > 0 ? '+' : ''}{h})</span>;
}

// Persona × game fun scores, plus who each game is for.
function Heatmap({ panel, onPersona, onGame }) {
  const stats = panel.stats, ps = panel.personas;
  if (!stats || stats.grid.length === 0) return <p className="empty">No game has panel scores yet. After a playtest the persona bots and scoring run and fill this in.</p>;
  return (
    <div className="heatwrap">
      <table className="heat">
        <thead><tr><td />{ps.map((p) => <th key={p.id}><button className="link" onClick={() => onPersona(p.id)}><Avatar p={p} size={22} /> {p.name.replace('The ', '')}</button></th>)}<th>Panel</th></tr></thead>
        <tbody>
          {stats.grid.map((g) => (
            <tr key={g.slug}>
              <th className="rowh"><button className="link" onClick={() => onGame(g.slug)}>{g.title}</button></th>
              {ps.map((p) => <td key={p.id} className="cell mono" style={heat(g.cells[p.id])} title={`${p.name}: ${g.cells[p.id] ?? 'no score'}`}>{g.cells[p.id] ?? '—'}</td>)}
              <td className="mono"><b>{num(g.summary?.averageFun)}</b> <span className="muted small">{g.summary?.agreement === 'split' ? 'split' : 'agrees'}</span></td>
            </tr>))}
        </tbody>
      </table>
      <h4>Who is each game for?</h4>
      {stats.grid.map((g) => {
        const s = g.summary; if (!s) return null;
        const best = ps.find((p) => p.id === s.bestFit), worst = ps.find((p) => p.id === s.worstFit);
        return <p key={g.slug} className="small" style={{ margin: '4px 0' }}><button className="link" onClick={() => onGame(g.slug)}>{g.title}</button>: best fit <b style={{ color: best?.color }}>{best?.name}</b>, worst fit <b style={{ color: worst?.color }}>{worst?.name}</b>. The panel {s.agreement === 'agrees' ? 'agrees' : 'is split'} (spread {s.spread}).</p>;
      })}
    </div>
  );
}

// The lounge: one card per persona and the panel-wide comparison.
function Lounge({ state, onPersona, onGame }) {
  const panel = state.panel, stats = panel.stats;
  return (
    <>
      <h2 style={{ marginTop: 0 }}>Test Panel <Help topic="test-panel" /></h2>
      <p className="muted" style={{ marginTop: 0 }}>Five types of player give every game a public test on top of the bot playtest. Their opinions are advisory; your own playtests are the final check.</p>
      <div className="tiles">
        <div className="tile"><span className="mono big">{num(stats?.averageFun)}</span><span className="lbl">Average fun given</span></div>
        <div className="tile"><span className="mono big">{stats?.gamesWithPanel ?? 0}</span><span className="lbl">Games with panel scores</span></div>
        <div className="tile"><span className="mono big">{num(stats?.kpis.calibrationError)}</span><span className="lbl">Mean calibration error <Help topic="calibration" /></span></div>
      </div>
      {panel.baselineQuality === 'low' && <p className="notice">Trust flags are provisional: the research behind the calibration is thin. Treat the personas as advisory.</p>}
      <div className="lounge">
        {panel.personas.map((p) => {
          const s = stats?.personas[p.id];
          return (
            <button key={p.id} className="lcard" style={{ '--accent': p.color }} onClick={() => onPersona(p.id)}>
              <div className="lhead"><Avatar p={p} size={44} /><div><b style={{ color: p.color }}>{p.name} <Help topic="persona" /></b><div className="muted small">{p.archetype}</div></div></div>
              <div className="small">“{p.tagline}”</div>
              <div className={`lstatus ${s?.state || 'idle'}`}><i className="dot" /> {s?.state === 'playing' ? `reviewing ${state.games.find((g) => g.slug === s.currentGame)?.title || s.currentGame}` : 'idle'}</div>
              <div className="lstats">
                <span><b className="mono">{s?.games ?? 0}</b> games</span>
                <span><b className="mono">{num(s?.averageFun)}</b> avg fun</span>
              </div>
              <div className="small muted"><HarshLabel h={s?.harshness} /></div>
              <TrustChip cal={p.calibration} limit={panel.trustLimit} />
              <div className="small verdict">{s?.verdict ? <>“{s.verdict}”</> : <span className="muted">No written verdict yet.</span>}</div>
            </button>);
        })}
      </div>
      <h3>Fun by game and persona</h3>
      <Heatmap panel={panel} onPersona={onPersona} onGame={onGame} />
    </>
  );
}

function ProfileText({ path, version }) {
  const [text, setText] = useState(null);
  useEffect(() => { let alive = true; fetchFile(path).then((t) => alive && setText(t.replace(/^---[\s\S]*?\n---\s*/, ''))).catch(() => alive && setText('')); return () => { alive = false; }; }, [path, version]);
  if (text === null) return <p className="muted">Loading…</p>;
  return text ? <Markdown text={text} /> : <p className="empty">No data yet for {path}</p>;
}

function Distribution({ rows, color }) {
  const data = rows.map((d) => ({ rating: String(d.rating), count: d.count }));
  if (data.every((d) => d.count === 0)) return <p className="empty">No ratings yet.</p>;
  return (
    <ResponsiveContainer width="100%" height={130}>
      <BarChart data={data} margin={{ top: 14, right: 8, left: -20, bottom: 0 }}><CartesianGrid vertical={false} stroke="#2a2d36" /><XAxis dataKey="rating" stroke="#8a8f9b" fontSize={11} /><YAxis allowDecimals={false} stroke="#8a8f9b" fontSize={11} />
        <Tooltip contentStyle={{ background: '#16181d', border: '1px solid #2a2d36' }} /><Bar dataKey="count" fill={color} radius={[3, 3, 0, 0]}><LabelList dataKey="count" position="top" fill="#8a8f9b" fontSize={11} /></Bar></BarChart>
    </ResponsiveContainer>);
}

function PlayedTab({ p, s, state, onGame, onOpenFile }) {
  if (!s || s.rows.length === 0) return <p className="empty">No data yet: {p.name} has not scored any game. After a playtest the panel scores appear here.</p>;
  return s.rows.map((r) => (
    <div className="item played" key={r.slug}>
      <div><button className="link" onClick={() => onGame(r.slug)}><b>{r.title}</b></button> <span className="mono">fun {num(r.fun)}</span> · <span className="mono">replay {num(r.replay)}</span> · {WOULD[r.wouldBuy] || '—'}{r.price ? ` at $${r.price}` : ''}</div>
      {r.review ? (
        <>
          <div className="small"><b>Best moment:</b> {r.review.best_moment}</div>
          <div className="small"><b>Worst moment:</b> {r.review.worst_moment}</div>
          <div className="small"><b>One change:</b> {r.review.one_change}</div>
          {state.games.find((g) => g.slug === r.slug)?.files.some((f) => f.name === `panel/${p.id}.md`) && <button className="link small" onClick={() => onOpenFile(`games/${r.slug}/panel/${p.id}.md`)}>Read the full review</button>}
        </>
      ) : <div className="small muted">Scored by code only so far ({num(r.predicted)} predicted); no written review yet.</div>}
    </div>));
}

function StatsTab({ p, s, color }) {
  if (!s || s.games === 0) return <p className="empty">No data yet. Statistics appear once this persona has scored a game.</p>;
  return (
    <>
      <h4 style={{ marginTop: 0 }}>Rating distribution</h4>
      <Distribution rows={s.distribution} color={color} />
      <p className="small">Average fun <b className="mono">{num(s.averageFun)}</b>, <HarshLabel h={s.harshness} />.</p>
      <h4>Against the critic</h4>
      {s.vsCritic.length ? <table className="score"><thead><tr className="muted"><td>Game</td><td>{p.name.replace('The ', '')}</td><td>Critic</td></tr></thead><tbody>{s.vsCritic.map((r) => <tr key={r.title}><td>{r.title}</td><td className="mono">{r.persona}</td><td className="mono">{r.critic}</td></tr>)}</tbody></table> : <p className="empty">No game has both a critique and a score from this persona yet.</p>}
      <h4>Predicted (code) versus written (AI) <Help topic="predicted-vs-written" /></h4>
      {s.predictedVsWritten.length ? <table className="score"><thead><tr className="muted"><td>Game</td><td>Predicted</td><td>Written</td></tr></thead><tbody>{s.predictedVsWritten.map((r) => <tr key={r.title}><td>{r.title}</td><td className="mono">{r.predicted}</td><td className="mono">{r.written}</td></tr>)}</tbody></table> : <p className="empty">No written reviews yet, so there is nothing to compare.</p>}
      <h4>How their bot performed</h4>
      {s.bot ? <p className="small" style={{ marginTop: 0 }}>Win rate <b className="mono">{Math.round(s.bot.winRate * 100)}%</b> over {s.bot.games.toLocaleString('en-US')} games · fell behind and lost <b className="mono">{Math.round(s.bot.fellBehind * 100)}%</b> · by seat: {Object.entries(s.bot.seatWinRates).map(([k, v]) => `seat ${k} ${Math.round(v * 100)}%`).join(', ')}</p> : <p className="empty">No bot results yet.</p>}
      <h4>Against the other personas</h4>
      {s.matchups.length ? (
        <table className="score"><thead><tr className="muted"><td>Opponent</td><td>Win rate</td><td>Fun at that table</td></tr></thead>
          <tbody>{s.matchups.map((m) => <tr key={m.other}><td>{m.other}{m.other === s.mostEnjoys ? ' ▲' : m.other === s.leastEnjoys ? ' ▼' : ''}</td><td className="mono">{Math.round(m.winRate * 100)}%</td><td className="mono">{num(m.fun)}</td></tr>)}</tbody></table>
      ) : <p className="empty">No rotation results yet.</p>}
      {s.mostEnjoys && <p className="small muted">▲ most fun with {s.mostEnjoys} · ▼ least fun with {s.leastEnjoys}</p>}
    </>
  );
}

function TrackTab({ p, s }) {
  const c = p.calibration;
  return (
    <>
      <h4 style={{ marginTop: 0 }}>Calibration games <Help topic="calibration" /></h4>
      {c ? (<>
        <p className="small"><TrustChip cal={c} limit={null} /> {c.confidence && <span className="chip">confidence: {c.confidence}</span>}</p>
        <table className="score"><thead><tr className="muted"><td>Game</td><td>Predicted</td><td>Real</td></tr></thead><tbody>{c.games.map((g) => <tr key={g.game}><td>{g.game}</td><td className="mono">{g.predicted ?? '—'}</td><td className="mono">{g.actual ?? '—'}</td></tr>)}</tbody></table>
        <p className="muted small">{c.notes}</p></>) : <p className="empty">Not calibrated yet.</p>}
      <h4>Versus real players of this type</h4>
      {s?.human.sessions.length ? (<>
        <table className="score"><thead><tr className="muted"><td>Game</td><td>Persona</td><td>Real players</td></tr></thead><tbody>{s.human.sessions.map((h, i) => <tr key={i}><td>{h.game}</td><td className="mono">{h.persona ?? '—'}</td><td className="mono">{h.fun}</td></tr>)}</tbody></table>
        {s.human.gap !== null && <p className="small">On average the persona rated {s.human.gap > 0 ? 'higher' : 'lower'} than real players by {Math.abs(s.human.gap)}.</p>}</>)
        : <p className="empty">No data yet. When you record a playtest, tell the Director which type of player you were (<code>player_type</code>) and it shows up here.</p>}
    </>
  );
}

function TalkTab({ p, state, s }) {
  const withPanel = state.games.filter((g) => g.panel?.personas?.[p.id]);
  const [game, setGame] = useState('');
  const [q, setQ] = useState('');
  const slug = game || withPanel[0]?.slug || state.games[0]?.slug || '<game>';
  const prompt = `Ask ${p.id} about ${slug}: ${q.trim() || '(write your question above)'}`;
  const past = state.games.flatMap((g) => (g.conversations || []).filter((c) => c.persona === p.id).map((c) => ({ ...c, title: g.title }))).sort((a, b) => Date.parse(b.time) - Date.parse(a.time));
  return (
    <>
      <p className="muted small" style={{ marginTop: 0 }}>The dashboard cannot run agents. Pick a game, write your question, copy the prompt and paste it into Claude Code.</p>
      <div className="ideaform">
        <label>About which game?<select value={game} onChange={(e) => setGame(e.target.value)}>{(withPanel.length ? withPanel : state.games).map((g) => <option key={g.slug} value={g.slug}>{g.title}</option>)}</select></label>
        <label>Your question<textarea rows={3} value={q} onChange={(e) => setQ(e.target.value)} placeholder="e.g. Would you buy this for your game group?" /></label>
        <CopyBox text={prompt} />
      </div>
      <h4>Past conversations</h4>
      {past.length === 0 && <p className="empty">No conversations yet.</p>}
      {past.map((c, i) => <div className="item" key={i}><div className="small muted">{c.title} · {ago(c.time)}</div><div className="small"><b>You:</b> {c.question}</div><div className="small" style={{ color: p.color }}><b>{p.name.replace('The ', '')}:</b> {c.answer}</div></div>)}
    </>
  );
}

const TABS = [['who', 'Who they are'], ['played', "What they've played"], ['stats', 'Stats'], ['track', 'Track record'], ['evidence', 'Evidence'], ['talk', 'Talk to them']];

function PersonaPage({ p, state, tab, setTab, onBack, onGame, onOpenFile }) {
  const s = state.panel.stats?.personas[p.id];
  const version = state.generatedAt;
  return (
    <div className="personapage" style={{ '--accent': p.color }}>
      <button className="link back" onClick={onBack}>← The panel</button>
      <header className="persona-head" style={{ marginBottom: 6 }}>
        <Avatar p={p} size={56} />
        <div>
          <h2 style={{ margin: 0, color: p.color }}>{p.name}</h2>
          <div className="muted">{p.archetype} · “{p.tagline}”</div>
          <div className="small" style={{ marginTop: 4 }}><TrustChip cal={p.calibration} limit={state.panel.trustLimit} /> <span className="muted">{s?.state === 'playing' ? `reviewing ${s.currentGame}` : 'idle'}</span></div>
        </div>
      </header>
      <div className="tabs" style={{ padding: '8px 0 0' }}>{TABS.map(([id, label]) => <button key={id} className={`tab ${tab === id ? 'on' : ''}`} onClick={() => setTab(id)}>{label}</button>)}</div>
      <div className="ptab">
        {tab === 'who' && <ProfileText path={p.profile} version={version} />}
        {tab === 'played' && <PlayedTab p={p} s={s} state={state} onGame={onGame} onOpenFile={onOpenFile} />}
        {tab === 'stats' && <StatsTab p={p} s={s} color={p.color} />}
        {tab === 'track' && <TrackTab p={p} s={s} />}
        {tab === 'evidence' && <><p className="muted small" style={{ marginTop: 0 }}>The research this persona is built on{state.panel.calibrated ? `, calibration last run ${state.panel.calibrated}` : ''}. Sources are listed in the file.</p><ProfileText path={p.evidence} version={version} /></>}
        {tab === 'talk' && <TalkTab p={p} state={state} s={s} />}
      </div>
    </div>
  );
}

// The Panel page: the lounge, or one persona's profile.
export function PanelView({ state, personaId, setPersonaId, tab, setTab, onGame }) {
  const panel = state.panel;
  const [file, setFile] = useState(null);
  if (file) return <><button className="link back" onClick={() => setFile(null)}>← Back</button><FileView path={file} version={state.generatedAt} /></>;
  if (!panel || panel.personas.length === 0) return <p className="empty">No personas yet. They live in panel/personas/ (see panel/README.md).</p>;
  const p = panel.personas.find((x) => x.id === personaId);
  if (p) return <PersonaPage p={p} state={state} tab={tab} setTab={setTab} onBack={() => setPersonaId(null)} onGame={onGame} onOpenFile={setFile} />;
  return <Lounge state={state} onPersona={(id) => { setTab('who'); setPersonaId(id); }} onGame={onGame} />;
}

// Game page section: how the panel rated this game.
export function GamePanel({ game: g, state, onPersona }) {
  const sum = g.panel?.personas ? (state.panel?.stats?.grid.find((x) => x.slug === g.slug)?.summary) : null;
  if (!sum || !state.panel) return <section className="card"><h3>Test panel <Help topic="test-panel" /></h3><p className="empty">No data yet: the panel scores appear after this game's playtest.</p></section>;
  const ps = state.panel.personas, rot = sum.rotation;
  const by = {}; for (const m of sum.matchups) { by[`${m.a}|${m.b}`] = { win: m.a_win_rate, fun: m.a_fun, games: m.games }; by[`${m.b}|${m.a}`] = { win: 1 - m.a_win_rate, fun: m.b_fun, games: m.games }; }
  return (
    <section className="card wide">
      <h3>Test panel <Help topic="test-panel" /></h3>
      <p className="small" style={{ marginTop: 0 }}>Average fun <b className="mono">{sum.averageFun}</b> · spread {sum.spread} · <b>{sum.agreement === 'agrees' ? 'the panel agrees' : 'the panel is split'}</b> · best fit <b style={{ color: ps.find((p) => p.id === sum.bestFit)?.color }}>{ps.find((p) => p.id === sum.bestFit)?.name}</b>, worst fit <b style={{ color: ps.find((p) => p.id === sum.worstFit)?.color }}>{ps.find((p) => p.id === sum.worstFit)?.name}</b>.{' '}
        {sum.hasReport && <>The full panel report is under Documents below.</>}</p>
      <table className="score">
        <thead><tr className="muted"><td>Persona</td><td>Fun</td><td>Replay</td><td>Would buy</td><td>In one line</td></tr></thead>
        <tbody>{sum.rows.map((r) => { const p = ps.find((x) => x.id === r.id); return (
          <tr key={r.id}><td><button className="link" onClick={() => onPersona(r.id)}><Avatar p={p} size={20} /> {p.name.replace('The ', '')}</button></td><td className="mono">{num(r.fun)}{r.written === null ? '*' : ''}</td><td className="mono">{num(r.replay)}</td><td>{WOULD[r.wouldBuy] || '—'}{r.price ? ` $${r.price}` : ''}</td><td className="small">{r.verdict || <span className="muted">no written review</span>}</td></tr>); })}</tbody>
      </table>
      {sum.rows.some((r) => r.written === null) && <p className="muted small">* predicted by code from the simulation; no written review yet.</p>}
      {rot && <p className="muted small">Rotation: {rot.player_counts?.join(' and ')} players, {rot.tables} tables, {rot.seatings_per_table} seatings each, {rot.games_per_seating} games per seating{rot.filler_bots?.length ? `, filler bots: ${rot.filler_bots.join(', ')}` : ', no filler bots'}.</p>}
      <h4>Who beats whom <span className="muted small">(row's win rate against column; hover for fun)</span></h4>
      <table className="heat grid">
        <thead><tr><td />{ps.map((p) => <th key={p.id} title={p.name}><Avatar p={p} size={22} /></th>)}</tr></thead>
        <tbody>{ps.map((a) => <tr key={a.id}><th className="rowh"><Avatar p={a} size={22} /></th>{ps.map((b) => {
          if (a.id === b.id) return <td key={b.id} className="cell self" />;
          const m = by[`${a.id}|${b.id}`]; if (!m) return <td key={b.id} className="cell">—</td>;
          const w = Math.round(m.win * 100);
          return <td key={b.id} className="cell mono" style={{ background: `hsl(${w >= 50 ? 160 : 8} 40% ${20 + Math.abs(w - 50) * 0.5}%)`, color: '#f2f3f5' }} title={`${a.name} vs ${b.name}: wins ${w}%, fun ${m.fun ?? '—'} (${m.games} games)`}>{w}%</td>;
        })}</tr>)}</tbody>
      </table>
    </section>
  );
}
