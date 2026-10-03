import { useState } from 'react';
import { Help } from './Help.jsx';

// One column per stage. A game sits in the column of its current stage.
const COLUMNS = [
  { id: 'ideas', label: 'Your ideas', note: 'waiting in the inbox' },
  { id: 'brief', label: 'Research', stages: ['brief'] },
  { id: 'design', label: 'Design', stages: ['design'] },
  { id: 'playtest', label: 'Playtest', stages: ['playtest'] },
  { id: 'critique', label: 'Critique', stages: ['critique'] },
  { id: 'pitch', label: 'Pitch', stages: ['pitch'] },
  { id: 'review', label: 'Your review', stages: ['owner-review'] },
  { id: 'done', label: 'Approved', stages: ['approved', 'prototyped'] },
];
const DEAD = ['killed', 'archived'];
export const STAGE_LABEL = { brief: 'Research', design: 'Design', playtest: 'Playtest', critique: 'Critique', pitch: 'Pitch', 'owner-review': 'Your review', approved: 'Approved', prototyped: 'Prototyped', killed: 'Killed', archived: 'Archived' };
const IDEA_STAGE = { research: 'Market Intel', design: 'Design Studio', playtest: 'Playtest Lab', critique: 'Review Board', pitch: "Director's Office" };

export function verdictClass(v) {
  if (!v) return '';
  if (/^(PASS|APPROVE)/i.test(v)) return 'good';
  if (/KILL|BROKEN/i.test(v)) return 'bad';
  return 'warn';
}

function Card({ g, onOpen }) {
  const info = [g.pitch?.players || g.brief?.players, (g.pitch?.minutes || g.brief?.minutes) && `${g.pitch?.minutes || g.brief?.minutes} min`].filter(Boolean).join(' · ');
  const opp = g.brief?.opportunity_score;
  return (
    <button className="pcard" onClick={() => onOpen(g.slug)}>
      <b>{g.title}</b>
      {info && <span className="muted">{info}</span>}
      <span className="pmeta">
        {opp != null && <span className="chip">{opp}/30</span>}
        {g.verdicts?.playtest && <span className={`chip v-${verdictClass(g.verdicts.playtest)}`}>test: {g.verdicts.playtest}</span>}
        {g.verdicts?.critic && <span className={`chip v-${verdictClass(g.verdicts.critic)}`}>critic: {g.verdicts.critic}</span>}
        {g.revision > 0 && <span className="chip">rev {g.revision}</span>}
      </span>
    </button>
  );
}

export function ProjectsView({ state, onOpen, onOpenIdea }) {
  const [showDead, setShowDead] = useState(false);
  const dead = state.games.filter((g) => DEAD.includes(g.stage));
  return (
    <div className="projects">
      <div className="plist-head">
        <h2>Projects <Help topic="revision-loop" /></h2>
        <span className="muted">{state.games.length} game{state.games.length === 1 ? '' : 's'}. Click one for its full overview.</span>
      </div>
      <div className="board">
        {COLUMNS.map((c) => {
          const games = c.stages ? state.games.filter((g) => c.stages.includes(g.stage)) : [];
          const ideas = c.id === 'ideas' ? state.inbox : [];
          return (
            <section className="col" key={c.id}>
              <h3>{c.label} <span className="count">{games.length + ideas.length}</span></h3>
              {games.map((g) => <Card key={g.slug} g={g} onOpen={onOpen} />)}
              {ideas.map((i) => (
                <button className="pcard idea" key={i.slug} onClick={onOpenIdea}>
                  <b>{i.title}</b><span className="muted">starts at {IDEA_STAGE[i.stage]}</span>
                </button>
              ))}
              {games.length + ideas.length === 0 && <div className="empty small">none</div>}
            </section>
          );
        })}
      </div>
      {dead.length > 0 && (
        <div className="dead">
          <button className="link" onClick={() => setShowDead(!showDead)}>{showDead ? '▾' : '▸'} Killed and archived ({dead.length})</button>
          {showDead && dead.map((g) => (
            <div className="item" key={g.slug}><button className="link" onClick={() => onOpen(g.slug)}>{g.title}</button><div className="meta">{g.kill_reason || 'no reason recorded'}</div></div>
          ))}
        </div>
      )}
    </div>
  );
}
