import unittest

from aegisforge.policy import assess


class PolicyTests(unittest.TestCase):
    def test_simple_documentation_change_is_lightweight(self):
        result = assess("Fix a typo in the README")
        self.assertEqual(result.workflow, "lightweight")
        self.assertEqual(result.task_type, "documentation")
        self.assertTrue(result.reversible)

    def test_oauth_production_change_is_high_assurance(self):
        result = assess("Add OAuth login and deploy it to production")
        self.assertEqual(result.workflow, "high-assurance")
        self.assertEqual(result.task_type, "operations")
        self.assertTrue(result.authorization_impact)
        self.assertTrue(result.production_scope)

    def test_data_deletion_is_critical(self):
        result = assess("Delete customer records from the production database")
        self.assertEqual(result.risk_level, "critical")
        self.assertFalse(result.reversible)
        self.assertIn("destructive action", result.reasons)

    def test_empty_request_is_explicitly_ambiguous(self):
        result = assess("")
        self.assertTrue(result.ambiguity)
        self.assertEqual(result.workflow, "standard")

    def test_external_email_requires_confirmation(self):
        result = assess("Send an email notification to every customer")
        self.assertEqual(result.risk_level, "high")
        self.assertTrue(result.external_side_effects)
        self.assertTrue(result.requires_confirmation)

    def test_non_destructive_migration_is_high_assurance(self):
        result = assess("Run a database migration and backfill customer data")
        self.assertEqual(result.risk_level, "high")
        self.assertTrue(result.reversible)
        self.assertIn("data or schema change", result.reasons)

    def test_critical_assessment_has_release_controls(self):
        result = assess("Delete customer records from the production database")
        self.assertIn("human approval", result.required_controls)
        self.assertIn("release evidence", result.required_controls)


if __name__ == "__main__":
    unittest.main()
