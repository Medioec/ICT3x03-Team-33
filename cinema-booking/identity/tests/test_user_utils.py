# test_user_utils.py

import unittest
from unittest.mock import patch
from user_utils import (
    isUsernameAvailable,
    isEmailAvailable,
    validateUsername,
    validatePassword,
    generateUUID,
    generateSecretKey
)

class TestUserUtils(unittest.TestCase):

    @patch('session.post')
    def test_isUsernameAvailable(self, mock_post):
        mock_post.return_value.status_code = 404
        result = isUsernameAvailable('john')
        self.assertTrue(result)

        mock_post.return_value.status_code = 200
        result = isUsernameAvailable('john')
        self.assertFalse(result)

    @patch('session.post')
    def test_isEmailAvailable(self, mock_post):
        mock_post.return_value.status_code = 404
        result = isEmailAvailable('john@example.com')
        self.assertTrue(result)

        mock_post.return_value.status_code = 200
        result = isEmailAvailable('john@example.com')
        self.assertFalse(result)

    def test_validateUsername(self):
        self.assertTrue(validateUsername('john'))
        self.assertFalse(validateUsername('john#'))

    def test_validatePassword(self):
        self.assertTrue(validatePassword('Password@123'))
        self.assertFalse(validatePassword('password'))

    def test_generateUUID(self):
        uuid = generateUUID()
        self.assertEqual(len(uuid), 36)

    def test_generateSecretKey(self):
        secret_key = generateSecretKey()
        self.assertEqual(len(secret_key), 32)

if __name__ == '__main__':
    unittest.main()
