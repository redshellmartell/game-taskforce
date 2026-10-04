import { useState } from 'react';
import { CopyBox } from './IdeaForm.jsx';
import { ago } from '../util.js';

const usageFor = (n) => (n <= 2 ? 'M' : n <= 5 ? 'L' : 'XL');
const USAGE_TEXT = { M: 'one agent pass', L: 'a full stage with research', XL: 'the heaviest kind: a long research run' };

const BUTTONS = [
  { kind: 'game-research', title: 'Game research', blurb: 'Fill the idea bank: a market scan for new scored ideas, tuned to your focus (card games, card-heavy games, tabletop RPGs).', usage: 'XL', gate: 'Market scan' },
  { kind: 'persona-research', title: 'Persona research', blurb: 'Build stronger playtesting profiles: refresh the evidence behind the six test-panel personas and re-run their calibration.', usage: 'XL', gate: 'Panel research' },
  { kind: 'reanalyze', title: 'Reanalyze pipeline', blurb: 'Deeper research on the games you pick: nearest comparables, originality, market fit, and any new insight.', usage: null, gate: 'Deep research' },
];

function hintFor(kind, h) {
  if (!h) return null;
  if (kind === 'game-research') {
    if (!h.scan) return 'No idea bank yet.';
    return h.scan.due ? { due: true, text: `Due: ${h.scan.reasons.join('; ')}` } : { text: `Last scan ${h.scan.days} day${h.scan.days === 1 ? '' : 's'} ago; ${h.scan.strongBanked} strong ideas banked.` };
  }
  if (kind === 'persona-research') return h.personas.updated ? { due: h.personas.due, text: `Calibration last run ${h.personas.updated} (${h.personas.days} day${h.personas.days === 1 ? '' : 's'} ago); evidence is thin until BoardGameGeek and Reddit are reachable.` } : { due: true, text: 'Never calibrated.' };
  const n = h.games.length, stale = h.games.filter((g) => g.days === null).length;
  return { text: `${n} game${n === 1 ? '' : 's'} in the pipeline; ${stale} never researched in depth.` };
}

function Modal({ children, onClose, title }) {
  return (
    <div className="modal-bg" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <div className="modal" role="dialog" aria-label={title}>
        <header><h2>{title}</h2><button className="close" onClick={onClose} aria-label="Close">×</button></header>
        {children}
      </div>
    </div>
  );
}

// Market Intel's "Research" tab: three buttons that each record an already-approved request for the Director to carry out.
export function ResearchTab({ state }) {
  const hints = state.research;
  const [open, setOpen] = useState(null);          // which button's popup is open
  const [picked, setPicked] = useState({});
  const [note, setNote] = useState('');
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState(null);
  const b = BUTTONS.find((x) => x.kind === open);
  const games = hints?.games || [];
  const chosen = games.filter((g) => picked[g.slug]).map((g) => g.slug);
  const usage = open === 'reanalyze' ? usageFor(chosen.length || 1) : b?.usage;
  const close = () => { setOpen(null); setNote(''); setBusy(false); };
  const send = async () => {
    setBusy(true); setMsg(null);
    try {
      const r = await fetch('/api/research', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ kind: open, games: open === 'reanalyze' ? chosen : undefined, note }) });
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || 'Could not save the request');
      setMsg({ ok: true, text: `Recorded (${body.id}). Nothing has run yet.` }); setPicked({}); close();
    } catch (e) { setMsg({ ok: false, text: e.message }); setBusy(false); }
  };
  const done = (id) => state.decisions.some((d) => String(d.notes || '').includes(id));
  const mine = state.approvals.requests.filter((r) => r.research_kind).slice(0, 6);
  return (
    <>
      <p className="muted small" style={{ marginTop: 0 }}>Each button opens a popup. <b>Run this</b> is your approval; the dashboard never starts anything. Say <span className="mono">continue with approved work</span> to the Director and it runs.</p>
      {BUTTONS.map((x) => {
        const h = hintFor(x.kind, hints);
        return (
          <div className="research-card" key={x.kind}>
            <div className="research-head"><b>{x.title}</b><span className="chip">{x.gate}</span><span className="chip" title={USAGE_TEXT[x.usage || 'M']}>usage {x.usage || 'M-XL'}</span></div>
            <p className="small" style={{ margin: '4px 0' }}>{x.blurb}</p>
            {h && <p className={`small ${h.due ? 'due' : 'muted'}`} style={{ margin: '0 0 6px' }}>{typeof h === 'string' ? h : h.text}</p>}
            <button className="primary" onClick={() => { setOpen(x.kind); setMsg(null); }}>{x.title}…</button>
          </div>);
      })}
      {msg && <p className={msg.ok ? 'saved-ok' : 'saved-err'} role="status">{msg.text}</p>}
      {mine.length > 0 && <><h4>Your research requests</h4>{mine.map((r) => (
        <div className="item" key={r.id}><b>{BUTTONS.find((x) => x.kind === r.research_kind)?.title || r.research_kind}</b>{r.targets ? ` (${r.targets.join(', ')})` : ''}<div className="meta">{done(r.id) ? 'done' : r.status === 'approved' ? 'approved, waiting for the Director' : r.status} · {ago(r.time)}</div></div>))}</>}
      {open && b && (
        <Modal title={b.title} onClose={close}>
          <p style={{ marginTop: 0 }}>{b.blurb}</p>
          {open === 'reanalyze' && (
            <>
              <div className="research-list">
                {games.length === 0 && <p className="empty">No games in the pipeline.</p>}
                {games.map((g) => (
                  <label key={g.slug} className="research-row">
                    <input type="checkbox" checked={!!picked[g.slug]} onChange={(e) => setPicked({ ...picked, [g.slug]: e.target.checked })} />
                    <span><b>{g.title}</b> <span className="muted small">{g.stage}{g.revision ? ` · revision ${g.revision}` : ''}</span></span>
                    <span className="muted small">{g.days === null ? 'never researched in depth' : `researched ${g.days} d ago`}</span>
                  </label>))}
              </div>
              <div className="small" style={{ margin: '6px 0' }}>
                <button className="link" onClick={() => setPicked(Object.fromEntries(games.map((g) => [g.slug, true])))}>Tick all</button> · <button className="link" onClick={() => setPicked({})}>Clear</button>
              </div>
            </>
          )}
          <p className="small">Estimated usage: <b>{usage}</b> ({USAGE_TEXT[usage]}){open === 'reanalyze' ? `, for ${chosen.length} game${chosen.length === 1 ? '' : 's'}` : ''}. {open === 'persona-research' && 'Thin evidence is likely until BoardGameGeek and Reddit are allowed in the environment’s network settings.'}</p>
          <textarea rows={2} value={note} onChange={(e) => setNote(e.target.value)} placeholder="Optional note for the researcher (for example: focus on tabletop RPGs)" style={{ width: '100%' }} />
          <div className="pitch-buttons">
            <button className="primary" disabled={busy || (open === 'reanalyze' && chosen.length === 0)} onClick={send}>{busy ? 'Saving…' : 'Run this'}</button>
            <button className="optbtn" onClick={close} disabled={busy}>Cancel</button>
          </div>
          {state.sample && <p className="muted small">Sample data: requests are not saved.</p>}
          {msg && !msg.ok && <p className="saved-err" role="status">{msg.text}</p>}
        </Modal>
      )}
    </>
  );
}
