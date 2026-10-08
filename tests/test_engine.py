import unittest

from automation_demo.engine import AutomationEngine, Decision, Request, redact
from automation_demo.simulation import generate_requests, run_simulation


class AutomationEngineTests(unittest.TestCase):
    def test_safe_request_uses_mock_automation(self) -> None:
        engine = AutomationEngine()
        request = Request("1", "invoice_copy", "Send a copy", "person@example.test")
        self.assertEqual(engine.process(request), Decision.AUTOMATE)

    def test_sensitive_request_requires_approval(self) -> None:
        engine = AutomationEngine()
        request = Request("2", "account_deletion", "Delete the test account", "person@example.test")
        self.assertEqual(engine.process(request), Decision.REQUIRE_APPROVAL)

    def test_duplicate_request_is_not_executed_twice(self) -> None:
        engine = AutomationEngine()
        request = Request("3", "invoice_copy", "Send a copy", "person@example.test")
        self.assertEqual(engine.process(request), Decision.AUTOMATE)
        self.assertEqual(engine.process(request), Decision.DUPLICATE)

    def test_evidence_redacts_email_and_phone(self) -> None:
        value = redact("Write to person@example.test or call +34 600 000 000")
        self.assertEqual(value, "Write to [EMAIL] or call [PHONE]")

    def test_simulation_has_reproducible_policy_counts(self) -> None:
        report = run_simulation(100)
        self.assertEqual(
            report["decisions"],
            {"automate": 50, "manual": 20, "require_approval": 30},
        )

    def test_simulation_rejects_non_positive_count(self) -> None:
        with self.assertRaises(ValueError):
            generate_requests(0)


if __name__ == "__main__":
    unittest.main()

