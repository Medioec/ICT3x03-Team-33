from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import booking_utils
app = Flask(__name__)  
CORS(app)

@app.route('/generateBooking', methods=["POST"])
def generateBooking():
    # Retrieve booking details from request
    data = request.get_json()
    userId = data['userId']
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