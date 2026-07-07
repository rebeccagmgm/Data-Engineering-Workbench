from datetime import datetime, timezone
from pathlib import Path
import unittest

from scripts.case_dashboard_generator import build_dashboard, render_dashboard_html


ROOT = Path(__file__).resolve().parents[1]


class CaseDashboardGeneratorTests(unittest.TestCase):
    def test_jinshida_sample_is_classified_into_attention_lanes(self):
        dashboard = build_dashboard(ROOT, now=datetime(2026, 7, 7, tzinfo=timezone.utc))

        self.assertEqual(dashboard["health"]["case_count"], 1)
        self.assertEqual(dashboard["health"]["failed_verification_count"], 2)
        self.assertEqual(dashboard["health"]["unverified_done_count"], 1)

        lanes = dashboard["cases"][0]["attention_lanes"]
        self.assertIn("B-001", lanes["waiting"])
        self.assertIn("T-003", lanes["failed_verification"])
        self.assertIn("T-004", lanes["failed_verification"])
        self.assertIn("T-005", lanes["done_not_verified"])

    def test_top_risks_precede_actions_and_explain_source_rules(self):
        dashboard = build_dashboard(ROOT, now=datetime(2026, 7, 7, tzinfo=timezone.utc))

        top_risk_sources = {item["source_ref"] for item in dashboard["top_risks"]}
        top_action_sources = {item["source_ref"] for item in dashboard["top_actions"]}

        self.assertIn("CASE-20260611-jinshida-market-push:T-003", top_risk_sources)
        self.assertIn("CASE-20260611-jinshida-market-push:T-004", top_risk_sources)
        self.assertIn("CASE-20260611-jinshida-market-push:B-001", top_action_sources)
        self.assertTrue(all(item["matched_rule"] for item in dashboard["top_risks"]))

    def test_rendered_html_is_local_only_and_orders_risks_before_actions(self):
        dashboard = build_dashboard(ROOT, now=datetime(2026, 7, 7, tzinfo=timezone.utc))
        html = render_dashboard_html(dashboard)

        self.assertIn("case-dashboard-generator", html)
        self.assertIn("Local-only generated view", html)
        self.assertLess(html.index("Top Risks"), html.index("Top Actions"))
        self.assertIn("T-005", html)


if __name__ == "__main__":
    unittest.main()
