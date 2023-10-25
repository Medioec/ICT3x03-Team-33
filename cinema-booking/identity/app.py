from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity)
import json
import requests
import user_utils
import base64

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = user_utils.generateSecretKey()

jwt = JWTManager(app)

############################## REGISTRATION #########################################
@app.route("/register", methods=["POST"])
def register():
    # get data from registration form
    data = request.get_json()
    email = data['email']
    username = data['username']
    password = data['password']

    # Sanitize email and username
    #email = html.escape(email)
    #username = html.escape(username)

    if not email or not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400

    # ensure username and password contain only allowed characters
    if not user_utils.validateUsername(username):
        return jsonify({"message": "Username does not meet the requirements"}), 400
    
    if not user_utils.validatePassword(password):
        return jsonify({"message": "Password does not meet the requirements"}), 400
    
    # check if username exists in db
    try:
        if not user_utils.isUsernameAvailable(username):
            return jsonify({"message": "Username is already taken"}), 409
    
    except Exception as e:
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
        return jsonify({"message": "Registration successful"}), 200
    
    # if insert unsuccessful, return error message from databaseservice
    else:
        try:
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
    # get data from login form
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400
    
    # if username does not exist in db
    try:
        if user_utils.isUsernameAvailable(username):
            return jsonify({"message": "Username or password was incorrect"}), 404
    except Exception as e:
        return jsonify({"message": {str(e)}}), 500


    # get password hash and role from db
    requestData = {"username": username}
    response = requests.post("http://databaseservice:8085/databaseservice/usersessions/get_userId_hash_role", json=requestData)

    if response.status_code != 200:
        # get error message from response. if no message, use default "Error occurred"
        try:
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
    phlogin = PasswordHasher(parallelism=1, memory_cost=1048576, time_cost=4, salt_len=16)
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
        error_message = response.json().get("message", "Error occurred")
        return jsonify({"message": error_message}), response.status_code
    
    else:
        print("token generated successfully", sessionToken)
        # return session token to client 
        return jsonify({"sessionToken": sessionToken}), 200
############################## END OF LOGIN #########################################



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
