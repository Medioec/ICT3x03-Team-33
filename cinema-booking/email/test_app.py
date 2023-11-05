import unittest
from unittest.mock import patch
from flask import Flask
from app import app  # Replace with actual path to your Flask application
import smtplib

# Define the mock environment variables
env_vars = {
    'EMAIL_HOST': 'smtp.example.com',
    'EMAIL_NAME': 'example@gmail.com',
    'EMAIL_PASSWORD': 'password',
    'EMAIL_PORT': '587'
}

@patch('os.getenv', side_effect=lambda k, d=None: env_vars.get(k, d))
@patch('smtplib.SMTP_SSL')
class TestSendStaffActivationEmail(unittest.TestCase):

    def setUp(self):
        # Import the Flask app inside the setUp method after the environment has been mocked
        from app import app
        self.app = app

    def test_email_sent_successfully(self, mock_smtp, mock_getenv):
        mock_server = mock_smtp.return_value.__enter__.return_value
        mock_server.login.return_value = True
        mock_server.sendmail.return_value = True
        
        client = self.app.test_client()
        response = client.post("/send_staff_activation_email", json={
            "email": "test@example.com",
            "username": "test_user",
            "activation_link": "https://None/activate?token=12345"
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Email sent!"})
        mock_server.login.assert_called_once_with('example@gmail.com', 'password')
        mock_server.sendmail.assert_called()

    def test_email_sent_failure(self, mock_smtp, mock_getenv):
        mock_server = mock_smtp.return_value.__enter__.return_value
        mock_server.login.side_effect = smtplib.SMTPException("SMTP authentication error")
        
        client = self.app.test_client()
        response = client.post("/send_staff_activation_email", json={
            "email": "test@example.com",
            "username": "test_user",
            "activation_link": "https://None/activate?token=12345"
        })

        self.assertEqual(response.status_code, 500)
        self.assertIn("Error sending email", response.json["message"])
        mock_server.login.assert_called_once_with('example@gmail.com', 'password')

if __name__ == '__main__':
    unittest.main()
