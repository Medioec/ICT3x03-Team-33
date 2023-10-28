# test_app.py

import unittest
from app import generate_email

class TestApp(unittest.TestCase):

    def test_generate_email(self):
        username = 'john'
        domain = 'example.com'
        email = generate_email(username, domain)
        self.assertEqual(email, 'john@example.com')

if __name__ == '__main__':
    unittest.main()
