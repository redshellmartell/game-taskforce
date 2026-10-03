#!/usr/bin/env python3
"""Usage meter: where do the studio's Claude Code tokens (and API-equivalent dollars) go?

Reads the session logs Claude Code keeps for this project (default: ~/.claude/projects/<this repo>/), totals tokens
per agent, model, game (or research / dashboard / panel / other) and day, and can append a summary of each session to
usage/sessions.jsonl so cloud-session data is kept in the repository. Only counts, names and times are stored:
never prompts or content. Standard library only.

  python3 tools/usage/usage.py                 # print the tables (tokens first)
  python3 tools/usage/usage.py --record        # also append/refresh usage/sessions.jsonl
  python3 tools/usage/usage.py --check         # usage guard: how full is each window? exit 0 ok, 1 warn, 2 STOP, 3 not calibrated
  python3 tools/usage/usage.py --calibrate 5h=63 7d=41   # tell it your plan's usage % (from the app) so it can turn tokens into %
  python3 tools/usage/usage.py --cost          # also show the API-equivalent dollar column
  python3 tools/usage/usage.py --logs DIR      # use another log folder (for example one copied from your Mac)
  python3 tools/usage/usage.py --json          # machine-readable output

How a session log is laid out (Claude Code 2.1): <session>.jsonl is the main (Director) conversation; each sub-agent has
<session>/subagents/agent-<id>.jsonl plus an agent-<id>.meta.json with its agentType. Assistant lines carry
message.usage (input, output, cache read and cache creation tokens) and message.model; 'cost-state' lines carry Claude
Code's own running cost total (reported_cost_usd), which includes work not visible in the message logs, such as the
Haiku calls behind web searches.
"""
import argparse, collections, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
FIELDS = ('input', 'output', 'cache_read', 'cache_write')
USAGE_KEYS = {'input': 'input_tokens', 'output': 'output_tokens', 'cache_read': 'cache_read_input_tokens', 'cache_write': 'cache_creation_input_tokens'}


DEFAULT_GUARD = {'stop_at_percent': 80, 'warn_at_percent': 60, 'cache_read_weight': 0.1,
                 'windows': {'5h': {'hours': 5, 'token_budget': None}, '7d': {'hours': 168, 'token_budget': None}}}
SETTINGS = os.path.join(REPO, 'studio-settings.json')


def zero(): return {f: 0 for f in FIELDS}
def weighted(tok, w=0.1):
    """One number for 'how much usage': input + output + cache writes, plus cache reads at a reduced weight (they are re-reads of
    an already-cached context). The weight is a setting; recalibrate with --calibrate if your plan percentages drift."""
    return tok['input'] + tok['output'] + tok['cache_write'] + w * tok['cache_read']
def add(a, b):
    for f in FIELDS: a[f] += b[f]
def load_prices(path=None):
    with open(path or os.path.join(HERE, 'prices.json')) as f: return json.load(f)['models']
def cost_of(tok, price):
    """API-equivalent dollars for a token dict, or None when the model's price is unknown."""
    if not price or price.get('input') is None or price.get('output') is None: return None
    return sum(tok[f] * (price.get(f) or 0) for f in FIELDS) / 1e6
def iter_jsonl(path):
    try:
        with open(path, errors='ignore') as f:
            for line in f:
                try: yield json.loads(line)
                except ValueError: continue
    except OSError: return


def default_log_dir(repo=REPO):
    root = os.path.join(os.path.expanduser('~'), '.claude', 'projects')
    exact = os.path.join(root, re.sub(r'[^A-Za-z0-9]', '-', repo))
    if os.path.isdir(exact): return exact
    hits = glob.glob(os.path.join(root, '*' + os.path.basename(repo)))
    return hits[0] if hits else None


