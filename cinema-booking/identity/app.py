import html
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                jwt_required, get_jwt_identity, get_jwt)
from itsdangerous import URLSafeTimedSerializer, TimestampSigner
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

logger.info("Identity Service started")

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# create serializer for generating links
EMAIL_SECRET_KEY = os.getenv("EMAIL_SECRET_KEY")
serializer = URLSafeTimedSerializer(EMAIL_SECRET_KEY)

############################## REGISTRATION #########################################
@app.route("/register", methods=["POST"])
def register():
    # logs registration attempt
    logger.info("Attempting registration...")
    
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
    logger.info("Password has been hashed.")

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
    
    # if email unsuccessful, delete user from db so admin can try again
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
    logger.info("Attempting login...")
    
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
    logger.info("Attempting logout...")
    
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
    logger.info("Basic authentication attempted. (user only)")
    
    # logs login success
    logger.info(f"Login successful")
    
    return jsonify({"message": "Authenticated"}), 200

# check if user is logged in with valid token and verify their role
@app.route("/enhancedAuth", methods=["POST"])
@jwt_required() # verifies jwt integrity + expiry
def enhancedAuth():
    logger.info("Enhanced authentication attempted (user and role).")
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
    try:
        # logs registration attempt
        logger.info("Attempting staff creation...")
        
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

        try:
            # create a unique activation link
            # timestamp is embedded into token, will be checked when token is decoded
            link_type = "activate-staff-account"
            activation_link = user_utils.generateEmailLinks(serializer, username, link_type) 
        except Exception as e:
            print("error generating email link", e)

        print("link generated")

        # store in db activation link in db -> will use this to verify when staff uses their activation link
        userId = user_utils.generateUUID()
        role = "staff"

        # insert all info into db
        data = {
            "userId": userId,
            "email": email,
            "username": username,
            "passwordHash": activation_link,
            "userRole": role,
            "activationLink": activation_link,
            "isActivationLinkUsed": False
        }
        
        response = requests.post("http://databaseservice:8085/databaseservice/user/add_user", json=data)
        if response.status_code != 201:
            return jsonify({"message": "Database insert error"}), 500

        print("added user to db")

        # send email to user with activation link
        requestData = {
                    "email": email,
                    "activation_link": activation_link,
                    "username": username
        }
        response = requests.post("http://email:587/send_staff_activation_email", json=requestData) 

        print("sent to email service")

        if response.status_code != 200:
            # delete user from db
            data = {"userId": userId}
            delete_response = requests.delete("http://databaseservice:8085/databaseservice/user/delete_user", json=data)

            print("delete_response", delete_response)

            return jsonify({"message": "Error sending email"}), 500
        
        else:
            return jsonify({"message": "Email sent"}), 200
    except:
        return jsonify({"message": "Error occurred"}), 500
############################## END OF STAFF REGISTRATION #########################################

############################## VERIFY STAFF ACCOUNT ACTIVATION LINK #########################################
# verifies if the link is valid  before loading form to set password
@app.route("/activate_staff_account/<token>", methods=["GET"])
def activate_staff_account(token):
    try:
        # check if activation link is valid
        expiration_time_in_seconds = 86400 # 24 hour window
        username = serializer.loads(token, salt="activate-staff-account", max_age=expiration_time_in_seconds)

        # if activation link is invalid
        if username is None:
            return jsonify({"message": "Invalid activation link"}), 400

        # if activation link is valid, double check against user info in db
        requestData = {"username": username}
        response = requests.post("http://databaseservice:8085/databaseservice/user/get_user_details", json=requestData)
        
        if response.status_code !=200:
            return jsonify({"message": "Error occurred"}), 500
        
        # get info from db
        db_activationLink = response.json()['activationLink']
        isActivationLinkUsed = response.json()['isActivationLinkUsed']

        # if activation link hasn't used and matches in db, link is valid
        if (isActivationLinkUsed == False and db_activationLink == token):
            return jsonify({"message": "Valid activation link"}), 200

        # else token is invalid
        return jsonify({"message": "Invalid activation link"}), 400

    except:
        return jsonify({"message": "Error occurred"}), 500    
############################## END OF VERIFY STAFF ACCOUNT ACTIVATION LINK #########################################

############################## STAFF SET PASSWORD #########################################
# let staff set their password
@app.route("/staff_set_password/<token>", methods=["PUT"])
def staff_set_password(token):
    try:
        print("in staff set password api")
        # get username from token
        expiration_time_in_seconds = 86400 # 24 hour window
        username = serializer.loads(token, salt="activate-staff-account", max_age=expiration_time_in_seconds)
        
        # if activation link is invalid
        if username is None:
            return jsonify({"message": "Invalid activation link"}), 400
        
        # if activation link is valid, double check against user info in db
        requestData = {"username": username}
        response = requests.post("http://databaseservice:8085/databaseservice/user/get_user_details", json=requestData)
        
        if response.status_code !=200:
            return jsonify({"message": "Error occurred"}), 500
        
        # get info from db
        db_activationLink = response.json()['activationLink']
        isActivationLinkUsed = response.json()['isActivationLinkUsed']

        # if activation link hasn't used and matches in db, link is valid
        if (isActivationLinkUsed == False and db_activationLink == token):
            # get password
            data = request.get_json()
            password = data['password']

            print("received password" + password)
            print("username", username)

            # if password is empty
            if not password:
                return jsonify({"message": "Please fill in all form data"}), 400

            # validate password
            if not user_utils.validatePassword(password):
                print("password not meet reqs")
                return jsonify({"message": "Password does not meet the requirements"}), 400
        
            # hash password
            ph = PasswordHasher()
            hash = ph.hash(password)

            # replace activation link/token hash with password hash in db
            data = {
                "username": username,
                "passwordHash": hash,
                "isActivationLinkUsed": True
            }
            response = requests.put("http://databaseservice:8085/databaseservice/user/update_password_by_username", json=data)
            print("set password response", response.status_code)

            # if database error
            if response.status_code != 200:
                return jsonify({"message": "Database update error"}), 500
            
            else:
                return jsonify({"message": "Password set successfully"}), 200
            
        # else token is invalid
        return jsonify({"message": "Invalid activation link"}), 400
            
    except:
        return jsonify({"message": "Error occurred"}), 500    
############################## END OF STAFF SET PASSWORD #########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
