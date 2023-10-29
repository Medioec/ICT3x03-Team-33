import unittest
from flask import Flask, jsonify
from databaseservice.showtimesQueries import showtimes_bp
from unittest.mock import patch
import json

class ShowtimesQueriesTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(showtimes_bp)
        self.client = self.app.test_client()

    def test_create_showtime(self):
        data = {
            'cinemaId': 1,
            'theaterId': 1,
            'movieId': 1,
            'showDate': '2023-10-29',
            'showTime': '19:00',
        }
        response = self.client.post('/create_showtime', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Showtime added successfully', response.get_data(as_text=True))

    def test_get_showtime_by_id(self):
        response = self.client.get('/get_showtime_by_id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cinemaId', response.get_data(as_text=True))

    def test_get_all_showtimes(self):
        response = self.client.get('/get_all_showtimes')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cinemaId', response.get_data(as_text=True))

    def test_update_showtime_by_id(self):
        data = {
            'cinemaId': 2,
            'theaterId': 2,
            'movieId': 2,
            'showDate': '2023-11-29',
            'showTime': '21:00',
        }
        response = self.client.put('/update_showtime_by_id/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Showtime updated successfully', response.get_data(as_text=True))

    def test_delete_showtime_by_id(self):
        response = self.client.delete('/delete_showtime_by_id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Showtime deleted successfully', response.get_data(as_text=True))

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
