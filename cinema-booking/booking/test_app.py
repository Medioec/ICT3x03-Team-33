# test_app.py
import unittest
from booking.app import app

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_generate_booking(self):
        # Add your test cases for /generateBooking endpoint
        # Example test case
        data = {
            "userId": "some-user-id",
            "creditCardId": 1,
            "showtimeId": 1,
            "seatId": 1,
            "ticketPriceId": 1
        }
        response = self.app.post('/generateBooking', json=data)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_one_booking(self):
        response = self.app.get('/retrieveOneBooking/some-user-id/1')
        self.assertEqual(response.status_code, 200)

    def test_retrieve_all_bookings(self):
        response = self.app.get('/retrieveAllBookings/some-user-id')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
