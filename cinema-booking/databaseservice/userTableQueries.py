from flask import request, jsonify, Blueprint
import os
import psycopg2
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create a blueprint
user_bp = Blueprint("user", __name__)

# Log user queries started
logger.info("User queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Adds a new user to the database     #####
@user_bp.route('/add_user', methods=['POST'])
def add_user():
    # Log the addition of a new user
    logger.info("Adding new user started.")
    try:
        # Get data from the request
        data = request.get_json()
        userId = data['userId']
        email = data['email']
        username = data['username']
        passwordHash = data['passwordHash']
        userRole = data['userRole']
        activationLink = data['activationLink']
        isActivationLinkUsed = data['isActivationLinkUsed']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the "cinemauser" table
        insert_query = "INSERT INTO cinemauser (userId, email, username, passwordHash, userRole, activationLink, isActivationLinkUsed) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (userId, email, username, passwordHash, userRole, activationLink, isActivationLinkUsed))
        conn.commit()

        cursor.close()
        conn.close()

        # Return HTTP 201 Created to indicate successful resource creation
        # log the successful creation of a new user
        logger.info("User added successfully. username: {username}")
        return jsonify({"message": "User added successfully"}), 201
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in add_user: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of add user     #####

##### Get user information #####
@user_bp.route('/get_user_details', methods=['POST'])    
def get_user_details():
    # Log the retrieval of a user
    logger.info("Retrieving user details started.")
    try:
        # Get data from the request
        data = request.get_json()
        username = data['username']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user exists in the "user" table
        select_query = "SELECT * FROM cinemauser WHERE username = %s"
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()

        print (user)
        
        cursor.close()
        conn.close()

        if user:
            # User found, return HTTP 200 OK
            user_details = {
                "userId": user[0],
                "email": user[1],
                "username": user[2],
                "passwordHash": user[3],
                "userRole": user[4],
                "isUserBanned": user[5],
                "activationLink": user[6],
                "isActivationLinkUsed": user[7]
            }
            
            # Log the successful retrieval of a user
            logger.info("User retrieved successfully. username: {username}")
            return jsonify(user_details), 200
        else:
            # User not found, return HTTP 404 Not Found
            # Log the user not found error
            logger.warning("User not found with username: {username}.")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in get_user_details: {str(e)}")
        return jsonify({"error": str(e)}), 500 
#####   End of get user information     #####    

##### Checks if username is taken #####
@user_bp.route('/check_user', methods=['POST'])    
def check_user():
    # Log checking if username is taken
    logger.info("Checking if username is taken started.")
    try:
        # Get data from the request
        data = request.get_json()
        username = data['username']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user exists in the "user" table
        select_query = "SELECT username FROM cinemauser WHERE username = %s"
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # User found, return HTTP 200 OK
            # Log the successful retrieval of a user
            logger.info("User found with username: {username}.")
            return jsonify({"message": "User found"}), 200
        else:
            # User not found, return HTTP 404 Not Found
            # Log the user not found error
            logger.warning("User not found with username: {username}.")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in check_user: {str(e)}")
        return jsonify({"error": str(e)}), 500 
#####   End of check user     #####

#####   Checks if email is taken     #####
@user_bp.route('/check_email', methods=['POST'])
def check_email():
    # Log checking if email is taken
    logger.info("Checking if email is taken started.")
    try:
        # Get data from the request
        data = request.get_json()
        email = data['email']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the email exists in the "user" table
        select_query = "SELECT email FROM cinemauser WHERE email = %s"
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Email found, return HTTP 200 OK
            # Log the successful retrieval of a user
            logger.info("Email found with email: {email}.")
            return jsonify({"message": "Email found"}), 200
        else:
            # Email not found, return HTTP 404 Not Found
            # Log the email not found error
            logger.warning("Email not found with email: {email}.")
            return jsonify({"message": "Email not found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in check_email: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####   End of check email     #####

#####   Delete user by user id     #####
@user_bp.route('/delete_user', methods=['DELETE'])
def delete_user_by_id():
    try:
        # Get data from the request
        data = request.get_json()
        userId = data['userId']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Checks to see if user exists
        select_query = "SELECT * FROM cinemauser WHERE userId = %s"
        
        cursor.execute(select_query, (userId,))
        session = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete user if it exists
        if session:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM cinemauser WHERE userId = %s"
            cursor.execute(delete_query, (userId,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # log the successful deletion of a user session
            logger.info("User deleted successfully. userId: {userId}")
            return jsonify({"message": "User deleted successfully"}), 200

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in delete_user: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####   End of delete user by user id     #####

#####     Update a user password by their username   #####
@user_bp.route('/update_password_by_username', methods=['PUT'])
def update_password_by_username():
    # Log the updating of a user password
    logger.info("Updating user password started.")
    try:
        # get username and password from json
        data = request.get_json()
        username = data['username']
        passwordHash = data['passwordHash']
        isActivationLinkUsed = data['isActivationLinkUsed']
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if user exists
        select_query = "SELECT * FROM cinemauser WHERE username = %s"
        
        cursor.execute(select_query, (username,))
        session = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Update session if it exists
        if session:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            update_query = "UPDATE cinemauser SET passwordHash = %s, isActivationLinkUsed = %s WHERE username = %s"
            cursor.execute(update_query, (passwordHash, isActivationLinkUsed, username,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # log the successful update of a user session status
            print("user password set", username)
            logger.info("User password updated successfully. username: {username}")
            return jsonify({"message": "User password updated successfully"}), 200
        else:
            # Session does not exist
            # log the error
            logger.error("User not found. username: {username}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        # Log the error
        logger.error(f"Error in update_password_by_username: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of update user password by username    #####