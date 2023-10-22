from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import user_utils
app = Flask(__name__)  
CORS(app)

@app.route('/makePayment', methods=["POST"])
def makePayment():
    # Retrieve payment details from request
    data = request.get_json()
    creditCardId = data['creditCardId']
    blob = data['blob']
    creditCardName = data['creditCardName']
    creditCardExpiry = data['creditCardExpiry']
    cvv = data['cvv']
    
    # TODO - decrypt information?
    
    # validate cc information
    if not user_utils.validateCreditCardNumber(blob):
        return jsonify({"message": "Invalid credit card number"}), 400
    if not user_utils.validateCreditCardName(creditCardName):
        return jsonify({"message": "Invalid credit card name"}), 400
    if not user_utils.validateCreditCardExpiry(creditCardExpiry):
        return jsonify({"message": "Invalid credit card expiry date"}), 400
    if not user_utils.validateCvv(cvv):
        return jsonify({"message": "Invalid CVV"}), 400
    
    while True:
            # Process payment after validation
            transaction_id = user_utils.processPayment() # This is hardcoded as we can't actually 
            
            # Get current datetime
            transaction_date_time = user_utils.getTransactionDateTime()
            
            # Form JSON data to be sent to the databaseservice
            transaction_data = {
                "transactionId": transaction_id,
                "creditCardId": creditCardId,
                "transactionDateTime": transaction_date_time
            }

            # Make an HTTP POST request to the databaseservice to create the transaction
            response = requests.post("http://databaseservice:8085/databaseservice/transactions/create_transaction", json=transaction_data)
            
            if response.status_code == 201:
                # Transaction was added successfully, return the response from the databaseservice
                return response.json(), 201
            elif response.status_code == 409:
                # Duplicate transaction ID detected, regenerate and retry
                continue
            else:
                # Handle other errors
                return jsonify({"message": "Error processing the payment"}), 500

@app.route('/addCreditCard', methods=["POST"])
def addCreditCard():
    # Retrieve credit card details from request
    data = request.get_json()
    # Credit card number is named as blob in the request. Also stored as raw bytes in the database.
    blob = data['blob']
    creditCardName = data['creditCardName']
    creditCardExpiry = data['creditCardExpiry']
    cvv = data['cvv']
    userId = data['userId']
    
    # validate cc information
    if not user_utils.validateCreditCardNumber(blob):
        return jsonify({"message": "Invalid credit card number"}), 400
    if not user_utils.validateCreditCardName(creditCardName):
        return jsonify({"message": "Invalid credit card name"}), 400
    if not user_utils.validateCreditCardExpiry(creditCardExpiry):
        return jsonify({"message": "Invalid credit card expiry date"}), 400
    if not user_utils.validateCvv(cvv):
        return jsonify({"message": "Invalid CVV"}), 400
    
    # TODO - Perform cryptography on information
    
    # Form JSON data to be sent to the databaseservice
    # TODO - change blob varaiable to ones that have cryptography applied
    credit_card_data = {
        "userId": userId,
        "blob": blob, # need change this one IS peeps
        # cvv not stored in database
    }
    
    # Make an HTTP POST request to the databaseservice to create the credit card
    response = requests.post("http://databaseservice:8085/databaseservice/creditcard/add_credit_card", json=credit_card_data)
    
    if response.status_code == 201:
        # Credit card was added successfully, return the response from the databaseservice
        return response.json(), 201
    elif response.status_code == 409:
        # Duplicate credit card detected, return HTTP 409 Conflict
        return jsonify({"message": "Credit card already exists"}), 409
    else:
        # Handle other errors
        return jsonify({"message": "Error adding the credit card"}), 500

@app.route('/getOneCreditCard/<uuid:userId>/<int:creditCardId>', methods=["GET"])
def getCreditCard(userId, creditCardId):
    # Make an HTTP GET request to the databaseservice to retrieve the credit card
    url = f"http://databaseservice:8085/databaseservice/creditcard/get_credit_card_by_id/{userId}/{creditCardId}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Credit card was retrieved successfully, return the response from the databaseservice
        return response.json(), 200
    elif response.status_code == 404:
        # Credit card not found, return HTTP 404 Not Found
        return jsonify({"message": "Credit card not found"}), 404
    elif response.status_code == 403:
        # No permissions to delete credit card, return HTTP 403 Forbidden
        return jsonify({"message": "Access denied: No permissions"}), 403   
    else:
        # Handle other errors
        return jsonify({"message": "Error retrieving the credit card"}), 500
    
@app.route('/getAllCreditCards/<uuid:userId>', methods=["GET"])
def getAllCreditCards(userId):
    # Make an HTTP GET request to the databaseservice to retrieve all credit cards
    url = f"http://databaseservice:8085/databaseservice/creditcard/get_all_credit_cards/{userId}"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Credit cards were retrieved successfully, return the response from the databaseservice
        return response.json(), 200
    elif response.status_code == 404:
        # No credit cards found, return HTTP 404 Not Found
        return jsonify({"message": "No credit cards found"}), 404
    else:
        # Handle other errors
        return jsonify({"message": "Error retrieving the credit cards"}), 500

@app.route('/updateOneCreditCard', methods=["PUT"])
def updateOneCreditCard():
    # Retrieve credit card details from request
    data = request.get_json()
    # Credit card number is named as blob in the request. Also stored as raw bytes in the database.
    blob = data['blob']
    creditCardName = data['creditCardName']
    creditCardExpiry = data['creditCardExpiry']
    cvv = data['cvv']
    userId = data['userId']
    
    # validate cc information
    if not user_utils.validateCreditCardNumber(blob):
        return jsonify({"message": "Invalid credit card number"}), 400
    if not user_utils.validateCreditCardName(creditCardName):
        return jsonify({"message": "Invalid credit card name"}), 400
    if not user_utils.validateCreditCardExpiry(creditCardExpiry):
        return jsonify({"message": "Invalid credit card expiry date"}), 400
    if not user_utils.validateCvv(cvv):
        return jsonify({"message": "Invalid CVV"}), 400
    
    # TODO - Perform cryptography on information.
    # cc number, name, expiry should be transformed into one blob of typebytea aka. raw bytes
    
    # Form JSON data to be sent to the databaseservice
    # TODO - change blob variable to the one that have cryptography applied
        
    updated_credit_card_data = {
        "userId": userId,
        "blob": blob, # need change this one IS peeps
        # cvv not stored in database
    }
        
    # Make an HTTP UPDATE request to the databaseservice to update the credit card
    url = f"http://databaseservice:8085/databaseservice/creditcard/update_credit_card"
    response = requests.put(url, json=updated_credit_card_data)
    
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

@app.route('/deleteCreditCard/<uuid:userId>/<int:creditCardId>', methods=["DELETE"])
def deleteCreditCard(userId, creditCardId):
    # Make an HTTP DELETE request to the databaseservice to delete the credit card
    url = f"http://databaseservice:8085/databaseservice/creditcard/delete_credit_card/{userId}/{creditCardId}"
    response = requests.delete(url)
    
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
