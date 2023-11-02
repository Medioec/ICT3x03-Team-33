from flask import request, jsonify, Blueprint
import os
import psycopg2
from psycopg2 import IntegrityError 
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create a blueprint
seat_bp = Blueprint("seat", __name__)

# Log seat queries started
logger.info(f"Seat queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Add new seat entry in the database     #####
@seat_bp.route('/add_seat', methods=['POST'])
def add_seat():
    # Log the addition of a new seat entry
    logger.info(f"Adding new seat started.")
    try:
        data = request.get_json()
        seatId = data['seatId']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO Seat (seatId) VALUES (%s) RETURNING seatId"
        try:
            cursor.execute(insert_query, (seatId,))
            new_seat_id = cursor.fetchone()[0]
            conn.commit()
        
            cursor.close()
            conn.close()
            
            # Log the successful creation of a new seat entry
            logger.info(f"Seat added successfully with new seatId: {new_seat_id}.")
            return jsonify({"message": "Seat added successfully", "seatId": new_seat_id}), 201
            
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            # Log the error
            logger.error(f"Duplicate entry in add_seat. seatId: {seatId}")
            return jsonify({"error": "Duplicate entry: This seat already exists."}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of add new seat entry    #####


#####     Retrieve a seat by its ID     #####
@seat_bp.route('/get_seat_by_id/<int:seat_id>', methods=['GET'])
def get_seat_by_id(seat_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Seat WHERE seatId = %s"
        cursor.execute(select_query, (seat_id,))
        seat = cursor.fetchone()

        cursor.close()
        conn.close()

        if seat:
            seat_details = {
                "seatId": seat[0]
            }
            return jsonify(seat_details), 200
        else:
            return jsonify({"message": "Seat not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve seat by ID     #####

#####     Retrieve all seats from the database     #####
@seat_bp.route('/get_all_seats', methods=['GET'])
def get_all_seats():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Seat"
        cursor.execute(select_query)
        seats = cursor.fetchall()

        cursor.close()
        conn.close()

        if seats:
            seat_list = []
            for seat in seats:
                seat_details = {
                    "seatId": seat[0]
                }
                seat_list.append(seat_details)

            return jsonify(seat_list), 200
        else:
            return jsonify({"message": "No seats found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve all seats     #####

#####     Update a seat entry by its ID     #####
@seat_bp.route('/update_seat_by_id/<int:seat_id>', methods=['PUT'])
def update_seat_by_id(seat_id):
    try:
        data = request.get_json()
        newSeatId = data['seatId']
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if seat exists
        select_query = "SELECT * FROM Seat WHERE seatId = %s"
        
        cursor.execute(select_query, (newSeatId,))
        seat = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Update seat if it exists
        if seat:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            
            update_query = "UPDATE Seat SET seatId = %s WHERE seatId = %s"
            cursor.execute(update_query, (newSeatId, seat_id))
            
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return jsonify({"message": "Seat updated successfully"}), 200            
        else:
            # Seat does not exist
            return jsonify({"message": "Seat not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of update seat by ID     #####


#####     Delete a seat entry by its ID     #####
@seat_bp.route('/delete_seat_by_id/<int:seat_id>', methods=['DELETE'])
def delete_seat_by_id(seat_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if seat exists
        select_query = "SELECT * FROM Seat WHERE seatId = %s"
        
        cursor.execute(select_query, (seat_id,))
        seat = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete seat if it exists
        if seat:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM Seat WHERE seatId = %s"
            cursor.execute(delete_query, (seat_id,))
            conn.commit()

            cursor.close()
            conn.close()
            
            return jsonify({"message": "Seat deleted successfully"}), 200
        else:
            # Seat does not exist
            return jsonify({"message": "Seat not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of delete seat by ID     #####

