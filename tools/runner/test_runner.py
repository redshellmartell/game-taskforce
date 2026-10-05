import json, os, sys, tempfile, unittest, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import state as st, loop, digest

T0 = datetime.datetime(2026, 10, 5, 12, 0, 0, tzinfo=datetime.timezone.utc)
STEPS = [('g1', 'design', 'revise', 'game-designer'), ('g1', 'playtest', 'simulate', 'playtester'),
         ('g1', 'critique', 'review', 'critic'), ('g2', 'design', 'write', 'game-designer')]


class Switch(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()

    def test_default_off_and_roundtrip(self):
        self.assertFalse(st.read_switch(self.d)['active'])
        st.write_switch(self.d, True, 'now', now=T0)
        s = st.read_switch(self.d)
        self.assertTrue(s['active'])
        self.assertEqual(s['pause_mode'], 'now')
        with self.assertRaises(ValueError):
            st.write_switch(self.d, True, 'whenever')

    def test_stop_reasons(self):
        self.assertEqual(st.stop_reason(self.d)[0], 'paused')
        st.write_switch(self.d, True)
        self.assertIsNone(st.stop_reason(self.d))
        self.assertEqual(st.stop_reason(self.d, guard_exit=2)[0], 'usage-stop')
        open(os.path.join(self.d, 'studio', 'STOP'), 'w').close()
        self.assertEqual(st.stop_reason(self.d)[0], 'stopped')


class Heartbeat(unittest.TestCase):
    def test_stale_and_display(self):
        d = tempfile.mkdtemp()
        s = st.begin_step(d, 'g1', 'design', 'revise', 'game-designer', T0)
        self.assertFalse(st.is_stale(s, T0 + datetime.timedelta(seconds=60)))
        later = T0 + datetime.timedelta(minutes=10)
        self.assertTrue(st.is_stale(s, later))
        self.assertEqual(st.display_status(s, later), 'interrupted')
        self.assertEqual(st.display_status(s, T0), 'running')

    def test_resume_action(self):
        d = tempfile.mkdtemp()
        self.assertEqual(st.resume_action(st.read_state(d)), 'fresh')
        s = st.begin_step(d, 'g1', 'design', 'revise', 'game-designer', T0)
        self.assertEqual(st.resume_action(s, T0 + datetime.timedelta(seconds=30)), 'continue')
        self.assertEqual(st.resume_action(s, T0 + datetime.timedelta(minutes=10)), 'redo-step')
        s = st.stop(d, 'error', 'network', T0)
        self.assertEqual(st.resume_action(s), 'redo-step')

    def test_sleep_gap(self):
        self.assertFalse(st.slept(T0, T0 + datetime.timedelta(seconds=30)))
        self.assertTrue(st.slept(T0, T0 + datetime.timedelta(minutes=5)))

    def test_atomic_write_leaves_no_temp_files(self):
        d = tempfile.mkdtemp()
        st.write_state(d, status='paused')
        self.assertEqual([f for f in os.listdir(os.path.join(d, 'studio')) if f.endswith('.tmp')], [])


class PaperRun(unittest.TestCase):
    """A stop and resume (including a simulated sleep) ends in the same state as an uninterrupted run."""

    def make(self):
        d = tempfile.mkdtemp()
        st.write_switch(d, True, now=T0)
        out = os.path.join(d, 'out.txt')
        return d, out

    def executor(self, out, interrupt_on=None):
        calls = {'n': 0}

        def run(game, stage, step, agent):
            calls['n'] += 1
            if interrupt_on and (game, stage) == interrupt_on and calls['n'] == 2:
                with open(out, 'a') as f:      # a half-written result, as after a sleep
                    f.write('PARTIAL %s %s\n' % (game, stage))
                raise loop.Interrupted()
            with open(out, 'a') as f:
                f.write('%s %s\n' % (game, stage))
        return run

    def clean_lines(self, out):
        return [l for l in open(out).read().splitlines() if not l.startswith('PARTIAL')]

    def test_uninterrupted(self):
        d, out = self.make()
        done = loop.run_steps(d, STEPS, self.executor(out), now=T0)
        self.assertEqual(len(done), 4)
        self.assertEqual(st.read_state(d)['status'], 'stopped')

    def test_sleep_mid_step_then_resume_matches_uninterrupted(self):
        d1, out1 = self.make()
        loop.run_steps(d1, STEPS, self.executor(out1), now=T0)
        d2, out2 = self.make()
        done = set()
        with self.assertRaises(loop.Interrupted):
            loop.run_steps(d2, STEPS, self.executor(out2, interrupt_on=('g1', 'playtest')), now=T0)
        s = st.read_state(d2)
        self.assertEqual((s['status'], s['step']), ('running', 'simulate'))     # checkpoint says it was mid-step
        later = T0 + datetime.timedelta(minutes=30)
        self.assertEqual(st.display_status(s, later), 'interrupted')
        self.assertEqual(st.resume_action(s, later), 'redo-step')
        done = {'g1/design/revise'}                                              # what the activity log recorded
        final = loop.run_steps(d2, STEPS, self.executor(out2), done=done, now=later)
        self.assertEqual(len(final), 4)
        self.assertEqual(self.clean_lines(out1), self.clean_lines(out2))        # same work, same order
        self.assertEqual(st.read_state(d2)['last_done'], st.read_state(d1)['last_done'])

    def test_switch_off_pauses_after_the_running_step(self):
        d, out = self.make()
        base_exec = self.executor(out)

        def exec_then_off(game, stage, step, agent):
            base_exec(game, stage, step, agent)
            if (game, stage) == ('g1', 'design'):
                st.write_switch(d, False, now=T0)          # owner switches off while this step runs
        done = loop.run_steps(d, STEPS, exec_then_off, now=T0)
        self.assertEqual(done, {'g1/design/revise'})        # the running step finished, the next did not start
        self.assertEqual(st.read_state(d)['status'], 'paused')
        st.write_switch(d, True, now=T0)
        final = loop.run_steps(d, STEPS, base_exec, done=done, now=T0)
        self.assertEqual(len(final), 4)
        self.assertEqual(self.clean_lines(out), ['g1 design', 'g1 playtest', 'g1 critique', 'g2 design'])

    def test_usage_guard_stops_before_the_next_step(self):
        d, out = self.make()
        done = loop.run_steps(d, STEPS, self.executor(out), guard=lambda: 2, now=T0)
        self.assertEqual(done, set())
        self.assertEqual(st.read_state(d)['status'], 'usage-stop')


class Digest(unittest.TestCase):
    def test_digest_lists_pitches_requests_and_status(self):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, 'games', 'g1'))
        json.dump({'games': [{'slug': 'g1', 'title': 'Game One', 'stage': 'owner-review', 'revision': 2},
                             {'slug': 'g2', 'title': 'Game Two', 'stage': 'critique', 'revision': 0}]},
                  open(os.path.join(d, 'games', 'status.json'), 'w'))
        json.dump({'requests': [{'id': 'g2-revision-1', 'gate': 'revision', 'game': 'g2', 'status': 'pending',
                                 'summary': 'Playtest NEEDS-FIXES'}]}, open(os.path.join(d, 'games', 'approvals.json'), 'w'))
        with open(os.path.join(d, 'games', 'g1', 'activity.jsonl'), 'w') as f:
            f.write(json.dumps({'time': '2026-10-05T10:00:00Z', 'agent': 'critic', 'game': 'g1', 'message': 'done'}) + '\n')
        st.write_switch(d, True, now=T0)
        text = digest.build(d)
        for needle in ('Switch:** ON', 'Pitch ready: Game One', 'g2-revision-1', 'critique:', 'critic g1: done'):
            self.assertIn(needle, text)

    def test_digest_on_empty_folder(self):
        self.assertIn('Nothing waiting', digest.build(tempfile.mkdtemp()))


if __name__ == '__main__':
    unittest.main()