class Attributor:
    """Which part of the studio is this work for? Looks at the paths in each tool call (games/<slug>, dashboard/, panel/,
    research/); a message with no path keeps the previous answer; failing that, the game whose activity.jsonl window
    (first to last event, plus 15 minutes either side) contains the time; failing that, 'other'."""
    def __init__(self, games_dir):
        self.slugs = set(); self.windows = []
        if games_dir and os.path.isdir(games_dir):
            for d in os.listdir(games_dir):
                if os.path.isdir(os.path.join(games_dir, d)) and not d.startswith('_'):
                    self.slugs.add(d)
                    times = [parse_ts(e.get('time')) for e in iter_jsonl(os.path.join(games_dir, d, 'activity.jsonl'))]
                    times = [t for t in times if t]
                    if times: self.windows.append((min(times) - 900, max(times) + 900, d))

    def from_text(self, text):
        for m in re.finditer(r'(games/([a-z0-9][a-z0-9-]*)|dashboard/|panel/|research/|tools/usage|usage/sessions)', text):
            g = m.group(0)
            if g.startswith('games/'):
                if m.group(2) in self.slugs: return m.group(2)
            elif g.startswith('dashboard/'): return 'dashboard'
            elif g.startswith('panel/'): return 'panel'
            elif g.startswith('research/'): return 'research'
            else: return 'usage tooling'
        return None

    def from_time(self, ts):
        if ts:
            for lo, hi, slug in self.windows:
                if lo <= ts <= hi: return slug
        return None


def parse_ts(s):
    try: return datetime.datetime.fromisoformat(str(s).replace('Z', '+00:00')).timestamp()
    except (ValueError, TypeError): return None


def read_agent_log(path, agent, attr):
    """One conversation file -> rows of (agent, model, category, day, tokens). Messages repeated across lines are counted once."""
    seen = {}; order = []; sticky = None
    for o in iter_jsonl(path):
        m = o.get('message')
        if o.get('type') != 'assistant' or not isinstance(m, dict) or not isinstance(m.get('usage'), dict): continue
        u = m['usage']; tok = {f: int(u.get(USAGE_KEYS[f]) or 0) for f in FIELDS}
        blocks = m.get('content') if isinstance(m.get('content'), list) else []
        text = ' '.join(json.dumps(b.get('input', {})) for b in blocks if isinstance(b, dict) and b.get('type') == 'tool_use')
        found = attr.from_text(text)
        if found: sticky = found
        ts = o.get('timestamp'); cat = sticky or attr.from_time(parse_ts(ts)) or 'other'
        key = m.get('id') or o.get('uuid') or id(o)
        if key not in seen: order.append(key)
        seen[key] = (agent, m.get('model') or 'unknown', cat, str(ts)[:10], tok, str(ts)[:13])   # later lines of the same message carry the final counts
    return [seen[k] for k in order]


def read_session(main_file, attr):
    sid = os.path.basename(main_file)[:-len('.jsonl')]
    rows = read_agent_log(main_file, 'director', attr)
    sub = os.path.join(os.path.dirname(main_file), sid, 'subagents')
    for f in sorted(glob.glob(os.path.join(sub, 'agent-*.jsonl'))):
        try: meta = json.load(open(f[:-len('.jsonl')] + '.meta.json'))
        except (OSError, ValueError): meta = {}
        rows += read_agent_log(f, meta.get('agentType') or 'general-purpose', attr)
    reported = None; web = 0; first = last = None
    for o in iter_jsonl(main_file):
        ts = o.get('timestamp')
        if ts: first = first or ts; last = ts
        if o.get('type') == 'cost-state':
            reported = {'cost_usd': o.get('totalCostUSD'), 'models': o.get('modelUsage') or {}}
    if reported: web = sum(int(v.get('webSearchRequests') or 0) for v in reported['models'].values())
    return {'session': sid, 'rows': rows, 'reported': reported, 'web_searches': web, 'start': first, 'end': last}


