from bookingDetailsQueries import generate_booking_details
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify

class TestGenerateBookingDetails(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        # Register your route
        @self.app.route('/generate_booking_details', methods=['POST'])
        def booking_details_route():
            return generate_booking_details()

    def test_add_new_booking_entry_with_mock_with_fix(self):
        # Mock data must be JSON-serializable as it's going to simulate the client input
        mock_data = {
            'userId': 1,
            'showtimeId': 1,
            'seatId': 1,
            'ticketPriceId': 1,
            'transactionId': 1
        }
        # Return values should be the actual results you'd expect from the database, not mocks
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1,)
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_logger = MagicMock()

        # Patch the required methods/classes with your mocks
        with patch('psycopg2.connect', return_value=mock_conn), \
             patch('logging.getLogger', return_value=mock_logger):
            response = self.client.post('/generate_booking_details', json=mock_data)
            status_code = response.status_code

            # Assert the response code
            self.assertEqual(status_code, 200, f"Expected status code 200, but got {status_code}")

            # Assert that the mock methods were called as expected
            mock_conn.commit.assert_called_once()
            mock_cursor.close.assert_called_once()
            mock_conn.close.assert_called_once()
            mock_logger.info.assert_called_once()
            mock_logger.error.assert_not_called()

    def test_handle_exceptions_fixed_with_app_context(self):
        # Patch with side_effect to simulate an exception being thrown
        with patch('psycopg2.connect', side_effect=Exception("Test exception")), \
             patch('logging.getLogger') as mock_logger:
            response = self.client.post('/generate_booking_details')
            status_code = response.status_code

            # Assert the response code
            self.assertEqual(status_code, 500, f"Expected status code 500, but got {status_code}")

            # Ensure that the error logging happened as expected
            mock_logger.error.assert_called_once()

if __name__ == '__main__':
    unittest.main()
