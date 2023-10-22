from argon2 import PasswordHasher
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
import json
import requests
import user_utils
from credit_card import CreditCard
from api_crypto import decrypt_gcm_to_bytes

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

    # TODO SANITIZE EMAIL & USERNAME

    if not email or not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400

    # ensure username and password contain only allowed characters
    if not user_utils.validateUsername(username):
        return jsonify({"message": "Username does not meet the requirements"}), 400
    
    if not user_utils.validatePassword(password):
        return jsonify({"message": "Password does not meet the requirements"}), 400
    
    # check if username still exists in db
    if not user_utils.isUsernameAvailable(username):
        return jsonify({"message": "Username is already taken"}), 409

    try:
        validate_email(email, check_deliverability=True)

        if not user_utils.isEmailAvailable(email):
            return jsonify({"message": "Email is already in use"}), 409

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
                return jsonify({"message": "JSON response decode error"}), 500
            

    except EmailNotValidError:
        return jsonify({"message": "Email is invalid"}), 400
    
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
    if user_utils.isUsernameAvailable(username):
        return jsonify({"message": "Username or password was incorrect"}), 404

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
        
    
    else:
        # hash password from login form
        dbHash = response.json()["passwordHash"]

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
            additional_claims = {"sessionId": sessionId,
                                "userRole": userRole}

            # generate session token storing username + user role
            sessionToken = create_access_token(identity=username, expires_delta=expirationTime, additional_claims=additional_claims)
        except:
            return jsonify({"message": "Token generation error"}), 500

        # insert session token and expiry into db
        requestData = {
            "sessionId": sessionId,
            "userId": response.json()["userId"],
            "expiryTimestamp": expirationTimestamp,
            "currStatus": "active"
        }

        response = requests.post("http://databaseservice:8085/databaseservice/usersessions/create_user_session", json=requestData)

        # get error message from response if insert unsuccessful
        if response.status_code != 201:
            error_message = response.json().get("message", "Error occurred")
            return jsonify({"message": error_message}), response.status_code
        
        else:
            print("token generated successfully", sessionToken)
            # return session token to client 
            return jsonify({"sessionToken": sessionToken}), 200
############################## END OF LOGIN #########################################



### Credit Card
@app.route("/add_credit_card", methods=["POST"])
def add_credit_card():
    """Receive the following information to add credit card to a user, encrypts card info:
    {
        "session_id":
        "hash":
        "card_number":
        "name":
        "expiry":
    }
    """
    try:
        data = request.get_json()
        # TODO get userID and key (private_key) from db with session_id
        user_id: str
        key: bytes
        ###############
        card_obj = CreditCard(data['card_number'], data['name'], data['expiry'])
        encrypted = bytes.fromhex(data['hash'])
        key = decrypt_gcm_to_bytes(encrypted, key, "PRIVATE")
        b64 = card_obj.encrypt_to_gcm(key)
        
        req_payload = {
            "userID": user_id,
            "blob": b64
        }
    except:
        return jsonify({"error": "69001"}), 500
    
    try:
        response = requests.post("http://databaseservice:8085/databaseservice/creditcard/add_credit_card", json=req_payload)
    except:
        return jsonify({"error": "69002"}), 500
    
    if response.status_code != 201:
        return jsonify({"error": "69003"}), 500
    
    return jsonify({"status": "success"}), 200


@app.route("/get_all_user_credit_cards", methods=["POST"])
def get_all_user_credit_cards():
    """Retrieve card info of a single user from db and decrypt
    Receive POST request:
    {
        "session_id":
        "hash":
    }
    """
    data = request.get_json()
    # TODO get userID and key (private_key) from db with session_id
    user_id: str
    key: bytes
    ###############
    try:
        response = requests.get(f"http://databaseservice:8085/databaseservice/creditcard/get_all_credit_cards/{user_id}")
    except:
        return jsonify({"error": "69004"}), 500
        # TODO more error handling if time allows
    if response.status_code != 201:
        return jsonify({"error": "69005"}), 400
    
    try:
        card_list = response.json()
        decrypted_list = []
        for card in card_list:
            cardobj = CreditCard.decrypt_from_gcm(card['blob'], key)
            dobj = {
                "creditCardId": card["creditCardId"],
                "userId": card["userId"],
                "card_number": cardobj.card_num,
                "name": cardobj.name,
                "expiry": cardobj.expiry
            }
            decrypted_list.append(dobj)
    except:
        return jsonify({"error": "69006"}), 400
    
    return jsonify(decrypted_list), 200


@app.route("/update_credit_card", methods=["PUT"])
def update_credit_card():
    """Relay update request while encrypting card information
    Receive POST request:
    {
        "session_id":
        "hash":
        "credit_card_id":
        "card_number":
        "name":
        "expiry":
    }
    """
    data = request.get_json()
    session_id: str
    hash: str
    credit_card_id: str
    card_num:str
    name:str
    expiry:str
    # TODO get userID and key (private_key) from db with session_id
    user_id: str
    key: bytes
    ###############
    
    # Encrypt card
    card = CreditCard(card_num, name, expiry)
    b64 = card.encrypt_to_gcm(key)
    
    payload = {
        "creditCardId": credit_card_id,
        "blob": b64
    }
    
    try:
        response = requests.put(f"http://databaseservice:8085/databaseservice/creditcard/update_credit_card", json=payload)
    except:
        return jsonify({"error": "69007"}), 500
        # TODO more error handling if time allows
    if response.status_code != 201:
        return jsonify({"error": "69008"}), 400
    
    return jsonify({"status": "success"}), 200


@app.route('/delete_credit_card/<uuid:userId>/<int:creditCardId>', methods=['DELETE'])
def delete_credit_card(userId, creditCardId):
    """Delete card"""
    try:
        response = requests.delete(f"http://databaseservice:8085/databaseservice/creditcard/delete_credit_card_by_id/{userId}/{creditCardId}")
    except:
        return jsonify({"error": "69009"}), 500
        # TODO more error handling if time allows
    if response.status_code != 201:
        return jsonify({"error": "69010"}), 400
    
    return jsonify({"status": "success"}), 200


        
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
