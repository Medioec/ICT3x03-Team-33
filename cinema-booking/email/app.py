from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
import os
import requests

app = Flask(__name__)  
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

#####   throw error when JWT token is not valid     #####
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("unauthorized callback")
    return jsonify({"message": "Unauthorized access"}), 401
#####   End of throw error when JWT token is not valid     #####

############################## CREATE ACTIVATION LINK #########################################
@app.route("/create_activation_link", methods=["POST"])
def create_activation_link():
    print("in email container")
    # # get email from request
    # data = request.get_json()
    # email = data["email"]

    return jsonify({"message": "Activation Link created"}), 200
############################## END OF CREATE ACTIVATION LINK #########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=587)