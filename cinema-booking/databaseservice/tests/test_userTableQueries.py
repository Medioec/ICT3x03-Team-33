import unittest
from userTableQueries import add_user, get_user_details, check_user, check_email
from flask import Flask

class UserTableQueriesTest(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        self.client = app.test_client()
        self.data = {
            "userId": "1",
            "email": "test@email.com",
            "username": "testuser",
            "passwordHash": "hashedpassword",
            "userRole": "user",
        }
    
    def test_add_user(self):
        response = self.client.post('/add_user', json=self.data)
        self.assertEqual(response.status_code, 201)
        
    def test_get_user_details(self):
        self.client.post('/add_user', json=self.data)
        response = self.client.post('/get_user_details', json={"username": "testuser"})
        self.assertEqual(response.status_code, 200)
        
    def test_check_user(self):
        self.client.post('/add_user', json=self.data)
        response = self.client.post('/check_user', json={"username": "testuser"})
        self.assertEqual(response.status_code, 200)
        
    def test_check_email(self):
        self.client.post('/add_user', json=self.data)
        response = self.client.post('/check_email', json={"email": "test@email.com"})
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
