from argon2 import PasswordHasher
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from email_validator import validate_email, EmailNotValidError
from flask import Flask, request, jsonify
from flask_cors import CORS
import flask_jwt_extended as jwt
import requests
import user_utils

app = Flask(__name__)
CORS(app)

# member registration
@app.route("/register", methods=["POST"])
def register():
    # get data from registration form
    data = request.get_json()
    email = data['email']
    username = data['username']
    password = data['password']

    # TODO SANITIZE EMAIL & USERNAME

    if not email or not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400

    # ensure username and password contain only allowed characters
    if not user_utils.validateUsername(username):
        return jsonify({"message": "Username does not meet the requirements"}), 400
    
    if not user_utils.validatePassword(password):
        return jsonify({"message": "Password does not meet the requirements"}), 400
    
    # check if username still exists in db
    if not user_utils.isUsernameAvailable(username):
        return jsonify({"message": "Username is already taken"}), 409

    try:
        validate_email(email, check_deliverability=True)

        if not user_utils.isEmailAvailable(email):
            return jsonify({"message": "Email is already in use"}), 409

        ph = PasswordHasher()
        hash = ph.hash(password)

        role = "member"
        userId = user_utils.generateUUID()
        
        data = {
            "userId": userId,
            "email": email,
            "username": username,
            "passwordHash": hash,
            "userRole": role
        }

        response = requests.post("http://databaseservice:8085/databaseservice/user/add_user", json=data)

        if response.status_code == 201:
            return jsonify({"message": "Registration successful"}), 200
        else:
            return jsonify({"message": "Error occurred"}), 500

    except EmailNotValidError:
        return jsonify({"message": "Email is invalid"}), 400

@app.route("/login", methods=["POST"])
def login():
    # get data from login form
    data = request.get_json()
    username = data['username']
    password = data['password']

    if not username or not password:
        return jsonify({"message": "Please fill in all form data"}), 400
    
    # if username does not exist in db
    if user_utils.isUsernameAvailable(username):
        return jsonify({"message": "Username or password was incorrect"}), 404

    # get password hash and role from db where username = ?
    reqData = {"username": username}
    response = requests.post("http://databaseservice:8085/databaseservice/usersessions/get_hash_role", json=reqData)

    if response.status_code != 200:
        return jsonify({"message": response.reason}), 500
    else:
        # hash password from login form and verify that hashes match
        ph = PasswordHasher()
        newHash = ph.hash(password)
        return jsonify(response.json()), 200
        # if (response.data != newHash):
        #     return jsonify({"message": "Username or password was incorrect"}), 404
        

        # if hashes match, login successful
        # generate session token BASED ON ROLE
        # insert session token and expiry into db
        # return session token

        # JWT SIGN TOKEN INTEGRITY - NOT ENABLED ON DEFAULT

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
