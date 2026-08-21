import unittest
from fastapi.testclient import TestClient
from agents.customer_support_triage.main import api
from agents.customer_support_triage.schema import CustomerTier

class TestCustomerSupportTriage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize the FastAPI TestClient
        cls.client = TestClient(api)

    def test_run_customer_support_triage_enterprise_urgent(self):
        # Scenario 1: Enterprise customer reporting a critical outage/account lockout.
        # This payload follows the SupportTicketInput schema.
        payload = {
            "raw_ticket_text": "I'm completely locked out of my Enterprise admin account and the password reset email is not arriving. Please help, I need to access it immediately!",
            "customer_tier": CustomerTier.ENTERPRISE.value,
            "timestamp": "2026-07-17T17:00:00Z"
        }
        
        response = self.client.post("/run-customer-support-triage", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data.get("status"), "success")
        
        results = data.get("results")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        triage_result = results[0]
        self.assertIn("priority_level", triage_result)
        self.assertIn("detected_sentiment", triage_result)
        self.assertIn("category", triage_result)
        self.assertIn("summary_sentence", triage_result)
        self.assertIn("requires_manager_intervention", triage_result)
        
        # Verify the triage logic works according to the instructions in prompt.py:
        # Outage / Critical account lockout for Enterprise customer should be P0 or P1 priority.
        self.assertIn(triage_result["priority_level"], ["P0", "P1"])
        self.assertEqual(triage_result["category"], "Account_Access")

    def test_run_customer_support_triage_free_billing(self):
        # Scenario 2: Free tier customer asking a routine billing question.
        # This payload follows the SupportTicketInput schema.
        payload = {
            "raw_ticket_text": "I would like to ask when my billing period starts for the free tier, is it monthly?",
            "customer_tier": CustomerTier.FREE.value,
            "timestamp": "2026-07-17T17:05:00Z"
        }
        
        response = self.client.post("/run-customer-support-triage", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data.get("status"), "success")
        
        results = data.get("results")
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        
        triage_result = results[0]
        self.assertEqual(triage_result["category"], "Billing")
        # Billing query for Free tier should not be a P0 blocker.
        self.assertNotEqual(triage_result["priority_level"], "P0")

    def test_invalid_input_validation(self):
        # Scenario 3: Testing input validation.
        # Sending an invalid payload to verify Pydantic correctly rejects it.
        payload = {
            "raw_ticket_text": "Missing customer tier and timestamp"
        }
        
        response = self.client.post("/run-customer-support-triage", json=payload)
        # Pydantic validation error returns 422 Unprocessable Entity
        self.assertEqual(response.status_code, 422)

if __name__ == "__main__":
    unittest.main()
