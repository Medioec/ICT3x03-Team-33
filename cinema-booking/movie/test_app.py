import unittest
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
from app import app, requests, unauthorized_callback, getAllMovies, get_jwt_identity
import requests
import werkzeug.wrappers
from flask import jsonify, Flask
from flask_cors import CORS
import os
import user_utils
import jwt
import json

class MockResponse:
    def __init__(self, status_code, json_data=None):
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        return self.json_data

class TestUnauthorizedCallback(unittest.TestCase):
    def test_with_callback_argument_returns_401_status_code(self):
        with app.app_context():
            response = unauthorized_callback(callback=True)
            self.assertEqual(response[1], 401)

    def test_with_callback_argument_returns_unauthorized_access_message(self):
        with app.app_context():
            response, status_code = unauthorized_callback(callback=True)
            data = response.get_json()
            self.assertEqual(data["message"], "Unauthorized access")

    def test_without_callback_argument_returns_401_status_code(self):
        with app.app_context():
            response = unauthorized_callback(callback=False)
            self.assertEqual(response[1], 401)

    def test_without_callback_argument_returns_message_key(self):
        with app.app_context():
            response, _ = unauthorized_callback(callback=False)
            data = response.get_json()
            self.assertIn("message", data)

    def test_without_callback_argument_returns_unauthorized_access_message(self):
        with app.app_context():
            response, _ = unauthorized_callback(callback=False)
            data = response.get_json()
            self.assertEqual(data["message"], "Unauthorized access")


class CreateMovieTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_create_movie_with_minimum_valid_inputs_with_request_context(self):
        with app.test_request_context():
            with patch('app.request.get_json', return_value={
                'title': 'Test Movie',
                'synopsis': 'This is a test movie',
                'genre': 'Action',
                'contentRating': 'PG-13',
                'lang': 'English',
                'subtitles': 'English'
            }), patch('app.requests.post', return_value=MockResponse(422)), \
                 patch('app.get_jwt_identity', return_value='valid_token'):
                response = self.client.post('/createMovie', headers={'Authorization': 'Bearer valid_token'})
                self.assertEqual(response.status_code, 422)

    def test_create_movie_with_all_valid_inputs_with_request_context_with_jwt_token(self):
        with app.test_request_context():
            with patch('app.request.get_json', return_value={
                'title': 'Test Movie',
                'synopsis': 'This is a test movie',
                'genre': 'Action',
                'contentRating': 'PG-13',
                'lang': 'English',
                'subtitles': 'English'
            }), patch('app.requests.post', return_value=MockResponse(422)):
                headers = {'Authorization': 'Bearer <valid_jwt_token>'}
                response = self.client.post('/createMovie', headers=headers)
                self.assertEqual(response.status_code, 422)

class TestGetmoviebyid(unittest.TestCase):

    def setUp(self):
        # Use the Flask test client
        self.client = app.test_client()

    def test_uncaught_exception_with_mocker(self):
        # Mock the requests.get call to throw an exception
        with patch('app.requests.get', side_effect=Exception('Mocked Exception')):
            # Call the getMovieById function with a movie_id that would trigger an exception
            response = self.client.get('/getMovieById/1')

            # Assert that the response is a server error
            self.assertEqual(response.status_code, 500)
            self.assertIn("error", response.json)

    def test_negative_movie_id(self):
        # Send a GET request to the '/getMovieById/-1' endpoint
        response = self.client.get('/getMovieById/-1')

        # Assert that the response is a 404 not found
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Not Found', response.data)

    def test_string_movie_id(self):
        # Call the getMovieById function with a string movie_id
        response = self.client.get('/getMovieById/abc')

        # Assert that the response is correct
        self.assertEqual(response.status_code, 404)

class TestUpdatemoviebyid(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['JWT_SECRET_KEY'] = 'your_default_test_secret_key'  # Replace with a suitable secret key for testing
        # Ensure JWT_SECRET_KEY is set and is a string before creating the token
        self.valid_token = jwt.encode({'sub': 1}, app.config['JWT_SECRET_KEY'], algorithm='HS256')

    def test_invalid_movie_id_with_404_status_code(self):
        response = self.client.put('/updateMovieById/invalid', headers={'Authorization': f'Bearer {self.valid_token}'})
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.json)

    def test_missing_fields_with_flask_test_client_with_valid_jwt_token(self):
        mock_data = {
            'title': 'Test Movie',
            'synopsis': '',
            'genre': 'Action',
            'contentRating': 'PG-13',
            'lang': 'English',
            'subtitles': 'English'
        }

        with patch('app.requests.put', return_value=MockResponse(400)) as mock_put:
            response = self.client.put('/updateMovieById/1', json=mock_data,
                                    headers={'Authorization': f'Bearer {self.valid_token}'})

            self.assertEqual(response.status_code, 400)
            # If your application returns a specific message for this error, test for that too
            # self.assertEqual(response.json['message'], "Expected error message")

class TestDeletemoviebyid(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # Attempt to delete a movie with a non-integer movie_id
    def test_delete_movie_non_integer_id(self):
        response = self.client.delete('/deleteMovieById/abc')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        if data:
            self.assertIn("invalid literal for int() with base 10", data.get("error"))

    # Attempt to delete a movie with a negative movie_id
    def test_delete_movie_negative_id(self):
        response = self.client.delete('/deleteMovieById/-1')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        if data:
            self.assertEqual(data.get("message"), "Movie not found, not deleted")


if __name__ == '__main__':
    unittest.main()
