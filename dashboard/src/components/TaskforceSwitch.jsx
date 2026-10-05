import { useState } from 'react';

const LABEL = { running: 'Running', paused: 'Paused', stopped: 'Stopped', 'waiting-gate': 'Waiting for you', 'usage-stop': 'Stopped: usage limit', error: 'Stopped: error', interrupted: 'Interrupted (the Mac may have slept)' };

// The taskforce on/off switch (task 014). It only writes studio/taskforce.json; the runner reads the file.
export function TaskforceSwitch({ state }) {
  const tf = state.taskforce;
  const [mode, setMode] = useState(tf?.pause_mode || 'after-step');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  if (!tf) return null;
  const toggle = async () => {
    setBusy(true); setError(null);
    try {
      const res = await fetch('/api/taskforce/switch', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ active: !tf.active, pause_mode: mode }) });
      const body = await res.json();
      if (!res.ok) throw new Error(body.error || 'Could not save the switch');
    } catch (e) { setError(e.message); }
    setBusy(false);
  };
  const run = tf.run || {};
  const label = LABEL[tf.displayStatus] || tf.displayStatus;
  const where = run.game && ['running', 'interrupted'].includes(tf.displayStatus) ? `${run.game}${run.step ? `: ${run.step}` : ''}` : null;
  return (
    <div className={`tf-switch ${tf.active ? 'on' : 'off'}`} title={run.reason ? `Last stop reason: ${run.reason}` : 'The taskforce switch'}>
      <button className={`tf-btn ${tf.active ? 'on' : 'off'}`} onClick={toggle} disabled={busy || state.sample} aria-pressed={tf.active}>
        <span className="tf-dot" /> Taskforce {tf.active ? 'ON' : 'OFF'}
      </button>
      <span className="tf-status">{label}{where ? ` · ${where}` : ''}</span>
      <select className="tf-mode" value={mode} onChange={(e) => setMode(e.target.value)} disabled={busy} title="What happens when you switch it off">
        <option value="after-step">Pause after this step</option>
        <option value="now">Stop now</option>
      </select>
      {tf.stopFile && <span className="chip v-bad" title="studio/STOP exists, so the runner will not start">STOP file</span>}
      {error && <span className="err">{error}</span>}
      {state.sample && <span className="muted small">sample data</span>}
    </div>
  );
}
