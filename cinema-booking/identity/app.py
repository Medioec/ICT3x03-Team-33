from flask import Flask, request, jsonify
from argon2 import PasswordHasher
from email_validator import validate_email, EmailNotValidError
import requests
from flask_cors import CORS
import user_utils

app = Flask(__name__)
CORS(app)

# member registration
@app.route("/register", methods=["POST"])
def register(email, username, password):
    if user_utils.fields_are_missing(email, username, password):
        return jsonify({"message": "Please fill in all form data"}), 400

    if not user_utils.isUsernameAvailable(username):
        return jsonify({"message": "Username is already taken"}), 409

    if not user_utils.validatePassword(password):
        return jsonify({"message": "Password does not meet the requirements"}), 400

    try:
        validate_email(email, check_deliverability=True)

        if not user_utils.isEmailAvailable(email):
            return jsonify({"message": "Email is already in use"}), 409

        ph = PasswordHasher()
        hash = ph.hash(password)

        salt = "blah"
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
            return jsonify({"message": "Registration unsuccessful"}), 500

    except EmailNotValidError:
        return jsonify({"message": "Email is invalid"}), 400



        
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
