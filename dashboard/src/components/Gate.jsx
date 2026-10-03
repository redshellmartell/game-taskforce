// Charts that compare games need at least two games to mean anything.
export const MIN_GAMES = 2;
export function Gate({ games, children, what = 'These charts' }) {
  if (games >= MIN_GAMES) return children;
  return <div className="nodata gate" style={{ minHeight: 90 }}>{what} appear once there are at least {MIN_GAMES} games. You have {games} so far.</div>;
}
