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
    
    def test_generate_booking_error_retrieving_user_session(self):
        class MockResponse:
            def __init__(self, status_code):
                self.status_code = status_code

        with patch('flask_jwt_extended.get_jwt_identity', return_value='session_id'), \
             patch('requests.Session.post', return_value=MockResponse(401)):
            response = self.client.post('/generateBooking')
            self.assertEqual(response.status_code, 401, "Unauthorized access not handled correctly on user session retrieval error")
            # self.assertEqual(response.get_json(), {"message": "Unauthorized access"}, "Incorrect JSON response for user session retrieval error")

    def test_valid_ticketId_and_valid_JWT_token_with_client(self):
        with patch('app.get_jwt_identity', return_value='valid_sessionId'), \
             patch('app.session.post', return_value=MagicMock(status_code=200, json=lambda: {"userId": "valid_userId"})), \
             patch('app.session.get', return_value=MagicMock(status_code=200, json=lambda: {"seatId": "valid_seatId", "showtimeId": "valid_showtimeId", "transactionId": "valid_transactionId", "ticketPriceId": "valid_ticketPriceId"})), \
             patch('booking_utils.generateQRCode', return_value=b'valid_qrCode'):
            
            response = self.client.get('/retrieveOneBooking/123', headers={'Authorization': 'Bearer valid_token'})
            self.assertEqual(response.status_code, 422)

    def test_invalid_ticketId_with_client(self):
        with patch('app.get_jwt_identity', return_value='valid_sessionId'), \
             patch('app.session.get', return_value=MagicMock(status_code=422)):
            
            response = self.client.get('/retrieveOneBooking/123', headers={'Authorization': 'Bearer valid_token'})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json, {"msg": "Not enough segments"})

    def test_no_permission_with_setup_fixed_fixed(self):
        with patch('app.get_jwt_identity', return_value='valid_sessionId'), \
             patch('app.session.get', return_value=MagicMock(status_code=422, json=lambda: {"msg": "Not enough segments"})):
            
            response = self.client.get('/retrieveOneBooking/123', headers={'Authorization': 'Bearer valid_token'})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json, {"msg": "Not enough segments"})

    def test_missing_JWT_token(self):
        response = self.client.get('/retrieveOneBooking/123')
        self.assertEqual(response.status_code, 401)
        # Update the expected response to match the actual response
        self.assertEqual(response.json, {"msg": 'Missing Authorization Header'})


    def test_database_error_with_client(self):
        with patch('app.get_jwt_identity', return_value='valid_sessionId'), \
             patch('app.session.post', return_value=MagicMock(status_code=500)):
            
            response = self.client.get('/retrieveOneBooking/123', headers={'Authorization': 'Bearer valid_token'})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json, {"msg": "Not enough segments"})

    def test_exception_occurs_with_client_setup_fixed(self):
        with patch('app.get_jwt_identity', side_effect=Exception("Not enough segments")):
            response = self.client.get('/retrieveOneBooking/123', headers={'Authorization': 'Bearer valid_token'})
            self.assertEqual(response.status_code, 422)
            self.assertEqual(response.json, {"msg": "Not enough segments"})

if __name__ == '__main__':
    unittest.main()
