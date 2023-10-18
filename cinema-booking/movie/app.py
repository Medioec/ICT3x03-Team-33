from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import user_utils

app = Flask(__name__)
CORS(app)

#####     Create a new movie entry in the database     #####
@app.route('/create_movie', methods=["POST"])
def create_movie():
    try:
        data = request.get_json()
        title = data['title']
        synopsis = data['synopsis']
        genre = data['genre']
        content_rating = data['contentRating']
        lang = data['lang']
        subtitles = data['subtitles']
        
        #checks empty fields
        if not title or not synopsis or not genre or not content_rating or not lang or not subtitles:
            return jsonify({"message": "Please fill in all form data"}), 400
        
        if not user_utils.validateRating(content_rating):
            return jsonify({"message": "Content rating is invalid"}), 400
        
        if not user_utils.validateAlphaWithSpace(title) or not user_utils.validateAlphaWithSpace(synopsis):
            return jsonify({"message": "Title and synopsis should only contain alphabets and spaces"}), 400
        
        if not user_utils.validateAlphaWithSpace(genre) or not user_utils.validateAlphaWithSpace(lang) or not user_utils.validateAlphaWithSpace(subtitles):
            return jsonify({"message": "Genre, language and subtitles should only contain alphabets and spaces"}), 400
        
        data = {
            "title": title,
            "synopsis": synopsis,
            "genre": genre,
            "contentRating": content_rating,
            "lang": lang,
            "subtitles": subtitles
        }
        response = requests.post("http://databaseservice:8085/databaseservice/movieDetails/create_movie", json=data)
        
        if response.status_code == 201:
            return jsonify({"message": "Adding movie successful", }), 201
        else:
            return jsonify({"message": "Adding movie " + str(title) +  " failed", }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of create movie entry     #####

#####     Retrieve all movies from the database     #####
@app.route('/get_all_movies', methods=["GET"])
def get_all_movies():
    try:
        response = requests.get("http://databaseservice:8085/databaseservice/movieDetails/get_all_movies")
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"message": "Get all movies failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all movies     #####

#####     Retrieve a movie by its ID     #####
@app.route('/get_movie_by_id/<int:movie_id>', methods=["GET"])
def get_movie_by_id(movie_id):
    try:
        validateInt = int(movie_id)
        response = requests.get("http://databaseservice:8085/databaseservice/movieDetails/get_movie_by_id/"+ validateInt)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"message": "Get movie with id: " + str(movie_id) + " failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve movie by ID     #####

#####     Update a movie entry by its ID     #####
@app.route('/update_movie_by_id/<int:movie_id>', methods=['PUT'])
def update_movie_by_id(movie_id):
    try:
        validateInt = int(movie_id)
  
        data = request.get_json()
        title = data.get('title')
        synopsis = data.get('synopsis')
        genre = data.get('genre')
        content_rating = data.get('contentRating')
        lang = data.get('lang')
        subtitles = data.get('subtitles')
        
         #checks empty fields
        if not title or not synopsis or not genre or not content_rating or not lang or not subtitles:
            return jsonify({"message": "Please fill in all form data"}), 400
        # validates content rating
        if not user_utils.validateRating(content_rating):
            return jsonify({"message": "Content rating is invalid"}), 400
        # validates title and synopsis
        if not user_utils.validateAlphaWithSpace(title) or not user_utils.validateAlphaWithSpace(synopsis):
            return jsonify({"message": "Title and synopsis should only contain alphabets and spaces"}), 400
        # validates genre, language and subtitles
        if not user_utils.validateAlphaWithSpace(genre) or not user_utils.validateAlphaWithSpace(lang) or not user_utils.validateAlphaWithSpace(subtitles):
            return jsonify({"message": "Genre, language and subtitles should only contain alphabets and spaces"}), 400
        
        response = requests.get("http://databaseservice:8085/databaseservice/movieDetails/update_movie_by_id/"+ validateInt)
        
        if response.status_code == 201:
            return jsonify({"message": "Update movie successful" }), 201
        else:
            return jsonify({"message": "Updating movie: " + str(title) +  " failed", }), 50        
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
#####     End of update movie by ID     #####   
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8082)
    
