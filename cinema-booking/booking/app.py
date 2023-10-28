from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
import os
import requests
import booking_utils

app = Flask(__name__)  
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

#####   throw error when JWT token is not valid     #####
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("unauthorized callback")
    return jsonify({"message": "Unauthorized access"}), 401
#####   End of throw error when JWT token is not valid     #####

@app.route('/generateBooking', methods=["POST"])
@jwt_required()
def generateBooking():
    # get sessionId from jwt
    sessionId = get_jwt_identity()
    if not sessionId:
        return jsonify({"message": "Error: No token sent"}), 500
    
    # use sessionId to get userId from db
    requestData = {"sessionId": sessionId}    
    response = requests.post("http://databaseservice:8085/databaseservice/usersessions/get_user_session", json=requestData)
    if response.status_code != 200:
        return jsonify({"message": "Database error"}), 500
    userId = response.json()["userId"]

    # Retrieve booking details from request
    data = request.get_json()
    creditCardId = data['creditCardId']
    showtimeId = data['showtimeId']
    seatId = data['seatId']
    ticketPriceId = data['ticketPriceId']
    
    data = {
        "userId": userId,
        "creditCardId": creditCardId,
    }
    
    # TODO - process payment with paymentservice via /makePayment
    url = f"http://paymentservice:8084/paymentservice/makePayment"
    response = requests.post(url, json=data)
    if response.status_code != 200:
        if response.status_code == 400:
            return jsonify(response.json()["message"]), 400 # Bad request: Invalid credit card
        elif response.status_code == 403:
            return jsonify(response.json()["message"]), 403 # Access denied: No permissions
        elif response.status_code == 404:
            return jsonify(response.json()["message"]), 404 # Credit card not found
        elif response.status_code == 409:
            return jsonify(response.json()["message"]), 409 # Duplicate entry: This transaction already exists.
    elif response.status_code == 200:
        data = {
            "userId": userId,
            "showtimeId": showtimeId,            
            "seatId": seatId,
            "ticketPriceId": ticketPriceId,
            "transactionId": response.json()["transactionId"]
        }
        
        # Create booking with databaseservice 
        url = f"http://databaseservice:8085/databaseservice/bookingdetails//generate_booking_details"
        response = requests.post(url, json=data)
        if response.status_code == 201:
            return jsonify({"message": "Booking created successfully"}), 201
        elif response.status_code == 409:
            return jsonify({"message": "Duplicate entry: This booking already exists."}), 409
        else:
            return jsonify({"message": "Error generating booking"}), 500
    else:
        return jsonify({"message": "Error generating booking"}), 500
    
    
@app.route('/retrieveOneBooking/<uuid:userId>/<int:ticketId>', methods=["get"])
@jwt_required()
def retrieveOneBooking(userId, ticketId):
    try:
        url = f"http://databaseservice:8085/databaseservice/bookingdetails/get_booking_details_by_id/{userId}/{ticketId}"
        response = requests.get(url)

        if response.status_code == 404:
            return jsonify({"message": "Booking not found"}), 404
        elif response.status_code == 403:
            return jsonify({"message": "Access denied: No permissions"}), 403
        else:
            # Bind the values retrieved from db to the variables below
            seatId = response.json()['seatId']
            showtimeId = response.json()['showtimeId']
            transactionId = response.json()['transactionId']
            ticketPriceId = response.json()['ticketPriceId']
            
            bookingDetails = {
                "seatId": seatId,
                "showtimeId": showtimeId,
                "transactionId": transactionId,
                "userId": userId,
                "ticketId": ticketId,
                "ticketPriceId": ticketPriceId   
            }
            
            # Generate QR code with booking details information and send to frontend
            qrCode = booking_utils.generateQRCode(bookingDetails)
            
            return jsonify({"qrCode": qrCode.decode('utf-8')}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/retrieveAllBookings/<uuid:userId>', methods=["get"])
def retrieveAllBookings(userId):
    try:
        url = f"http://databaseservice:8085/databaseservice/bookingdetails/get_all_bookings_by_userId/{userId}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json(), 200
        elif response.status_code == 404:
            return jsonify({"message": "No bookings found"}), 404
        else:
            return jsonify({"message": "Error retrieving the bookings"}), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#NOTE: No need do cancellation or updating booking, cause we not allowing both.    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8083)