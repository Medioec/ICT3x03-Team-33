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
        insert_query = "INSERT INTO user (userId, email, username, passwordHash, userRole) VALUES (%d, %s, %s, %s, %s)"
        cursor.execute(insert_query, (userId, email, username, passwordHash, userRole))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})
#####     End of add user     #####    

##### Checks if username is taken #####    
@app.route('/databaseservice/check_user', methods=['GET'])
def check_user():
    try:
        # Get data from the request
        data = request.get_json()
        username = data['username']
        

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the "user" table
        select_query = "SELECT username FROM user WHERE username = %s"
        cursor.execute(select_query, (username))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})    
#####   End of check user     #####

#####   Checks if email is taken     #####
@app.route('/databaseservice/check_email', methods=['GET'])
def check_email():
    try:
        # Get data from the request
        data = request.get_json()
        username = data['email']
        

        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into the "user" table
        select_query = "SELECT email FROM user WHERE email = %s"
        cursor.execute(select_query, (username))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})  
#####   End of check email     #####

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8085)
