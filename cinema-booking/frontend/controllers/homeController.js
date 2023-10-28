// models
const movieService = require('../models/movieServiceModel');

// custom middleware
const checkLoggedIn = require('../middleware/checkLoggedIn');
const checkHeaders = require('../middleware/checkHeaders'); 

exports.getHomePage = [checkLoggedIn, async (req, res) => {
    try {
        // get all movies from movie service
        const movies = await movieService.getAllMovies();
        console.log(movies);
        
        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;
        
        res.render('index.ejs', { movies, loggedIn });

    } catch (error) {
        // Handle errors
        console.error("Error in getHomePage:", error);
        res.status(500).send('Internal Server Error: ' + error.message);

        // res.status(500).send('Internal Server Error');
    }
}];

exports.getMovieDetailsPage = [async (req, res) => {
    try {
        // Get the movieId from the query parameters
        const movieId = req.query.movieId;

        // Fetch the movie details using the movieServiceModel function
        const movie = await movieService.getMovieById(movieId);

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/moviedetails.ejs', { movie, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getMovieDetailsPage:", error);
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];

exports.getAllMoviesPage = [async (req, res) => {
    try {
        // get all movies from movie service
        const movies = await movieService.getAllMovies();

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/movielistings.ejs', { movies, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getAllMoviesPage:", error);
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];
