from flask import request, jsonify, Blueprint
import os
import psycopg2
import datetime
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create a blueprint
user_sessions_bp = Blueprint("user_sessions", __name__)

# Log user session queries started
logger.info(f"User session queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Adds a new session for a specific user to the database     #####
@user_sessions_bp.route('/create_user_session', methods=['POST'])
def create_user_session():
    # Log the addition of a new user session
    logger.info(f"Adding new user session started.")
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
        # log the successful creation of a new user session
        logger.info(f"User session added successfully. sessionId: {sessionId}")
        return jsonify({"message": "User session added successfully"}), 201
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in create_user_session: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of create session     #####


#####     Get session info given a sessionId     #####
@user_sessions_bp.route('/get_user_session', methods=['POST'])
def get_user_session():
    # Log the getting user session
    logger.info(f"Getting user session started.")
    try:
        # Get data from the request
        data = request.get_json()
        sessionId = data['sessionId']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Query session data
        select_query = "SELECT userId, expiryTimestamp, currStatus, encryptionKey FROM UserSessions WHERE sessionId = %s"
        cursor.execute(select_query, (sessionId,))
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
            
            # log the successful retrieval of a user session
            logger.info(f"User session retrieved successfully. sessionId: {sessionId}")
            return jsonify(response_data), 200
        else:
            # Session does not exist
            # log the error
            logger.error(f"Session not found. sessionId: {sessionId}")
            return jsonify({"message": "No data found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in get_user_session: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of create session     #####

##### Retrieves userId, password hash and user role from database #####
@user_sessions_bp.route('/get_userId_hash_role', methods=['POST'])
def get_userId_hash_role():
    # Log the getting user pwhash and role
    logger.info(f"Getting user pwhash and role started.")
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
            
            # log the successful retrieval of a user pwhash and role
            logger.info(f"User pwhash and role retrieved successfully. username: {username}")
            return jsonify(response_data), 200
        else:
            # User does not exist
            # log the error
            logger.error(f"User not found. username: {username}")
            return jsonify({"message": "No data found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in get_userId_hash_role: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####   End of pw hash retrieval   #####

##### Updates private key and expiry timestamp into database #####
@user_sessions_bp.route('/update_timestamp', methods=['PUT'])
def update_timestamp():
    # Log the updating of timestamp
    logger.info(f"Updating timestamp started.")
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
            # Session does not exist
            # log the error
            logger.error(f"Session not found. sessionId: {sessionId}")
            return jsonify({"error": "Session not found"}), 404
        else:
            conn.close()
            # log the successful update of timestamp
            logger.info(f"Timestamp updated successfully. sessionId: {sessionId}")
            return jsonify({"message": "Session updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####   End of updating keys and expiry   #####

##### Store encryption key associated with SessionID, for testing purpose, almost duplicate of user session #####
@user_sessions_bp.route('/store_key_in_database', methods=['POST'])
def store_key_in_database():
    # Log the storing of key in db
    logger.info(f"Storing key in db started.")
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
        # log the successful storing of key in db
        logger.info(f"Key stored in db successfully. userId: {userId}")
        return jsonify({
            "loginResult": "Success",  # This can be dynamic based on your login logic
            "expiryTimestamp": expiryTimestamp,
            "message" : "your mother pass, passaway"
            }), 201
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in store_key_in_database: {str(e)}")
        return jsonify({"error": str(e),
                        "message":"your mother failure"}), 500
##### End of Store encryption key associated with SessionID #####    

#####     Delete a user session by its ID     #####
@user_sessions_bp.route('/delete_session_by_id', methods=['DELETE'])
def delete_session_by_id():
    # Log the deletion of a user session
    logger.info(f"Deleting user session started.")
    try:
        # get sessionId from json
        data = request.get_json()
        sessionId = data['sessionId']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if session exists
        select_query = "SELECT * FROM usersessions WHERE sessionId = %s"
        
        cursor.execute(select_query, (sessionId,))
        session = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete session if it exists
        if session:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM usersessions WHERE sessionId = %s"
            cursor.execute(delete_query, (sessionId,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # log the successful deletion of a user session
            logger.info(f"User session deleted successfully. sessionId: {sessionId}")
            return jsonify({"message": "Session deleted successfully"}), 200
        else:
            # Session does not exist
            # log the error
            logger.error(f"Session not found. sessionId: {sessionId}")
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in delete_session_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of delete user session by ID     #####

#####     Update a user session status by its ID     #####
@user_sessions_bp.route('/update_session_status_by_id', methods=['PUT'])
def update_session_status_by_id():
    # Log the updating of a user session status
    logger.info(f"Updating user session status started.")
    try:
        # get sessionId from json
        data = request.get_json()
        sessionId = data['sessionId']
        currStatus = data['currStatus']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if session exists
        select_query = "SELECT * FROM usersessions WHERE sessionId = %s"
        
        cursor.execute(select_query, (sessionId,))
        session = cursor.fetchone()

        cursor.close()
        conn.close()
        

        # Delete session if it exists
        if session:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "UPDATE usersessions SET currStatus = %s WHERE sessionId = %s"
            cursor.execute(delete_query, (currStatus, sessionId,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # log the successful update of a user session status
            logger.info(f"User session status updated successfully. sessionId: {sessionId}")
            return jsonify({"message": "Session status updated successfully"}), 200
        else:
            # Session does not exist
            # log the error
            logger.error(f"Session not found. sessionId: {sessionId}")
            return jsonify({"message": "Session not found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in update_session_status_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of update user session status by ID     #####

##### Retrieves user role based on user ID #####
@user_sessions_bp.route('/get_role_by_id', methods=['POST'])
def get_role_by_id():
    # Log the getting user role
    logger.info(f"Getting user role started.")
    try:
        # Get data from the request
        data = request.get_json()
        userId = data['userId']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Construct the SQL query to retrieve the user role using userId
        select_data_query = "SELECT userRole FROM cinemauser WHERE userId = %s "
        cursor.execute(select_data_query, (userId,))
        data_result = cursor.fetchone()

        # Close the cursor and the database connection
        cursor.close()
        conn.close()

        # Separate the data into two attributes in a JSON response
        if data_result:
            # Assuming there's one result
            userRole = data_result[0]

            response_data = {
                "userRole": userRole
            }
            
            # log the successful retrieval of a user role
            logger.info(f"User role retrieved successfully. userId: {userId}")
            return jsonify(response_data), 200
        else:
            # User does not exist
            # log the error
            logger.error(f"User not found. userId: {userId}")
            return jsonify({"message": "No data found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in get_role_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####   End of user role by user ID retrieval   #####