// Reads the player test panel (panel/personas/*.md, panel/calibration.json) for the dashboard.
// Persona files start with a small settings block between --- lines (see panel/README.md).
import fs from 'node:fs';
import path from 'node:path';

function scalar(v) {
  const t = v.trim();
  if (t.startsWith('[')) { try { return JSON.parse(t); } catch { return t; } }
  if ((t.startsWith('"') && t.endsWith('"')) || (t.startsWith("'") && t.endsWith("'"))) return t.slice(1, -1);
  return /^-?\d+(\.\d+)?$/.test(t) ? Number(t) : t;
}

// Parses the --- block: "key: value", "key: [a, b]", and one level of nested "  key: number" (the weights).
export function parseFrontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return {};
  const out = {}; let nested = null;
  for (const raw of m[1].split(/\r?\n/)) {
    const line = raw.replace(/\s+#.*$/, '');
    let k = line.match(/^([A-Za-z_][\w]*):\s*(.*)$/);
    if (k) { if (k[2] === '') { nested = {}; out[k[1]] = nested; } else { nested = null; out[k[1]] = scalar(k[2]); } continue; }
    k = line.match(/^\s+([A-Za-z_][\w]*):\s*(.+)$/);
    if (k && nested) nested[k[1]] = scalar(k[2]);
  }
  return out;
}

function readJson(file) { try { return JSON.parse(fs.readFileSync(file, 'utf8')); } catch { return null; } }

export function loadPanel(repoRoot) {
  const dir = path.join(repoRoot, 'panel', 'personas');
  let files = [];
  try { files = fs.readdirSync(dir).filter((f) => f.endsWith('.md')).sort(); } catch { return null; }
  const cal = readJson(path.join(repoRoot, 'panel', 'calibration.json'));
  const personas = [];
  for (const f of files) {
    try {
      const fm = parseFrontmatter(fs.readFileSync(path.join(dir, f), 'utf8'));
      if (!fm.id) continue;
      const c = cal?.personas?.[fm.id] || null;
      const drivers = Object.entries(fm.weights || {}).filter(([, w]) => w > 0).sort((a, b) => b[1] - a[1]).slice(0, 3)
        .map(([metric, weight]) => ({ metric, percent: Math.round(weight * 100) }));
      personas.push({
        id: fm.id, name: fm.name || fm.id, archetype: fm.archetype || '', tagline: fm.tagline || '', color: fm.color || '#8a8f9b', initials: fm.initials || fm.id.slice(0, 2).toUpperCase(),
        botStyle: fm.bot_style || null, preferredMinutes: fm.preferred_minutes || null, priceUsd: fm.price_tolerance_usd || null, drivers,
        veto: fm.veto || null, profile: `panel/personas/${f}`, evidence: fm.evidence || `panel/evidence/${fm.id}.md`,
        calibration: c ? { trusted: !!c.trusted, meanAbsError: c.mean_abs_error, ratedGames: c.rated_games, confidence: c.confidence || null, notes: c.notes || '',
          games: (c.games || []).map((g) => ({ game: g.game, predicted: g.predicted, actual: g.actual })) } : null,
      });
    } catch { /* unreadable persona file: skip it */ }
  }
  return { personas, trustLimit: cal?.trust_limit ?? null, baselineQuality: cal?.baseline_quality || null, baselineNotes: cal?.baseline_notes || [], calibrated: cal?.updated || null };
}
