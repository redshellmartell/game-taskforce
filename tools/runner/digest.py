#!/usr/bin/env python3
"""One-page digest of the studio's state, from the existing files (task 014, stage 1). Standard library only.

  python3 tools/runner/digest.py              # print the digest for this repository
  python3 tools/runner/digest.py --base DIR   # use another folder (for tests or sample data)
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import state as st

REPO = os.path.abspath(os.path.join(HERE, '..', '..'))


def _load(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _activity(base, limit=8):
    rows = []
    gdir = os.path.join(base, 'games')
    if os.path.isdir(gdir):
        for slug in os.listdir(gdir):
            p = os.path.join(gdir, slug, 'activity.jsonl')
            if os.path.isfile(p):
                with open(p) as f:
                    for line in f:
                        try:
                            rows.append(json.loads(line))
                        except ValueError:
                            pass
    rows.sort(key=lambda r: r.get('time', ''))
    return rows[-limit:]


def build(base):
    games = _load(os.path.join(base, 'games', 'status.json'), {}).get('games', [])
    reqs = _load(os.path.join(base, 'games', 'approvals.json'), {}).get('requests', [])
    run = st.read_state(base)
    sw = st.read_switch(base)
    pending = [r for r in reqs if r.get('status') == 'pending']
    pitches = [g for g in games if g.get('stage') == 'owner-review']
    by_stage = {}
    for g in games:
        by_stage.setdefault(g.get('stage', '?'), []).append(g)
    out = ['# Taskforce digest', '']
    out.append('**Switch:** %s  |  **Runner:** %s' % ('ON' if sw['active'] else 'OFF', st.display_status(run)))
    if run.get('game'):
        out.append('Current: %s, %s, %s%s' % (run['game'], run.get('stage'), run.get('step'),
                                              ' (agent %s)' % run['agent'] if run.get('agent') else ''))
    if run.get('reason'):
        out.append('Last stop reason: %s' % run['reason'])
    out += ['', '## Needs you', '']
    if not pending and not pitches:
        out.append('- Nothing waiting.')
    for g in pitches:
        out.append('- Pitch ready: %s' % g.get('title', g['slug']))
    for r in pending:
        out.append('- %s (%s, %s): %s' % (r['id'], r.get('gate'), r.get('game') or '-', (r.get('summary') or '')[:100]))
    out += ['', '## Games', '']
    for stage in sorted(by_stage):
        names = ', '.join('%s (rev %s)' % (g.get('title', g['slug']), g.get('revision', 0)) for g in by_stage[stage])
        out.append('- **%s:** %s' % (stage, names))
    out += ['', '## Latest activity', '']
    acts = _activity(base)
    out += ['- %s %s %s: %s' % (a.get('time', '')[:16], a.get('agent', ''), a.get('game', ''), (a.get('message') or '')[:80])
            for a in acts] or ['- None.']
    return '\n'.join(out) + '\n'


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', default=REPO)
    print(build(ap.parse_args().base))
