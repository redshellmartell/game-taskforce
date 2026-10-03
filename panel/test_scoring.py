import unittest, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scoring as S

PT = {"skill_expression": 38.6, "length": {"estimated_minutes": 12}, "seat_balance_gap": 3.4,
      "cards": [{"flag": "dominated: x"}, {"flag": "inert: y"}, {"flag": None}]}
RAW = dict(decisions_per_turn=1.5, lead_changes=2.0, comeback_rate=0.25, interaction_rate=0.15, downtime=2)

class T(unittest.TestCase):
    def test_frontmatter(self):
        fm = S.parse_frontmatter('---\nid: x\nbot_style: planner   # c\nweights:\n  a: 0.5\n  b: 0.5\npreferred_minutes: [45, 120]\ntagline: "hi: there"\n---\nbody')
        self.assertEqual(fm["id"], "x"); self.assertEqual(fm["bot_style"], "planner")
        self.assertEqual(fm["weights"], {"a": 0.5, "b": 0.5}); self.assertEqual(fm["preferred_minutes"], [45, 120]); self.assertEqual(fm["tagline"], "hi: there")
    def test_real_personas_weights_sum_to_one(self):
        ps = S.load_personas()
        self.assertEqual(len(ps), 5)
        for p in ps.values():
            self.assertAlmostEqual(sum(p["weights"].values()), 1.0, places=6); self.assertTrue(p["peeves"])
    def test_simple_metrics(self):
        self.assertEqual(S.rules_simplicity(500), 1); self.assertEqual(S.rules_simplicity(3000), 0); self.assertAlmostEqual(S.rules_simplicity(1800), 0.5)
        self.assertEqual(S.length_fit(20, [10, 30]), 1); self.assertAlmostEqual(S.length_fit(12, [45, 120]), 1 - 33 / 45)
        self.assertEqual(S.length_fit(300, [45, 120]), 0); self.assertEqual(S.skill_expression(80), 1)
        self.assertAlmostEqual(S.dominant_absent(PT["cards"]), 2 / 3)
    def test_fun_bounds_and_weighting(self):
        best = {k: 1.0 for k in S.METRICS}; worst = {k: 0.0 for k in S.METRICS}
        w = {"skill_expression": 0.5, "length_fit": 0.5}
        self.assertEqual(S.fun_from_metrics(best, w), 5.0); self.assertEqual(S.fun_from_metrics(worst, w), 1.0)
        self.assertEqual(S.fun_from_metrics({"skill_expression": 1, "length_fit": 0}, w), 3.0)
    def test_would_buy(self):
        self.assertEqual(S.would_buy(2.5, 30, [10, 30], [10, 30]), ("no", None))
        self.assertEqual(S.would_buy(4.0, 30, [10, 30], [10, 30])[0], "yes")
        v, price = S.would_buy(5.0, 30, [10, 30], [10, 30]); self.assertEqual(price, 30)
        v, price = S.would_buy(4.0, 12, [30, 80], [45, 120]); self.assertGreaterEqual(price, 30); self.assertLessEqual(price, 80)
    def test_peeves(self):
        m = {**S.game_metrics(PT, 1400, [30, 90]), **S.bot_metrics(RAW)}
        raw = {**RAW, "minutes": 12, "preferred_max": 90, "seat_gap": 3.4}
        hit = S.peeves_hit(["A dominant or solved strategy.", "Long, bloated endgames", "Luck that decides the result"], m, raw)
        self.assertEqual(hit, ["A dominant or solved strategy"])   # too SHORT is not a "long game" peeve; skill is high so luck is fine
    def test_build_panel(self):
        ps = S.load_personas(only={"strategist", "casual"})
        res = {"personas": {k: {"raw": RAW, "bot": {"win_rate": .5}, "best_table": ["casual", "strategist"], "worst_table": ["casual", "strategist"]} for k in ps},
               "matchups": [{"a": "casual", "b": "strategist", "games": 400, "a_win_rate": .4, "note": "", "a_raw": RAW, "b_raw": RAW}],
               "rotation": {"tables": 1}}
        out = S.build_panel(PT, 1400, res, ps, 1)
        self.assertEqual(set(out["personas"]), {"strategist", "casual"}); self.assertIsNone(out["personas"]["casual"]["review"])
        self.assertIn("a_fun", out["matchups"][0]); self.assertNotIn("a_raw", out["matchups"][0])
        self.assertEqual(out["summary"]["best_fit"] in ("casual", "strategist"), True)

if __name__ == "__main__": unittest.main()
