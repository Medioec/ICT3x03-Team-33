from flask import request, jsonify, Blueprint
import os
import psycopg2

movie_details_bp = Blueprint("movie_details", __name__)

db_config = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
}

#####     Create a new movie entry in the database     #####
@movie_details_bp.route('/create_movie', methods=['POST'])
def create_movie():
    try:
        data = request.get_json()
        title = data['title']
        synopsis = data['synopsis']
        genre = data['genre']
        content_rating = data['contentRating']
        lang = data['lang']
        subtitles = data['subtitles']

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO MovieDetails (title, synopsis, genre, contentRating, lang, subtitles) VALUES (%s, %s, %s, %s, %s, %s) RETURNING movieId"
        cursor.execute(insert_query, (title, synopsis, genre, content_rating, lang, subtitles))
        new_movie_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Movie added successfully", "movieId": new_movie_id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of create movie entry     #####


#####     Retrieve a movie by its ID     #####
@movie_details_bp.route('/get_movie_by_id/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM MovieDetails WHERE movieId = %s"
        cursor.execute(select_query, (movie_id,))
        movie = cursor.fetchone()

        cursor.close()
        conn.close()

        if movie:
            movie_details = {
                "movieId": movie[0],
                "title": movie[1],
                "synopsis": movie[2],
                "genre": movie[3],
                "contentRating": movie[4],
                "lang": movie[5],
                "subtitles": movie[6]
            }
            return jsonify(movie_details), 200
        else:
            return jsonify({"message": "Movie not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve movie by ID     #####

#####     Retrieve all movies from the database     #####
@movie_details_bp.route('/get_all_movies', methods=['GET'])
def get_all_movies():
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        select_query = "SELECT * FROM MovieDetails"
        cursor.execute(select_query)
        movies = cursor.fetchall()

        cursor.close()
        conn.close()

        if movies:
            movie_list = []
            for movie in movies:
                movie_details = {
                    "movieId": movie[0],
                    "title": movie[1],
                    "synopsis": movie[2],
                    "genre": movie[3],
                    "contentRating": movie[4],
                    "lang": movie[5],
                    "subtitles": movie[6]
                }
                movie_list.append(movie_details)

            return jsonify(movie_list), 200
        else:
            return jsonify({"message": "No movies found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of retrieve all movies     #####

#####     Update a movie entry by its ID     #####
@movie_details_bp.route('/update_movie_by_id/<int:movie_id>', methods=['PUT'])
def update_movie_by_id(movie_id):
    try:
        data = request.get_json()
        title = data.get('title')
        synopsis = data.get('synopsis')
        genre = data.get('genre')
        content_rating = data.get('contentRating')
        lang = data.get('lang')
        subtitles = data.get('subtitles')
        
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if movie exists
        select_query = "SELECT * FROM MovieDetails WHERE movieId = %s"
        
        cursor.execute(select_query, (movie_id,))
        movie = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Update movie if it exists
        if movie:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()
            
            update_query = "UPDATE MovieDetails SET title = %s, synopsis = %s, genre = %s, contentRating = %s, lang = %s, subtitles = %s WHERE movieId = %s"
            cursor.execute(update_query, (title, synopsis, genre, content_rating, lang, subtitles, movie_id))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            return jsonify({"message": "Movie updated successfully"}), 200            
        else:
            # Movie does not exist
            return jsonify({"message": "Movie not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of update movie by ID     #####


#####     Delete a movie entry by its ID     #####
@movie_details_bp.route('/delete_movie_by_id/<int:movie_id>', methods=['DELETE'])
def delete_movie_by_id(movie_id):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        
        # Checks to see if movie exists
        select_query = "SELECT * FROM MovieDetails WHERE movieId = %s"
        
        cursor.execute(select_query, (movie_id,))
        movie = cursor.fetchone()

        cursor.close()
        conn.close()
        
        # Delete movie if it exists
        if movie:
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor()

            delete_query = "DELETE FROM MovieDetails WHERE movieId = %s"
            cursor.execute(delete_query, (movie_id,))
            conn.commit()

            cursor.close()
            conn.close()
            
            return jsonify({"message": "Movie deleted successfully"}), 200
        else:
            # Movie does not exist
            return jsonify({"message": "Movie not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#####     End of delete movie by ID     #####
