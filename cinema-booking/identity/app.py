import html
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity, get_jwt)
import json
import os 
import requests
import user_utils
import base64
import logging

app = Flask(__name__)
CORS(app)

# Create or get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# File handler
file_handler_path = './logs/identityServiceLogs.log'
file_handler = logging.FileHandler(file_handler_path)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# Stream (console) handler for stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)

logger.info(f"Identity Service started")

app.config['JWT_SECRET_KEY'] = user_utils.generateSecretKey()

jwt = JWTManager(app)

############################## REGISTRATION #########################################
@app.route("/register", methods=["POST"])
def register():
    # logs registration attempt
    logger.info(f"Attempting registration...")
    
    # get data from registration form
    data = request.get_json()
    email = data['email']
    username = data['username']
    password = data['password']

    # Sanitize email and username
    email = html.escape(email)
    username = html.escape(username)
    
    # logs sanitized user input
    logger.info(f"Sanitized user input: Email: {email}, Username: {username}")

    if not email or not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400

    # ensure username and password contain only allowed characters
    if not user_utils.validateUsername(username):
        return jsonify({"message": "Username does not meet the requirements"}), 400
    
    if not user_utils.validatePassword(password):
        print("password not meet reqs")
        return jsonify({"message": "Password does not meet the requirements"}), 400
    
    # check if username exists in db
    try:
        if not user_utils.isUsernameAvailable(username):
            # log registration failure due to username already taken
            logger.warning(f"Username '{username}' is already taken.")
            return jsonify({"message": "Username is already taken"}), 409
    
    except Exception as e:
        logger.error(f"Error during username availability check: {str(e)}")
        return jsonify({"message": {str(e)}}), 500
    
    # check if email address is valid
    try:
        validate_email(email, check_deliverability=True)

    except EmailNotValidError:
        return jsonify({"message": "Email is invalid"}), 400

    # check if email address is still available 
    try:
        if not user_utils.isEmailAvailable(email):
            return jsonify({"message": "Email is already in use"}), 409
    except Exception as e:
        return jsonify({"message": {str(e)}}), 500

    ph = PasswordHasher()
    hash = ph.hash(password)
    
    # logs that password has been hashed
    logger.info(f"Password has been hashed.")

    role = "member"
    userId = user_utils.generateUUID()
    
    data = {
        "userId": userId,
        "email": email,
        "username": username,
        "passwordHash": hash,
        "userRole": role
    }

    response = requests.post("http://databaseservice:8085/databaseservice/user/add_user", json=data)
    
    if response.status_code == 201:
        logger.info(f"User '{username}' registered successfully!")
        return jsonify({"message": "Registration successful"}), 200
    
    # if insert unsuccessful, return error message from databaseservice
    else:
        try:
            logger.error(f"Registration failed with username {username}, email {email}, role {role}. Error during registration: {response.json()['message']}")
            response_json = response.json()
            # get error message from response. if no message, use default "Error occurred"
            error_message = response_json.get("message", "Error occurred")
            return jsonify({"message": error_message}), response.status_code
    
        except json.JSONDecodeError as e:
            return jsonify({"message": "Error occurred"}), 500
        
############################## END OF REGISTRATION #########################################


