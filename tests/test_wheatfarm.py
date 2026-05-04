from __future__ import annotations

import json
import unittest
from pathlib import Path

from wheatfarm.access_policy import classify_action, load_access_policy
from wheatfarm.adapters import FixtureStore
from wheatfarm.receipts import render_public_receipt


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "fixtures"
WEIGHTS = ROOT / "config" / "rci_weights.yaml"
POLICY = ROOT / "config" / "access_policy.yaml"


class WheatFarmTests(unittest.TestCase):
    def test_fixture_scores_match_expected_ranges(self) -> None:
        store = FixtureStore(FIXTURE_DIR)
        self.assertGreaterEqual(len(store.list_fixture_ids()), 6)
        for fixture_id in store.list_fixture_ids():
            with self.subTest(fixture_id=fixture_id):
                fixture = store.load_fixture(fixture_id)
                score = store.score_fixture(fixture_id, WEIGHTS)
                expected = fixture["expected"]
                low, high = expected["rci_range"]
                self.assertGreaterEqual(score.score, low)
                self.assertLessEqual(score.score, high)
                self.assertEqual(score.verdict.value, expected["verdict"])

    def test_receipt_has_public_boundary(self) -> None:
        store = FixtureStore(FIXTURE_DIR)
        fixture = store.load_fixture("fixture_event_clean_wheat")
        score = store.score_fixture("fixture_event_clean_wheat", WEIGHTS)
        receipt = render_public_receipt(fixture, score)
        self.assertIn("WHEAT FARM RECEIPT", receipt)
        self.assertIn("Verdict: Wheat", receipt)
        self.assertIn("does not prove causation", receipt)

    def test_policy_classification(self) -> None:
        policy = load_access_policy(POLICY)
        self.assertEqual(classify_action("read", policy), "safe_read_only")
        self.assertEqual(classify_action("write", policy), "manual_approval_required")
        self.assertEqual(classify_action("teleport", policy), "unknown_requires_review")

    def test_cli_json_shape_source_fixture_is_valid(self) -> None:
        fixture_path = FIXTURE_DIR / "fixture_event_clean_wheat.json"
        data = json.loads(fixture_path.read_text(encoding="utf-8"))
        self.assertEqual(data["event"]["event_id"], "fixture_event_clean_wheat")


if __name__ == "__main__":
    unittest.main()
