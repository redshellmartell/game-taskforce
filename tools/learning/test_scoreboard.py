"""Tests for the scoreboard with small synthetic files. Run: python3 -m unittest discover tools/learning"""
import json, os, tempfile, unittest
import scoreboard


def w(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w') as f: f.write(o if isinstance(o, str) else json.dumps(o))


class T(unittest.TestCase):
    def setUp(self):
        self.r = tempfile.mkdtemp(); g = os.path.join(self.r, 'games')
        w(g + '/status.json', {'games': [
            {'slug': 'a', 'stage': 'critique', 'revision': 2, 'history': [
                {'stage': 'playtest', 'verdict': 'NEEDS-FIXES', 'note': 'x'}, {'stage': 'critique', 'verdict': 'REVISE', 'note': 'critic avg 3.0'}]},
            {'slug': 'b', 'stage': 'critique', 'revision': 0, 'history': [
                {'stage': 'critique', 'verdict': None, 'note': 'Playtest PASS; ok'}, {'stage': 'critique', 'verdict': 'PASS', 'note': 'Average 3.8/5'}]},
            {'slug': 'c', 'stage': 'brief', 'revision': 0, 'history': [{'stage': 'brief', 'verdict': None, 'note': ''}]}]})
        w(g + '/a/critique.json', {'average': 3.5, 'verdict': 'REVISE-MINOR'})
        w(g + '/a/cycles.json', {'cycles': [{'cycle': 1, 'moved': True}, {'cycle': 2, 'moved': False}]})
        w(g + '/approvals.json', {'requests': [
            {'id': 'x', 'gate': 'revision', 'status': 'approved', 'recommendation': 'approve', 'decision': 'approve'},
            {'id': 'y', 'gate': 'revision', 'status': 'approved', 'recommendation': 'alternative', 'decision': 'approve'},
            {'id': 'z', 'gate': 'revision', 'status': 'pending', 'recommendation': 'approve'}]})
        w(g + '/decisions.json', {'decisions': [{'kind': 'pitch', 'decision': 'approve'}, {'decision': 'approve'}]})

    def test_metrics(self):
        s = scoreboard.build(self.r)
        self.assertEqual((s['games_tested'], s['first_pass_playtest_pass'], s['first_pass_rate']), (2, 1, 0.5))
        self.assertEqual((s['critic_avg_first'], s['critic_avg_latest']), (3.4, 3.5))
        self.assertEqual(s['director_calibration'], {'decided': 2, 'agreed': 1, 'rate': 0.5})
        self.assertEqual(s['revision_effectiveness']['rate'], 0.5)
        self.assertEqual(s['decisions_by_kind'], {'pitch': {'approve': 1}, 'gate': {'approve': 1}})
        self.assertEqual(s['human']['sessions'], 0)

    def test_empty_and_render(self):
        s = scoreboard.build(tempfile.mkdtemp())
        self.assertIsNone(s['first_pass_rate']); self.assertIn('no data', scoreboard.render(s))

    def test_usage_attribution(self):
        w(self.r + '/games/a/activity.jsonl', '{"time":"2026-10-03T10:30:00Z"}\n')
        w(self.r + '/usage/sessions.jsonl', json.dumps({'start': '2026-10-03T10:00:00Z', 'end': '2026-10-03T11:00:00Z', 'by_agent': [{'weighted_tokens': 100}]}) + '\n')
        self.assertEqual(scoreboard.build(self.r)['usage_tokens']['per_game'], {'a': 100})


if __name__ == '__main__': unittest.main()
