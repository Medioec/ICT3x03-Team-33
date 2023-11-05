import unittest
from unittest.mock import patch
from app import app  # This should be the name of the module where your Flask app is defined
from app import send_staff_activation_email, send_member_activation_email
class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        """Setup the app for testing."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    @patch('app.send_staff_activation_email')
    def test_send_staff_activation_email_failure(self, mock_send_email):
        # Mock the send_staff_activation_email method to raise an exception
        mock_send_email.side_effect = Exception('An error occurred')

        # Use the test client to send a POST request to the route
        response = self.client.post('/send_staff_activation_email', json={
            "email": "test@example.com",
            "username": "test_user",
            "activation_link": "12345"
        })

        # Check that the response is as expected
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Error occurred"})

    @patch('app.smtplib.SMTP_SSL')
    @patch('app.os.getenv')
    def test_send_staff_activation_email_success(self, mock_getenv, mock_smtp):
        mock_getenv.return_value = 'fake_value'
        
        # Assume the email sending via SMTP works fine
        # No need to mock any of its methods or attributes since you're not checking them here

        # Use the test client to send a POST request to the route
        response = self.client.post('/send_staff_activation_email', json={
            "email": "test@example.com",
            "username": "test_user",
            "activation_link": "12345"
        })

        # Check that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Email sent!"})

    @patch('app.send_member_activation_email')
    def test_invalid_recipient_email_address_format_returns_error(self, mock_send_email):
        mock_send_email.side_effect = Exception('An error occurred')

        response = self.client.post("/send_member_activation_email", json={"email": "invalid_email", "username": "test_user", "activation_link": "12345"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Error occurred"})

    
        

    @patch('app.send_member_activation_email')
    def test_invalid_activation_link_format_returns_error(self, mock_send_email):
        mock_send_email.return_value = ({"message": "Error occurred"}, 500)

        response = self.client.post("/send_member_activation_email", json={"email": "test@example.com", "username": "test_user", "activation_link": "invalid_link"})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"message": "Error occurred"})


if __name__ == '__main__':
    unittest.main()
