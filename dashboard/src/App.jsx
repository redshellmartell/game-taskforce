import { useEffect, useState } from 'react';
import { useStudioState } from './useStudioState.js';
import { TopBar } from './components/TopBar.jsx';
import { NetworkView } from './components/NetworkView.jsx';
import { ActivityFeed } from './components/ActivityFeed.jsx';
import { Replay } from './components/Replay.jsx';
import { ProjectsView } from './components/ProjectsView.jsx';
import { StudioFloor } from './components/StudioFloor.jsx';
import { GamePage } from './components/GamePage.jsx';
import { LearnContext } from './components/Help.jsx';
import { IdeaForm } from './components/IdeaForm.jsx';
import { AgentPanel, OwnerPanel, EdgePanel } from './components/SidePanel.jsx';
import { replayEvents, replayFrame } from './replay.js';

const store = {
  get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* storage blocked: fine */ } },
};

export default function App() {
  const { state, error } = useStudioState();
  const [selection, setSelection] = useState(null);
  const [view, setView] = useState('network'); // network | floor | pipeline
  const [game, setGame] = useState(null); // slug of the open Game page
  const [learn, setLearnState] = useState(() => store.get('learn') === '1');
  const [replay, setReplay] = useState(null);
  const [ideaOpen, setIdeaOpen] = useState(false);
  const setLearn = (v) => { setLearnState(v); store.set('learn', v ? '1' : '0'); };
  useEffect(() => { if (view !== 'network') setReplay(null); }, [view]);

  if (!state) return <div style={{ padding: 24 }} className="muted">{error ? `Could not reach the dashboard server: ${error}` : 'Loading…'}</div>;

  const agent = selection?.type === 'agent' ? state.agents.find((a) => a.id === selection.id) : null;
  const openGame = state.games.find((g) => g.slug === game);
  let frame = null;
  if (replay) {
    const g = state.games.find((x) => x.slug === replay.slug);
    frame = replayFrame(replayEvents(state, replay.slug), replay.index, g?.title || replay.slug, replay.slug);
  }

  return (
    <LearnContext.Provider value={learn}>
      <div className="app">
        <div>
          <TopBar state={state} learn={learn} setLearn={setLearn} />
          <nav className="nav">
            <button className={view === 'network' ? 'on' : ''} onClick={() => setView('network')}>Agent Network</button>
            <button className={view === 'floor' ? 'on' : ''} onClick={() => setView('floor')}>Studio Floor</button>
            <button className={view === 'pipeline' ? 'on' : ''} onClick={() => { setView('pipeline'); setGame(null); }}>Pipeline <span className="count">{state.games.length}</span></button>
            <span className="spacer" />
            <button className="newidea" onClick={() => setIdeaOpen(true)}>+ New idea</button>
          </nav>
          {view === 'network' && <Replay state={state} replay={replay} setReplay={setReplay} />}
        </div>
        {view === 'network' ? (
          <div className={`main ${selection ? 'open' : ''}`}>
            <NetworkView compact={!!selection} state={state} selection={selection} onSelect={setSelection} frame={frame} />
            {agent && <AgentPanel agent={agent} state={state} initialTab={selection.tab} onClose={() => setSelection(null)} />}
            {selection?.type === 'owner' && <OwnerPanel state={state} onClose={() => setSelection(null)} />}
            {selection?.type === 'edge' && <EdgePanel edge={selection.edge} state={state} onClose={() => setSelection(null)} />}
          </div>
        ) : view === 'floor' ? (
          <div className="page"><StudioFloor state={state} /></div>
        ) : (
          <div className="page">
            {openGame
              ? <GamePage game={openGame} state={state} onBack={() => setGame(null)} />
              : <ProjectsView state={state} onOpen={setGame} onOpenIdea={() => setIdeaOpen(true)} />}
          </div>
        )}
        {view === 'network' && <ActivityFeed state={state} />}
        {ideaOpen && (
          <div className="modal-bg" onMouseDown={(e) => e.target === e.currentTarget && setIdeaOpen(false)}>
            <div className="modal" role="dialog" aria-label="New idea">
              <header><h2>Inject an idea of your own</h2><button className="close" onClick={() => setIdeaOpen(false)} aria-label="Close">×</button></header>
              <p className="muted" style={{ marginTop: 0 }}>Already researched or developed something? Pick where it joins the pipeline. It is saved to your inbox; then ask the Director to run it.</p>
              <IdeaForm state={state} />
            </div>
          </div>
        )}
      </div>
    </LearnContext.Provider>
  );
}
