import unittest
from your_flask_app import create_app, db  # Update the import statement according to your project structure

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_test_database_uri'  # Update this to your test database URI

class MovieDetailsQueriesTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.movie_data = {
            'title': 'Test Movie',
            'synopsis': 'This is a test movie.',
            'genre': 'Action',
            'contentRating': 'PG-13',
            'lang': 'English',
            'subtitles': 'English'
        }
        
        # Create a movie for test_get_movie_by_id, test_update_movie_by_id and test_delete_movie_by_id
        response = self.client.post('/create_movie', json=self.movie_data)
        self.movie_id = response.get_json()['movieId']

    def test_create_movie(self):
        response = self.client.post('/create_movie', json=self.movie_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Movie added successfully', response.get_data(as_text=True))

    def test_get_movie_by_id(self):
        response = self.client.get(f'/get_movie_by_id/{self.movie_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Movie', response.get_data(as_text=True))

    def test_get_all_movies(self):
        response = self.client.get('/get_all_movies')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Movie', response.get_data(as_text=True))

    def test_update_movie_by_id(self):
        updated_data = {
            'title': 'Updated Test Movie',
            'synopsis': 'This is an updated test movie.',
            'genre': 'Comedy',
            'contentRating': 'G',
            'lang': 'Spanish',
            'subtitles': 'Spanish'
        }
        response = self.client.put(f'/update_movie_by_id/{self.movie_id}', json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Movie updated successfully', response.get_data(as_text=True))
        
        # Check if the movie data was updated
        response = self.client.get(f'/get_movie_by_id/{self.movie_id}')
        self.assertEqual(response.status_code, 200)
        for key, value in updated_data.items():
            self.assertIn(value, response.get_data(as_text=True))

    def test_delete_movie_by_id(self):
        response = self.client.delete(f'/delete_movie_by_id/{self.movie_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Movie deleted successfully', response.get_data(as_text=True))
        
        # Check if the movie was deleted
        response = self.client.get(f'/get_movie_by_id/{self.movie_id}')
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        # Clean up the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()