def summarise(sess, prices):
    by_am = collections.defaultdict(zero); by_cat = collections.defaultdict(zero); by_day = collections.defaultdict(zero); by_hour = collections.defaultdict(zero)
    unknown = set()
    for agent, model, cat, day, tok, hour in sess['rows']:
        add(by_am[(agent, model)], tok); add(by_cat[(cat, model)], tok); add(by_day[(day, model)], tok); add(by_hour[(hour, model)], tok)
    def money(d):
        out = collections.defaultdict(lambda: {'tokens': zero(), 'cost_usd': 0.0})
        for (name, model), tok in d.items():
            c = cost_of(tok, prices.get(model)); add(out[name]['tokens'], tok)
            if c is None: unknown.add(model)
            else: out[name]['cost_usd'] += c
        return out
    est = sum(r['cost_usd'] for r in money(by_am).values())
    rep = (sess['reported'] or {}).get('cost_usd')
    return {'by_agent': money({(a, m): t for (a, m), t in by_am.items()}), 'by_agent_model': by_am, 'by_category': money(by_cat), 'by_day': money(by_day), 'by_hour': money(by_hour),
            'estimated_cost_usd': est, 'reported_cost_usd': rep, 'unpriced_models': sorted(unknown)}


def record_line(sess, summ):
    rnd = lambda x: round(x, 4)
    def block(d): return [{'name': k, **v['tokens'], 'weighted_tokens': int(weighted(v['tokens'])), 'cost_usd': rnd(v['cost_usd'])} for k, v in sorted(d.items(), key=lambda kv: -weighted(kv[1]['tokens']))]
    return {'session': sess['session'], 'start': sess['start'], 'end': sess['end'], 'recorded_at': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'reported_cost_usd': None if summ['reported_cost_usd'] is None else rnd(summ['reported_cost_usd']), 'estimated_cost_usd': rnd(summ['estimated_cost_usd']),
            'web_searches': sess['web_searches'], 'unpriced_models': summ['unpriced_models'],
            'by_agent': block(summ['by_agent']), 'by_category': block(summ['by_category']), 'by_day': block(summ['by_day']), 'by_hour': block(summ['by_hour']),
            'by_agent_model': [{'agent': a, 'model': m, **t} for (a, m), t in sorted(summ['by_agent_model'].items())]}


def record(path, lines):
    """Append, or replace the existing line for the same session (a session's totals grow over time)."""
    keep = [l for l in iter_jsonl(path) if l.get('session') not in {x['session'] for x in lines}] if os.path.exists(path) else []
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        for l in keep + lines: f.write(json.dumps(l) + '\n')


def load_settings(path=SETTINGS):
    try:
        with open(path) as f: return json.load(f)
    except (OSError, ValueError): return {}
def guard_config(settings):
    g = json.loads(json.dumps(DEFAULT_GUARD)); g.update({k: v for k, v in (settings.get('usage_guard') or {}).items() if k != 'windows'})
    for name, w in ((settings.get('usage_guard') or {}).get('windows') or {}).items(): g['windows'].setdefault(name, {}).update(w)
    return g
def hourly_weighted(summs, recorded, live_ids, w):
    """hour -> weighted tokens, from the live logs plus recorded sessions that are not live (so nothing is counted twice)."""
    h = collections.defaultdict(float)
    for m in summs:
        for hour, v in m['by_hour'].items(): h[hour] += weighted(v['tokens'], w)
    for r in recorded:
        if r.get('session') in live_ids: continue
        for b in r.get('by_hour', []): h[b['name']] += weighted({f: b.get(f, 0) for f in FIELDS}, w)
    return h
def window_used(hourly, hours, now):
    cut = now - hours * 3600
    return sum(v for hour, v in hourly.items() if (parse_ts(hour + ':00:00Z') or 0) >= cut - 3599)   # hour buckets: include the one that overlaps the cut
def check_guard(hourly, cfg, now):
    out = []; worst = 0
    for name, w in cfg['windows'].items():
        used = window_used(hourly, w['hours'], now); budget = w.get('token_budget')
        pct = None if not budget else 100.0 * used / budget
        status = 'uncalibrated' if pct is None else 'stop' if pct >= cfg['stop_at_percent'] else 'warn' if pct >= cfg['warn_at_percent'] else 'ok'
        worst = max(worst, {'ok': 0, 'warn': 1, 'stop': 2, 'uncalibrated': 3}[status] if status != 'uncalibrated' else 0)
        out.append({'name': name, 'hours': w['hours'], 'used_tokens': int(used), 'token_budget': budget, 'percent': None if pct is None else round(pct, 1), 'status': status})
    code = 2 if any(o['status'] == 'stop' for o in out) else 1 if any(o['status'] == 'warn' for o in out) else 3 if any(o['status'] == 'uncalibrated' for o in out) else 0
    return out, code
