// The dashboard's second allowed write (after the ideas inbox): recording the owner's decision on one approval request
// in games/approvals.json. It changes only that request's status, decision, decided_at and owner_notes, and never starts anything.
import fs from 'node:fs';

const EXPIRE_DAYS = 14;
const MAX_NOTES = 2000;
function fail(status, message) { const e = new Error(message); e.status = status; throw e; }

export function decideApproval(file, id, key, notes, now = Date.now()) {
  let data;
  try { data = JSON.parse(fs.readFileSync(file, 'utf8')); } catch { fail(404, 'There are no approval requests yet.'); }
  const req = (data.requests || []).find((r) => r && r.id === id);
  if (!req) fail(404, 'No such request.');
  if (req.status !== 'pending') fail(409, `This request was already ${req.status}.`);
  const age = Date.parse(req.time);
  if (!Number.isNaN(age) && now - age > EXPIRE_DAYS * 24 * 3600 * 1000) fail(409, 'This request has expired. Ask the Director to raise it again if it still matters.');
  if (!Array.isArray(req.options) || !req.options.some((o) => o.key === key)) fail(400, 'That is not one of this request\'s options.');
  const cleanNotes = notes == null ? '' : String(notes).trim();
  if (cleanNotes.length > MAX_NOTES) fail(400, `Notes are too long (max ${MAX_NOTES} characters).`);
  req.status = key === 'approve' ? 'approved' : 'declined';   // any other option (pitch, park, kill, ...) means the gated step is not run
  req.decision = key;
  req.decided_at = new Date(now).toISOString();
  req.owner_notes = cleanNotes || null;
  const tmp = `${file}.tmp`;
  fs.writeFileSync(tmp, JSON.stringify(data, null, 2) + '\n');
  fs.renameSync(tmp, file);                                  // replace in one step so a reader never sees half a file
  return { id, status: req.status, decision: req.decision, decided_at: req.decided_at };
}
