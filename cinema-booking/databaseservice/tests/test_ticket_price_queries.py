import unittest
from flask import Flask
from unittest.mock import patch, Mock
from your_project_directory.ticket_price_queries import ticket_price_bp

class TicketPriceQueriesTest(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(ticket_price_bp)
        self.client = self.app.test_client()

    def test_create_ticket_price_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1]
            
            response = self.client.post('/create_ticket_price', json={"ticketPriceCategory": "Adult", "ticketPriceValue": "15"})
            self.assertEqual(response.status_code, 201)
            self.assertIn(b"Ticket price added successfully", response.data)

    def test_get_ticket_price_by_id_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1, "Adult", 15]
            
            response = self.client.get('/get_ticket_price_by_id/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'"ticketPriceCategory": "Adult"', response.data)
            self.assertIn(b'"ticketPriceValue": 15', response.data)

    def test_get_ticket_price_by_id_not_found(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None
            
            response = self.client.get('/get_ticket_price_by_id/1')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Ticket price not found", response.data)

    def test_get_all_ticket_prices_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchall.return_value = [(1, "Adult", 15), (2, "Child", 10)]
            
            response = self.client.get('/get_all_ticket_prices')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'"ticketPriceCategory": "Adult"', response.data)
            self.assertIn(b'"ticketPriceValue": 15', response.data)
            self.assertIn(b'"ticketPriceCategory": "Child"', response.data)
            self.assertIn(b'"ticketPriceValue": 10', response.data)

    def test_update_ticket_price_by_id_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1, "Adult", 15]
            
            response = self.client.put('/update_ticket_price_by_id/1', json={"ticketPriceCategory": "Adult", "ticketPriceValue": "20"})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Ticket prices  updated successfully", response.data)

    def test_update_ticket_price_by_id_not_found(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None
            
            response = self.client.put('/update_ticket_price_by_id/1', json={"ticketPriceCategory": "Adult", "ticketPriceValue": "20"})
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Ticket price not found", response.data)

    def test_delete_ticket_price_by_id_success(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = [1, "Adult", 15]
            
            response = self.client.delete('/delete_ticket_price_by_id/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Ticket price deleted successfully", response.data)

    def test_delete_ticket_price_by_id_not_found(self):
        with patch('psycopg2.connect') as mock_connect:
            mock_cursor = Mock()
            mock_connect.return_value.cursor.return_value = mock_cursor
            mock_cursor.fetchone.return_value = None
            
            response = self.client.delete('/delete_ticket_price_by_id/1')
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Ticket price not found", response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
