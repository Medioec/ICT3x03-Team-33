import unittest
from flask import Flask
from unittest.mock import patch, Mock
from databaseservice.transactionQueries import transaction_bp

class TransactionQueriesTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(transaction_bp)
        self.client = self.app.test_client()

    def test_create_transaction_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1]
            
            response = self.client.post('/create_transaction', json={"transactionId": "1", "creditCardId": "1", "transactionDateTime": "2023-10-29 10:00:00"})
            self.assertEqual(response.status_code, 201)
            self.assertIn(b"Transaction added successfully", response.data)

    def test_get_all_transactions_by_userId_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [(1, "1", "2023-10-29 10:00:00")]
            
            response = self.client.get('/get_all_transactions_by_userId/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'"transactionId": "1"', response.data)
            self.assertIn(b'"creditCardId": "1"', response.data)
            self.assertIn(b'"transactionDateTime": "2023-10-29 10:00:00"', response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
