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

app = Flask(__name__)
CORS(app)

# To use the endpoints in userQueries.py, access it via the url prefix '/databaseservice/user'. e.g. http://localhost:8085/databaseservice/user/add_user
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
app.register_blueprint(cinema_bp,url_prefix='/databaseservice/cinema')

# Seat table queries
app.register_blueprint(seat_bp,url_prefix='/databaseservice/seat')

# Theater table queries
app.register_blueprint(theater_bp,url_prefix='/databaseservice/theater')




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
