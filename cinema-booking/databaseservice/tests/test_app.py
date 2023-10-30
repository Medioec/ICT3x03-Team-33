import unittest
from flask_testing import TestCase
from app import app

class AppTestCase(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_index(self):
        response = self.client.get('/databaseservice/user')
        self.assertEqual(response.status_code, 200)

    def test_user_sessions(self):
        response = self.client.get('/databaseservice/usersessions')
        self.assertEqual(response.status_code, 200)

    def test_moviedetails(self):
        response = self.client.get('/databaseservice/moviedetails')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
