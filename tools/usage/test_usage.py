"""Tests for the usage meter, using small synthetic logs (no real session data). Run: python3 -m unittest discover tools/usage"""
import json, os, tempfile, unittest
import usage


def line(**kw): return json.dumps(kw) + '\n'


def assistant(mid, ts, model, inp, out, cr, cw, tool_input=None):
    content = [{'type': 'tool_use', 'name': 'Write', 'input': tool_input}] if tool_input else [{'type': 'text', 'text': 'hello'}]
    return line(type='assistant', timestamp=ts, uuid='u' + mid, message={'id': mid, 'model': model, 'content': content,
                'usage': {'input_tokens': inp, 'output_tokens': out, 'cache_read_input_tokens': cr, 'cache_creation_input_tokens': cw}})


PRICES = {'m1': {'input': 2.0, 'output': 10.0, 'cache_read': 0.2, 'cache_write': 2.5}, 'm2': {'input': None, 'output': None}}


class UsageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.games = os.path.join(self.tmp, 'games'); os.makedirs(os.path.join(self.games, 'foo')); os.makedirs(os.path.join(self.games, '_inbox'))
        with open(os.path.join(self.games, 'foo', 'activity.jsonl'), 'w') as f:
            f.write(line(time='2026-10-03T10:00:00Z', agent='critic', game='foo', event='start', message='x'))
            f.write(line(time='2026-10-03T11:00:00Z', agent='critic', game='foo', event='done', message='y'))
        self.logs = os.path.join(self.tmp, 'logs'); os.makedirs(os.path.join(self.logs, 's1', 'subagents'))
        with open(os.path.join(self.logs, 's1.jsonl'), 'w') as f:
            f.write(assistant('a', '2026-10-03T10:05:00Z', 'm1', 1000, 500, 100000, 20000, {'file_path': 'games/foo/rules.md'}))
            f.write(assistant('a', '2026-10-03T10:05:00Z', 'm1', 1000, 500, 100000, 20000))          # same message id repeated on a second line: counted once
            f.write(assistant('b', '2026-10-03T10:06:00Z', 'm1', 10, 10, 0, 0))                          # no path: keeps the previous answer ('foo')
            f.write(assistant('c', '2026-10-03T13:00:00Z', 'm1', 10, 10, 0, 0, {'file_path': 'dashboard/src/App.jsx'}))
            f.write(assistant('d', '2026-10-04T09:00:00Z', 'm2', 5, 5, 0, 0, {'command': 'ls games/_inbox'}))   # unknown model, _inbox is not a game
            f.write(line(type='cost-state', timestamp='2026-10-04T09:01:00Z', totalCostUSD=1.5, modelUsage={'m1': {'webSearchRequests': 3}}))
        with open(os.path.join(self.logs, 's1', 'subagents', 'agent-x.jsonl'), 'w') as f:
            f.write(assistant('e', '2026-10-03T10:30:00Z', 'm1', 100, 100, 0, 0))                         # no path: falls back to foo's activity window
        with open(os.path.join(self.logs, 's1', 'subagents', 'agent-x.meta.json'), 'w') as f: json.dump({'agentType': 'critic'}, f)
        attr = usage.Attributor(self.games)
        self.sess = usage.read_session(os.path.join(self.logs, 's1.jsonl'), attr)
        self.summ = usage.summarise(self.sess, PRICES)

    def test_messages_counted_once_and_agents_named(self):
        a = self.summ['by_agent']
        self.assertEqual(a['director']['tokens']['input'], 1000 + 10 + 10 + 5)
        self.assertEqual(a['critic']['tokens']['output'], 100)

    def test_cost_math(self):
        # director on m1: input 1020*2 + output 520*10 + cache_read 100000*0.2 + cache_write 20000*2.5, per million
        expected = (1020 * 2 + 520 * 10 + 100000 * 0.2 + 20000 * 2.5) / 1e6
        self.assertAlmostEqual(self.summ['by_agent']['director']['cost_usd'], expected, places=9)

    def test_unknown_model_is_flagged_not_charged(self):
        self.assertEqual(self.summ['unpriced_models'], ['m2'])

    def test_attribution(self):
        c = self.summ['by_category']
        self.assertIn('foo', c); self.assertIn('dashboard', c)
        self.assertNotIn('_inbox', c)                              # 'games/_inbox' is not a game, so message d keeps the previous answer
        self.assertEqual(c['dashboard']['tokens']['input'], 10 + 5)
        self.assertEqual(c['foo']['tokens']['input'], 1000 + 10 + 100)   # a, b (sticky) and the sub-agent (time window)

    def test_by_day_and_reported_cost(self):
        self.assertEqual(sorted(self.summ['by_day']), ['2026-10-03', '2026-10-04'])
        self.assertEqual(self.summ['reported_cost_usd'], 1.5); self.assertEqual(self.sess['web_searches'], 3)

    def test_record_replaces_the_same_session(self):
        out = os.path.join(self.tmp, 'usage', 'sessions.jsonl')
        usage.record(out, [usage.record_line(self.sess, self.summ)]); usage.record(out, [usage.record_line(self.sess, self.summ)])
        rows = [json.loads(l) for l in open(out)]
        self.assertEqual(len(rows), 1); self.assertEqual(rows[0]['session'], 's1')
        self.assertNotIn('hello', open(out).read())                # no content is stored, only counts and names

    def test_default_log_dir_missing_is_none_and_main_reports_it(self):
        self.assertEqual(usage.main(['--logs', os.path.join(self.tmp, 'nope'), '--out', os.path.join(self.tmp, 'none.jsonl'), '--settings', os.path.join(self.tmp, 's.json')]), 1)


