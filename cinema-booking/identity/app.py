from flask import Flask, request, jsonify
from argon2 import PasswordHasher
from email_validator import validate_email, EmailNotValidError
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


# member registration
@app.route("/register", methods=["POST"])
def register():
    # get data from registration form
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")

    # check if username is available
    response, status_code = isUsernameAvailable(username)

    # if username is not in the database
    if status_code == 200:
        # validate email
        try:
            validate_email(email, check_deliverability=True)

            # generate password hash
            ph = PasswordHasher()
            hash = ph.hash(password)
            
            # get salt from hash
            temp_arr = hash.split('$')
            salt = temp_arr[:-2]

            # join remaining string together as hash
            temp_arr = temp_arr[:-2] + temp_arr[-1:]
            hash = '$'.join(temp_arr)

            # insert email, username, hash, salt, and role into database
            role = "member"

            return jsonify({"message": "Registration successful"}), 200
        
        # if email is invalid
        except EmailNotValidError:
            return jsonify({"message": "Email is invalid"}), 400

    # if username is taken
    else:
        return jsonify({"message": response}), status_code 

# for registrationL: check if username is available/does not exist in db
def isUsernameAvailable(username): 
    # check if username is taken
    if username == "test": # placeholder: to replace with db service code
        return "Username is already taken", 409

    # if username does not exist
    else:
        return "Username is available", 200
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
