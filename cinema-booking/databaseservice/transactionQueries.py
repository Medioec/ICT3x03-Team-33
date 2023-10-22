from flask import request, jsonify, Blueprint
import os
import psycopg2
from psycopg2 import IntegrityError 

transaction_bp = Blueprint("transaction", __name__)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
}

##### Create a new transaction entry in the database #####
@transaction_bp.route('/create_transaction', methods=['POST'])
def create_transaction():
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
            return jsonify({"message": "Transaction added successfully", "transactionId": transaction_id}), 201
        except IntegrityError as e:
            # Handle the IntegrityError (duplicate insertion) and return an HTTP error 409
            conn.rollback()  # Rollback the transaction
            cursor.close()
            conn.close()
            return jsonify({"error": "Duplicate entry: This transaction already exists."}), 409

    except Exception as e:
        return jsonify({"error": str(e)}), 500
##### End of create transaction entry #####

#####     Retrieve all transaction by userId     #####
@transaction_bp.route('/get_all_transactions_by_userId/<uuid:userId>', methods=['GET'])
def get_ticket_price_by_id(userId):
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

            return jsonify(transaction_list), 200
        else:
            return jsonify({"message": "No transactions found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all transaction by userId    #####

'''
NOTE: 
Update and Delete queries are not added intentionally 
to prevent tampering of transaction records. 

If required, should be done with database admin access.
'''
