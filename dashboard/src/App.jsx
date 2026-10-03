import { useState } from 'react';
import { useStudioState } from './useStudioState.js';
import { TopBar } from './components/TopBar.jsx';
import { NetworkView } from './components/NetworkView.jsx';
import { ActivityFeed } from './components/ActivityFeed.jsx';
import { AgentPanel, OwnerPanel, EdgePanel } from './components/SidePanel.jsx';

export default function App() {
  const { state, error } = useStudioState();
  const [selection, setSelection] = useState(null);

  if (!state) return <div style={{ padding: 24 }} className="muted">{error ? `Could not reach the dashboard server: ${error}` : 'Loading…'}</div>;

  const agent = selection?.type === 'agent' ? state.agents.find((a) => a.id === selection.id) : null;
  return (
    <div className="app">
      <TopBar state={state} />
      <div className={`main ${selection ? 'open' : ''}`}>
        <NetworkView compact={!!selection} state={state} selection={selection} onSelect={setSelection} />
        {agent && <AgentPanel agent={agent} state={state} onClose={() => setSelection(null)} />}
        {selection?.type === 'owner' && <OwnerPanel state={state} onClose={() => setSelection(null)} />}
        {selection?.type === 'edge' && <EdgePanel edge={selection.edge} state={state} onClose={() => setSelection(null)} />}
      </div>
      <ActivityFeed state={state} />
    </div>
  );
}
