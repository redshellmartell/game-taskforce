export const METRIC = { skill_expression: 'skill over luck', decisions_per_turn: 'meaningful decisions', lead_changes: 'lead changes', length_fit: 'fitting their time', rules_simplicity: 'simple rules', catch_up: 'nobody left behind', interaction: 'interaction', dominant_strategy_absent: 'no dominant strategy', originality: 'originality' };

export function Avatar({ p, size = 38 }) {
  return <span className="avatar" style={{ background: p.color, width: size, height: size, fontSize: size * 0.38 }} aria-hidden>{p.initials}</span>;
}

export function TrustChip({ cal, limit }) {
  if (!cal) return <span className="chip">not calibrated</span>;
  return <span className={`chip ${cal.trusted ? 'v-good' : 'v-warn'}`} title={`mean error ${cal.meanAbsError} over ${cal.ratedGames} games (limit ${limit})`}>{cal.trusted ? 'trusted' : 'not trusted'} · error {cal.meanAbsError}</span>;
}

// One persona: who they are, what drives their fun, how well they matched real receptions, and links to the files.
function PersonaDetail({ p, panel, onBack, onOpen, onPersona }) {
  const c = p.calibration;
  return (
    <>
      <button className="link back" onClick={onBack}>← All personas</button>
      <div className="persona-head"><Avatar p={p} size={48} /><div><h3 style={{ margin: 0, textTransform: 'none', letterSpacing: 0, fontSize: 17, color: p.color }}>{p.name}</h3><div className="muted">{p.archetype}</div></div></div>
      <p className="hook" style={{ margin: '10px 0' }}>“{p.tagline}”</p>
      <h4>What drives their fun</h4>
      {p.drivers.map((d) => <div className="bar" key={d.metric} style={{ gridTemplateColumns: '150px 1fr 40px' }}><span>{METRIC[d.metric] || d.metric}</span><i style={{ width: `${d.percent * 2}%`, '--accent': p.color }} /><b className="mono">{d.percent}%</b></div>)}
      <div className="muted small" style={{ marginTop: 4 }}>{p.preferredMinutes && `Likes games of ${p.preferredMinutes[0]}-${p.preferredMinutes[1]} minutes`}{p.priceUsd && ` · pays about $${p.priceUsd[0]}-${p.priceUsd[1]}`}{p.botStyle && ` · plays like a "${p.botStyle}" in simulations`}</div>
      <h4>Calibration <TrustChip cal={c} limit={panel.trustLimit} /></h4>
      {c ? (
        <>
          <table className="score"><thead><tr className="muted"><td>Game</td><td>Predicted</td><td>Real</td></tr></thead>
            <tbody>{c.games.map((g) => <tr key={g.game}><td>{g.game}</td><td className="mono">{g.predicted ?? '—'}</td><td className="mono">{g.actual ?? '—'}</td></tr>)}</tbody></table>
          <p className="muted small">Predicted: what this persona said from its profile alone. Real: how this type of player received the game, from the research.{c.notes && ` ${c.notes}`}</p>
        </>
      ) : <p className="empty">Not calibrated yet.</p>}
      <h4>Read more</h4>
      <div>{onPersona && <><button className="link" onClick={() => onPersona(p.id)}>Open their full page</button> · </>}<button className="link" onClick={() => onOpen(p.profile)}>Full profile</button> · <button className="link" onClick={() => onOpen(p.evidence)}>Research evidence</button></div>
    </>
  );
}

// The Playtest Lab's "Test panel" tab: the player personas that give games a public test.
export function PanelTab({ state, onOpen, id, setId, onPersona }) {
  const panel = state.panel;
  if (!panel || panel.personas.length === 0) return <p className="empty">No personas yet. They live in panel/personas/ (see panel/README.md).</p>;
  const p = panel.personas.find((x) => x.id === id);
  if (p) return <PersonaDetail p={p} panel={panel} onBack={() => setId(null)} onOpen={onOpen} onPersona={onPersona} />;
  return (
    <>
      <p style={{ marginTop: 0 }}>A panel of {panel.personas.length} player types gives each game a public test on top of the bot playtest. Click one to see who they are and how well they match real players.</p>
      {panel.baselineQuality === 'low' && <p className="notice">Trust flags are provisional: the research behind the calibration is thin ({panel.baselineNotes[0] ? 'see the notes in panel/calibration.json' : 'low-confidence baseline'}). Treat the personas as advisory.</p>}
      <div className="persona-list">
        {panel.personas.map((x) => (
          <button className="persona-card" key={x.id} onClick={() => setId(x.id)} style={{ '--accent': x.color }}>
            <Avatar p={x} />
            <span className="persona-main"><b style={{ color: x.color }}>{x.name}</b><span className="muted small">{x.archetype}</span><span className="small">“{x.tagline}”</span>
              <span className="persona-chips"><TrustChip cal={x.calibration} limit={panel.trustLimit} />{x.drivers.slice(0, 2).map((d) => <span className="chip" key={d.metric}>{METRIC[d.metric] || d.metric} {d.percent}%</span>)}</span></span>
          </button>))}
      </div>
    </>
  );
}
