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
def register():
    # get data from registration form
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    # ensure all fields are filled in
    if (email is not None) and (username is not None) and (password is not None):
        # if username is not in the database
        if user_utils.isUsernameAvailable(username):
            
            # validate password
            if user_utils.validatePassword(password): 

                # validate email
                try:
                    validate_email(email, check_deliverability=True)

                    # check if email is available
                    if user_utils.isEmailAvailable(email):

                        # generate password hash
                        ph = PasswordHasher()
                        hash = ph.hash(password)

                        salt = "blah"

                        # generate userId and role
                        role = "member"
                        userId = user_utils.generateUUID()

                        # insert email, username, hash and role into database
                        data = {
                            "userId": userId,
                            "email": email,
                            "username": username,
                            "passwordHash": hash,
                            "userRole": role
                        }
                        response = requests.post("http://databaseservice:8085/databaseservice/user/add_user", json=data)
                        
                        # if data inserted successfully into db, return HTTP ok
                        if response.status_code == 201:
                            return jsonify({"message": "Registration successful"}), 200
                        
                        # if data not inserted successfully into db, return HTTP internal server error
                        else:
                            return jsonify({"message": "Registration unsuccessful"}), 500
                
                    else:
                        return jsonify({"message": "Email is already in use"}), 409
                    
                # if email is invalid, return HTTP bad request
                except EmailNotValidError:
                    return jsonify({"message": "Email is invalid"}), 400

            else:
                return jsonify({"message": "Password does not meet the requirements"}), 400
        
        # if username is taken, return HTTP conflict 
        else:
            return jsonify({"message": "Username is already taken"}), 409 
    
    # if any field in form is incomplete, return error 
    else:
        return jsonify({"message": "Please fill in all form data"}), 400
        
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
