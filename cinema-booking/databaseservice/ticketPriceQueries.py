from flask import request, jsonify, Blueprint
import os
import psycopg2
import logging

# Create or get the logger
logger = logging.getLogger(__name__)

# Create blueprint
ticket_price_bp = Blueprint("ticket_price", __name__)

# Log ticket price queries started
logger.info("Ticket price queries started.")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Create a new ticket price entry in the database     #####
@ticket_price_bp.route('/create_ticket_price', methods=['POST'])
def create_ticket_price():
    # Log the addition of a new ticket price entry
    logger.info("Adding new ticket price started.")
    try:
        data = request.get_json()
        ticketPriceCategory = data['ticketPriceCategory']
        ticketPriceValue = data['ticketPriceValue']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO TicketPrice (ticketPriceCategory, ticketPriceValue) VALUES (%s, %s) RETURNING ticketPriceId"
        cursor.execute(insert_query, (ticketPriceCategory, ticketPriceValue))
        new_ticket_price_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        # Log the successful creation of a new ticket price entry
        logger.info("Ticket price added successfully with new ticketPriceId: {new_ticket_price_id}.")
        return jsonify({"message": "Ticket price added successfully", "ticketPriceId": new_ticket_price_id}), 201
    except Exception as e:
        # Log the error
        logger.error(f"Error in create_ticket_price: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of create ticket price entry     #####


#####     Retrieve a ticket price by its ID     #####
@ticket_price_bp.route('/get_ticket_price_by_id/<int:ticket_price_id>', methods=['GET'])
def get_ticket_price_by_id(ticket_price_id):
    # Log the retrieval of a ticket price entry
    logger.info(f"Retrieving ticket price details for ticketPriceId: {ticket_price_id}.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM TicketPrice WHERE ticketPriceId = %s"
        cursor.execute(select_query, (ticket_price_id,))
        ticket_price = cursor.fetchone()

        cursor.close()
        conn.close()

        if ticket_price:
            one_ticket_price = {
                "ticketPriceId": ticket_price[0],
                "ticketPriceCategory": ticket_price[1],
                "ticketPriceValue": ticket_price[2]
            }
            
            # Log the successful retrieval of a ticket price entry
            logger.info("Ticket price retrieved successfully.")
            return jsonify(one_ticket_price), 200
        else:
            # Ticket price Id does not exist
            # Log the error
            logger.error(f"Ticket price not found for ticketPriceId: {ticket_price_id}.")
            return jsonify({"message": "Ticket price not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_ticket_price_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of retrieve ticket price by ID     #####

#####     Retrieve all ticket prices from the database     #####
@ticket_price_bp.route('/get_all_ticket_prices', methods=['GET'])
def get_all_ticket_prices():
    # Log the retrieval of all ticket prices
    logger.info("Retrieving all ticket prices.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM TicketPrice"
        cursor.execute(select_query)
        all_ticket_prices = cursor.fetchall()

        cursor.close()
        conn.close()

        all_ticket_prices_list = []
        for ticket in all_ticket_prices:
            ticketPrice = {
                "ticketPriceId": ticket[0],
                "ticketPriceCategory": ticket[1],
                "ticketPriceValue": ticket[2]
            }
            all_ticket_prices_list.append(ticketPrice)

        # Log the successful retrieval of all ticket prices
        logger.info("All ticket prices retrieved successfully.")
        return jsonify(all_ticket_prices_list), 200
    except Exception as e:
        # Log the error
        logger.error(f"Error in get_all_ticket_prices: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all ticket prices     #####

#####     Update a ticket price entry by its ID     #####
@ticket_price_bp.route('/update_ticket_price_by_id/<int:ticket_price_id>', methods=['PUT'])
def update_ticket_price_by_id(ticket_price_id):
    # Log the update of a ticket price entry
    logger.info(f"Updating ticket price details for ticketPriceId: {ticket_price_id}.")
    try:
        data = request.get_json()
        ticketPriceCategory = data['ticketPriceCategory']
        ticketPriceValue = data['ticketPriceValue']
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if Ticket price exists
        select_query = "SELECT * FROM TicketPrice WHERE ticketPriceId = %s"
        
        cursor.execute(select_query, (ticket_price_id,))
        ticket_price = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Update Ticket price if it exists
        if ticket_price:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            
            update_query = "UPDATE TicketPrice SET ticketPriceCategory = %s, ticketPriceValue = %s WHERE ticketPriceId = %s"
            cursor.execute(update_query, (ticketPriceCategory, ticketPriceValue, ticket_price_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # Log the successful update of a ticket price entry
            logger.info("Ticket price updated successfully. ticketPriceId: {ticket_price_id}.")
            return jsonify({"message": "Ticket prices  updated successfully"}), 200            
        else:
            # Ticket price does not exist
            # Log the error
            logger.error(f"Ticket price not found for ticketPriceId: {ticket_price_id}.")
            return jsonify({"message": "Ticket price not found"}), 404
    except Exception as e:
        # Log the error
        return jsonify({"error": str(e)}), 500
#####     End of update ticket price by ID     #####

#####     Delete a ticket price entry by its ID     #####
@ticket_price_bp.route('/delete_ticket_price_by_id/<int:ticket_price_id>', methods=['DELETE'])
def delete_ticket_price_by_id(ticket_price_id):
    # Log the deletion of a ticket price entry
    logger.info(f"Deleting ticket price details for ticketPriceId: {ticket_price_id}.")
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if Ticket price exists
        select_query = "SELECT * FROM TicketPrice WHERE ticketPriceId = %s"
        
        cursor.execute(select_query, (ticket_price_id,))
        ticket_price = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete ticket price if it exists
        if ticket_price:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM TicketPrice WHERE ticketPriceId = %s"
            cursor.execute(delete_query, (ticket_price_id,))
            conn.commit()

            cursor.close()
            conn.close()
            
            # Log the successful deletion of a ticket price entry
            logger.info("Ticket price deleted successfully. ticketPriceId: {ticket_price_id}.")
            return jsonify({"message": "Ticket price deleted successfully"}), 200
        else:
            # Ticket price Id does not exist
            # Log the error
            logger.error(f"Ticket price not found for ticketPriceId: {ticket_price_id}.")
            return jsonify({"message": "Ticket price not found"}), 404
    except Exception as e:
        # Log the error
        logger.error(f"Error in delete_ticket_price_by_id: {str(e)}")
        return jsonify({"error": str(e)}), 500
#####     End of delete ticket price by ID     #####
