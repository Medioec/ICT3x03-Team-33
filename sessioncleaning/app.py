import Flask
from flask_cors import CORS
import psycopg2
import os
import logging

app=Flask(__name__)
CORS(app)

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

def delete_inactive_sessions():
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Delete sessions marked as 'inactive'
        delete_query = "DELETE FROM UserSessions WHERE currStatus = 'inactive'"
        try:
            cursor.execute(delete_query)
        conn.commit()

        logger.info("Deleted inactive sessions")

        cursor.close()
        conn.close()
    except Exception as e:
        logger.error("Error in delete_inactive_sessions")

if __name__ == "__main__":
    delete_inactive_sessions()