# test_app.py
import unittest
from unittest.mock import patch
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch('requests.post')
    def test_get_all_credit_cards(self, mock_post):
        # Mocking the response from the databaseservice
        mock_post.return_value.json.return_value = {'encryptionKey': 'ENCRYPTION_KEY'}
        mock_post.return_value.status_code = 200

        response = self.client.post('/getAllCreditCards', json={'userId': '1', 'sessionId': 'SESSION_ID', 'hash': 'HASH'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('creditCardNumber', response.json[0])

    @patch('requests.put')
    def test_update_one_credit_card(self, mock_put):
        # Mocking the response from the databaseservice
        mock_put.return_value.json.return_value = {'message': 'Credit card updated'}
        mock_put.return_value.status_code = 200

        response = self.client.put('/updateOneCreditCard', json={'creditCardId': '1', 'creditCardNumber': '1234567812345678', 'creditCardName': 'Test', 'creditCardExpiry': '12/34', 'cvv': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Credit card updated')

    @patch('requests.delete')
    def test_delete_credit_card(self, mock_delete):
        # Mocking the response from the databaseservice
        mock_delete.return_value.json.return_value = {'message': 'Credit card deleted'}
        mock_delete.return_value.status_code = 200

        response = self.client.delete('/deleteCreditCard', json={'creditCardId': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Credit card deleted')

    @patch('requests.post')
    @patch('requests.get')
    def test_get_all_credit_cards_success(self, mock_get, mock_post):
        # Mocking the response from the databaseservice
        mock_get.return_value.json.return_value = [{'creditCardId': '1', 'blob': 'BLOB'}]
        mock_get.return_value.status_code = 200

        mock_post.return_value.json.return_value = {'encryptionKey': 'ENCRYPTION_KEY'}
        mock_post.return_value.status_code = 200

        response = self.client.post('/getAllCreditCards', json={'userId': '1', 'sessionId': 'SESSION_ID', 'hash': 'HASH'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('creditCardNumber', response.json[0])

    @patch('requests.post')
    @patch('requests.get')
    def test_get_all_credit_cards_no_credit_cards(self, mock_get, mock_post):
        # Mocking the response from the databaseservice
        mock_get.return_value.status_code = 404

        response = self.client.post('/getAllCreditCards', json={'userId': '1', 'sessionId': 'SESSION_ID', 'hash': 'HASH'})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['message'], 'No credit cards found')

    @patch('requests.post')
    def test_update_one_credit_card_success(self, mock_post):
        # Mocking the response from the databaseservice
        mock_post.return_value.json.return_value = {'message': 'Credit card updated'}
        mock_post.return_value.status_code = 200

        response = self.client.put('/updateOneCreditCard', json={'creditCardId': '1', 'creditCardNumber': '1234567812345678', 'creditCardName': 'Test', 'creditCardExpiry': '12/34', 'cvv': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Credit card updated')

    @patch('requests.delete')
    def test_delete_credit_card_success(self, mock_delete):
        # Mocking the response from the databaseservice
        mock_delete.return_value.json.return_value = {'message': 'Credit card deleted'}
        mock_delete.return_value.status_code = 200

        response = self.client.delete('/deleteCreditCard', json={'creditCardId': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Credit card deleted')
        
if __name__ == '__main__':
    unittest.main()
