"""Studio scoreboard: is the first-pass failure rate falling? Free, reads files only.
Run: python3 tools/learning/scoreboard.py [--root DIR]   Writes studio/scoreboard.json and studio/scoreboard.md."""
import argparse, glob, json, os, re
from datetime import datetime, timezone


def load(path, default=None):
    try:
        with open(path) as f: return json.load(f)
    except (OSError, ValueError): return default


def load_jsonl(path):
    out = []
    try:
        with open(path) as f:
            for line in f:
                try: out.append(json.loads(line))
                except ValueError: pass
    except OSError: pass
    return out


def mean(xs): return round(sum(xs) / len(xs), 2) if xs else None


def first_pass(game):
    """First playtest verdict from the history: a verdict on a playtest/critique line, or 'playtest PASS|NEEDS-FIXES' in a note."""
    for h in game.get('history', []):
        if h.get('stage') not in ('playtest', 'critique'): continue
        v = h.get('verdict')
        if v in ('PASS', 'NEEDS-FIXES', 'FAIL'): return v
        m = re.search(r'playtest\s+(PASS|NEEDS-FIXES|FAIL)', h.get('note') or '', re.I)
        if m: return m.group(1).upper()
    return None


def first_critic_avg(game):
    for h in game.get('history', []):
        if h.get('stage') != 'critique': continue
        m = re.search(r'(?:avg|average)\s*(\d(?:\.\d+)?)', h.get('note') or '', re.I)
        if m: return float(m.group(1))
    return None


def usage_by_game(root, games):
    """Weighted tokens per game. A session counts for a game only when its window holds activity lines for exactly one game."""
    acts = []
    for slug in games:
        for a in load_jsonl(os.path.join(root, 'games', slug, 'activity.jsonl')):
            if a.get('time'): acts.append((a['time'], slug))
    totals, shared = {}, 0
    for s in load_jsonl(os.path.join(root, 'usage', 'sessions.jsonl')):
        tok = sum(a.get('weighted_tokens', 0) for a in s.get('by_agent', []))
        slugs = {g for t, g in acts if s.get('start', '') <= t <= s.get('end', '')}
        if len(slugs) == 1:
            g = slugs.pop(); totals[g] = totals.get(g, 0) + tok
        else: shared += tok
    return {'per_game': totals, 'unattributed': shared}


def build(root):
    st = load(os.path.join(root, 'games', 'status.json'), {'games': []})['games']
    appr = load(os.path.join(root, 'games', 'approvals.json'), {'requests': []})['requests']
    dec = load(os.path.join(root, 'games', 'decisions.json'), {'decisions': []})['decisions']
    games = []
    for g in st:
        d = os.path.join(root, 'games', g['slug'])
        crit = load(os.path.join(d, 'critique.json'), {})
        cycles = load(os.path.join(d, 'cycles.json'), {}).get('cycles', [])
        games.append({'slug': g['slug'], 'stage': g.get('stage'), 'revisions': g.get('revision', 0),
                      'first_playtest': first_pass(g), 'first_critic_avg': first_critic_avg(g),
                      'latest_critic_avg': crit.get('average'), 'latest_critic': crit.get('verdict'), 'cycles': cycles})
    tested = [g for g in games if g['first_playtest']]
    passed = [g for g in tested if g['first_playtest'] == 'PASS']
    decided = [r for r in appr if r.get('status') in ('approved', 'declined') and r.get('recommendation')]
    agree = [r for r in decided if r.get('decision') == r.get('recommendation')]
    by_gate = {}
    for r in appr:
        k = by_gate.setdefault(r.get('gate', '?'), {})
        k[r.get('status', '?')] = k.get(r.get('status', '?'), 0) + 1
    by_kind = {}
    for x in dec:
        k = x.get('kind') or 'gate'
        by_kind.setdefault(k, {})[x.get('decision')] = by_kind.get(k, {}).get(x.get('decision'), 0) + 1
    all_cycles = [c for g in games for c in g['cycles'] if c.get('moved') is not None]
    human = [s for g in games for s in load(os.path.join(root, 'games', g['slug'], 'human-playtests.json'), {}).get('sessions', [])]
    return {
        'generated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'games_total': len(games), 'games_tested': len(tested),
        'first_pass_playtest_pass': len(passed), 'first_pass_rate': round(len(passed) / len(tested), 2) if tested else None,
        'critic_avg_first': mean([g['first_critic_avg'] for g in games if g['first_critic_avg'] is not None]),
        'critic_avg_latest': mean([g['latest_critic_avg'] for g in games if g['latest_critic_avg'] is not None]),
        'revisions_per_game': mean([g['revisions'] for g in tested]),
        'director_calibration': {'decided': len(decided), 'agreed': len(agree), 'rate': round(len(agree) / len(decided), 2) if decided else None},
        'approvals_by_gate': by_gate, 'decisions_by_kind': by_kind,
        'revision_effectiveness': {'cycles': len(all_cycles), 'moved_target': sum(1 for c in all_cycles if c['moved']),
                                   'rate': round(sum(1 for c in all_cycles if c['moved']) / len(all_cycles), 2) if all_cycles else None},
        'human': {'sessions': len(human), 'fun': mean([s['fun'] for s in human if 'fun' in s]),
                  'replay': mean([s['replay'] for s in human if 'replay' in s]), 'clarity': mean([s['clarity'] for s in human if 'clarity' in s])},
        'usage_tokens': usage_by_game(root, [g['slug'] for g in games]),
        'games': games}


