// The dashboard's third allowed write: the owner's decision on a pitch waiting in the Review Queue.
// It only appends one entry to games/decisions.json (atomic write). It never edits status.json and never starts anything:
// the Director reads the decision on "continue with approved work" and moves the game's stage.
import fs from 'node:fs';

const KEYS = ['approve', 'reject', 'send-back'];
export const SEND_BACK_TARGETS = ['market-researcher', 'game-designer', 'playtester', 'test-panel', 'critic'];   // the departments a pitch can be sent back to
const MAX_NOTES = 2000;
function fail(status, message) { const e = new Error(message); e.status = status; throw e; }

// Which games are in owner-review and when they got there (from status.json).
function waitingSince(statusFile) {
  let st; try { st = JSON.parse(fs.readFileSync(statusFile, 'utf8')); } catch { return {}; }
  const out = {};
  for (const g of st.games || []) if (g.stage === 'owner-review') {
    const h = [...(g.history || [])].reverse().find((e) => e.stage === 'owner-review');
    out[g.slug] = h ? Date.parse(h.time) || 0 : 0;
  }
  return out;
}

// The pitch decision (if any) recorded for a game since it entered owner-review.
// Only entries marked kind "pitch" count: decisions.json also holds approval-gate decisions ("approve" on a revision, a scan...) that must not be mistaken for a decision on the pitch.
export function pitchDecisionFor(slug, since, decisions) {
  return [...(decisions || [])].reverse().find((d) => d && d.kind === 'pitch' && d.slug === slug && KEYS.includes(d.decision) && (Date.parse(d.time) || 0) >= since) || null;
}

export function decidePitch(decisionsFile, statusFile, slug, key, notes, now = Date.now(), target = null) {
  if (!KEYS.includes(key)) fail(400, 'That is not a pitch decision (approve, reject or send-back).');
  if (target != null && target !== '' && (key !== 'send-back' || !SEND_BACK_TARGETS.includes(target))) fail(400, 'Pick one of the departments to send it back to.');
  const cleanNotes = notes == null ? '' : String(notes).trim();
  if (cleanNotes.length > MAX_NOTES) fail(400, `Notes are too long (max ${MAX_NOTES} characters).`);
  const waiting = waitingSince(statusFile);
  if (!(slug in waiting)) fail(404, 'That game is not waiting for your decision.');
  let data = { decisions: [] };
  try { data = JSON.parse(fs.readFileSync(decisionsFile, 'utf8')); if (!Array.isArray(data.decisions)) data.decisions = []; } catch { /* no file yet: start one */ }
  if (pitchDecisionFor(slug, waiting[slug], data.decisions)) fail(409, 'You already decided on this pitch.');
  const entry = { slug, kind: 'pitch', time: new Date(now).toISOString(), decision: key, ...(key === 'send-back' ? { target: target || 'game-designer' } : {}), notes: cleanNotes || 'decided in the dashboard (Review Queue)' };
  data.decisions.push(entry);
  const tmp = `${decisionsFile}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n');
  fs.renameSync(tmp, decisionsFile);
  return entry;
}
