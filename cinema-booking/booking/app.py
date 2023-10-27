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
    
    # TODO - get user's credit card chosen from paymentservice via /getOneCreditCard/<uuid:userId>/<int:creditCardId>
    
    # TODO - process payment with paymentservice via /makePayment

    # TODO - create booking with databaseservice via /create_booking
    
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