class GuardTests(unittest.TestCase):
    NOW = 1791036000.0      # 2026-10-03T14:00:00Z
    def hourly(self): return {'2026-10-03T13': 1000.0, '2026-10-03T09': 500.0, '2026-09-30T10': 4000.0}

    def test_windows_only_count_their_own_hours(self):
        self.assertEqual(usage.window_used(self.hourly(), 5, self.NOW), 1500.0)       # 09:00 is inside the last 5 hours (incl. the overlapping bucket)
        self.assertEqual(usage.window_used(self.hourly(), 168, self.NOW), 5500.0)

    def test_status_thresholds_and_exit_codes(self):
        cfg = usage.guard_config({'usage_guard': {'windows': {'5h': {'token_budget': 2000}, '7d': {'token_budget': 100000}}}})
        rows, code = usage.check_guard(self.hourly(), cfg, self.NOW)
        self.assertEqual([r['status'] for r in rows], ['warn', 'ok']); self.assertEqual(code, 1)      # 1500/2000 = 75% (warn at 60, stop at 80)
        cfg['windows']['5h']['token_budget'] = 1800
        self.assertEqual(usage.check_guard(self.hourly(), cfg, self.NOW)[1], 2)                       # 83% -> STOP
        cfg['windows']['5h']['token_budget'] = 100000
        self.assertEqual(usage.check_guard(self.hourly(), cfg, self.NOW)[1], 0)

    def test_uncalibrated_is_reported_not_guessed(self):
        rows, code = usage.check_guard(self.hourly(), usage.guard_config({}), self.NOW)
        self.assertEqual(code, 3); self.assertTrue(all(r['percent'] is None for r in rows))

    def test_calibration_turns_a_reading_into_a_budget(self):
        settings = usage.calibrate({'approval_mode': 'relaxed'}, self.hourly(), {'5h': 50.0}, self.NOW)
        self.assertEqual(settings['usage_guard']['windows']['5h']['token_budget'], 3000)               # 1500 tokens used = 50% -> 100% is 3000
        self.assertEqual(settings['approval_mode'], 'relaxed')                                         # other settings are kept
        with self.assertRaises(ValueError): usage.calibrate({}, {}, {'5h': 50.0}, self.NOW)             # nothing used: cannot calibrate
        with self.assertRaises(ValueError): usage.calibrate({}, self.hourly(), {'1h': 50.0}, self.NOW)  # unknown window

    def test_recorded_sessions_are_not_double_counted_with_live_ones(self):
        rec = [{'session': 'old', 'by_hour': [{'name': '2026-10-03T12', 'input': 10, 'output': 10, 'cache_read': 0, 'cache_write': 0}]},
               {'session': 'live', 'by_hour': [{'name': '2026-10-03T12', 'input': 999, 'output': 0, 'cache_read': 0, 'cache_write': 0}]}]
        h = usage.hourly_weighted([], rec, {'live'}, 0.1)
        self.assertEqual(h['2026-10-03T12'], 20)


if __name__ == '__main__':
    unittest.main()
