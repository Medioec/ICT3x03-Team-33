from flask import request, jsonify, Blueprint
import os
import psycopg2
from psycopg2 import IntegrityError
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create a blueprint
transaction_bp = Blueprint("transaction", __name__)

# Log transaction queries started
logger.info("Transaction queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

##### Create a new transaction entry in the database #####
@transaction_bp.route('/create_transaction', methods=['POST'])
def create_transaction():
    # Log the addition of a new transaction entry
    logger.info("Adding new transaction started.")
    try:
        data = request.get_json()
        transactionId = data['transactionId']
        creditCardId = data['creditCardId']
        transactionDateTime = data['transactionDateTime']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO Transaction (transactionId, creditCardId, transactionDateTime) VALUES (%s, %s, %s)"
        
        try:
            cursor.execute(insert_query, (transactionId, creditCardId, transactionDateTime))
            transaction_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            # Log the successful creation of a new transaction entry
            logger.info("Transaction added successfully with new transactionId: {transaction_id}.")
            return jsonify({"message": "Transaction added successfully", "transactionId": transaction_id}), 201
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            # Log the error
            logger.error(f"Duplicate entry in create_transaction. transactionId: {transactionId}")
            return jsonify({"error": "Duplicate entry: This transaction already exists."}), 409
    except Exception as e:
        # Log the error
        logger.error(f"Error in create_transaction: {str(e)}")
        return jsonify({"error": str(e)}), 500
##### End of create transaction entry #####

#####     Retrieve all transaction by userId     #####
@transaction_bp.route('/get_all_transactions_by_userId/<uuid:userId>', methods=['GET'])
def get_all_transactions_by_userId(userId):
    # Log the retrieval of all transaction by userId
    logger.info("Retrieving all transactions by userId started.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM Transaction WHERE userId = %s"
        cursor.execute(select_query, (userId,))
        transactions = cursor.fetchone()

        cursor.close()
        conn.close()

        if transactions:
            transaction_list = []
            for transaction in transactions:
                one_transaction = {
                    "transactionId": transaction[0],
                    "creditCardId": transaction[1],
                    "transactionDateTime": transaction[2]
                }
                transaction_list.append(one_transaction)

            # Log the successful retrieval of all transaction by userId
            logger.info("All transactions by userId retrieved successfully. userId: {userId}.")
            return jsonify(transaction_list), 200
        else:
            # Log the error
            logger.error("No transactions found.")
            return jsonify({"message": "No transactions found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_all_transactions_by_userId: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all transaction by userId    #####

'''
NOTE: 
Update and Delete queries are not added intentionally 
to prevent tampering of transaction records. 

If required, should be done with database admin access.
'''
