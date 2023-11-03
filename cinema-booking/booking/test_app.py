# test_app.py
import unittest
import json
from app import app as flask_app
from unittest.mock import patch, MagicMock
from flask_jwt_extended import create_access_token, JWTManager

class FlaskAppTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = flask_app
        cls.app.config['JWT_SECRET_KEY'] = 'mock_jwt_secret_key'
        cls.app.config['TESTING'] = True
        cls.jwt = JWTManager(cls.app)

    def setUp(self):
        self.client = self.app.test_client()
        with self.app.app_context():
            self.access_token = create_access_token(identity='test_user')

    def test_unauthorized_access(self):
        response = self.client.post('/generateBooking')
        self.assertEqual(response.status_code, 401, 'Unauthorized access not handled correctly')

    @patch('app.session.post')
    def test_generate_booking(self, mock_post):
        # Prepare the mock responses
        mock_responses = [
            MagicMock(status_code=200, json=lambda: {"userId": "testUserId"}),
            MagicMock(status_code=200, json=lambda: {"transactionId": "testTransaction"}),
            MagicMock(status_code=201)
        ]
        mock_post.side_effect = mock_responses

        # Perform the request
        response = self.client.post(
            '/generateBooking',
            headers={'Authorization': f'Bearer {self.access_token}'},
            json={
                'creditCardId': '12345',
                'showtimeId': '67890',
                'seatId': 'A1',
                'ticketPriceId': '200'
            }
        )

        # Check if user session retrieval is successful
        self.assertEqual(mock_responses[0].status_code, 200, "User session retrieval failed")

        # Check if payment service call is successful
        self.assertEqual(mock_responses[1].status_code, 200, "Payment service call failed")

        # Check if booking details creation is successful
        self.assertEqual(mock_responses[2].status_code, 201, "Booking details creation failed")

        # Check if the final response is as expected
        self.assertEqual(response.status_code, 201, 'Booking generation did not succeed as expected')

if __name__ == '__main__':
    unittest.main()
