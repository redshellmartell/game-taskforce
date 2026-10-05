#!/usr/bin/env python3
"""Switch, checkpoint and resume logic for the taskforce runner (task 014, stage 1). Standard library only.

Files (under <base>/studio/):
  taskforce.json   the switch: {"active": bool, "pause_mode": "after-step"|"now", "updated", "by"}
  run-state.json   the checkpoint: status, game, stage, step, agent, started, heartbeat, last_done, reason, queue
  STOP             an empty file; if it exists the runner stops at the next check (kill switch)

Everything is written atomically (temp file, then rename), so a crash or a sleep never leaves a half-written file.
The runner itself is built in a later stage; this module is the part that decides whether to run, stop or redo.
"""
import json, os, datetime, tempfile

STALE_SECONDS = 120          # a heartbeat older than this means the runner was interrupted (e.g. the Mac slept)
SLEEP_GAP_SECONDS = 120      # a gap this long between loop checks means the machine slept


def now_iso(now=None):
    return (now or datetime.datetime.now(datetime.timezone.utc)).strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_iso(s):
    return datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc)


def _path(base, name):
    return os.path.join(base, 'studio', name)


def _read(path, default):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def _write_atomic(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix='.tmp')
    with os.fdopen(fd, 'w') as f:
        json.dump(data, f, indent=2)
    os.replace(tmp, path)


# ---- the switch ----
def read_switch(base):
    s = _read(_path(base, 'taskforce.json'), {})
    return {'active': bool(s.get('active', False)), 'pause_mode': s.get('pause_mode', 'after-step'),
            'updated': s.get('updated'), 'by': s.get('by')}


def write_switch(base, active, pause_mode='after-step', by='dashboard', now=None):
    if pause_mode not in ('after-step', 'now'):
        raise ValueError('pause_mode must be after-step or now')
    _write_atomic(_path(base, 'taskforce.json'),
                  {'active': bool(active), 'pause_mode': pause_mode, 'updated': now_iso(now), 'by': by})


# ---- the checkpoint ----
EMPTY_STATE = {'status': 'stopped', 'game': None, 'stage': None, 'step': None, 'agent': None, 'started': None,
               'heartbeat': None, 'last_done': None, 'reason': None, 'queue': []}


def read_state(base):
    s = dict(EMPTY_STATE)
    s.update(_read(_path(base, 'run-state.json'), {}))
    return s


def write_state(base, **changes):
    s = read_state(base)
    s.update(changes)
    _write_atomic(_path(base, 'run-state.json'), s)
    return s


def heartbeat(base, now=None):
    return write_state(base, heartbeat=now_iso(now))


def begin_step(base, game, stage, step, agent, now=None):
    return write_state(base, status='running', game=game, stage=stage, step=step, agent=agent,
                       started=now_iso(now), heartbeat=now_iso(now), reason=None)


def finish_step(base, done_id, now=None):
    return write_state(base, status='running', agent=None, step=None, last_done=done_id, heartbeat=now_iso(now))


def stop(base, status, reason, now=None):
    """status: paused | stopped | waiting-gate | usage-stop | error"""
    return write_state(base, status=status, reason=reason, heartbeat=now_iso(now))


# ---- decisions ----
def stop_reason(base, guard_exit=0):
    """Why the runner must not start another step, or None. guard_exit is the exit code of usage.py --check."""
    if os.path.exists(_path(base, 'STOP')):
        return ('stopped', 'STOP file present')
    if not read_switch(base)['active']:
        return ('paused', 'switch is off')
    if guard_exit == 2:
        return ('usage-stop', 'usage guard says stop')
    return None


def is_stale(state, now=None):
    if state.get('status') != 'running' or not state.get('heartbeat'):
        return False
    age = ((now or datetime.datetime.now(datetime.timezone.utc)) - parse_iso(state['heartbeat'])).total_seconds()
    return age > STALE_SECONDS


def slept(last_check, now=None):
    """True if the gap since the last loop check suggests the machine slept."""
    return ((now or datetime.datetime.now(datetime.timezone.utc)) - last_check).total_seconds() > SLEEP_GAP_SECONDS


def resume_action(state, now=None):
    """What to do when the switch is turned on.
    'fresh'      nothing was in flight: pick the next piece of work
    'redo-step'  a step was in flight and the runner was interrupted (stale heartbeat, or stopped mid-step): redo it
    'continue'   the runner is alive and running (do nothing)"""
    if state.get('status') == 'running' and state.get('step'):
        return 'redo-step' if is_stale(state, now) else 'continue'
    if state.get('step') and state.get('status') in ('error', 'stopped'):
        return 'redo-step'
    return 'fresh'


def display_status(state, now=None):
    """What the dashboard should show: running, paused, stopped, waiting-gate, usage-stop, error or interrupted."""
    if is_stale(state, now):
        return 'interrupted'
    return state.get('status') or 'stopped'
