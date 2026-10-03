import { createContext, useContext, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { topics, REPO_URL } from '../learn.js';

export const LearnContext = createContext(false);

// A small "?" that only appears in Learn mode and opens a 2-3 sentence explanation.
export function Help({ topic }) {
  const learn = useContext(LearnContext);
  const [pos, setPos] = useState(null);
  const btn = useRef(null);
  const t = topics[topic];

  useEffect(() => {
    if (!pos) return undefined;
    const close = (e) => {
      if (e.type === 'keydown' ? e.key === 'Escape' : !e.target.closest?.('.learn-pop, .help')) setPos(null);
    };
    document.addEventListener('mousedown', close);
    document.addEventListener('keydown', close);
    return () => { document.removeEventListener('mousedown', close); document.removeEventListener('keydown', close); };
  }, [pos]);

  if (!learn || !t) return null;
  const toggle = (e) => {
    e.stopPropagation(); e.preventDefault();
    if (pos) return setPos(null);
    const r = btn.current.getBoundingClientRect();
    return setPos({ x: Math.min(r.left, window.innerWidth - 320), y: r.bottom + 6 });
  };
  return (
    <>
      <button ref={btn} className="help nodrag nopan" onClick={toggle} onMouseDown={(e) => e.stopPropagation()} aria-label={`Explain: ${t.title}`}>?</button>
      {pos && createPortal(
        <div className="learn-pop" style={{ left: Math.max(8, pos.x), top: pos.y }} role="dialog">
          <b>{t.title}</b>
          <p>{t.body}</p>
          {t.link && <a href={REPO_URL + t.link} target="_blank" rel="noreferrer">See the real file: {t.link}</a>}
        </div>, document.body)}
    </>
  );
}
