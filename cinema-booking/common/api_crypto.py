import requests
import base64
import json
from Crypto.Cipher import AES
from typing import Union


def encrypted_api_get(url: str, key: bytes):
    response = requests.get(url)
    return decrypt_api_response(response.json(), key, "GET"), response


def encrypted_api_post(url: str, json_input: dict, key: bytes):
    """Creates a post request containing data encrypted with a shared key.
    Returns: Decrypted response string
    Args:
        url (str): url
        json_input (str): json payload to send
        key (bytes): 256 bit key to use for encryption
    """
    json_dict = encrypt_json_to_gcm(json_input, key, "POST")
    response = requests.post(url, json=json_dict)
    
    return decrypt_api_response(response.json(), key, "POST"), response


def encrypted_api_put(url: str, json_input: dict, key: bytes):
    json_dict = encrypt_json_to_gcm(json_input, key, "PUT")
    response = requests.post(url, json=json_dict)
    
    return decrypt_api_response(response.json(), key, "PUT"), response


def encrypt_string_to_gcm(text: str, key: bytes, http_method: str):
    cipher = AES.new(key, AES.MODE_GCM, mac_len=16)
    cipher.update(http_method.encode())
    ct, tag = cipher.encrypt_and_digest(text.encode())
    concat_bytes = cipher.nonce + tag + ct
    b64 = base64.b64encode(concat_bytes).decode()
    payload = {
        "data": b64
    }
    return payload


def encrypt_json_to_gcm(json_input: Union[dict,list], key: bytes, http_method: str):
    cipher = AES.new(key, AES.MODE_GCM, mac_len=16)
    cipher.update(http_method.encode())
    ct, tag = cipher.encrypt_and_digest(json.dumps(json_input).encode())
    concat_bytes = cipher.nonce + tag + ct
    b64 = base64.b64encode(concat_bytes).decode()
    payload = {
        "data": b64
    }
    return payload


def decrypt_api_response(response: dict, key: bytes, http_method: str):
    b64 = response["data"]
    concat_bytes = base64.b64decode(b64)
    nonce = concat_bytes[:16]
    tag = concat_bytes[16:32]
    ct = concat_bytes[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(http_method.encode())
    pt = cipher.decrypt_and_verify(ct, tag)
    return pt.decode()
