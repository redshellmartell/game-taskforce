import datetime, json, os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fix_future_times as F

NOW = datetime.datetime(2026, 10, 4, 13, 13, 0, tzinfo=datetime.timezone.utc)

class T(unittest.TestCase):
    def test_future_lines_get_now_and_a_flag_past_lines_are_untouched(self):
        lines = [json.dumps({"time": "2026-10-04T12:00:00Z", "message": "past"}) + "\n", json.dumps({"time": "2026-10-04T13:25:00Z", "message": "future"}) + "\n", "not json\n"]
        out, n = F.fix_lines(lines, NOW)
        self.assertEqual(n, 1)
        self.assertEqual(json.loads(out[0])["time"], "2026-10-04T12:00:00Z")
        o = json.loads(out[1]); self.assertEqual(o["time"], "2026-10-04T13:13:00Z"); self.assertTrue(o["time_estimated"])
        self.assertEqual(out[2], "not json\n")
    def test_a_few_seconds_ahead_is_tolerated(self):
        out, n = F.fix_lines([json.dumps({"time": "2026-10-04T13:13:30Z"}) + "\n"], NOW); self.assertEqual(n, 0)

if __name__ == "__main__": unittest.main()
