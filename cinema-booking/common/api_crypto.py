import requests
import base64
import json
from Crypto.Cipher import AES
from typing import Union


def encrypted_api_get(url: str, key: bytes):
    """Creates a GET request
    Returns: Decrypted response string and original response object
    Args:
        url (str): url        
        key (bytes): 256 bit key to use for encryption
    """
    response = requests.get(url)
    return decrypt_api_response(response.json(), key, "GET"), response


def encrypted_api_post(url: str, json_input: Union[dict,list], key: bytes):
    """Creates a POST request containing data encrypted with a shared key
    Returns: Decrypted response string and original response object
    Args:
        url (str): url
        json_input (dict): json payload to send
        key (bytes): 256 bit key to use for encryption
    """
    json_dict = encrypt_json_to_json_gcm(json_input, key, "POST")
    response = requests.post(url, json=json_dict)
    
    return decrypt_api_response(response.json(), key, "POST"), response


def encrypted_api_put(url: str, json_input: Union[dict,list], key: bytes):
    """Creates a PUT request containing data encrypted with a shared key
    Returns: Decrypted response string
    Args:
        url (str): url
        json_input (dict): json payload to send
        key (bytes): 256 bit key to use for encryption
    """
    json_dict = encrypt_json_to_json_gcm(json_input, key, "PUT")
    response = requests.post(url, json=json_dict)
    
    return decrypt_api_response(response.json(), key, "PUT"), response


def encrypt_string_to_gcm(text: str, key: bytes, http_method: str):
    """Encrypt a text string into a dictionary object containing the ciphertext
    Args:
        text (str): text to encrypt
        key (bytes): 256bit key
        http_method (str): GET, POST or PUT, depending on the request

    Returns:
        Python dictionary object with a single key "data" with value of the ciphertext
        Output format: { "data": "<base64 ciphertext>" }
    """
    cipher = AES.new(key, AES.MODE_GCM, mac_len=16)
    cipher.update(http_method.encode())
    ct, tag = cipher.encrypt_and_digest(text.encode())
    concat_bytes = cipher.nonce + tag + ct
    b64 = base64.b64encode(concat_bytes).decode()
    payload = {
        "data": b64
    }
    return payload


def encrypt_json_to_json_gcm(input_obj: Union[dict,list], key: bytes, http_method: str):
    """Convert a python dictionary or list object into json and encrypts json into a dictionary object containing the ciphertext
    Args:
        input_obj (dict, list): object to encrypt
        key (bytes): 256bit key
        http_method (str): GET, POST, PUT, DELETE depending on the request

    Returns:
        Python dictionary object with a single key "data" with value of the ciphertext
        Output format: { "data": "<base64 ciphertext>" }
    """
    cipher = AES.new(key, AES.MODE_GCM, mac_len=16)
    cipher.update(http_method.encode())
    ct, tag = cipher.encrypt_and_digest(json.dumps(input_obj).encode())
    concat_bytes = cipher.nonce + tag + ct
    b64 = base64.b64encode(concat_bytes).decode()
    payload = {
        "data": b64
    }
    return payload


def encrypt_json_to_gcm(input_obj: Union[dict,list], key: bytes, aad: str):
    """Convert a python dictionary or list object into json and encrypts json into base64 encoded ciphertext
    Args:
        input_obj (dict, list): object to encrypt
        key (bytes): 256bit key
        aad (str): additional text data for verification

    Returns:
        Encrypted bytes with the structure: <nonce><tag><ct>
    """
    cipher = AES.new(key, AES.MODE_GCM, mac_len=16)
    cipher.update(aad.encode())
    ct, tag = cipher.encrypt_and_digest(json.dumps(input_obj).encode())
    concat_bytes = cipher.nonce + tag + ct
    return base64.b64encode(concat_bytes).decode()


def decrypt_api_response(response: dict, key: bytes, http_method: str):
    b64 = response["data"]
    concat_bytes = base64.b64decode(b64)
    return decrypt_gcm_to_plaintext(concat_bytes, key, http_method)


def decrypt_gcm_to_plaintext(encrypted_ct: bytes, key: bytes, aad: str):
    nonce = encrypted_ct[:16]
    tag = encrypted_ct[16:32]
    ct = encrypted_ct[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(aad.encode())
    pt = cipher.decrypt_and_verify(ct, tag)
    return pt.decode()

def decrypt_gcm_to_bytes(encrypted_ct: bytes, key: bytes, aad: str):
    nonce = encrypted_ct[:16]
    tag = encrypted_ct[16:32]
    ct = encrypted_ct[32:]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    cipher.update(aad.encode())
    pt = cipher.decrypt_and_verify(ct, tag)
    return pt