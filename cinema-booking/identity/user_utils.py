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
    response = requests.post("http://databaseservice:8085/databaseservice/user/check_user", json=data)

    # if username is not found in db, username is available
    if response.status_code == 404:
        return True 
    
     # username is taken
    else:
        return False 

# check if email is available/does not exist in db
def isEmailAvailable(email):
    data = {"email": email}
    response = requests.post("http://databaseservice:8085/databaseservice/user/check_email", json=data)

    # if email is not found in db, email is available
    if response.status_code == 404:
        return True 
    
     # username is taken
    else:
        return False 

# ensure that username is 3 - 16 characters, and only alphanumeric
def validateUsername(username):
    pattern = "^[a-zA-Z0-9]{3,16}$"
    if re.match(pattern, username):
        return True
    else:
        return False

# ensure that password is 8 - 32 characters with at least 1 uppercase, 1 lowercase, 1 special character and 1 number
def validatePassword(password):
    pattern = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,32}$"

    # check if the password meets the requirements
    if re.match(pattern, password):
        return True
    
    # if password does not meet the requirements
    else:
        return False
    
# generate uuid for inserting into db
def generateUUID():
    return str(uuid.uuid4())

# generate 32 bytes for a 256-bit key
def generateSecretKey():
    secret_key = secrets.token_bytes(32) 
    return secret_key