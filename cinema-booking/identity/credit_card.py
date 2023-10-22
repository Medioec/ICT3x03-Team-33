from api_crypto import *
import base64

class CreditCard:
    credit_card_id: str
    card_num: str
    name: str
    expiry: str
    aad = "CARD"
    def __init__(self, card_num, name, expiry):
        self.card_num = card_num
        self.name = name
        self.expiry = expiry
    
    @classmethod
    def decrypt_from_gcm(cls, b64: str, key: bytes):
        """Returns class object"""
        data = base64.b64decode(b64)
        pt = decrypt_gcm_to_plaintext(data, key, cls.aad)
        cc_info = json.loads(pt)
        return cls(cc_info['card_num'], cc_info['name'], cc_info['expiry'])
    
    def encrypt_to_gcm(self, key):
        """Returns base64 encoded encrypted data"""
        dobj = {
            "card_num": self.card_num,
            "name": self.name,
            "expiry": self.expiry
        }
        b64 = encrypt_json_to_gcm(dobj, key, self.aad)
        return b64
    