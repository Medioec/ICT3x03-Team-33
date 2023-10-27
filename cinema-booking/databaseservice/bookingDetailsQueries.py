from flask import request, jsonify, Blueprint
import os
import psycopg2
from psycopg2 import IntegrityError 

booking_details_bp = Blueprint("bookingdetails", __name__)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}


##### Create a new booking entry in the database #####
@booking_details_bp.route('/generate_booking_details', methods=['POST'])
def generate_booking_details():
    try:
        data = request.get_json()
        userId = data['userId']
        showtimeId = data['showtimeId']
        seatId = data['seatId']
        ticketPriceId = data['ticketPriceId']
        transaction_id = data['transactionId']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO BookingDetails (showtimeId, seatId, transactionId, userId, ticketPriceId) VALUES (%s, %s, %s, %s, %s)"
        
        try:
            cursor.execute(insert_query, (showtimeId, seatId, transaction_id, userId, ticketPriceId))
            ticket_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Booking details added successfully", "ticketId": ticket_id}), 201
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            return jsonify({"error": "Duplicate entry: This booking already exists."}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500
##### End of create new booking entry #####

#####     Retrieve a booking by its bookingId and userId    #####
@booking_details_bp.route('/get_booking_details_by_id/<uuid:user_id>/<int:ticket_id>', methods=['GET'])
def get_booking_details_by_id(user_id, ticket_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user with the given userId owns the booking with the given ticketId
        select_owner_query = "SELECT userId FROM BookingDetails WHERE ticketId = %s"
        cursor.execute(select_owner_query, (ticket_id,))
        owner_id = cursor.fetchone()

        if owner_id and owner_id[0] == user_id:
            # If the user owns the booking, retrieve it
            select_query = "SELECT * FROM BookingDetails WHERE ticketId = %s"
            cursor.execute(select_query, (ticket_id,))
            booking_details = cursor.fetchone()

            if booking_details:
                bookingDetails = {
                    "ticketId": booking_details[0],
                    "showtimeId": booking_details[1],
                    "seatId": booking_details[2],
                    "transactionId": booking_details[3],
                    "userId": booking_details[4],
                    "ticketPriceId": booking_details[5]
                }
                return jsonify(bookingDetails), 200
            else:
                return jsonify({"message": "Booking not found"}), 404
        else:
            return jsonify({"message": "Access denied: No permissions"}), 403

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve booking by its bookingId and userId     #####

#####     Retrieve all bookings by userId     #####
@booking_details_bp.route('/get_all_bookings_by_userId/<uuid:userId>', methods=['GET'])
def get_ticket_price_by_id(userId):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM BookingDetails WHERE userId = %s"
        cursor.execute(select_query, (userId,))
        booking_details = cursor.fetchone()

        cursor.close()
        conn.close()

        if booking_details:
            booking_details_list = []
            for booking in booking_details:
                one_booking = {
                    "ticketId": booking[0],
                    "showtimeId": booking[1],
                    "seatId": booking[2],
                    "transactionId": booking[3],
                    "userId": booking[4],
                    "ticketPriceId": booking[5]
                }
                booking_details_list.append(one_booking)

            return jsonify(booking_details_list), 200
        else:
            return jsonify({"message": "No bookings found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all booking by userId    #####

'''
NOTE: 
Update and Delete queries are not added intentionally 
as we do not allow cancellation or updates for bookings made aka no refunds. 

If required, should be done with database admin access.
'''
