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
    
    # TODO - get user's credit card chosen from paymentservice via /getOneCreditCard/<uuid:userId>/<int:creditCardId>
    
    # TODO - process payment with paymentservice via /makePayment

    # TODO - create booking with databaseservice via /create_booking
    
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