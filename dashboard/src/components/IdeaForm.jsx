import { useState } from 'react';

// Where an idea can enter the pipeline. Stages before it are skipped: your material stands in for them.
const AGENT_STAGE = { 'market-researcher': 'research', 'game-designer': 'design', playtester: 'playtest', critic: 'critique', manager: 'pitch' };
const STAGE_HELP = {
  research: 'Research it first (I only have a rough thought)',
  design: 'Design the rules (I already have a brief)',
  playtest: 'Playtest it (I already have rules)',
  critique: 'Critique it (I already have a tested design)',
  pitch: 'Write the pitch (it is ready)',
};
const STAGE_SHORT = { research: 'rough idea', design: 'have a brief', playtest: 'have rules', critique: 'tested design', pitch: 'ready to pitch' };
export const stageForAgent = (id) => AGENT_STAGE[id] || 'research';

export function CopyBox({ text }) {
  const [done, setDone] = useState(false);
  const copy = async () => {
    try { await navigator.clipboard.writeText(text); } catch { /* clipboard blocked: user can still select the text */ }
    setDone(true); setTimeout(() => setDone(false), 1500);
  };
  return (
    <div className="copybox">
      <code>{text}</code>
      <button onClick={copy}>{done ? 'Copied' : 'Copy'}</button>
    </div>
  );
}

// Saves your own idea into games/_inbox/ (the dashboard's only write). The Director runs it when you ask.
export function IdeaForm({ state, fixedStage, heading }) {
  const roomFor = (stage) => state.agents.find((a) => AGENT_STAGE[a.id] === stage)?.room || stage;
  const [title, setTitle] = useState('');
  const [notes, setNotes] = useState('');
  const [stage, setStage] = useState(fixedStage || 'research');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [saved, setSaved] = useState(null);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true); setError(null);
    try {
      const r = await fetch('/api/ideas', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title, notes, stage: fixedStage || stage }) });
      const body = await r.json();
      if (!r.ok) throw new Error(body.error || 'Could not save');
      setSaved({ ...body, title }); setTitle(''); setNotes('');
    } catch (err) { setError(err.message); }
    setBusy(false);
  };

  return (
    <form className="ideaform" onSubmit={submit}>
      {heading && <h4>{heading}</h4>}
      <label>Name of the idea<input value={title} onChange={(e) => setTitle(e.target.value)} maxLength={120} placeholder="e.g. Paper Lanterns" required /></label>
      <label>Your notes, brief, or rules (paste anything you already have)
        <textarea value={notes} onChange={(e) => setNotes(e.target.value)} rows={6} placeholder="What is the game? Who is it for? What do you already know?" />
      </label>
      {!fixedStage && (
        <div>
          <div className="lbl-small">Where should it enter the pipeline?</div>
          <div className="stages" role="radiogroup">
            {Object.keys(STAGE_HELP).map((s) => <button type="button" role="radio" aria-checked={stage === s} key={s} className={stage === s ? 'on' : ''} onClick={() => setStage(s)}>{roomFor(s)}<small>{STAGE_SHORT[s]}</small></button>)}
          </div>
          <p className="muted small" style={{ margin: '6px 0 0' }}>{STAGE_HELP[stage]}. Earlier steps are skipped.</p>
        </div>
      )}
      {fixedStage && <p className="muted" style={{ margin: '0 0 8px' }}>Starts at <b>{roomFor(fixedStage)}</b>: {STAGE_HELP[fixedStage]}.</p>}
      <button className="primary" disabled={busy || !title.trim()}>{busy ? 'Saving…' : 'Save idea to inbox'}</button>
      {error && <p className="err">{error}</p>}
      {saved && (
        <div className="saved">
          <p>Saved to <span className="mono">{saved.file}</span>. Nothing has run yet. To push it through the agents, tell the Director:</p>
          <CopyBox text={`Process my idea "${saved.title}" from ${saved.file}. Start at the ${saved.stage} stage.`} />
        </div>
      )}
    </form>
  );
}
