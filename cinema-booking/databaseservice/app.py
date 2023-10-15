from flask import Flask
from flask_cors import CORS
from userTableQueries import user_bp
app = Flask(__name__)
CORS(app)

# To use the endpoints in userQueries.py, access it via the url prefix '/databaseservice/user'. e.g. http://localhost:8085/databaseservice/user/add_user
app.register_blueprint(user_bp,url_prefix='/databaseservice/user')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
