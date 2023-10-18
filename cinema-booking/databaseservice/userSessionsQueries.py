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
        privateKey = data['privateKey']
        expiryTimestamp = data['expiryTimestamp']
        currStatus = data['currStatus']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the UserSessions table
        insert_query = "INSERT INTO usersessions (sessionId, userId, privateKey, expiryTimestamp, currStatus) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (sessionId, userId,
                       privateKey, expiryTimestamp, currStatus))
        conn.commit()

        cursor.close()
        conn.close()

        # Return HTTP 201 Created to indicate successful resource creation
        return jsonify({"message": "User session added successfully"}), 201

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        return jsonify({"error": str(e)}), 500
#####     End of create session     #####

##### Retrieves password hash and private key from database #####
@user_sessions_bp.route('/get_key_hash', methods=['POST'])
def get_key_hash():
    try:
        # Get data from the request
        data = request.get_json()
        sessionId = data['sessionId']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Construct the SQL query to retrieve the password hash and private key using session id
        select_data_query = """
            SELECT cu.passwordHash, us.privateKey
            FROM CinemaUser cu
            JOIN UserSessions us ON cu.userId = us.userId
            WHERE us.sessionId = %s;
        """
        cursor.execute(select_data_query, (sessionId,))
        data_result = cursor.fetchall()

        # Close the cursor and the database connection
        cursor.close()
        conn.close()

        # Separate the data into two attributes in a JSON response
        if data_result:
            # Assuming there's one result
            passwordHash, privateKey = data_result[0]
            response_data = {
                "passwordHash": passwordHash,
                "privateKey": privateKey
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"message": "No data found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####   End of pw hash and private key retrieval   #####

##### Updates private key and expiry timestamp into database #####
@user_sessions_bp.route('/update_key_timestamp', methods=['PUT'])
def update_key_timestamp():
    try:
        # Get data from the request
        data = request.get_json()
        sessionId = data['sessionId']
        newPrivateKey = data['privateKey']
        newExpiryTimestamp = data['expiryTimestamp']
        
        if sessionId is None or newPrivateKey is None or newExpiryTimestamp is None:
            return jsonify({"error": "Missing data in the request"}), 400

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        update_data_query = """
        UPDATE UserSessions
        SET privateKey = %s, expiryTimestamp = %s
        WHERE sessionId = %s
        """
        cursor.execute(update_data_query, (newPrivateKey, newExpiryTimestamp, sessionId))
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Session not found"}), 404

        conn.close()
        return jsonify({"message": "Session updated successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####   End of updating keys and expiry   #####
