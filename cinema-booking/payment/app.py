from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity, get_jwt)
import os
import requests
import user_utils
from credit_card import *

app = Flask(__name__)  
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

# required for tls e.g. use session.get(url) to make request instead
session = requests.Session()
client_cert = ('/app/fullchain.pem', '/app/privkey.pem')
ca_cert = '/app/ca-cert.pem'
session.cert = client_cert
session.verify = ca_cert

#####   throw error when JWT token is not valid     #####
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("unauthorized callback")
    return jsonify({"message": "Unauthorized access"}), 401
#####   End of throw error when JWT token is not valid     #####

@app.route('/makePayment', methods=["POST"])
@jwt_required()
def makePayment():
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500
    
    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}    
    response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
    userId = response.json()["userId"]
    
    # Retrieve payment details from request
    data = request.get_json()
    creditCardId = data['creditCardId']
    
    url = f"https://databaseservice/databaseservice/creditcard/get_credit_card_by_id/{userId}/{creditCardId}"
    response = session.get(url)
    
    if response.status_code == 404:
        return jsonify({"message": "Credit card not found"}), 404
    elif response.status_code == 403:
        return jsonify({"message": "Access denied: No permissions"}), 403
    else:
        blob = response.json()['blob']

    token = get_jwt()
    hash = token["hash"]
    
    # Get session encryption key from db here
    payload = {
        "sessionId": sessionId
    }
    try:
        response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=payload)
    except:
        return jsonify({"error": "690001"})
    if response.status_code != 200:
        return jsonify({"error": "690002"})
    
    b64key = response.json()["encryptionKey"]
    encryption_key = b64key.encode()
    
    # decrypt card blob with encryption key and hash
    card = CreditCard.decrypt_from_b64_blob(blob, hash, encryption_key)
    
    # validate cc information
    if not user_utils.validateCreditCardNumber(card.card_num):
        return jsonify({"message": "Invalid credit card number"}), 400
    if not user_utils.validateCreditCardName(card.name):
        return jsonify({"message": "Invalid credit card name"}), 400
    if not user_utils.validateCreditCardExpiry(card.expiry):
        return jsonify({"message": "Invalid credit card expiry date"}), 400
    if not user_utils.validateCvv(card.cvv):
        return jsonify({"message": "Invalid CVV"}), 400
    
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        # Process payment after validation
        transaction_id = user_utils.processPayment()  # This is hardcoded as we can't actually process payment

        # Get current datetime
        transaction_date_time = user_utils.getTransactionDateTime()

        # Form JSON data to be sent to the databaseservice
        transaction_data = {
            "transactionId": transaction_id,
            "creditCardId": creditCardId,
            "transactionDateTime": transaction_date_time
        }

        # Make an HTTP POST request to the databaseservice to create the transaction
        response = session.post("https://databaseservice/databaseservice/transactions/create_transaction", json=transaction_data)

        # Transaction was added successfully, return the response from the databaseservice
        if response.status_code == 201:
            return response.json(), 201
        # Duplicate transaction ID detected, regenerate and retry
        elif response.status_code == 409:
            retry_count += 1
            continue
        else:
            # Handle other errors
            return jsonify({"message": "Error processing the payment"}), 500

    # If we reach this point, we've exhausted all retry attempts, break out of loop to prevent infinite loop
    return jsonify({"message": "Exceeded maximum retry attempts"}), 500

###################################################################################################################################

