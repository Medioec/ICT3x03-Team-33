// models
const movieService = require('../models/movieServiceModel');
const bookingService = require('../models/bookingServiceModel');

exports.getHomePage = [async (req, res) => {
    var movies;
    var showtimes;
    var cinemas;
    const loggedIn = req.loggedIn;
    try {
        // Get all movies and showtimes
        movies = await movieService.getAllMovies();
        showtimes = await movieService.getAllShowtimes();
        cinemas = await movieService.getAllCinemas();
    } catch (error) {
        console.log("Internal Server Error");
        movies = null;
        showtimes = null;
        cinemas = null;
    }
    return res.render('index.ejs', { movies, cinemas, showtimes, loggedIn });
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
        const movies = await movieService.getAllMovies();
        const cinemas = await movieService.getAllCinemas();

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'showtimes.ejs' page with the movie data and cinemaMapping
        res.render('pages/showtimes.ejs', { movies, cinemas, showtimes, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getAllShowtimesPage:", error);
    }
}];

exports.getBookingForMoviePage = [async (req, res) => {
    try {
        const showtimeId = req.query.showtimeId;
        const showtimeDetails = await movieService.getShowtimeById(showtimeId);
        let bookedSeats = await bookingService.retrieveAllBookedSeats(showtimeId);

        // if bookedSeats is empty or not defined return an empty array
        if (!bookedSeats || bookedSeats.length === 0) {
            bookedSeats = [];
        }

        const loggedIn = req.loggedIn;

        res.render('pages/booking.ejs', { bookedSeats, showtimeDetails, loggedIn });
    } catch (error) {
        console.error("Error in getBookingForMoviePage:", error);
    }
}];

exports.getAllMovies = [async (req, res) => {
    try {
        const movies = await movieService.getAllMovies();
        return res.status(200).json(movies);
    } catch (error) {
        console.error("Error in getAllMovies:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
}];


exports.getAllCinemas = [async (req, res) => {  
    try {
        const cinemas = await movieService.getAllCinemas();
        return res.status(200).json(cinemas);
    } catch (error) {
        console.error("Error in getAllCinemas:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
}];

exports.getAllShowtimes = [async (req, res) => {  
    try {
        const showtimeData = await movieService.getAllShowtimes();
        return res.status(200).json(showtimeData);
    } catch (error) {
        console.error("Error in getAllShowtimes:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
}];

exports.getShowtimeById = [async (req, res) => {  
    try {
        const showtimeId = req.query.showtimeId;
        const showtimeData = await movieService.getAllShowtimes(showtimeId);
        return res.status(200).json(showtimeData);
    } catch (error) {
        console.error("Error in getAllShowtimes:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
}];

exports.getAllBookedSeats = [async (req, res) => {
    try {
        const showtimeId = req.query.showtimeId;
        const bookedSeats = await bookingService.retrieveAllBookedSeats(showtimeId);
        return res.status(200).json(bookedSeats);
    } catch (error) {
        console.error("Error in getAllBookedSeats:", error);
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
}];