// models
const movieService = require('../models/movieServiceModel');

exports.getHomePage = [async (req, res) => {
    try {
        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;
        
        // get all movies from movie service
        const movies = await movieService.getAllMovies();
        
        // console.log("Rendering index.ejs");
        return res.render('index.ejs', { movies, loggedIn });

    } catch (error) {
        // Handle errors
        return res.status(500).json({ 'message': 'Internal Server Error' });
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
        return res.status(500).json({ 'message': 'Internal Server Error' });
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

exports.getAllShowtimesPage = [async (req, res) => {
    try {
        // get all movies from movie service
        const showtimes = await movieService.getAllShowtimes();

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/showtimes.ejs', { showtimes, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getAllShowtimesPage:", error);
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

exports.getAllShowtimesPage = [async (req, res) => {
    try {
        // get all movies from movie service
        const showtimes = await movieService.getAllShowtimes();

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/showtimes.ejs', { showtimes, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getAllShowtimesPage:", error);
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];

exports.getShowtimesDetailsPage = [async (req, res) => {
    try {
        // Get the movieId from the query parameters
        const showtimeId = req.query.showtimeId;

        // Fetch the movie details using the movieServiceModel function
        const showtimes = await movieService.getShowtimeById(showtimeId);

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/showtimedetails.ejs', { showtimes, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getShowtimesDetailsPage:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];