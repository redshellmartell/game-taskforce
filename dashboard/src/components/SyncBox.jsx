import { useState } from 'react';
import { CopyBox } from './IdeaForm.jsx';

// After a decision is saved on this computer, Claude Code in the cloud only sees it once it is pushed. One click commits and pushes the decision files.
export function SyncBox({ message, onDismiss }) {
  const [state, setState] = useState({ busy: false, done: null, error: null });
  const sync = async () => {
    setState({ busy: true, done: null, error: null });
    try {
      const res = await fetch('/api/sync', { method: 'POST' });
      const body = await res.json();
      if (!res.ok) throw new Error(body.error || 'Could not push');
      setState({ busy: false, done: body, error: null });
    } catch (e) { setState({ busy: false, done: null, error: e.message }); }
  };
  return (
    <div className="card saved-decision">
      <p style={{ margin: '0 0 6px' }}><b>Saved on this computer:</b> {message} Nothing has run yet.</p>
      {!state.done && <p className="muted small" style={{ margin: '0 0 6px' }}>If you use Claude Code in the cloud, push first so it can see your decision.</p>}
      {!state.done && <button className="primary" disabled={state.busy} onClick={sync}>{state.busy ? 'Pushing…' : 'Push my decision'}</button>}
      {state.done && <p style={{ margin: '0 0 6px' }}>Pushed to <span className="mono">{state.done.branch}</span>. Now tell Claude Code:</p>}
      {state.error && <p className="err">{state.error}</p>}
      {state.done && <CopyBox text="Continue with approved work" />}
      <button className="link" onClick={onDismiss}>Dismiss</button>
    </div>
  );
}
