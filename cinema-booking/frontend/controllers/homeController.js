// models
const movieService = require('../models/movieServiceModel');

exports.getHomePage = [async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // Get all movies and showtimes
        const movies = await movieService.getAllMovies();
        const showtimes = await movieService.getAllShowtimes();

        const cinemas = ['Golden Village Tampines', 'Shaw JCube', 'Cathay AMK Hub', 'GV Suntec City', 'The Projector'];

        return res.render('index.ejs', { movies, cinemas, showtimes, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
}];


exports.getMovieDetailsPage = [async (req, res) => {
    try {
        const movieId = req.query.movieId;
        // Get movie details from movie service with movie id
        const movieData = movieService.getMovieById(movieId);

        // Get all showtimes from the service
        const showtimesData = movieService.getAllShowtimes();
        const movieIdNumber = parseInt(movieId);

        // Get all cinemas from db
        const cinemaData = movieService.getAllCinemas();

        const [movie, showtimes, cinemas] = await Promise.all([movieData, showtimesData, cinemaData]);

        const filteredShowtimes = showtimes
            .filter((showtime) => showtime.movieId === movieIdNumber);

        // Create a mapping from cinemaId to cinemaName
        const cinemaMapping = {};
        cinemas.forEach(cinema => {
            cinemaMapping[cinema.cinemaId] = cinema.cinemaName;
        });

        // Form up the showtime details for front end to display
        const showtimeDetails = {};

        filteredShowtimes.forEach(showtime => {
            const cinemaName = cinemaMapping[showtime.cinemaId];

            if (!showtimeDetails[cinemaName]) {
                showtimeDetails[cinemaName] = [];
            }

            showtimeDetails[cinemaName].push({
                cinemaId: showtime.cinemaId,
                cinemaName: cinemaName,
                locationName: cinemas.find(cinema => cinema.cinemaId === showtime.cinemaId).locationName,
                showDate: showtime.showDate,
                showTime: showtime.showTime,
                showtimeId: showtime.showtimeId,
                theaterId: showtime.theaterId,
            });
        });

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

        // Render the 'showtimes.ejs' page with the movie data and cinemaMapping
        res.render('pages/showtimes.ejs', { showtimes, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getAllShowtimesPage:", error);
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