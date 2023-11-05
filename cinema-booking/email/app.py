from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

app = Flask(__name__)  
CORS(app)

# gmail credentials
sender_email = os.getenv("EMAIL_NAME")
sender_password = os.getenv("EMAIL_PASSWORD")
base_host = os.getenv("BASE_HOST")
https_port = os.getenv("HTTPS_PORT")

############################## SEND STAFF ACTIVATION LINK #########################################
@app.route("/send_staff_activation_email", methods=["POST"])
def send_staff_activation_email():
    # get email from request
    data = request.get_json()
    recipient_email = data["email"]
    username = data["username"]
    activation_link = data["activation_link"]

    # Create activation link
    activation_link = f'https://{base_host}:{https_port}/activate?token={activation_link}'
    print("activation link: {}".format(activation_link))

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

                <p>Welcome to CineGo Team!</p>
                
                <p style="color: #666;">Your username is: <strong>{}</strong></p>

                <p style="color: #666;">To activate your staff account, please click the button below:</p>

                <a href="{}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; font-size: 16px; margin-top: 10px;">Activate Account</a>

                <p style="color: #999; font-size: 12px;">This email was sent by CineGo. Please do not reply to this email.</p>

            </div>

        </body>
        </html>
    """.format(username, activation_link)

    message = MIMEMultipart()
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    try:
        # Establish a connection to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            
            # Send the email
            smtp_server.sendmail(sender_email, recipient_email, message.as_string())

        return jsonify({"message": "Email sent!"}), 200
    
    except Exception as e:
        return jsonify({"message": "Error occurred"}), 500
############################## END OF SEND STAFF ACTIVATION LINK #########################################

############################## SEND MEMBER ACTIVATION LINK #########################################
@app.route("/send_member_activation_email", methods=["POST"])
def send_member_activation_email():
    # get email from request
    data = request.get_json()
    recipient_email = data["email"]
    username = data["username"]
    activation_link = data["activation_link"]

    # TODO: replace with actual url in production
    activation_link = f'https://{base_host}/verify?token={activation_link}'

    # create email
    subject = "Activate Your CineGo Account Now!"
    body = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Member Account Activation</title>
        </head>
        <body style="font-family: 'Arial', sans-serif;">

            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">

                <h2 style="color: #333;">Hello, {}</h2>

                <p>Welcome to CineGo - your ticket to a personalized cinema experience! we're delighted to have you onboard as our newest member.</p>

                <p>Once your account is activated, you'll be able to explore the magic of movies with our location-based cinema recommendations. Whether you're in the mood for a blockbuster or an indie film, we've got you covered.</p>

                <p style="color: #666;">To activate your account, please click the button below:</p>

                <a href="{}" style="display: inline-block; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; font-size: 16px; margin-top: 10px;">Activate Account</a>

                <p>Thanks for choosing CineGo. Get ready to discover the best cinemas near you!</p>

                <p style="color: #999; font-size: 12px;">This email was sent by CineGo. Please do not reply to this email.</p>

            </div>

        </body>
        </html>
    """.format(username, activation_link)

    message = MIMEMultipart()
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    try:
        # Establish a connection to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            
            # Send the email
            smtp_server.sendmail(sender_email, recipient_email, message.as_string())

        return jsonify({"message": "Email sent!"}), 200
    
    except Exception as e:
        return jsonify({"message": "Error occurred"}), 500
############################## END OF SEND MEMBER ACTIVATION LINK #########################################

############################## SEND OTP #########################################
@app.route("/send_otp", methods=["POST"])
def send_otp():
    # get email from request
    data = request.get_json()
    recipient_email = data["email"]
    username = data["username"]
    otp = data["otp"]

    # create email
    subject = "Code to Sign In to CineGo"
    body = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP for Signing In to CineGo</title>
        </head>
        <body style="font-family: 'Arial', sans-serif;">

            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd;">

                <h2 style="color: #333;">Hello, {}</h2>

                <p>Enter the code below within the next 60 seconds to sign in to CineGo:</p>

                <h1 style="color: #333;">{}</h1>

                <p style="color: #999; font-size: 12px;">This email was sent by CineGo. Please do not reply to this email.</p>

            </div>

        </body>
        </html>
    """.format(username, otp)

    message = MIMEMultipart()
    message['Subject'] = subject
    message.attach(MIMEText(body, 'html'))

    try:
        # Establish a connection to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            
            # Send the email
            smtp_server.sendmail(sender_email, recipient_email, message.as_string())

        return jsonify({"message": "Email sent!"}), 200
    
    except Exception as e:
        return jsonify({"message": "Error occurred"}), 500
############################## END OF SEND OTP #########################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=587)