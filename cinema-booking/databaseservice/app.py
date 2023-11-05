from flask import Flask
from flask_cors import CORS
from userTableQueries import user_bp
from userSessionsQueries import user_sessions_bp
from movieDetailsQueries import movie_details_bp
from ticketPriceQueries import ticket_price_bp
from transactionQueries import transaction_bp
from creditCardQueries import credit_card_bp
from bookingDetailsQueries import booking_details_bp
from showtimesQueries import showtimes_bp
from cinemaTableQueries import cinema_bp
from seatTableQueries import seat_bp
from theaterTableQueries import theater_bp
import logging

app = Flask(__name__)
CORS(app)

# Create or get the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

# File handler
file_handler_path = './logs/databaseServiceLogs.log'
file_handler = logging.FileHandler(file_handler_path)
file_handler.setFormatter(log_format)
logger.addHandler(file_handler)

# Stream (console) handler for stdout
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)

logger.info(f"Database Service started")

# User table queries
app.register_blueprint(user_bp,url_prefix='/databaseservice/user')

# User sessions table queries
app.register_blueprint(user_sessions_bp,url_prefix='/databaseservice/usersessions')

# Movie details table queries
app.register_blueprint(movie_details_bp,url_prefix='/databaseservice/moviedetails')

# Ticket price table queries
app.register_blueprint(ticket_price_bp,url_prefix='/databaseservice/ticketprice')

# Transaction table queries
app.register_blueprint(transaction_bp,url_prefix='/databaseservice/transactions')

# Credit card table queries
app.register_blueprint(credit_card_bp,url_prefix='/databaseservice/creditcard')

# Booking details table queries
app.register_blueprint(booking_details_bp,url_prefix='/databaseservice/bookingdetails')

# Showtimes table queries
app.register_blueprint(showtimes_bp,url_prefix='/databaseservice/showtimes')

# Cinema table queries
app.register_blueprint(cinema_bp,url_prefix='/databaseservice/cinemas')

# Seat table queries
app.register_blueprint(seat_bp,url_prefix='/databaseservice/seats')

# Theater table queries
app.register_blueprint(theater_bp,url_prefix='/databaseservice/theaters')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
