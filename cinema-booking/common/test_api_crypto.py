import unittest
from api_crypto import (
    encrypted_api_get,
    encrypted_api_post,
    encrypted_api_put,
    encrypt_string_to_gcm,
    encrypt_json_to_json_gcm,
    encrypt_json_to_gcm,
    decrypt_api_response,
    decrypt_gcm_to_plaintext,
    decrypt_gcm_to_bytes,
)
from Crypto.Cipher import AES
import base64

class TestApiCrypto(unittest.TestCase):

    def setUp(self):
        self.key = b'Sixteen byte key'
    
    def test_encrypt_string_to_gcm(self):
        # Test data
        text = "Hello World"
        http_method = "GET"
        
        # Test
        encrypted_data = encrypt_string_to_gcm(text, self.key, http_method)
        self.assertIsInstance(encrypted_data, dict)
        self.assertIn("data", encrypted_data)
    
    def test_encrypt_json_to_json_gcm(self):
        # Test data
        input_data = {"message": "Hello World"}
        http_method = "POST"
        
        # Test
        encrypted_data = encrypt_json_to_json_gcm(input_data, self.key, http_method)
        self.assertIsInstance(encrypted_data, dict)
        self.assertIn("data", encrypted_data)
    
    def test_encrypt_json_to_gcm(self):
        # Test data
        input_data = {"message": "Hello World"}
        aad = "POST"
        
        # Test
        encrypted_data = encrypt_json_to_gcm(input_data, self.key, aad)
        self.assertIsInstance(encrypted_data, str)
    
    def test_decrypt_gcm_to_plaintext(self):
        # Test data
        text = "Hello World"
        http_method = "GET"
        
        # Test
        encrypted_data = encrypt_string_to_gcm(text, self.key, http_method)
        decrypted_text = decrypt_gcm_to_plaintext(base64.b64decode(encrypted_data["data"]), self.key, http_method)
        self.assertEqual(decrypted_text, text)
    
    def test_decrypt_gcm_to_bytes(self):
        # Test data
        input_data = {"message": "Hello World"}
        aad = "POST"
        
        # Test
        encrypted_data = encrypt_json_to_gcm(input_data, self.key, aad)
        decrypted_bytes = decrypt_gcm_to_bytes(base64.b64decode(encrypted_data), self.key, aad)
        self.assertEqual(decrypted_bytes, json.dumps(input_data).encode())

if __name__ == '__main__':
    unittest.main()
