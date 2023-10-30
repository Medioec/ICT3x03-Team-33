// models
const movieService = require('../models/movieServiceModel');

exports.getHomePage = [async (req, res) => {
    try {
        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;
        
        // get all movies from movie service
        const movies = await movieService.getAllMovies();
        
        return res.render('index.ejs', { movies, loggedIn });

    } catch (error) {
        // Handle errors
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
}];


exports.getMovieDetailsPage = [async (req, res) => {
    try {
        const movieId = req.query.movieId;
        const movie = await movieService.getMovieById(movieId);

        // Get all showtimes from the service
        const showtimes = await movieService.getAllShowtimes();
        const movieIdNumber = parseInt(movieId);

        // Filter and map the showtimes array to get an array of objects with movieId and showtimeId
        const filteredShowtimes = showtimes
            .filter((showtime) => showtime.movieId === movieIdNumber) 
            .map((showtime) => ({
                movieId: showtime.movieId,
                showtimeId: showtime.showtimeId
            }));

        const showtimeDetails = {};

        // Retrieve showtime details for each showtime in filteredShowtimes
        for (const showtime of filteredShowtimes) {
            const showtimeData = await movieService.getShowtimeById(showtime.showtimeId);
            showtimeDetails[showtimeData.cinemaName] = showtimeDetails[showtimeData.cinemaName] || [];
            showtimeDetails[showtimeData.cinemaName].push(showtimeData);
        }

        const loggedIn = req.loggedIn;
        res.render('pages/moviedetails.ejs', { movie, showtimeDetails, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getMovieDetailsPage:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
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

exports.getBookingForMoviePage = [async (req, res) => {
    try {
        const showtimeId = req.query.showtimeId;
        const showtimeDetails = await movieService.getShowtimeById(showtimeId);

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/booking.ejs', { showtimeDetails, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getBookingForMoviePage:", error);
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];
