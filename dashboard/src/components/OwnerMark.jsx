// A small gold star shown next to a game that came from one of YOUR submitted ideas.
export const OWNER_MARK = '★';
export function OwnerMark({ game }) {
  if (!game?.ownerIdea) return null;
  return <span className="ownermark" title="Your idea: you submitted this" aria-label="Your idea">{OWNER_MARK}</span>;
}
// For places that only take plain text (select options).
export const ownerPrefix = (game) => (game?.ownerIdea ? `${OWNER_MARK} ` : '');
