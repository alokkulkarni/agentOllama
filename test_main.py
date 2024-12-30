import unittest
from fastapi.testclient import TestClient
from main import app, getComplaintStatus, getFinanceSummary, getCustomerDetails, getRecentTransactions

# FILE: test_main.py


client = TestClient(app)

class TestMain(unittest.TestCase):

    # def test_getComplaintStatus(self):
    #     self.assertEqual(getComplaintStatus(123, "abcdef"), "pending")
    #     self.assertEqual(getComplaintStatus(123, "ghefds"), "resolved")
    #     self.assertEqual(getComplaintStatus(123, "unknown"), "Complaint not found for given customer id {{customerId}} and complaint id {{complaintId}}")

    # def test_getFinanceSummary(self):
    #     self.assertEqual(getFinanceSummary(123), {"customerId": 123, "balance": 1000, "lastTransaction": "2021-01-01"})
    #     self.assertEqual(getFinanceSummary(124), {"customerId": 124, "balance": 2000, "lastTransaction": "2021-01-01"})
    #     self.assertEqual(getFinanceSummary(125), "Finance summary not found for given customer id {{customerId}}")

    # def test_getCustomerDetails(self):
    #     self.assertEqual(getCustomerDetails(123), {"customerId": 123, "name": "John Doe", "email": "john.doe@gmail.com"})
    #     self.assertEqual(getCustomerDetails(124), {"customerId": 124, "name": "Jane Doe", "email": "jane.doe@gmail.com"})
    #     self.assertEqual(getCustomerDetails(125), "Customer details not found for given customer id {{customerId}}")

    # def test_getRecentTransactions(self):
    #     self.assertEqual(len(getRecentTransactions(123, "Tesco")), 4)
    #     self.assertEqual(len(getRecentTransactions(123, "Sainsbury")), 1)
    #     self.assertEqual(len(getRecentTransactions(123, "Unknown")), 0)

    def test_handle_query(self):
        response = client.post("/banking-agent/?query=get the customer details for customer id 123")
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())

if __name__ == '__main__':
    unittest.main()