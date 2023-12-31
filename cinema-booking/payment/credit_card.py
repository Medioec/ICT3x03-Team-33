from api_crypto import *
import base64
from cryptography.fernet import Fernet

class CreditCard:
    card_num: str
    name: str
    expiry: str
    cvv: str
    aad = "CARD"
    def __init__(self, card_num, name, expiry, cvv):
        self.card_num = card_num
        self.name = name
        self.expiry = expiry
        self.cvv = cvv
    
    @classmethod
    def decrypt_from_b64_blob(cls, b64: str, hash: bytes, encryption_key: bytes):
        """Use the encrypted hash in JWT and encryption key to decrypt a b64 blob. Returns class object."""
        f = Fernet(encryption_key)
        key = base64.b64decode(f.decrypt(hash) + b"===")
        return cls.decrypt_from_gcm(b64, key)
    
    def encrypt_to_b64_blob(self, hash: bytes, encryption_key: bytes):
        """Use the encrypted hash in JWT and encryption key to encrypt to a b64 blob."""
        f = Fernet(encryption_key)
        key = base64.b64decode(f.decrypt(hash) + b"===")
        return self.encrypt_card_to_gcm(key)
    
    @classmethod
    def decrypt_from_gcm(cls, b64: str, key: bytes):
        """Returns class object"""
        data = base64.b64decode(b64)
        pt = decrypt_gcm_to_plaintext(data, key, cls.aad)
        cc_info = json.loads(pt)
        return cls(cc_info['card_num'], cc_info['name'], cc_info['expiry'], cc_info['cvv'])
    
    def encrypt_card_to_gcm(self, key):
        """Returns base64 encoded encrypted data"""
        dobj = {
            "card_num": self.card_num,
            "name": self.name,
            "expiry": self.expiry,
            "cvv": self.cvv
        }
        b64 = encrypt_json_to_gcm(dobj, key, self.aad)
        return b64
    