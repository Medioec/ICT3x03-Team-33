from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
import os
import requests
import smtplib

app = Flask(__name__)  
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# gmail credentials
sender_email = os.getenv("EMAIL_NAME")
sender_password = os.getenv("EMAIL_PASSWORD")

#####   throw error when JWT token is not valid     #####
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("unauthorized callback")
    return jsonify({"message": "Unauthorized access"}), 401
#####   End of throw error when JWT token is not valid     #####

############################## CREATE ACTIVATION LINK #########################################
@app.route("/create_activation_link", methods=["POST"])
def create_activation_link():
    # get email from request
    data = request.get_json()
    recipient_email = data["email"]
    username = data["username"]
    activation_link = data["activation_link"]

    # TODO: replace with actual url in production
    activation_link = f'https://localhost.com/activate?token={activation_link}'

    # create email
    subject = "Activate Your Account"
    body = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Staff Account Activation</title>
        </head>
        <body style="font-family: 'Arial', sans-serif;">

            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">

                <h2 style="color: #333;">Staff Account Activation</h2>

                <p>Welcome to Secuu Movies Team!</p>
                
                <p style="color: #666;">Your username is:</p><bold>{username}</bold>

                <p style="color: #666;">To activate your staff account, please click the button below:</p>

                <a href="{activation_link}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; font-size: 16px; margin-top: 10px;">Activate Account</a>

                <p style="color: #999; font-size: 12px;">This email was sent by Secuu Movies. Please do not reply to this email.</p>

            </div>

        </body>
        </html>
    """

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    try:
        # Establish a connection to Gmail's SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            
            # Login to your Gmail account
            server.login(sender_email, sender_password)
            
            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

        return jsonify({"message": "Email sent!"}), 200
    
    except Exception as e:
        return jsonify({"message": f"Error sending email: {str(e)}"}), 500
############################## END OF CREATE ACTIVATION LINK #########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=587)