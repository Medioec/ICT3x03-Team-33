import unittest
from flask import Flask
from flask_testing import TestCase
from bookingDetailsQueries import booking_details_bp

class BookingDetailsQueriesTestCase(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.register_blueprint(booking_details_bp, url_prefix='/databaseservice/bookingdetails')
        return app

    def test_generate_booking_details(self):
        data = {
            'userId': 'test_user',
            'showtimeId': 1,
            'seatId': 1,
            'ticketPriceId': 1,
            'transactionId': 1
        }
        response = self.client.post('/databaseservice/bookingdetails/generate_booking_details', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_booking_details_by_id(self):
        user_id = 'test_user'
        ticket_id = 1
        response = self.client.get(f'/databaseservice/bookingdetails/get_booking_details_by_id/{user_id}/{ticket_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_all_bookings_by_userId(self):
        user_id = 'test_user'
        response = self.client.get(f'/databaseservice/bookingdetails/get_all_bookings_by_userId/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_duplicate_booking(self):
        data = {
            'userId': 'test_user',
            'showtimeId': 1,
            'seatId': 1,
            'ticketPriceId': 1,
            'transactionId': 1
        }
        # First request should be successful
        response1 = self.client.post('/databaseservice/bookingdetails/generate_booking_details', json=data)
        self.assertEqual(response1.status_code, 201)

        # Second request should return 409 Conflict due to duplicate entry
        response2 = self.client.post('/databaseservice/bookingdetails/generate_booking_details', json=data)
        self.assertEqual(response2.status_code, 409)


if __name__ == '__main__':
    unittest.main()
