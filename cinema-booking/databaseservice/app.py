from flask import Flask
from flask_cors import CORS
from userTableQueries import user_bp
from userSessionsQueries import user_sessions_bp
from movieDetailsQueries import movie_details_bp
from ticketPriceQueries import ticket_price_bp
from transactionQueries import transaction_bp
from creditCardQueries import credit_card_bp
from bookingDetailsQueries import booking_details_bp

app = Flask(__name__)
CORS(app)

# To use the endpoints in userQueries.py, access it via the url prefix '/databaseservice/user'. e.g. http://localhost:8085/databaseservice/user/add_user
app.register_blueprint(user_bp,url_prefix='/databaseservice/user')
app.register_blueprint(user_sessions_bp,url_prefix='/databaseservice/usersessions')
app.register_blueprint(movie_details_bp,url_prefix='/databaseservice/moviedetails')
app.register_blueprint(ticket_price_bp,url_prefix='/databaseservice/ticketprice')
app.register_blueprint(transaction_bp,url_prefix='/databaseservice/transactions')
app.register_blueprint(credit_card_bp,url_prefix='/databaseservice/creditcard')
app.register_blueprint(booking_details_bp,url_prefix='/databaseservice/bookingdetails')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
