import unittest
from your_flask_app import create_app, db  # Update this according to your project structure
from your_flask_app.seatTableQueries import seat_bp  # Update this according to your project structure

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_test_database_uri'  # Update this to your test database URI
app.register_blueprint(seat_bp)

class SeatTableQueriesTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.seat_data = {
            'seatId': 1,
        }

    def test_add_seat(self):
        response = self.client.post('/add_seat', json=self.seat_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Seat added successfully', response.get_data(as_text=True))

    def test_get_seat_by_id(self):
        # Add a seat first
        self.client.post('/add_seat', json=self.seat_data)

        response = self.client.get('/get_seat_by_id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1', response.get_data(as_text=True))

    def test_get_all_seats(self):
        # Add some seats first
        self.client.post('/add_seat', json={'seatId': 1})
        self.client.post('/add_seat', json={'seatId': 2})
        self.client.post('/add_seat', json={'seatId': 3})

        response = self.client.get('/get_all_seats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('1', response.get_data(as_text=True))
        self.assertIn('2', response.get_data(as_text=True))
        self.assertIn('3', response.get_data(as_text=True))

    def test_update_seat_by_id(self):
        # Add a seat first
        self.client.post('/add_seat', json={'seatId': 1})

        response = self.client.put('/update_seat_by_id/1', json={'seatId': 2})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Seat updated successfully', response.get_data(as_text=True))

        # Verify that the seat has been updated
        response = self.client.get('/get_seat_by_id/2')
        self.assertEqual(response.status_code, 200)
        self.assertIn('2', response.get_data(as_text=True))

    def test_delete_seat_by_id(self):
        # Add a seat first
        self.client.post('/add_seat', json={'seatId': 1})

        response = self.client.delete('/delete_seat_by_id/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Seat deleted successfully', response.get_data(as_text=True))

        # Verify that the seat has been deleted
        response = self.client.get('/get_seat_by_id/1')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Seat not found', response.get_data(as_text=True))

    def tearDown(self):
        # Clean up the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()
