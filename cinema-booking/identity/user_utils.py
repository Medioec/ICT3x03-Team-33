'''
    This file contains utility functions for the identity service.
    These include: checking availability of username and email, validating password, generating random number and generating uuid.
'''
from zxcvbn import zxcvbn
import hashlib
import requests
import re
import secrets 
import uuid

# required for tls e.g. use session.get(url) to make request instead
session = requests.Session()
client_cert = ('/app/fullchain.pem', '/app/privkey.pem')
ca_cert = '/app/ca-cert.pem'
session.cert = client_cert
session.verify = ca_cert

# check if username is available/does not exist in db
def isUsernameAvailable(username):
    data = {"username": username}
    response = session.post("https://databaseservice/databaseservice/user/check_user", json=data)

    # if username is not found in db, username is available
    if response.status_code == 404:
        return True 
    
     # username is taken
    elif response.status_code == 200:
        return False 
    
    else:
        raise Exception("Error occurred")

# check if email is available/does not exist in db
def isEmailAvailable(email):
    data = {"email": email}
    response = session.post("https://databaseservice/databaseservice/user/check_email", json=data)

    # if email is not found in db, email is available
    if response.status_code == 404:
        return True 
    
     # email is taken
    elif response.status_code == 200:
        return False 

    else:
        raise Exception("Error occurred")

# ensure that username is 3 - 16 characters, and only alphanumeric
def validateUsername(username):
    pattern = "^[a-zA-Z0-9]{3,16}$"
    if re.match(pattern, username):
        return True
    else:
        return False

# Load the wordlist into a set for efficient lookups
with open('/app/wordlist/blacklistedPW.txt', 'r', encoding='latin-1') as f:
    BLACKLISTED_PASSWORDS = set(line.strip() for line in f)

def check_pwned_api(password):
    # Hash the password with SHA-1
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    url = f'https://api.pwnedpasswords.com/range/{first5_char}'
    response = requests.get(url)
    
    # Check if the password has been breached
    return tail in (line.split(':')[0] for line in response.text.splitlines())

def password_strength(password):
    results = zxcvbn(password)
    # returns the strength score
    return results['score']

def validatePassword(password):
    # Check if password is in the blacklist
    if password in BLACKLISTED_PASSWORDS:
        return False, "Password is in the blacklist."

    # # Check password against Have I Been Pwned API
    if check_pwned_api(password):
        return False, "Password has been breached before according to Have I Been Pwned."

    # Check password strength
    strength_score = password_strength(password)
    if strength_score < 3:  # You can set the threshold as you see fit
        return False, f"Password is too weak (score: {strength_score})."

    # Regular expression pattern check
    # ensure that password is 12 - 32 characters 
    if not (12 <= len(password) <= 32):
        return False, "Password length must be between 12 and 32 characters."

    return True, "Password is valid."

# generate uuid for inserting into db
def generateUUID():
    return str(uuid.uuid4())

# generate 32 bytes for a 256-bit key
def generateSecretKey():
    secret_key = secrets.token_bytes(32) 
    return secret_key

# generate a random 16 character string
def generateRandomString():
    return secrets.token_urlsafe(16)