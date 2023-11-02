import psycopg2
import os
import logging
import argparse

# Create or get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# File handler
file_handler_path = './logs/sessioncleaner.log'
file_handler = logging.FileHandler(file_handler_path)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# Stream (console) handler for stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)

logger.info("Database Service started")

# Set up db config credentials
db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_NORMALUSER"),
    "password": os.getenv("DB_NORMALPASSWORD"),
    "host": os.getenv("DB_HOST"),
}

# Function to delete inactive sessions
def delete_inactive_sessions():
    # log the function call
    logger.info("delete_inactive_sessions called")
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        currStatus = 'inactive'
        
        # Checks to see if inactive session exists
        select_query = "SELECT * FROM usersessions WHERE currStatus = %s"
        
        cursor.execute(select_query, (currStatus,))
        sessionInactiveExists = cursor.fetchone()
        
        
        # If inactive session exists, delete it
        if sessionInactiveExists:
            delete_query = "DELETE FROM UserSessions WHERE currStatus = %s"
            cursor.execute(delete_query, (currStatus,))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # log deleted inactive sessions
            logger.info("Deleted inactive sessions")
        else:
            cursor.close()
            conn.close()
            # log no sessions to delete
            logger.info("No inactive sessions to delete")
    except Exception as e:
        cursor.close()
        conn.close()
        logger.error("Uncaught error in delete_inactive_sessions")
        logger.error(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run specific functions from this script.")
    parser.add_argument('--run-function', action='store_true', help='Run the special function')

    args = parser.parse_args()

    if args.run_function:
        delete_inactive_sessions()