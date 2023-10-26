from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import user_utils

app = Flask(__name__)
CORS(app)

#####     Create a new movie entry in the database     #####
@app.route('/createMovie', methods=["POST"])
def createMovie():
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
        response = requests.post("http://databaseservice:8085/databaseservice/moviedetails/create_movie", json=data)
        
        if response.status_code == 201:
            return jsonify({"message": "Adding movie successful", }), 201
        else:
            return jsonify({"message": "Adding movie " + str(title) +  " failed", }), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of create movie entry     #####

#####     Retrieve all movies from the database     #####
@app.route('/getAllMovies', methods=["GET"])
def getAllMovies():
    try:
        response = requests.get("http://databaseservice:8085/databaseservice/moviedetails/get_all_movies")
        if response.status_code == 200:
            print(jsonify(response.json()))

            return jsonify(response.json()), 200
        else:
            return jsonify({"message": "Get all movies failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all movies     #####

#####     Retrieve a movie by its ID     #####
@app.route('/getMovieById/<int:movie_id>', methods=["GET"])
def getMovieById(movie_id):
    try:
        #ensure movie_id is an integer
        validateInt = int(movie_id)
        url = f"http://databaseservice:8085/databaseservice/moviedetails/get_movie_by_id/{validateInt}"
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        elif response.status_code == 404:
            return jsonify({"message": "Movie not found"}), 404
        else:
            return jsonify({"message": "Get movie with id: " + str(movie_id) + " failed with uncaught exception"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve movie by ID     #####

#####     Update a movie entry by its ID     #####
@app.route('/updateMovieById/<int:movie_id>', methods=['PUT'])
def updateMovieById(movie_id):
    try:
        #ensure movie_id is an integer, throws exception otherwise
        validateInt = int(movie_id)
  
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
        # validates content rating
        if not user_utils.validateRating(content_rating):
            return jsonify({"message": "Content rating is invalid"}), 400
        # validates title and synopsis
        if not user_utils.validateAlphaWithSpace(title) or not user_utils.validateAlphaWithSpace(synopsis):
            return jsonify({"message": "Title and synopsis should only contain alphabets and spaces"}), 400
        # validates genre, language and subtitles
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
        url = f"http://databaseservice:8085/databaseservice/moviedetails/update_movie_by_id/{validateInt}"
        response = requests.put(url)
        
        if response.status_code == 200:
            return jsonify({"message": "Update movie successful" }), 200
        elif response.status_code == 404:
            return jsonify({"message": "Movie not found, not updated"}), 404
        else:
            return jsonify({"message": "Updating movie: " + str(title) +  " failed", }), 500        
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
#####     End of update movie by ID     #####   

#####     Delete a movie entry in the database     #####
@app.route('/deleteMovieById/<int:movie_id>', methods=["DELETE"])
def deleteMovieById(movie_id):
    try:
        #ensure movie_id is an integer, throws exception otherwise
        validateInt = int(movie_id)
        
        url = f"http://databaseservice:8085/databaseservice/moviedetails/delete_movie_by_id/{validateInt}"
        response = requests.delete(url)
        if response.status_code == 200:
            return jsonify({"message": "Movie deleted successfully"}), 200
        elif response.status_code == 404:
            return jsonify({"message": "Movie not found, not deleted"}), 404
        else:
            return jsonify({"message": "Delete movie with id: " + str(movie_id) + " failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of delete movie by ID     #####

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8082)