def render(s):
    def pct(a, b): return f'{a} of {b}'
    h = s['human']
    L = ['# Studio scoreboard', '', f"_Generated {s['generated']} by `tools/learning/scoreboard.py`. Bots are unvalidated until human playtests exist._", '',
         f"**First-pass playtest PASS: {pct(s['first_pass_playtest_pass'], s['games_tested'])}** (target: at least 2 of the next 6 games).", '',
         '| Metric | Value |', '|---|---|',
         f"| Critic average, first critique / latest | {s['critic_avg_first']} / {s['critic_avg_latest']} |",
         f"| Revisions per tested game | {s['revisions_per_game']} |",
         f"| Director recommendation matched owner | {pct(s['director_calibration']['agreed'], s['director_calibration']['decided'])} |",
         f"| Revision effectiveness (cycles that moved their target) | {pct(s['revision_effectiveness']['moved_target'], s['revision_effectiveness']['cycles']) if s['revision_effectiveness']['cycles'] else 'no data'} |",
         f"| Human fun / replay / clarity | " + (f"{h['fun']} / {h['replay']} / {h['clarity']} ({h['sessions']} sessions)" if h['sessions'] else 'no data') + ' |',
         f"| Tokens not attributable to one game | {s['usage_tokens']['unattributed']:,} |", '',
         '## Per game', '', '| Game | Stage | First playtest | Critic first / latest | Revisions | Tokens |', '|---|---|---|---|---|---|']
    for g in s['games']:
        t = s['usage_tokens']['per_game'].get(g['slug'])
        L.append(f"| {g['slug']} | {g['stage']} | {g['first_playtest'] or '-'} | {g['first_critic_avg'] or '-'} / {g['latest_critic_avg'] or '-'} | {g['revisions']} | {f'{t:,}' if t else '-'} |")
    L += ['', '## Owner decisions', '', 'By gate (status counts): ' + '; '.join(f'{k} {v}' for k, v in sorted(s['approvals_by_gate'].items())),
          '', 'In `decisions.json` by kind: ' + '; '.join(f'{k} {v}' for k, v in sorted(s['decisions_by_kind'].items())), '']
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--root', default=os.path.join(os.path.dirname(__file__), '..', '..'))
    root = os.path.abspath(ap.parse_args().root)
    s = build(root); os.makedirs(os.path.join(root, 'studio'), exist_ok=True)
    with open(os.path.join(root, 'studio', 'scoreboard.json'), 'w') as f: json.dump(s, f, indent=1)
    with open(os.path.join(root, 'studio', 'scoreboard.md'), 'w') as f: f.write(render(s))
    print(f"First-pass playtest PASS: {s['first_pass_playtest_pass']} of {s['games_tested']}; critic avg first {s['critic_avg_first']}, latest {s['critic_avg_latest']}; "
          f"Director matched owner {s['director_calibration']['agreed']}/{s['director_calibration']['decided']}")


if __name__ == '__main__': main()
