import { useEffect, useState } from 'react';
import { useStudioState } from './useStudioState.js';
import { TopBar } from './components/TopBar.jsx';
import { NetworkView } from './components/NetworkView.jsx';
import { ActivityFeed } from './components/ActivityFeed.jsx';
import { Replay } from './components/Replay.jsx';
import { ProjectsView } from './components/ProjectsView.jsx';
import { StudioFloor } from './components/StudioFloor.jsx';
import { ReviewQueueView } from './components/ReviewQueueView.jsx';
import { QualityLabView } from './components/QualityLabView.jsx';
import { MarketView } from './components/MarketView.jsx';
import { OpsView } from './components/OpsView.jsx';
import { ApprovalsView } from './components/ApprovalsView.jsx';
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
  const [view, setView] = useState('network'); // network | floor | pipeline | review | quality | market | ops
  const [game, setGame] = useState(null); // slug of the open Game page
  const [learn, setLearnState] = useState(() => store.get('learn') === '1');
  const [replay, setReplay] = useState(null);
  const [ideaOpen, setIdeaOpen] = useState(false);
  const go = (v) => { setView(v); setGame(null); };
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
          <TopBar state={state} learn={learn} setLearn={setLearn} onWaiting={() => go('approvals')} />
          <nav className="nav">
            <button className={view === 'network' ? 'on' : ''} onClick={() => go('network')}>Agent Network</button>
            <button className={view === 'floor' ? 'on' : ''} onClick={() => go('floor')}>Studio Floor</button>
            <button className={view === 'pipeline' ? 'on' : ''} onClick={() => go('pipeline')}>Pipeline <span className="count">{state.games.length}</span></button>
            <button className={view === 'approvals' ? 'on' : ''} onClick={() => go('approvals')}>Approvals {state.approvals.pending > 0 && <span className="count amber">{state.approvals.pending}</span>}</button>
            <button className={view === 'review' ? 'on' : ''} onClick={() => go('review')}>Review Queue {state.waitingPitches.length > 0 && <span className="count amber">{state.waitingPitches.length}</span>}</button>
            <button className={view === 'quality' ? 'on' : ''} onClick={() => go('quality')}>Quality Lab</button>
            <button className={view === 'market' ? 'on' : ''} onClick={() => go('market')}>Market &amp; Portfolio</button>
            <button className={view === 'ops' ? 'on' : ''} onClick={() => go('ops')}>Ops</button>
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
        ) : openGame ? (
          <div className="page"><GamePage game={openGame} state={state} onBack={() => setGame(null)} /></div>
        ) : view === 'floor' ? (
          <div className="page"><StudioFloor state={state} /></div>
        ) : view === 'approvals' ? (
          <div className="page"><ApprovalsView state={state} onOpen={setGame} /></div>
        ) : view === 'review' ? (
          <div className="page"><ReviewQueueView state={state} onOpen={setGame} /></div>
        ) : view === 'quality' ? (
          <div className="page"><QualityLabView state={state} onOpen={setGame} /></div>
        ) : view === 'market' ? (
          <div className="page"><MarketView state={state} onOpen={setGame} /></div>
        ) : view === 'ops' ? (
          <div className="page"><OpsView state={state} /></div>
        ) : (
          <div className="page">
            <ProjectsView state={state} onOpen={setGame} onOpenIdea={() => setIdeaOpen(true)} />
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
