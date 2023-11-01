from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, get_jwt_identity)
import os
import requests
import user_utils

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

#####   throw error when JWT token is not valid     #####
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    print("unauthorized callback")
    return jsonify({"message": "Unauthorized access"}), 401
#####   End of throw error when JWT token is not valid     #####

#####     Create a new movie entry in the database     #####
@app.route('/createMovie', methods=["POST"])
@jwt_required()
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
        response = requests.post("https://databaseservice/databaseservice/moviedetails/create_movie", json=data, verify=False)
        
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
        response = requests.get("https://databaseservice/databaseservice/moviedetails/get_all_movies", verify=False)
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
        url = f"https://databaseservice/databaseservice/moviedetails/get_movie_by_id/{validateInt}"
        response = requests.get(url, verify=False)
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
@jwt_required()
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
        url = f"https://databaseservice/databaseservice/moviedetails/update_movie_by_id/{validateInt}"
        response = requests.put(url, verify=False)
        
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
@jwt_required()
def deleteMovieById(movie_id):
    try:
        #ensure movie_id is an integer, throws exception otherwise
        validateInt = int(movie_id)
        
        url = f"https://databaseservice/databaseservice/moviedetails/delete_movie_by_id/{validateInt}"
        response = requests.delete(url, verify=False)
        if response.status_code == 200:
            return jsonify({"message": "Movie deleted successfully"}), 200
        elif response.status_code == 404:
            return jsonify({"message": "Movie not found, not deleted"}), 404
        else:
            return jsonify({"message": "Delete movie with id: " + str(movie_id) + " failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of delete movie by ID     #####

#####     Create a new showtime entry in the database     #####
@app.route('/createShowtime', methods=["POST"])
@jwt_required()
def createShowtime():
    try:
        data = request.get_json()
        cinema_id = data['cinemaId']
        theater_id = data['theaterId']
        movie_id = data['movieId']
        show_date = data['showDate']
        show_time = data['showTime']

        #checks empty fields
        if not cinema_id or not theater_id or not movie_id or not show_date or not show_time:
            return jsonify({"message": "Please fill in all form data"}), 400
        # validates cinema_id and movie_id for integers
        if not user_utils.validateInteger(cinema_id) or not user_utils.validateInteger(movie_id):
            return jsonify({"message": "cinema_id or movie_id not correct format"}), 400
        # validates theater_id, 
        if not user_utils.validate_theaterId_format(theater_id):
            return jsonify({"message": "theaterID not correct fomat"}), 400
        # validates show_date
        if not user_utils.validate_showdate_format(show_date):
            return jsonify({"message": "showdate not in correct format (e.g 12-3-2023)"}), 400
        # validates show_time
        if not user_utils.validate_showtime_format(show_time):
            return jsonify({"message": "showtime not in correct format (e.g 12:30 AM/PM)"}), 400
        
        data = {
            "cinemaId": cinema_id,
            "theaterId": theater_id,
            "movieId": movie_id,
            "showDate": show_date,
            "showTime": show_time
        }

        response = requests.post("https://databaseservice/databaseservice/showtimes/create_showtime", json=data, verify=False)

        if response.status_code == 201:
            return jsonify({"message": "Adding showtime successful"}), 201
        else:
            return jsonify({"message": "Adding showtime failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of create showtime entry     #####

#####     Retrieve all showtimes from the database     #####
@app.route('/getAllShowtimes', methods=["GET"])
def getAllShowtimes():
    try:
        response = requests.get("https://databaseservice/databaseservice/showtimes/get_all_showtimes", verify=False)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"message": "Get all showtimes failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve all showtimes     #####

#####     Retrieve a showtime by its ID     #####
@app.route('/getShowtimeById/<int:showtime_id>', methods=["GET"])
def getShowtimeById(showtime_id):
    try:
        validate_int = int(showtime_id)
        showtime_url = f"https://databaseservice/databaseservice/showtimes/get_showtime_by_id/{validate_int}"
        response = requests.get(showtime_url, verify=False)
        if response.status_code == 200:
            showtime_id = response.json()['showtimeId']
            movie_id = response.json()['movieId']
            cinema_id = response.json()['cinemaId']
            theater_id = response.json()['theaterId']
            show_date = response.json()['showDate']
            show_time = response.json()['showTime']
            
            movie_url = f"https://databaseservice/databaseservice/moviedetails/get_movie_by_id/{movie_id}"
            movie_response = requests.get(movie_url, verify=False)
            
            if movie_response.status_code == 200:
                movie_title = movie_response.json()['title']
                movie_synopsis = movie_response.json()['synopsis']
                movie_genre = movie_response.json()['genre']
                movie_content_rating = movie_response.json()['contentRating']
                movie_lang = movie_response.json()['lang']
                movie_subtitles = movie_response.json()['subtitles']
                
                url = f"https://databaseservice/databaseservice/cinemas/get_cinema_by_id/{cinema_id}"
                cinema_response = requests.get(url, verify=False)
                
                if cinema_response.status_code == 200:
                    cinemaName = cinema_response.json()['cinemaName']
                    locationName = cinema_response.json()['locationName']
                    
                    theater_url = f"https://databaseservice/databaseservice/theaters/get_theater_by_number/{theater_id}"
                    theater_response = requests.get(theater_url, verify=False)
                    
                    if theater_response.status_code == 200:
                        theaterNumber = theater_response.json()['theaterNumber']
                        
                        showtime_details = {
                            "showtimeId": showtime_id,
                            "cinemaId": cinema_id,
                            "cinemaName": cinemaName,
                            "locationName": locationName,
                            "theaterId": theater_id,
                            "theaterNumber": theaterNumber,
                            "movieId": movie_id,
                            "movieTitle": movie_title,
                            "movieSynopsis": movie_synopsis,
                            "movieGenre": movie_genre,
                            "movieContentRating": movie_content_rating,
                            "movieLang": movie_lang,
                            "movieSubtitles": movie_subtitles,
                            "showDate": show_date,
                            "showTime": show_time
                        }
                        return jsonify(showtime_details), 200
                    elif theater_response.status_code == 404:
                        return jsonify({"message": "Showtime retrieving theater details error"}), 404
                    else:
                        return jsonify({"message": f"Get showtime with id: {showtime_id} failed with uncaught exception at theater"}), 500
                elif cinema_response.status_code == 404:
                    return jsonify({"message": "Showtime retrieving cinema details error"}), 404
                else:
                    return jsonify({"message": f"Get showtime with id: {showtime_id} failed with uncaught exception at cinema"}), 500     
            elif movie_response.status_code == 404:
                return jsonify({"message": "Showtime retrieving movie details error"}), 404
            else:
                return jsonify({"message": f"Get showtime with id: {showtime_id} failed with uncaught exception at movie"}), 500
        elif response.status_code == 404:
            return jsonify({"message": "Showtime not found"}), 404
        else:
            return jsonify({"message": f"Get showtime with id: {showtime_id} failed with uncaught exception at showtime"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of retrieve showtime by ID     #####

#####     Update a showtime entry by its ID     #####
@app.route('/updateShowtimeById/<int:showtime_id>', methods=['PUT'])
@jwt_required()
def updateShowtimeById(showtime_id):
    try:
        validate_int = int(showtime_id)
        data = request.get_json()
        cinema_id = data['cinemaId']
        theater_id = data['theaterId']
        movie_id = data['movieId']
        show_date = data['showDate']
        show_time = data['showTime']

        #checks empty fields
        if not cinema_id or not theater_id or not movie_id or not show_date or not show_time:
            return jsonify({"message": "Please fill in all form data"}), 400
        # validates cinema_id and movie_id for integers
        if not user_utils.validateInteger(cinema_id) or not user_utils.validateInteger(movie_id):
            return jsonify({"message": "cinema_id or movie_id not correct format"}), 400
        # validates theater_id, 
        if not user_utils.validate_theaterId_format(theater_id):
            return jsonify({"message": "theaterID not correct fomat"}), 400
        # validates show_date
        if not user_utils.validate_showdate_format(show_date):
            return jsonify({"message": "showdate not in correct format (e.g 12-3-2023)"}), 400
        # validates show_time
        if not user_utils.validate_showtime_format(show_time):
            return jsonify({"message": "showtime not in correct format (e.g 12:30 AM/PM)"}), 400
        
        url = f"https://databaseservice/databaseservice/showtimes/update_showtime_by_id/{validate_int}"
        response = requests.put(url, json=data, verify=False)

        if response.status_code == 200:
            return jsonify({"message": "Update showtime successful"}), 200
        elif response.status_code == 404:
            return jsonify({"message": "Showtime not found, not updated"}), 404
        else:
            return jsonify({"message": "Updating showtime failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of update showtime by ID     #####

#####     Delete a showtime entry in the database     #####
@app.route('/deleteShowtimeById/<int:showtime_id>', methods=["DELETE"])
@jwt_required()
def deleteShowtimeById(showtime_id):
    try:
        validate_int = int(showtime_id)
        url = f"https://databaseservice/databaseservice/showtimes/delete_showtime_by_id/{validate_int}"
        response = requests.delete(url, verify=False)
        if response.status_code == 200:
            return jsonify({"message": "Showtime deleted successfully"}), 200
        elif response.status_code == 404:
            return jsonify({"message": "Showtime not found, not deleted"}), 404
        else:
            return jsonify({"message": f"Delete showtime with id: {showtime_id} failed"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
#####     End of delete showtime by ID     #####

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8082)
