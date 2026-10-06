"""Run: python3 -m unittest discover tools/sim-kit"""
import os, sys, tempfile, unittest, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "template"))
import simkit
from game import play
import bots as B


class Kit(unittest.TestCase):
    def test_wilson_and_leaders(self):
        lo, hi = simkit.wilson(50, 100); self.assertTrue(lo < 0.5 < hi); self.assertAlmostEqual((lo + hi) / 2, 0.5, delta=0.02)
        self.assertEqual(simkit.wilson(0, 0), (0.0, 1.0))
        L = simkit.leaders_from_diff([1, 2, 0, -1, -3, 2]); self.assertEqual(L, [0, 0, None, 1, 1, 0]); self.assertEqual(simkit.lead_changes(L), 2)

    def test_seat_rotation_cancels_seat_order(self):
        rows = simkit.run_match(play, [B.MAKERS["strategic"]] * 2, 600, seed=1)
        s = simkit.summarize(rows, 2)
        self.assertEqual(s["games"], 600); self.assertAlmostEqual(sum(s["seat_win_rates"]), 1.0, delta=0.01)
        self.assertLess(s["seat_gap"], 8)                       # Pig has a real first-player edge, but it is bounded
        self.assertAlmostEqual(sum(s["maker_win_rates"]), 1.0, delta=0.01)

    def test_skill_ladder_orders_bots(self):
        t = simkit.round_robin(play, B.MAKERS, 300)
        self.assertGreater(t["avg"]["strategic"], t["avg"]["random"]); self.assertGreater(t["avg"]["greedy"], t["avg"]["random"])
        self.assertGreater(t["spread_pts"], 5)

    def test_ablation_detects_inert_and_real_rules(self):
        real = simkit.ablation(play, B.MAKERS["strategic"], B.MAKERS["random"], 400)          # a clearly worse bot loses
        self.assertTrue(real["passes"] and real["significant"])
        inert = simkit.ablation(play, B.MAKERS["strategic"], B.MAKERS["strategic"], 400)      # identical bot: no margin
        self.assertFalse(inert["passes"])

    def test_kpi_table_and_json_keys(self):
        s = simkit.summarize(simkit.run_match(play, [B.MAKERS["strategic"]] * 2, 200, seed=3), 2)
        rows = simkit.evaluate(s, 25.0, 10, 11, dead_cards=1)
        self.assertEqual({r[0]: r[3] for r in rows}["dead cards"], False)
        self.assertTrue({r[0]: r[3] for r in rows}["length (min)"])
        none = dict(s, runaway_leader_rate=None); self.assertFalse(dict((r[0], r[3]) for r in simkit.evaluate(none, 25, 10, 10))["runaway leader rate"])
        out = simkit.to_playtest_json(s, {"strategic": 0.5}, 25.0, 10, 11, "PASS", 1, previous={"x": 1})
        for k in ("verdict", "revision", "games_simulated", "seat_win_rates", "seat_balance_gap", "bot_win_rates", "skill_expression", "length",
                  "length_histogram", "ties", "turn_cap_hits", "lead_changes_mean", "runaway_leader_rate", "cards", "ambiguities", "problems"):
            self.assertIn(k, out)
        self.assertEqual(out["validation"], "bots only, unvalidated")

    def test_template_run_writes_json(self):
        import run
        p = os.path.join(tempfile.mkdtemp(), "playtest.json"); run.main(150, p)
        with open(p) as f: d = json.load(f)
        self.assertIn("ablations", d); self.assertEqual(d["games_simulated"], 150)

    def test_ties_split_credit_and_caps(self):
        rows = [dict(winner=None, turns=5, capped=True, order=[0, 1]), dict(winner=0, turns=7, capped=False, order=[1, 0])]
        s = simkit.summarize(rows, 2); self.assertEqual(s["ties"], 0.5); self.assertEqual(s["turn_cap_hits"], 1)
        self.assertEqual(s["seat_win_rates"], [0.75, 0.25]); self.assertEqual(s["maker_win_rates"], [0.25, 0.75])


if __name__ == "__main__": unittest.main()