@app.route('/addCreditCard', methods=["POST"])
@jwt_required()
def addCreditCard():
    # Retrieve credit card details from request
    data = request.get_json()
    creditCardNumber = data['creditCardNumber']
    creditCardName = data['creditCardName']
    creditCardExpiry = data['creditCardExpiry']
    cvv = data['cvv']
    
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500

    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}    
    response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
    
    # set information retrieved via sessionId
    userId = response.json()["userId"]
    
    token = get_jwt()
    hash = token["hash"]

    # validate cc information
    if not user_utils.validateCreditCardNumber(creditCardNumber):
        return jsonify({"message": "Invalid credit card number"}), 400
    if not user_utils.validateCreditCardName(creditCardName):
        return jsonify({"message": "Invalid credit card name"}), 400
    if not user_utils.validateCreditCardExpiry(creditCardExpiry):
        return jsonify({"message": "Invalid credit card expiry date"}), 400
    if not user_utils.validateCvv(cvv):
        return jsonify({"message": "Invalid CVV"}), 400
    
    # Get session encryption key from db here
    payload = {
        "sessionId": sessionId
    }
    try:
        response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=payload)
    except:
        return jsonify({"error": "690101"})
    if response.status_code != 200:
        return jsonify({"error": "690102"})
    
    rjson = response.json()
    b64key = rjson["encryptionKey"]
    encryption_key = b64key.encode()
    
    userId = rjson['userId']
        
    # use encryption key and hash to encrypt credit card info into blob (b64 cos cannot send binary)
    card_obj = CreditCard(creditCardNumber, creditCardName, creditCardExpiry, cvv)
    b64 = card_obj.encrypt_to_b64_blob(hash, encryption_key)
    
    # Form JSON data to be sent to the databaseservice
    credit_card_data = {
        "userId": userId,
        "blob": b64,
        # cvv not stored in database
    }
    
    # Make an HTTP POST request to the databaseservice to create the credit card
    response = session.post("https://databaseservice/databaseservice/creditcard/add_credit_card", json=credit_card_data)
    
    if response.status_code == 201:
        # Credit card was added successfully, return the response from the databaseservice
        return response.json(), 201
    elif response.status_code == 409:
        # Duplicate credit card detected, return HTTP 409 Conflict
        return jsonify({"message": "Credit card already exists"}), 409
    else:
        # Handle other errors
        return jsonify({"message": "Error adding the credit card"}), 500

###################################################################################################################################

@app.route('/getOneCreditCard', methods=["POST"])
@jwt_required()
def getCreditCard(userId, creditCardId):
    data = request.get_json()
    creditCardId = data['creditCardId']
    userId = data['userId']
    
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500
    
    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}    
    response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
    
    # set information retrieved via sessionId
    userId = response.json()["userId"]
    
    token = get_jwt()
    hash = token["hash"]
    
    # Make an HTTP GET request to the databaseservice to retrieve the credit card
    url = f"https://databaseservice/databaseservice/creditcard/get_credit_card_by_id/{userId}/{creditCardId}"
    response = session.get(url)
    
    if response.status_code == 200:
        # Credit cards were retrieved successfully, return the response from the databaseservice
        cc = response.json()
        # Get session encryption key from db here
        payload = {
            "sessionId": sessionId
        }
        try:
            response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=payload)
        except:
            return jsonify({"error": "690201"})
        if response.status_code != 200:
            return jsonify({"error": "690202"})
        
        b64key = response.json()["encryptionKey"]
        encryption_key = b64key.encode()
        
        for card in cc:
            creditCardId = card["creditCardId"]
            blob = card["blob"]
            dec_card = CreditCard.decrypt_from_b64_blob(blob, hash, encryption_key)
            ccobj = {
                "creditCardId": creditCardId,
                "creditCardNumber": dec_card.card_num,
                "creditCardName": dec_card.name,
                "creditCardExpiry": dec_card.expiry,
                "cvv": dec_card.cvv
            }
        
        return jsonify(ccobj), 200
        
    elif response.status_code == 404:
        # Credit card not found, return HTTP 404 Not Found
        return jsonify({"message": "Credit card not found"}), 404
    elif response.status_code == 403:
        # No permissions to get credit card, return HTTP 403 Forbidden
        return jsonify({"message": "Access denied: No permissions"}), 403   
    else:
        # Handle other errors
        return jsonify({"message": "Error retrieving the credit card"}), 500

###################################################################################################################################

@app.route('/getAllCreditCards', methods=["POST"])
@jwt_required()
def getAllCreditCards():
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500

    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}
    response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
    
    # set information retrieved via sessionId
    userId = response.json()["userId"]
    
    token = get_jwt()
    hash = token["hash"]

    # Make an HTTP GET request to the databaseservice to retrieve all credit cards
    url = f"https://databaseservice/databaseservice/creditcard/get_all_credit_cards/{userId}"
    response = session.get(url)
    
    if response.status_code == 200:
        # Credit cards were retrieved successfully, return the response from the databaseservice
        cc_list = response.json()
        # Get session encryption key from db here
        payload = {
            "sessionId": sessionId
        }
        try:
            response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=payload)
        except:
            return jsonify({"error": "690201"})
        if response.status_code != 200:
            return jsonify({"error": "690202"})
        
        b64key = response.json()["encryptionKey"]
        encryption_key = b64key.encode()
        
        response_list = []
        for card in cc_list:
            creditCardId = card["creditCardId"]
            blob = card["blob"]
            dec_card = CreditCard.decrypt_from_b64_blob(blob, hash, encryption_key)
            dictobj = {
                "creditCardId": creditCardId,
                "creditCardNumber": dec_card.card_num,
                "creditCardName": dec_card.name,
                "creditCardExpiry": dec_card.expiry,
                "cvv": dec_card.cvv
            }
            response_list.append(dictobj)
        
        return jsonify(response_list), 200
    elif response.status_code == 404:
        # No credit cards found, return HTTP 404 Not Found
        return jsonify({"message": "No credit cards found"}), 404
    else:
        # Handle other errors
        return jsonify({"message": "Error retrieving the credit cards"}), 500