def calibrate(settings, hourly, readings, now):
    cfg = guard_config(settings); g = settings.setdefault('usage_guard', {}); g.setdefault('windows', {})
    g.setdefault('stop_at_percent', cfg['stop_at_percent']); g.setdefault('warn_at_percent', cfg['warn_at_percent']); g.setdefault('cache_read_weight', cfg['cache_read_weight'])
    for name, pct in readings.items():
        if name not in cfg['windows']: raise ValueError(f'unknown window {name!r} (known: {", ".join(cfg["windows"])})')
        used = window_used(hourly, cfg['windows'][name]['hours'], now)
        if pct <= 0 or used <= 0: raise ValueError(f'cannot calibrate {name}: needs a usage percentage above 0 and some recorded usage in that window')
        g['windows'].setdefault(name, {'hours': cfg['windows'][name]['hours']})['hours'] = cfg['windows'][name]['hours']
        g['windows'][name]['token_budget'] = int(used / (pct / 100.0))
    return settings

def fmt(n): return f'{n:,}'
def table(title, rows, head):
    print('\n' + title)
    widths = [max(len(str(r[i])) for r in [head] + rows) for i in range(len(head))]
    for r in [head] + rows: print('  ' + '  '.join(str(c).ljust(widths[i]) if i < 2 else str(c).rjust(widths[i]) for i, c in enumerate(r)))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--logs'); ap.add_argument('--repo', default=REPO); ap.add_argument('--record', action='store_true'); ap.add_argument('--json', action='store_true')
    ap.add_argument('--cost', action='store_true', help='also show the API-equivalent dollar column')
    ap.add_argument('--check', action='store_true'); ap.add_argument('--calibrate', nargs='+', metavar='WINDOW=PERCENT')
    ap.add_argument('--out', default=os.path.join(REPO, 'usage', 'sessions.jsonl')); ap.add_argument('--prices'); ap.add_argument('--settings', default=SETTINGS)
    ap.add_argument('--now', type=float, help=argparse.SUPPRESS)
    a = ap.parse_args(argv)
    now = a.now or datetime.datetime.now(datetime.timezone.utc).timestamp()
    settings = load_settings(a.settings); cfg = guard_config(settings); w = cfg['cache_read_weight']
    logs = a.logs or default_log_dir(a.repo)
    prices = load_prices(a.prices); attr = Attributor(os.path.join(a.repo, 'games'))
    sessions = [read_session(f, attr) for f in sorted(glob.glob(os.path.join(logs, '*.jsonl')))] if logs and os.path.isdir(logs) else []
    recorded = list(iter_jsonl(a.out)) if os.path.exists(a.out) else []
    if not sessions and not recorded:
        print('No Claude Code session logs found for this project, and nothing recorded yet.\n'
              'Cloud sessions keep their logs inside the session; local sessions keep them in ~/.claude/projects/. '
              'Run this at the end of a session (python3 tools/usage/usage.py --record) or copy the folder and pass --logs.', file=sys.stderr)
        return 1
    sums = [summarise(s_, prices) for s_ in sessions]

    if a.calibrate or a.check:
        hourly = hourly_weighted(sums, recorded, {s_['session'] for s_ in sessions}, w)
        if a.calibrate:
            try: readings = {k: float(v) for k, v in (x.split('=', 1) for x in a.calibrate)}
            except ValueError: print('Use WINDOW=PERCENT, for example: --calibrate 5h=63 7d=41', file=sys.stderr); return 1
            try: settings = calibrate(settings, hourly, readings, now)
            except ValueError as e: print(str(e), file=sys.stderr); return 1
            if 'approval_mode' not in settings: settings['approval_mode'] = 'normal'
            with open(a.settings, 'w') as f: json.dump(settings, f, indent=2); f.write('\n')
            cfg = guard_config(settings)
            for n in readings: print(f"Calibrated {n}: {readings[n]:g}% of the window = {cfg['windows'][n]['token_budget']:,} usage tokens (saved in {os.path.basename(a.settings)}).")
        rows, code = check_guard(hourly, cfg, now)
        print('\nUsage guard (usage tokens = input + output + cache writes + %g x cache reads); stop at %g%%, warn at %g%%' % (w, cfg['stop_at_percent'], cfg['warn_at_percent']))
        for r in rows:
            pct = 'not calibrated' if r['percent'] is None else f"{r['percent']}% of {r['token_budget']:,}"
            print(f"  {r['name']:>3} window ({r['hours']}h): {r['used_tokens']:>12,} tokens  {pct:<28} {r['status'].upper()}")
        msg = {0: 'OK to run.', 1: 'WARNING: close to the limit. Run only what is needed and tell the owner.', 2: 'STOP: at or over the stop percentage. Do not start scheduled or batch work.',
               3: 'NOT CALIBRATED: read your plan usage % in the app (5-hour and weekly) and run: python3 tools/usage/usage.py --calibrate 5h=<percent> 7d=<percent>'}[code]
        print('  ' + msg)
        os.makedirs(os.path.join(REPO, 'usage'), exist_ok=True)
        with open(os.path.join(os.path.dirname(a.out), 'guard.json'), 'w') as f:
            json.dump({'checked_at': datetime.datetime.fromtimestamp(now, datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'status': {0: 'ok', 1: 'warn', 2: 'stop', 3: 'uncalibrated'}[code],
                       'stop_at_percent': cfg['stop_at_percent'], 'warn_at_percent': cfg['warn_at_percent'], 'windows': rows}, f, indent=2); f.write('\n')
        if a.record: record(a.out, [record_line(s_, m_) for s_, m_ in zip(sessions, sums)])
        return code

    if a.json:
        print(json.dumps([record_line(s_, m_) for s_, m_ in zip(sessions, sums)], indent=2)); return 0
    for s_, m_ in zip(sessions, sums):
        print(f"\n=== Session {s_['session'][:8]}  {str(s_['start'])[:16]} to {str(s_['end'])[:16]}")
        head = ['agent', 'model', 'usage tokens', 'input', 'output', 'cache read', 'cache write'] + (['cost'] if a.cost else [])
        rows = []
        for (agent, model), t in sorted(m_['by_agent_model'].items(), key=lambda kv: -weighted(kv[1], w)):
            c = cost_of(t, prices.get(model)); r = [agent, model.replace('claude-', ''), fmt(int(weighted(t, w))), fmt(t['input']), fmt(t['output']), fmt(t['cache_read']), fmt(t['cache_write'])]
            rows.append(r + ([ 'n/a' if c is None else f'${c:,.2f}'] if a.cost else []))
        table('Usage by agent and model (tokens; "usage tokens" weights cache reads at %g)' % w, rows, tuple(head))
        crow = [(k, fmt(int(weighted(v['tokens'], w)))) for k, v in sorted(m_['by_category'].items(), key=lambda kv: -weighted(kv[1]['tokens'], w))]
        total = sum(weighted(v['tokens'], w) for v in m_['by_category'].values()) or 1
        table('By game / area', [(k, n, f"{100 * weighted(m_['by_category'][k]['tokens'], w) / total:.0f}%") for k, n in crow], ('area', 'usage tokens', 'share'))
        if a.cost:
            est, rep = m_['estimated_cost_usd'], m_['reported_cost_usd']
            print(f"\n  API-equivalent: estimated from message logs ${est:,.2f}; Claude Code reported total " + ('n/a' if rep is None else f'${rep:,.2f}') + f"; web searches {s_['web_searches']}")
        if m_['unpriced_models'] and a.cost: print('  Models with no price (cost shown as n/a): ' + ', '.join(m_['unpriced_models']))
    if a.record:
        record(a.out, [record_line(s_, m_) for s_, m_ in zip(sessions, sums)]); print(f'\nRecorded {len(sessions)} session(s) in {os.path.relpath(a.out, a.repo)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
