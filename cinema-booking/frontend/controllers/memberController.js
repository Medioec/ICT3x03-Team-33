const movieService = require('../models/movieServiceModel');
const bookingService = require('../models/bookingServiceModel');
const paymentService = require('../models/paymentServiceModel');

exports.getMembersHomePage = async (req, res) => {
    try {
        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        const movies = await movieService.getAllMovies();
        const showtimes = await movieService.getAllShowtimes();
        const movieId = req.query.movieId;
        const movieDetails = await movieService.getMovieById(movieId);
        //const showtimeDetails = await movieService.getShowtimeById();

        console.log(movies);
        
        res.render('pages/membershome.ejs', { movies, movieDetails, showtimes, loggedIn });

        //res.render('pages/membershome.ejs', { movies, showtimes, showtimeDetails, loggedIn });

    } catch (error) {
        // Handle errors
        res.status(500).send('Internal Server Error');
    }    
};