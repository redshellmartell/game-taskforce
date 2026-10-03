import { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { fetchFile } from '../useStudioState.js';

// Renders a Markdown string.
export function Markdown({ text }) {
  return <div className="md"><ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown></div>;
}

// Loads one repository file through /api/file and renders it (reloads when `version` changes).
export function FileView({ path, version }) {
  const [text, setText] = useState(null);
  const [err, setErr] = useState(false);
  useEffect(() => {
    let alive = true;
    setErr(false);
    fetchFile(path).then((t) => alive && setText(t)).catch(() => alive && setErr(true));
    return () => { alive = false; };
  }, [path, version]);
  if (err) return <p className="empty">No data yet for {path}</p>;
  if (text === null) return <p className="muted">Loading…</p>;
  return <><div className="muted mono" style={{ fontSize: 11, marginBottom: 8 }}>{path}</div><Markdown text={text} /></>;
}
