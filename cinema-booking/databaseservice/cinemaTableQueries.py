from flask import request, jsonify, Blueprint
import os
import psycopg2
from psycopg2 import IntegrityError 

cinema_bp = Blueprint("cinema", __name__)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Add new cinema entry in the database     #####
@cinema_bp.route('/add_cinema', methods=['POST'])
def add_cinema():
    try:
        data = request.get_json()
        cinemaName = data['cinemaName']
        locationName = data['locationName']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO Cinema (cinemaName, locationName) VALUES (%s, %s) RETURNING cinemaId"
        try:
            cursor.execute(insert_query, (cinemaName, locationName))
            new_cinema_id = cursor.fetchone()[0]
            conn.commit()
        
            cursor.close()
            conn.close()
            
            return jsonify({"message": "Cinema added successfully", "cinemaId": new_cinema_id}), 201
            
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            return jsonify({"error": "Duplicate entry: This cinema already exists."}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of add new cinema entry    #####


#####     Retrieve a cinema by its ID     #####
@cinema_bp.route('/get_cinema_by_id/<int:cinema_id>', methods=['GET'])
def get_cinema_by_id(cinema_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Cinema WHERE cinemaId = %s"
        cursor.execute(select_query, (cinema_id,))
        cinema = cursor.fetchone()

        cursor.close()
        conn.close()

        if cinema:
            cinema_details = {
                "cinemaId": cinema[0],
                "cinemaName": cinema[1],
                "locationName": cinema[2]
            }
            return jsonify(cinema_details), 200
        else:
            return jsonify({"message": "Cinema not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve cinema by ID     #####

#####     Retrieve all cinemas from the database     #####
@cinema_bp.route('/get_all_cinemas', methods=['GET'])
def get_all_cinemas():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Cinema"
        cursor.execute(select_query)
        cinemas = cursor.fetchall()

        cursor.close()
        conn.close()

        if cinemas:
            cinema_list = []
            for cinema in cinemas:
                cinema_details = {
                    "cinemaId": cinema[0],
                    "cinemaName": cinema[1],
                    "locationName": cinema[2]
                }
                cinema_list.append(cinema_details)

            return jsonify(cinema_list), 200
        else:
            return jsonify({"message": "No cinemas found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve all cinemas     #####

#####     Update a cinema entry by its ID     #####
@cinema_bp.route('/update_cinema_by_id/<int:cinema_id>', methods=['PUT'])
def update_cinema_by_id(cinema_id):
    try:
        data = request.get_json()
        cinemaName = data['cinemaName']
        locationName = data['locationName']
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if cinema exists
        select_query = "SELECT * FROM Cinema WHERE cinemaId = %s"
        
        cursor.execute(select_query, (cinema_id,))
        cinema = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Update cinema if it exists
        if cinema:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            
            update_query = "UPDATE Cinema SET cinemaName = %s, locationName = %s WHERE cinemaId = %s"
            cursor.execute(update_query, (cinemaName, locationName, cinema_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return jsonify({"message": "Cinema updated successfully"}), 200            
        else:
            # Cinema does not exist
            return jsonify({"message": "Cinema not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of update cinema by ID     #####


#####     Delete a cinema entry by its ID     #####
@cinema_bp.route('/delete_cinema_by_id/<int:cinema_id>', methods=['DELETE'])
def delete_cinema_by_id(cinema_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if cinema exists
        select_query = "SELECT * FROM Cinema WHERE cinemaId = %s"
        
        cursor.execute(select_query, (cinema_id,))
        cinema = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete cinema if it exists
        if cinema:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM Cinema WHERE cinemaId = %s"
            cursor.execute(delete_query, (cinema_id,))
            conn.commit()

            cursor.close()
            conn.close()
            
            return jsonify({"message": "Cinema deleted successfully"}), 200
        else:
            # Cinema does not exist
            return jsonify({"message": "Cinema not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of delete cinema by ID     #####