############################## LOGIN #########################################
@app.route("/login", methods=["POST"])
def login():
    # logs login attempt
    logger.info(f"Attempting login...")
    
    # get data from login form
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400
    
    # if username does not exist in db
    try:
        if user_utils.isUsernameAvailable(username):
            # log login failure
            logger.warning(f"Login attempt with non-existent username '{username}'.")
            return jsonify({"message": "Username or password was incorrect"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


    # get password hash and role from db
    requestData = {"username": username}
    response = requests.post("http://databaseservice:8085/databaseservice/usersessions/get_userId_hash_role", json=requestData)

    if response.status_code != 200:
        # get error message from response. if no message, use default "Error occurred"
        try:
            # log login failure
            logger.error(f"Login failed with username {username}. Error: {response.json()['message']}")
            response_json = response.json()
            # get error message from response. if no message, use default "Error occurred"
            error_message = response_json.get("message", "Error occurred")
            return jsonify({"message": error_message}), response.status_code
    
        except json.JSONDecodeError as e:
            return jsonify({"message": "JSON response decode error"}), 500
    
    # password hash from DB
    dbHash = response.json()["passwordHash"]
    
    # Generate a Fernet encryption key using password
    fix_salt = b'\x00' * 16
    phlogin = PasswordHasher(parallelism=1, memory_cost=262144, time_cost=4, salt_len=16)
    loginhash = phlogin.hash(password, salt = fix_salt)
    
    # Extract hash only from raw hash raw-> $argon2i$v=19$m=16,t=2,p=1$YXNmYXNmc2E$lDi8mox+g9cUyEIcC/NDFqZlJmLvZ4doW16LzRiHMVU
    loginhash = loginhash.split("$")[5]

    # generate encryption key
    fernet_keystring = Fernet.generate_key().decode()
    # Create dictionary with encoded, then serialize the dictionary
    #fernet_json = json.dumps({"fernet_key": fernet_str})
    cipher_suite = Fernet(fernet_keystring)
    

    # Example of Encryption 
    # encrypted_data = cipher_suite.encrypt(b"Sensitive Data")
    
    # Encrypt the user_passwordhash_salted
    encrypted_hash = cipher_suite.encrypt(loginhash.encode())
    
    # Example of Decryption
    # decrypted_data = cipher_suite.decrypt(encrypted_data)
    
    try:
        # verify password
        ph = PasswordHasher()
        ph.verify(dbHash, password)
    
    # if password hashes do not match, throw error
    except Exception as e:
        # log login failure
        logger.error(f"Password verification failed for username '{username}'. Reason: {e}")

        print(f"Exception during password verification: {e}")
        return jsonify({"message": "Username or password was incorrect"}), 404

    # generate session token
    try:
        # set token expiration to 15 minutes and get expiry timestamp in iso format
        expirationTime = timedelta(minutes=15)
        current_time = datetime.utcnow()
        expirationTimestamp = current_time + expirationTime
        expirationTimestamp = expirationTimestamp.isoformat()

        # generate session id
        sessionId = user_utils.generateUUID()
        
        # get user role
        userRole = response.json()["userRole"]
        additional_claims = {
            "sessionId": sessionId,
            "userRole": userRole,
            "hash": encrypted_hash.decode()
        }

        # generate session token storing username + user role
        sessionToken = create_access_token(identity=sessionId, expires_delta=expirationTime, additional_claims=additional_claims)
    except:
        return jsonify({"message": "Token generation error"}), 500
    
    # After generating the encryption key (fernet_key)
    # insert session token, sessionID, encryption_key and expiry into db
    requestData = {
        "fernet_key": fernet_keystring,
        "sessionId": sessionId,
        "userId": response.json()["userId"],
        "expiryTimestamp": expirationTimestamp,
        "currStatus": "active",
        #"encrypted_dbHash": encrypted_dbHash  # Store the encrypted hash
    }
    
    #response = requests.post("http://databaseservice:8085/databaseservice/usersessions/create_user_session", json=requestData)
    response = requests.post("http://databaseservice:8085/databaseservice/usersessions/store_key_in_database", json=requestData)

    # get error message from response if insert unsuccessful
    if response.status_code != 201:
        # log login failure
        logger.error(f"Login failed with username {username}. Error: {response.json()['message']}")
        error_message = response.json().get("message", "Error occurred")
        return jsonify({"message": error_message}), response.status_code
    
    else:
        print("token generated successfully", sessionToken)
        # return session token to client 
        return jsonify({"sessionToken": sessionToken}), 200
############################## END OF LOGIN #########################################

############################## LOGOUT #########################################
@app.route("/logout", methods=["PUT"])
@jwt_required() # verifies jwt integrity + expiry
def logout():
    # logs logout attempt
    logger.info(f"Attempting logout...")
    
    # get sessionId from jwt
    sessionId = get_jwt_identity()

    if not sessionId:
        # log logout failure
        logger.error(f"Logout failed. Attempted logout without token")
        return jsonify({"message": "Error: No token sent"}), 500
    
    # set status to inactive
    currStatus = "inactive"

    # set session status to inactive in db
    requestData = {"sessionId": sessionId, "currStatus": currStatus}
    
    response = requests.put("http://databaseservice:8085/databaseservice/usersessions/update_session_status_by_id", json=requestData)

    if response.status_code == 200:
        print("logout successful")
        # log logout success
        logger.info(f"Logout successful")
        return jsonify({"message": "Logout successful"}), 200
    else:
        # log database error
        logger.error(f"Logout failed due to database error. Error: {response.json()['message']}")
        return jsonify({"message": "Database error"}), 500
############################## END OF LOGOUT #########################################

############################## AUTH #########################################
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    # log unauthorized access
    logger.error(f"Unauthorized access detected")
    print("unauthorized callback")
    return jsonify({"message": "Unauthorized access"}), 401

# check if user is logged in with valid token
@app.route("/basicAuth", methods=["POST"])
@jwt_required() # verifies jwt integrity + expiry
def basicAuth():
    #logs authentication attempt
    logger.info(f"Basic authentication attempted. (user only)")
    
    # logs login success
    logger.info(f"Login successful")
    
    return jsonify({"message": "Authenticated"}), 200

# check if user is logged in with valid token and verify their role
@app.route("/enhancedAuth", methods=["POST"])
@jwt_required() # verifies jwt integrity + expiry
def enhancedAuth():
    logger.info(f"Enhanced authentication attempted (user and role).")
    try:
        # get session id + role from token
        sessionId = get_jwt_identity()
        token = get_jwt()
        role = token["userRole"]
            
        # check against db to see if it's a legit token
        requestData = {"sessionId": sessionId}
        response = requests.post("http://databaseservice:8085/databaseservice/usersessions/get_user_session", json=requestData)
        
        if response.status_code != 200:
            # log authentication failure
            logger.error(f"Authentication failed due to database error Error: {response.json()['message']}")
            return jsonify({"message": "Database error"}), 500

        # get userId from db
        userId = response.json()["userId"]
        print("userId", userId)
        
        # check that the user role in the db matches the user role in the token
        requestData = {"userId": userId}
        response = requests.post("http://databaseservice:8085/databaseservice/usersessions/get_role_by_id", json=requestData)    
        dbRole = response.json()["userRole"]

        print("token role", role)
        print("db role", dbRole)

        if role != dbRole:
            # log unauthorized access
            logger.error(f"Unauthorized access detected")
            return jsonify({"message": "Invalid token"}), 401
        else:
            # log authentication success
            logger.info(f"Authentication successful")
            print("authenticated")
            return jsonify({"message": "Authenticated"}), 200
    
    except:
        return jsonify({"message": "Error occurred"}), 500
############################## END OF AUTH #########################################

############################## STAFF REGISTRATION #########################################
@app.route("/create_staff", methods=["POST"])
@jwt_required() # can only be accessed by admins
def create_staff():
    # logs registration attempt
    logger.info(f"Attempting staff creation...")
    
    # get data from registration form
    data = request.get_json()
    email = data['email']
    username = data['username']

    # Sanitize email and username
    email = html.escape(email)
    username = html.escape(username)
    
    # logs sanitized user input
    logger.info(f"Sanitized user input: Email: {email}, Username: {username}")

    if not email or not username:
        return jsonify({"message": "Please fill in all form data"}), 400

    # ensure username and password contain only allowed characters
    if not user_utils.validateUsername(username):
        return jsonify({"message": "Username does not meet the requirements"}), 400
    
    # check if username exists in db
    try:
        if not user_utils.isUsernameAvailable(username):
            # log registration failure due to username already taken
            logger.warning(f"Username '{username}' is already taken.")
            return jsonify({"message": "Username is already taken"}), 409
    
    except Exception as e:
        logger.error(f"Error during username availability check: {str(e)}")
        return jsonify({"message": {str(e)}}), 500
    
    # check if email address is valid
    try:
        validate_email(email, check_deliverability=True)

    except EmailNotValidError:
        return jsonify({"message": "Email is invalid"}), 400

    # check if email address is still available 
    try:
        if not user_utils.isEmailAvailable(email):
            return jsonify({"message": "Email is already in use"}), 409
    except Exception as e:
        return jsonify({"message": {str(e)}}), 500

    # TODO
    # CREATE UNIQUE ACTIVATION LINK + EXPIRY
    # SEND EMAIL TO USER WITH ACTIVATION LINK

    ph = PasswordHasher()
    hash = ph.hash(password)
    
    # logs that password has been hashed
    logger.info(f"Password has been hashed.")

    role = "staff"
    userId = user_utils.generateUUID()
    
    data = {
        "userId": userId,
        "email": email,
        "username": username,
        "passwordHash": hash,
        "userRole": role
    }

    response = requests.post("http://databaseservice:8085/databaseservice/user/add_user", json=data)
    
    if response.status_code == 201:
        logger.info(f"User '{username}' registered successfully!")
        return jsonify({"message": "Registration successful"}), 200
    
    # if insert unsuccessful, return error message from databaseservice
    else:
        try:
            logger.error(f"Registration failed with username {username}, email {email}, role {role}. Error during registration: {response.json()['message']}")
            response_json = response.json()
            # get error message from response. if no message, use default "Error occurred"
            error_message = response_json.get("message", "Error occurred")
            return jsonify({"message": error_message}), response.status_code
    
        except json.JSONDecodeError as e:
            return jsonify({"message": "Error occurred"}), 500
        
############################## END OF STAFF REGISTRATION #########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
