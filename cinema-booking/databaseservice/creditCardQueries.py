from flask import request, jsonify, Blueprint
import os
import psycopg2
import psycopg2.extras
import base64
from psycopg2 import IntegrityError
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create blueprint
credit_card_bp = Blueprint("credit_card", __name__)

# Log credit card queries started
logger.info(f"Credit card queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

psycopg2.extras.register_uuid()

#####     Create a new credit card entry for user in the database     #####
@credit_card_bp.route('/add_credit_card', methods=['POST'])
def add_credit_card():
    # Log the addition of a new credit card entry
    logger.info(f"Adding new credit card started.")
    try:
        data = request.get_json()
        userId = data['userId']
        blob = data['blob']
        
        # convert blob to bytes
        blob_bytes = base64.b64decode(blob)

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO CreditCard (userId, blob) VALUES (%s, %s)"
        try:
            cursor.execute(insert_query, (userId, blob_bytes))
            conn.commit()
            cursor.close()
            conn.close()
            
            # Log the successful creation of a new credit card entry
            logger.info(f"Credit card added successfully.")
            return jsonify({"message": "CreditCard added successfully"}), 201
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            # Log the duplicate entry error
            logger.warning(f"Duplicate entry detected: This credit card already exists. userId: {userId}")
            return jsonify({"error": "Duplicate entry: This transaction already exists."}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of create credit card entry for user   #####

#####     Retrieve a credit card by its ID     #####
@credit_card_bp.route('/get_credit_card_by_id/<uuid:userId>/<int:creditCardId>', methods=['GET'])
def get_credit_card_by_id(userId, creditCardId):
    # Log the retrieval of a credit card entry
    logger.info(f"Retrieving credit card started.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user with the given userId owns the credit card with the given creditCardId
        select_owner_query = "SELECT userId FROM CreditCard WHERE creditCardId = %s"
        cursor.execute(select_owner_query, (creditCardId,))
        owner_id = cursor.fetchone()
    
        if owner_id and str(owner_id[0]) == str(userId): # uuid need to convert to string
            # If the user owns the credit card, retrieve it
            select_query = "SELECT * FROM CreditCard WHERE creditCardId = %s"
            cursor.execute(select_query, (creditCardId,))
            credit_card = cursor.fetchone()

            if credit_card:
                one_credit_card = {
                    "creditCardId": credit_card[0],
                    "userId": credit_card[1],
                    "blob": base64.b64encode(credit_card[2]).decode() # encode to b64 string
                }
                # Log the successful retrieval of a credit card entry
                logger.info(f"Credit card retrieved successfully.")
                return jsonify(one_credit_card), 200
            else:
                # Log the error
                logger.error(f"Credit card not found.")
                return jsonify({"message": "Credit Card not found"}), 404
        else:
            # Log the error
            logger.error(f"Access denied: No permissions. userId: {userId}")
            return jsonify({"message": "Access denied: No permissions"}), 403
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_credit_card_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of retrieve credit card by ID     #####

#####     Retrieve all credit cards from the database for user  #####
@credit_card_bp.route('/get_all_credit_cards/<uuid:userId>', methods=['GET'])
def get_all_credit_cards(userId):
    # Log the retrieval of all credit cards
    logger.info(f"Retrieving all credit cards started.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user with the given userId exists
        check_user_query = "SELECT userId FROM CinemaUser WHERE userId = %s"
        cursor.execute(check_user_query, (userId,))
        user = cursor.fetchone()

        if user:
            # If the user exists, retrieve all credit cards associated with that user
            select_query = "SELECT * FROM CreditCard WHERE userId = %s"
            cursor.execute(select_query, (userId,))
            all_credit_cards = cursor.fetchall()

            if all_credit_cards:
                all_credit_cards_list = []
                for credit_card in all_credit_cards:
                    one_credit_card = {
                        "creditCardId": credit_card[0],
                        "userId": credit_card[1],
                        "blob": base64.b64encode(credit_card[2]).decode() # encode to b64 string
                    }
                    all_credit_cards_list.append(one_credit_card)

                # Log the successful retrieval of all credit cards
                logger.info(f"Credit cards retrieved successfully.")
                return jsonify(all_credit_cards_list), 200
            else:
                # Log the error
                logger.error(f"No credit cards found for this user. userId: {userId}")
                return jsonify({"message": "No credit cards found for this user"}), 404
        else:
            # Log the error
            logger.error(f"User not found. userId: {userId}")
            return jsonify({"message": "User not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_all_credit_cards: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of all credit cards for user    #####

#####     Update a credit card entry by its ID     #####
@credit_card_bp.route('/update_credit_card', methods=['PUT'])
def update_credit_card():
    # Log the update of a credit card entry
    logger.info(f"Updating credit card started.")
    try:
        data = request.get_json()
        creditCardId = data.get('creditCardId')
        newUserId = data.get('userId')
        newBlob = data.get('blob')
        
        # convert blob to bytes
        blob_bytes = base64.b64decode(newBlob)
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if the user with the given userId owns the credit card with the given creditCardId
        select_owner_query = "SELECT userId FROM CreditCard WHERE creditCardId = %s"
        cursor.execute(select_owner_query, (creditCardId,))
        owner_id = cursor.fetchone()

        if owner_id and str(owner_id[0]) == newUserId:
            # If the user owns the credit card, update it
            update_query = "UPDATE CreditCard SET userId = %s, blob = %s WHERE creditCardId = %s"
            cursor.execute(update_query, (newUserId, blob_bytes, creditCardId))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # Log the successful update of a credit card entry
            logger.info(f"Credit card updated successfully.")
            return jsonify({"message": "Credit card updated successfully"}), 200
        else:
            # If the user does not own the credit card, reject the request with a 403 Forbidden response
            # Log the error
            logger.error(f"Access denied: No permissions. userId: {userId}")
            return jsonify({"message": "Access denied: No permissions"}), 403
    except Exception as e:
        # Log the error
        logger.error(f"Error in update_credit_card: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of update credit card entry by its ID     #####

#####     Delete a credit card entry by its ID     #####
@credit_card_bp.route('/delete_credit_card_by_id/<uuid:userId>/<int:creditCardId>', methods=['DELETE'])
def delete_credit_card_by_id(userId, creditCardId):
    # Log the deletion of a credit card entry
    logger.info(f"Deleting credit card started.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Check if the user with the given userId owns the credit card with the given creditCardId
        select_owner_query = "SELECT userId FROM CreditCard WHERE creditCardId = %s"
        cursor.execute(select_owner_query, (creditCardId,))
        owner_id = cursor.fetchone()

        if owner_id and str(owner_id[0]) == userId: # uuid need to convert to string
            # If the user owns the credit card, delete it
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM CreditCard WHERE creditCardId = %s"
            cursor.execute(delete_query, (creditCardId,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # Log the successful deletion of a credit card entry
            logger.info(f"Credit card deleted successfully.")
            return jsonify({"message": "Credit card deleted successfully"}), 200
        else:
            # If the user does not own the credit card, reject the request with a 403 Forbidden response
            # Log the error
            logger.error(f"Access denied: No permissions. userId: {userId}")
            return jsonify({"message": "Access denied: No permissions"}), 403
    except Exception as e:
        # Log the error
        logger.error(f"Error in delete_credit_card_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of delete credit card by ID     #####
