'''
    This file contains utility functions for the identity service.
    These include: checking availability of username and email, validating password, generating random number and generating uuid.
'''

import requests
import re
import secrets 
import uuid

# check if username is available/does not exist in db
def isUsernameAvailable(username):
    data = {"username": username}
    response = requests.post("https://databaseservice/databaseservice/user/check_user", json=data, verify=False)

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
    response = requests.post("https://databaseservice/databaseservice/user/check_email", json=data, verify=False)

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

# ensure that password is valid
def validatePassword(password):
    # Check if password is in the blacklist
    if password in BLACKLISTED_PASSWORDS:
        return False

    # Regular expression pattern check
    # ensure that password is 12 - 32 characters 
    print("password validity: {}".format(12 <= len(password) <= 32))
    return (12 <= len(password) <= 32)

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