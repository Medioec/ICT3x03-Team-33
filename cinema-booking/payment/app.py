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
    creditCardNumber = data['creditCardNumber']
    creditCardName = data['creditCardName']
    creditCardExpiry = data['creditCardExpiry']
    cvv = data['cvv']
    
    # TODO - decrypt information?
    
    # validate cc information
    if not user_utils.validateCreditCardNumber(creditCardNumber):
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8084)
