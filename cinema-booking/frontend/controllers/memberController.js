const movieService = require('../models/movieServiceModel');
const bookingService = require('../models/bookingServiceModel');
const paymentService = require('../models/paymentServiceModel');

exports.getMembersHomePage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // Get all movies and showtimes
        const movies = await movieService.getAllMovies();
        const showtimes = await movieService.getAllShowtimes();
        const cinemas = await movieService.getAllCinemas();

        return res.render('pages/membershome.ejs', { movies, cinemas, showtimes, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

exports.getCinemasPage  = [async (req, res) => {
    try {
        const cinemaId = req.query.cinemaId;
        
        // match showtimeId with cinemaId
        const showtimes = await movieService.getAllShowtimes();
        const cinemaData = await movieService.getAllCinemas();
        
        const filteredCinemaShowtimes = showtimes
        .filter((showtime) => showtime.cinemaId === cinemaId);

        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;

        // Render the 'moviedetails.ejs' page with the movie data
        res.render('pages/cinemas.ejs', {showtimes, cinemaData, filteredCinemaShowtimes, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getBookingForMoviePage:", error);
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];
