from flask import request, jsonify, Blueprint
import os
import psycopg2

user_sessions_bp = Blueprint("user_sessions", __name__)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Adds a new session for a specific user to the database     #####
@user_sessions_bp.route('/create_user_session', methods=['POST'])
def create_user_session():
    try:
        # Get data from the request
        data = request.get_json()
        sessionId = data['sessionId']
        userId = data['userId']
        expiryTimestamp = data['expiryTimestamp']
        currStatus = data['currStatus']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the UserSessions table
        insert_query = "INSERT INTO usersessions (sessionId, userId, expiryTimestamp, currStatus) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (sessionId, userId, expiryTimestamp, currStatus))
        conn.commit()

        cursor.close()
        conn.close()

        # Return HTTP 201 Created to indicate successful resource creation
        return jsonify({"message": "User session added successfully"}), 201

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        return jsonify({"error": str(e)}), 500
#####     End of create session     #####


#####     Get session info given a sessionId     #####
@user_sessions_bp.route('/get_user_session', methods=['POST'])
def get_user_session():
    try:
        # Get data from the request
        data = request.get_json()
        sessionId = data['sessionId']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Query session data
        select_query = "SELECT userId, expiryTimestamp, currStatus, encryptionKey FROM UserSessions WHERE sessionId = %s"
        cursor.execute(select_query, (sessionId))
        conn.commit()
        data_result = cursor.fetchall()

        cursor.close()
        conn.close()

        # Separate the data into two attributes in a JSON response
        if data_result:
            userId, expiryTimestamp, currStatus, encryptionKey = data_result[0]
            response_data = {
                "userId": userId,
                "expiryTimestamp": expiryTimestamp,
                "currStatus": currStatus,
                "encryptionKey": encryptionKey
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"message": "No data found"}), 404

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        return jsonify({"error": str(e)}), 500
#####     End of create session     #####

##### Retrieves userId, password hash and user role from database #####
@user_sessions_bp.route('/get_userId_hash_role', methods=['POST'])
def get_hash_role():
    try:
        # Get data from the request
        data = request.get_json()
        username = data['username']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Construct the SQL query to retrieve the password hash and user role using username
        select_data_query = "SELECT userId, passwordHash, userRole FROM CinemaUser WHERE username = %s "
        cursor.execute(select_data_query, (username,))
        data_result = cursor.fetchall()

        # Close the cursor and the database connection
        cursor.close()
        conn.close()

        # Separate the data into two attributes in a JSON response
        if data_result:
            # Assuming there's one result
            userId, passwordHash, userRole = data_result[0]
            response_data = {
                "userId": userId,
                "passwordHash": passwordHash,
                "userRole": userRole
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"message": "No data found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####   End of pw hash retrieval   #####

##### Updates private key and expiry timestamp into database #####
@user_sessions_bp.route('/update_timestamp', methods=['PUT'])
def update_timestamp():
    try:
        # Get data from the request
        data = request.get_json()
        sessionId = data['sessionId']
        newExpiryTimestamp = data['expiryTimestamp']
        
        if sessionId is None or newExpiryTimestamp is None:
            return jsonify({"error": "Missing data in the request"}), 400

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        update_data_query = """
        UPDATE UserSessions
        SET expiryTimestamp = %s
        WHERE sessionId = %s
        """
        cursor.execute(update_data_query, (newExpiryTimestamp, sessionId))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Session not found"}), 404

        conn.close()
        return jsonify({"message": "Session updated successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####   End of updating keys and expiry   #####

##### Store encryption key associated with SessionID, for testing purpose, almost duplicate of user session #####
@user_sessions_bp.route('/store_key_in_database', methods=['POST'])
def store_key_in_database():
    try:
        # Get data from the request
        data = request.get_json()
        userId = data['userId']
        expiryTimestamp = data['expiryTimestamp']
        currStatus = data['currStatus']
        encryptionKey = data['fernet_key']
        sessionId = data['sessionId']
        
        
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO usersessions (sessionId, userId, expiryTimestamp, currStatus, encryptionKey) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (sessionId, userId, expiryTimestamp, currStatus, encryptionKey))
        conn.commit()
        cursor.close()
        conn.close()
        
        # login result and encrypted hash, expiry timestamp
        return jsonify({
            "loginResult": "Success",  # This can be dynamic based on your login logic
            "expiryTimestamp": expiryTimestamp,
            "message" : "your mother pass, passaway"
            }), 201
    except Exception as e:
        print(e)
        return jsonify({"error": str(e),
                        "message":"your mother failure"}), 500
##### End of Store encryption key associated with SessionID #####    