###################################################################################################################################

@app.route('/updateOneCreditCard', methods=["PUT"])
@jwt_required()
def updateOneCreditCard():
    # Retrieve credit card details from request
    data = request.get_json()
    creditCardId = data['creditCardId']
    creditCardNumber = data['creditCardNumber']
    creditCardName = data['creditCardName']
    creditCardExpiry = data['creditCardExpiry']
    cvv = data['cvv']
    
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500
    
    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}    
    response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
       
    # set information retrieved via sessionId
    userId = response.json()["userId"]
    
    token = get_jwt()
    hash = token["hash"]
    
    # validate cc information
    if not user_utils.validateCreditCardNumber(creditCardNumber):
        return jsonify({"message": "Invalid credit card number"}), 400
    if not user_utils.validateCreditCardName(creditCardName):
        return jsonify({"message": "Invalid credit card name"}), 400
    if not user_utils.validateCreditCardExpiry(creditCardExpiry):
        return jsonify({"message": "Invalid credit card expiry date"}), 400
    if not user_utils.validateCvv(cvv):
        return jsonify({"message": "Invalid CVV"}), 400
    
    # Get session encryption key from db here
    payload = {
        "sessionId": sessionId
    }
    try:
        response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=payload)
    except:
        return jsonify({"error": "690301"})
    if response.status_code != 200:
        return jsonify({"error": "690302"})
    
    rjson = response.json()
    b64key = rjson["encryptionKey"]
    encryption_key = b64key.encode()
    
    userId = rjson['userId']
    
    # use encryption key and hash to encrypt credit card info into blob (b64 cos cannot send binary)
    card_obj = CreditCard(creditCardNumber, creditCardName, creditCardExpiry, cvv)
    b64 = card_obj.encrypt_to_b64_blob(hash, encryption_key)
    
    # Form JSON data to be sent to the databaseservice        
    updated_credit_card_data = {
        "userId": userId,
        "creditCardId": creditCardId,
        "blob": b64, # need change this one IS peeps
        # cvv not stored in database
    }
        
    # Make an HTTP UPDATE request to the databaseservice to update the credit card
    url = f"https://databaseservice/databaseservice/creditcard/update_credit_card"
    response = session.put(url, json=updated_credit_card_data)
    
    if response.status_code == 200:
        # Credit card was updated successfully, return the response from the databaseservice
        return response.json(), 200
    elif response.status_code == 404:
        # Credit card not found, return HTTP 404 Not Found
        return jsonify({"message": "Credit card not found"}), 404
    elif response.status_code == 403:
        # No permissions to update credit card, return HTTP 403 Forbidden
        return jsonify({"message": "Access denied: No permissions"}), 403
    else:
        # Handle other errors
        return jsonify({"message": "Error updating the credit card"}), 500

###################################################################################################################################

@app.route('/deleteCreditCard', methods=["DELETE"])
@jwt_required()
def deleteCreditCard():
    # Retrieve credit card id from request
    data = request.get_json()
    creditCardId = data['creditCardId']
    print(f"creditCardId: {creditCardId}")
    
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500
    
    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}    
    response = session.post("https://databaseservice/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
    
    # set information retrieved via sessionId
    userId = response.json()["userId"]
    
    # Make an HTTP DELETE request to the databaseservice to delete the credit card
    url = f"https://databaseservice/databaseservice/creditcard/delete_credit_card_by_id/{userId}/{creditCardId}"
    response = session.delete(url)
    
    if response.status_code == 200:
        # Credit card was deleted successfully, return the response from the databaseservice
        return response.json(), 200
    elif response.status_code == 404:
        # Credit card not found, return HTTP 404 Not Found
        return jsonify({"message": "Credit card not found"}), 404
    elif response.status_code == 403:
        # No permissions to delete credit card, return HTTP 403 Forbidden
        return jsonify({"message": "Access denied: No permissions"}), 403
    else:
        # Handle other errors
        return jsonify({"message": "Error deleting the credit card"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8084)
