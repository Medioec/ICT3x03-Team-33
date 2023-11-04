from flask import request, jsonify, Blueprint
import os
import psycopg2
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create a blueprint
showtimes_bp = Blueprint("showtimes", __name__)

# log showtimes queries started
logger.info(f"Showtimes queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

# Create a new showtime entry in the database
@showtimes_bp.route('/create_showtime', methods=['POST'])
def create_showtime():
    # Log the addition of a new showtime entry
    logger.info(f"Adding new showtime started.")
    try:
        data = request.get_json()
        cinema_id = data['cinemaId']
        theater_id = data['theaterId']
        movie_id = data['movieId']
        show_date = data['showDate']
        show_time = data['showTime']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO Showtimes (cinemaId, theaterId, movieId, showDate, showTime) VALUES (%s, %s, %s, %s, %s) RETURNING showtimeId"
        cursor.execute(insert_query, (cinema_id, theater_id, movie_id, show_date, show_time))
        new_showtime_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        # Log the successful creation of a new showtime entry
        logger.info(f"Showtime added successfully with new showtimeId: {new_showtime_id}.")
        return jsonify({"message": "Showtime added successfully", "showtimeId": new_showtime_id}), 201
    except Exception as e:
        # Log the error
        logger.error(f"Error in create_showtime: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Retrieve a showtime by its ID
@showtimes_bp.route('/get_showtime_by_id/<int:showtime_id>', methods=['GET'])
def get_showtime_by_id(showtime_id):
    # Log the retrieval of a showtime entry
    logger.info(f"Retrieving showtime details for showtimeId: {showtime_id}.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Showtimes WHERE showtimeId = %s"
        cursor.execute(select_query, (showtime_id,))
        showtime = cursor.fetchone()

        cursor.close()
        conn.close()

        if showtime:
            showtime_details = {
                "showtimeId": showtime[0],
                "cinemaId": showtime[1],
                "theaterId": showtime[2],
                "movieId": showtime[3],
                "showDate": showtime[4],
                "showTime": showtime[5]
            }
            
            # Log the successful retrieval of a showtime entry
            logger.info(f"Showtime details retrieved successfully for showtimeId: {showtime_id}.")
            return jsonify(showtime_details), 200
        else:
            # Showtime does not exist
            logger.info(f"Showtime not found for showtimeId: {showtime_id}.")
            return jsonify({"message": "Showtime not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_showtime_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Retrieve all showtimes from the database
@showtimes_bp.route('/get_all_showtimes', methods=['GET'])
def get_all_showtimes():
    # Log the retrieval of all showtime entries
    logger.info(f"Retrieving all showtime details.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Showtimes"
        cursor.execute(select_query)
        showtimes = cursor.fetchall()

        cursor.close()
        conn.close()

        if showtimes:
            showtime_list = []
            for showtime in showtimes:
                showtime_details = {
                    "showtimeId": showtime[0],
                    "cinemaId": showtime[1],
                    "theaterId": showtime[2],
                    "movieId": showtime[3],
                    "showDate": showtime[4],
                    "showTime": showtime[5]
                }
                showtime_list.append(showtime_details)

            # Log the successful retrieval of all showtime entries
            logger.info(f"Showtime details retrieved successfully.")
            return jsonify(showtime_list), 200
        else:
            # No showtimes found
            # Log the error
            logger.warning(f"No showtimes found.")
            return jsonify({"message": "No showtimes found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_all_showtimes: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Update a showtime entry by its ID
@showtimes_bp.route('/update_showtime_by_id/<int:showtime_id>', methods=['PUT'])
def update_showtime_by_id(showtime_id):
    # Log the update of a showtime entry
    logger.info(f"Updating showtime details for showtimeId: {showtime_id}.")
    try:
        data = request.get_json()
        cinema_id = data.get('cinemaId')
        theater_id = data.get('theaterId')
        movie_id = data.get('movieId')
        show_date = data.get('showDate')
        show_time = data.get('showTime')

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if showtime exists
        select_query = "SELECT * FROM Showtimes WHERE showtimeId = %s"

        cursor.execute(select_query, (showtime_id,))
        showtime = cursor.fetchone()

        cursor.close()
        conn.close()

        # Update showtime if it exists
        if showtime:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            update_query = "UPDATE Showtimes SET cinemaId = %s, theaterId = %s, movieId = %s, showDate = %s, showTime = %s WHERE showtimeId = %s"
            cursor.execute(update_query, (cinema_id, theater_id, movie_id, show_date, show_time, showtime_id))
            conn.commit()

            cursor.close()
            conn.close()

            # Log the successful update of a showtime entry
            logger.info(f"Showtime details updated successfully for showtimeId: {showtime_id}.")
            return jsonify({"message": "Showtime updated successfully"}), 200
        else:
            # Showtime does not exist
            # Log the error
            return jsonify({"message": "Showtime not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in update_showtime_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Delete a showtime entry by its ID
@showtimes_bp.route('/delete_showtime_by_id/<int:showtime_id>', methods=['DELETE'])
def delete_showtime_by_id(showtime_id):
    # Log the deletion of a showtime entry
    logger.info(f"Deleting showtime details for showtimeId: {showtime_id}.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if showtime exists
        select_query = "SELECT * FROM Showtimes WHERE showtimeId = %s"

        cursor.execute(select_query, (showtime_id,))
        showtime = cursor.fetchone()

        cursor.close()
        conn.close()

        # Delete showtime if it exists
        if showtime:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM Showtimes WHERE showtimeId = %s"
            cursor.execute(delete_query, (showtime_id,))
            conn.commit()

            cursor.close()
            conn.close()

            # Log the successful deletion of a showtime entry
            logger.info(f"Showtime deleted successfully for showtimeId: {showtime_id}.")
            return jsonify({"message": "Showtime deleted successfully"}), 200
        else:
            # Showtime does not exist
            # Log the error
            logger.warning(f"Showtime not found for showtimeId: {showtime_id}.")
            return jsonify({"message": "Showtime not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in delete_showtime_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
