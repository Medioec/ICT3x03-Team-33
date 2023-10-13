from flask import Flask, request, jsonify
import os
import psycopg2

app = Flask(__name__)


db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Adds a new user to the database     #####
@app.route('/databaseservice/add_user', methods=['POST'])
def add_user():
    try:
        # Get data from the request
        data = request.get_json()
        userId = data['userId']
        email = data['email']
        username = data['username']
        passwordHash = data['passwordHash']
        userRole = data['userRole']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the "user" table
        insert_query = "INSERT INTO user (userId, email, username, passwordHash, userRole) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (userId, email, username, passwordHash, userRole))
        conn.commit()

        cursor.close()
        conn.close()

        # Return HTTP 201 Created to indicate successful resource creation
        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        return jsonify({"error": str(e)}), 500
#####     End of add user     #####    

##### Checks if username is taken #####    
def check_user():
    try:
        # Get data from the request
        data = request.get_json()
        username = data['username']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user exists in the "user" table
        select_query = "SELECT username FROM user WHERE username = %s"
        cursor.execute(select_query, (username,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # User found, return HTTP 200 OK
            return jsonify({"message": "User found"}), 200
        else:
            # User not found, return HTTP 404 Not Found
            return jsonify({"message": "User not found"}), 404

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        return jsonify({"error": str(e)}), 500 
#####   End of check user     #####

#####   Checks if email is taken     #####
@app.route('/databaseservice/check_email', methods=['POST'])
def check_email():
    try:
        # Get data from the request
        data = request.get_json()
        email = data['email']

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Check if the email exists in the "user" table
        select_query = "SELECT email FROM user WHERE email = %s"
        cursor.execute(select_query, (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            # Email found, return HTTP 200 OK
            return jsonify({"message": "Email found"}), 200
        else:
            # Email not found, return HTTP 404 Not Found
            return jsonify({"message": "Email not found"}), 404

    except Exception as e:
        # Return HTTP 500 Internal Server Error for any unexpected errors
        return jsonify({"error": str(e)}), 500
#####   End of check email     #####

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
