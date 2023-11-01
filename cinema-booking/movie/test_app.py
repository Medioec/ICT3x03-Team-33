import unittest
from app import app

class AppTest(unittest.TestCase):
    # Set up a test client
    def setUp(self):
        self.app = app.test_client()
    
    def test_update_showtime_by_id(self):
        # Create test data
        data = {
            "cinemaId": 1,
            "theaterId": "A",
            "movieId": 1,
            "showDate": "12-3-2023",
            "showTime": "12:30 PM"
        }
        # Send a PUT request with the test data
        response = self.app.put('/updateShowtimeById/1', json=data)
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
    
    def test_delete_showtime_by_id(self):
        # Send a DELETE request
        response = self.app.delete('/deleteShowtimeById/1')
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

# Run the tests
if __name__ == '__main__':
    unittest.main()
