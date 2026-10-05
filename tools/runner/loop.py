#!/usr/bin/env python3
"""The runner's loop logic, with the agent call left as a plug-in (task 014, stage 1: paper-run version).

run_steps() is what the real runner (stage 3) will do around each agent call. It is tested with a fake executor, so a stop,
a pause and a resume can be proven without any agent running.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state as st


class Interrupted(Exception):
    """Raised by an executor to simulate the machine sleeping or the runner being killed mid-step."""


def run_steps(base, steps, executor, guard=lambda: 0, done=None, now=None):
    """steps: list of (game, stage, step, agent). executor(game, stage, step, agent) does the work (must be safe to repeat).
    done: set of step ids already finished (the real runner reads this from the activity log). Returns the done set.
    Stops cleanly when the switch is off, STOP exists or the guard says stop, between steps ('after-step' pause)."""
    done = set(done or [])
    action = st.resume_action(st.read_state(base), now)
    for game, stage, step, agent in steps:
        sid = '%s/%s/%s' % (game, stage, step)
        if sid in done:
            continue
        why = st.stop_reason(base, guard())
        if why:
            st.stop(base, why[0], why[1], now)
            return done
        st.begin_step(base, game, stage, step, agent, now)
        try:
            executor(game, stage, step, agent)
        except Interrupted:
            # nothing is recorded as done; the checkpoint still says 'running' with this step, so a resume redoes it
            raise
        done.add(sid)
        st.finish_step(base, sid, now)
    st.stop(base, 'stopped', 'queue empty', now)
    return done
