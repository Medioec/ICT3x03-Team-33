import unittest
from flask import Flask
from unittest.mock import patch, Mock
from your_project_directory.theaterTableQueries import theater_bp

class TheaterTableQueriesTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(theater_bp)
        self.client = self.app.test_client()

    def test_add_theater_success(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1]

            response = self.client.post('/add_theater', json={"theaterNumber": "1"})
            self.assertEqual(response.status_code, 201)
            self.assertIn(b"Theater added successfully", response.data)

    def test_add_theater_failure_duplicate(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = IntegrityError("duplicate key value violates unique constraint")

            response = self.client.post('/add_theater', json={"theaterNumber": "1"})
            self.assertEqual(response.status_code, 409)
            self.assertIn(b"Duplicate entry: This theater already exists.", response.data)

    def test_get_theater_by_number_success(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1]

            response = self.client.get('/get_theater_by_number/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'"theaterNumber": 1', response.data)

    def test_get_theater_by_number_failure(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None

            response = self.client.get('/get_theater_by_number/2')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Theater not found", response.data)

    def test_get_all_theaters_success(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [[1], [2], [3]]

            response = self.client.get('/get_all_theaters')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'"theaterNumber": 1', response.data)
            self.assertIn(b'"theaterNumber": 2', response.data)
            self.assertIn(b'"theaterNumber": 3', response.data)

    def test_get_all_theaters_failure(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = []

            response = self.client.get('/get_all_theaters')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"No theaters found", response.data)

    def test_update_theater_by_id_success(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1]

            response = self.client.put('/update_theater_by_id/1', json={"theaterNumber": "2"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Theater updated successfully", response.data)

    def test_update_theater_by_id_failure(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None

            response = self.client.put('/update_theater_by_id/3', json={"theaterNumber": "2"})
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Theater not found", response.data)

    def test_delete_theater_by_id_success(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1]

            response = self.client.delete('/delete_theater_by_id/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Theater deleted successfully", response.data)

    def test_delete_theater_by_id_failure(self):
        with patch('psycopg2.connect') as mock_connect:
            # Mock the database connection and cursor
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None

            response = self.client.delete('/delete_theater_by_id/3')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Theater not found", response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
