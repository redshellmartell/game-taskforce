import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import repair as R

BASE = {"requests": [{"id": "a", "game": "g1", "status": "pending", "decision": None, "decided_at": None, "owner_notes": None},
                     {"id": "b", "game": "g2", "status": "approved", "decision": "approve", "decided_at": "t0", "owner_notes": "cloud"},
                     {"id": "c", "game": "g3", "status": "pending", "decision": None, "decided_at": None, "owner_notes": None}]}
LOCAL = {"requests": [{"id": "a", "status": "approved", "decision": "approve", "decided_at": "t1", "owner_notes": "mac"},
                      {"id": "b", "status": "declined", "decision": "decline", "decided_at": "t2", "owner_notes": "mac"},
                      {"id": "c", "status": "pending"}]}

class T(unittest.TestCase):
    def test_only_pending_requests_take_your_answer(self):
        merged, applied = R.merge_approvals(BASE, LOCAL)
        self.assertEqual(applied, ["a"])
        s = {r["id"]: r for r in merged["requests"]}
        self.assertEqual(s["a"]["status"], "approved"); self.assertEqual(s["a"]["owner_notes"], "mac")
        self.assertEqual(s["b"]["owner_notes"], "cloud")       # already decided on GitHub: kept
        self.assertEqual(s["c"]["status"], "pending")
    def test_nothing_local_changes_nothing(self):
        merged, applied = R.merge_approvals(BASE, None); self.assertEqual(applied, [])
    def test_decisions_are_merged_without_duplicates(self):
        d = R.merge_decisions({"decisions": [{"slug": "x", "notes": "old"}]}, {"decisions": [{"slug": "x", "notes": "old"}, {"slug": "y", "notes": "mine"}]},
                              [{"id": "a", "game": "g1", "decision": "approve", "decided_at": "t1"}], ["a"])
        notes = [x["notes"] for x in d["decisions"]]
        self.assertEqual(notes.count("old"), 1); self.assertIn("mine", notes); self.assertTrue(any(n.startswith("a:") for n in notes))
    def test_decision_not_added_twice_when_notes_already_name_the_request(self):
        d = R.merge_decisions({"decisions": [{"notes": "a: owner approved"}]}, None, [{"id": "a", "game": "g"}], ["a"])
        self.assertEqual(len(d["decisions"]), 1)

if __name__ == "__main__": unittest.main()
