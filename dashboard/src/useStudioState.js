import { useEffect, useState } from 'react';

// Loads /api/state, and reloads it whenever the server says a watched file changed.
export function useStudioState() {
  const [state, setState] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let alive = true;
    const load = () => fetch('/api/state').then((r) => r.json()).then((s) => { if (alive) { setState(s); setError(null); } }).catch((e) => alive && setError(e.message));
    load();
    const es = new EventSource('/api/events');
    es.addEventListener('changed', load);
    const tick = setInterval(load, 30000); // also refresh now and then so "working" states age out
    return () => { alive = false; es.close(); clearInterval(tick); };
  }, []);

  return { state, error };
}

export async function fetchFile(path) {
  const r = await fetch(`/api/file?path=${encodeURIComponent(path)}`);
  if (!r.ok) throw new Error('No data yet');
  return (await r.json()).text;
}
