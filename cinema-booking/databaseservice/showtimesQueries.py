from flask import request, jsonify, Blueprint
import os
import psycopg2

showtimes_bp = Blueprint("showtimes", __name__)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

# Create a new showtime entry in the database
@showtimes_bp.route('/create_showtime', methods=['POST'])
def create_showtime():
    try:
        data = request.get_json()
        cinema_id = data['cinemaId']
        theater_id = data['theaterId']
        movie_id = data['movieId']
        show_date = data['showDate']
        show_time = data['showTime']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO Showtimes (cinemaId, theaterId, movieId, showDate, showTime) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (cinema_id, theater_id, movie_id, show_date, show_time))
        new_showtime_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Showtime added successfully", "showtimeId": new_showtime_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve a showtime by its ID
@showtimes_bp.route('/get_showtime_by_id/<int:showtime_id>', methods=['GET'])
def get_showtime_by_id(showtime_id):
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
            return jsonify(showtime_details), 200
        else:
            return jsonify({"message": "Showtime not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieve all showtimes from the database
@showtimes_bp.route('/get_all_showtimes', methods=['GET'])
def get_all_showtimes():
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

            return jsonify(showtime_list), 200
        else:
            return jsonify({"message": "No showtimes found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a showtime entry by its ID
@showtimes_bp.route('/update_showtime_by_id/<int:showtime_id>', methods=['PUT'])
def update_showtime_by_id(showtime_id):
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

            return jsonify({"message": "Showtime updated successfully"}), 200
        else:
            # Showtime does not exist
            return jsonify({"message": "Showtime not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a showtime entry by its ID
@showtimes_bp.route('/delete_showtime_by_id/<int:showtime_id>', methods=['DELETE'])
def delete_showtime_by_id(showtime_id):
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

            return jsonify({"message": "Showtime deleted successfully"}), 200
        else:
            # Showtime does not exist
            return jsonify({"message": "Showtime not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
