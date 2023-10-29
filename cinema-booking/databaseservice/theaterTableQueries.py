from flask import request, jsonify, Blueprint
import os
import psycopg2
from psycopg2 import IntegrityError
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create a blueprint
theater_bp = Blueprint("theater", __name__)

# Log theater queries started
logger.info("Theater queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Add new theater entry in the database     #####
@theater_bp.route('/add_theater', methods=['POST'])
def add_theater():
    # Log the addition of a new theater entry
    logger.info("Adding new theater started.")
    try:
        data = request.get_json()
        theaterNumber = data['theaterNumber']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO Theater (theaterNumber) VALUES (%s) RETURNING theaterNumber"
        try:
            cursor.execute(insert_query, (theaterNumber,))
            new_theater_number = cursor.fetchone()[0]
            conn.commit()
        
            cursor.close()
            conn.close()
            
            # Log the successful creation of a new theater entry
            logger.info("Theater added successfully with new theaterNumber: {new_theater_number}.")
            return jsonify({"message": "Theater added successfully", "theaterNumber": new_theater_number}), 201
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            # Log the error
            logger.error(f"Duplicate entry in add_theater. theaterNumber: {theaterNumber}")
            return jsonify({"error": "Duplicate entry: This theater already exists."}), 409
    except Exception as e:
        # Log the error
        logger.error(f"Error in add_theater: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of add new theater entry    #####


#####     Retrieve a theater by its ID     #####
@theater_bp.route('/get_theater_by_number/<string:theater_number>', methods=['GET'])
def get_theater_by_number(theater_number):
    # Log the retrieval of a theater entry
    logger.info(f"Retrieving theater details for theaterNumber: {theater_number}.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Theater WHERE theaterNumber = %s"
        cursor.execute(select_query, (theater_number,))
        theater = cursor.fetchone()

        cursor.close()
        conn.close()

        if theater:
            theater_details = {
                "theaterNumber": theater[0]
            }
            
            # Log the successful retrieval of a theater entry
            logger.info(f"Theater details retrieved successfully for theaterNumber: {theater_number}.")
            return jsonify(theater_details), 200
        else:
            # Theater does not exist
            logger.info(f"Theater not found for theaterNumber: {theater_number}.")
            return jsonify({"message": "Theater not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_theater_by_number: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of retrieve theater by ID     #####

#####     Retrieve all theaters from the database     #####
@theater_bp.route('/get_all_theaters', methods=['GET'])
def get_all_theaters():
    # Log the retrieval of all theaters
    logger.info("Retrieving all theaters from the database.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Theater"
        cursor.execute(select_query)
        theaters = cursor.fetchall()

        cursor.close()
        conn.close()

        if theaters:
            theater_list = []
            for theater in theaters:
                theater_details = {
                    "theaterNumber": theater[0]
                }
                theater_list.append(theater_details)

            # Log the successful retrieval of all theaters
            logger.info("All theaters retrieved successfully.")
            return jsonify(theater_list), 200
        else:
            # No theaters found
            logger.info("No theaters found.")
            return jsonify({"message": "No theaters found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_all_theaters: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all theaters     #####

#####     Update a theater entry by its ID     #####
@theater_bp.route('/update_theater_by_id/<string:theater_number>', methods=['PUT'])
def update_theater_by_id(theater_number):
    # Log the update of a theater entry
    logger.info(f"Updating theater details for theaterNumber: {theater_number}.")
    try:
        data = request.get_json()
        newTheaterNumber = data['theaterNumber']
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if theater exists
        select_query = "SELECT * FROM Theater WHERE theaterNumber = %s"
        
        cursor.execute(select_query, (newTheaterNumber,))
        theater = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Update theater if it exists
        if theater:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            
            update_query = "UPDATE Theater SET theaterNumber = %s WHERE theaterNumber = %s"
            cursor.execute(update_query, (newTheaterNumber, theater_number))
            
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # Log the successful update of a theater entry
            logger.info(f"Theater details updated successfully for theaterNumber: {theater_number}.")
            return jsonify({"message": "Theater updated successfully"}), 200            
        else:
            # Theater does not exist
            # Log the error
            logger.warning(f"Theater not found for theaterNumber: {theater_number}.")
            return jsonify({"message": "Theater not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in update_theater_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500

#####     End of update theater by ID     #####


#####     Delete a theater entry by its ID     #####
@theater_bp.route('/delete_theater_by_id/<string:theater_number>', methods=['DELETE'])
def delete_theater_by_id(theater_number):
    # Log the deletion of a theater entry
    logger.info(f"Deleting theater details for theaterNumber: {theater_number}.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if theater exists
        select_query = "SELECT * FROM Theater WHERE theaterNumber = %s"
        
        cursor.execute(select_query, (theater_number,))
        theater = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete theater if it exists
        if theater:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM Theater WHERE theaterNumber = %s"
            cursor.execute(delete_query, (theater_number,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # Log the successful deletion of a theater entry
            logger.info(f"Theater deleted successfully for theaterNumber: {theater_number}.")
            return jsonify({"message": "Theater deleted successfully"}), 200
        else:
            # Theater does not exist
            # Log the error
            logger.warning(f"Theater not found for theaterNumber: {theater_number}.")
            return jsonify({"message": "Theater not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in delete_theater_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of delete theater by ID     #####

