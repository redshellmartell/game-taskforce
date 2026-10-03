import { Gate } from './Gate.jsx';
import { Help } from './Help.jsx';
import { ValueBars, colorOf } from './charts.jsx';
import { IdeaBank } from './IdeaBank.jsx';

const mixData = (rows) => rows.map((r) => ({ name: r.name, count: r.count }));

// What are we making, and is the portfolio varied? Where have we not looked yet?
export function MarketView({ state, onOpen }) {
  const m = state.market;
  const c = colorOf(state, 'market-researcher');
  const n = state.games.length;
  return (
    <div className="view">
      <div className="plist-head"><h2>Market and portfolio</h2><span className="muted">{m.briefs} brief{m.briefs === 1 ? '' : 's'} so far.</span></div>
      <div className="tiles">
        <div className={`kpi tile ${m.topMechanic?.status || 'none'}`}>
          <span className="num">{m.topMechanic ? `${m.topMechanic.share}%` : '—'}</span>
          <span className="lbl">Most common mechanic <Help topic="kpi" /></span>
          <span className="tgt">{m.topMechanic ? `${m.topMechanic.name} · ${m.topMechanic.target}` : 'no data yet'}</span>
        </div>
      </div>
      <IdeaBank bank={m.ideaBank} />
      <section className="card"><h3>Opportunity score for every brief</h3>
        <Gate games={n} what="This chart"><ValueBars data={m.opportunity} xKey="title" yKey="score" domain={[0, 30]} ticks={[0, 6, 12, 18, 24, 30]} refLine={18} refText="18 of 30 is the cut-off to proceed" color={c} label="score out of 30" /></Gate>
      </section>
      <div className="gp-grid">
        {[['Players', m.players], ['Play time', m.minutes], ['Complexity', m.complexity], ['Core mechanic', m.mechanics], ['Theme', m.themes]].map(([title, rows]) => (
          <section className="card" key={title}><h3>{title}</h3>
            <Gate games={n} what="This chart"><ValueBars data={mixData(rows)} xKey="name" yKey="count" horizontal color={c} label="games" /></Gate>
          </section>
        ))}
        <section className="card"><h3>Not explored yet</h3>
          <p className="muted" style={{ marginTop: 0 }}>Common mechanics none of your games use. Steer the researcher toward one with "+ New idea" or by asking Claude Code.</p>
          {m.unexplored.map((u) => <span className="chip" key={u}>{u}</span>)}
          {m.unexplored.length === 0 && <p className="empty">You have covered every mechanic on the list.</p>}
        </section>
      </div>
      <section className="card"><h3>Comparable titles <span className="muted" style={{ fontWeight: 400 }}>(at least 2 per brief)</span></h3>
        {m.comparables.length === 0 && <p className="empty">No briefs yet.</p>}
        {m.comparables.map((g) => (
          <div className="item" key={g.slug}>
            <button className="link" onClick={() => onOpen(g.slug)}>{g.title}</button> <span className={`chip ${g.status === 'good' ? 'v-good' : 'v-warn'}`}>{g.items.length} comparable{g.items.length === 1 ? '' : 's'}</span>
            {g.items.length === 0 && <div className="meta">None found.</div>}
            {g.items.map((x) => <div className="meta" key={x.name}><b>{x.name}</b> {x.bgg_rating != null ? `· BGG ${x.bgg_rating}` : ''} {x.crowdfunding ? `· ${x.crowdfunding}` : ''} {x.difference ? `· ours differs: ${x.difference}` : ''}</div>)}
          </div>
        ))}
      </section>
    </div>
  );
}
