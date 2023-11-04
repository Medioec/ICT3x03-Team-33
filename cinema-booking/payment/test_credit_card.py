# test_credit_card.py

import unittest
from unittest.mock import MagicMock, patch
from credit_card import CreditCard

class TestCreditCard(unittest.TestCase):

    def setUp(self):
        self.b64 = 'base64_blob'
        self.hash = b'encrypted_hash'
        self.encryption_key = b'encryption_key'
        self.plaintext = '{"card_num": "1234", "name": "John Doe", "expiry": "12/34", "cvv": "567"}'
        self.card = CreditCard('1234', 'John Doe', '12/34', '567')

    @patch('credit_card.Fernet')
    @patch('credit_card.base64')
    @patch('credit_card.decrypt_gcm_to_plaintext')
    def test_decrypt_from_b64_blob(self, mock_decrypt, mock_base64, mock_fernet):
        # Setup mocks
        mock_decrypt.return_value = self.plaintext
        mock_base64.b64decode.return_value = b'decrypted_hash'
        fernet_instance = MagicMock()
        fernet_instance.decrypt.return_value = b'decrypted_hash'
        mock_fernet.return_value = fernet_instance

        # Call the method
        card = CreditCard.decrypt_from_b64_blob(self.b64, self.hash, self.encryption_key)

        # Assert
        self.assertEqual(card.card_num, '1234')
        self.assertEqual(card.name, 'John Doe')
        self.assertEqual(card.expiry, '12/34')
        self.assertEqual(card.cvv, '567')

        # Verify mock calls
        mock_decrypt.assert_called_once_with(self.plaintext, b'decrypted_hash', CreditCard.aad)
        mock_base64.b64decode.assert_called_once_with(fernet_instance.decrypt.return_value + b'===')
        fernet_instance.decrypt.assert_called_once_with(self.hash)
        mock_fernet.assert_called_once_with(self.encryption_key)

    @patch('credit_card.Fernet')
    @patch('credit_card.base64')
    @patch('credit_card.encrypt_json_to_gcm')
    def test_encrypt_to_b64_blob(self, mock_encrypt, mock_base64, mock_fernet):
        # Setup mocks
        mock_encrypt.return_value = self.b64
        mock_base64.b64decode.return_value = b'decrypted_hash'
        fernet_instance = MagicMock()
        fernet_instance.decrypt.return_value = b'decrypted_hash'
        mock_fernet.return_value = fernet_instance

        # Call the method
        b64_blob = self.card.encrypt_to_b64_blob(self.hash, self.encryption_key)

        # Assert
        self.assertEqual(b64_blob, self.b64)

        # Verify mock calls
        mock_encrypt.assert_called_once_with({
            "card_num": '1234',
            "name": 'John Doe',
            "expiry": '12/34',
            "cvv": '567'
        }, b'decrypted_hash', CreditCard.aad)
        mock_base64.b64decode.assert_called_once_with(fernet_instance.decrypt.return_value + b'===')
        fernet_instance.decrypt.assert_called_once_with(self.hash)
        mock_fernet.assert_called_once_with(self.encryption_key)

    @patch('credit_card.decrypt_gcm_to_plaintext')
    def test_decrypt_from_gcm(self, mock_decrypt):
        # Setup mocks
        mock_decrypt.return_value = self.plaintext

        # Call the method
        card = CreditCard.decrypt_from_gcm(self.b64, self.encryption_key)

        # Assert
        self.assertEqual(card.card_num, '1234')
        self.assertEqual(card.name, 'John Doe')
        self.assertEqual(card.expiry, '12/34')
        self.assertEqual(card.cvv, '567')

        # Verify mock calls
        mock_decrypt.assert_called_once_with(self.b64, self.encryption_key, CreditCard.aad)

    @patch('credit_card.encrypt_json_to_gcm')
    def test_encrypt_card_to_gcm(self, mock_encrypt):
        # Setup mocks
        mock_encrypt.return_value = self.b64

        # Call the method
        b64_blob = self.card.encrypt_card_to_gcm(self.encryption_key)

        # Assert
        self.assertEqual(b64_blob, self.b64)

        # Verify mock calls
        mock_encrypt.assert_called_once_with({
            "card_num": '1234',
            "name": 'John Doe',
            "expiry": '12/34',
            "cvv": '567'
        }, self.encryption_key, CreditCard.aad)

if __name__ == '__main__':
    unittest.main()
