import pytest
from flask_testing import TestCase
from your_flask_app import create_app, db
from your_flask_app.cinemaTableQueries import cinema_bp

class TestCinemaTableQueries(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'your_test_database_uri'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_cinema(self):
        # Test adding a new cinema
        response = self.client.post('/add_cinema', json={
            'cinemaName': 'Test Cinema',
            'locationName': 'Test Location',
        })
        assert response.status_code == 201
        assert 'Cinema added successfully' in response.json['message']

    def test_get_cinema_by_id(self):
        # Add a test cinema to the database
        cinema = Cinema(cinemaName='Test Cinema', locationName='Test Location')
        db.session.add(cinema)
        db.session.commit()

        # Test getting the cinema by ID
        response = self.client.get(f'/get_cinema_by_id/{cinema.cinemaId}')
        assert response.status_code == 200
        assert response.json['cinemaName'] == 'Test Cinema'
        assert response.json['locationName'] == 'Test Location'
        assert response.json['cinemaId'] == cinema.cinemaId

        # Test getting a cinema that does not exist
        response = self.client.get('/get_cinema_by_id/0')
        assert response.status_code == 404
        assert 'Cinema not found' in response.json['message']


if __name__ == '__main__':
    pytest.main()
