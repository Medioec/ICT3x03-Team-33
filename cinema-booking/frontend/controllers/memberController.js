const movieService = require('../models/movieServiceModel');
const bookingService = require('../models/bookingServiceModel');
const paymentService = require('../models/paymentServiceModel');

exports.getMembersHomePage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // Get all movies and showtimes
        const movies = await movieService.getAllMovies();
        const showtimes = await movieService.getAllShowtimes();

        const cinemas = ['Golden Village Tampines', 'Shaw JCube', 'Cathay AMK Hub', 'GV Suntec City', 'The Projector'];

        return res.render('pages/membershome.ejs', { movies, cinemas, showtimes, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

exports.getCinemasPage  = [async (req, res) => {
    try {
        // const cinemaId = req.query.cinemaId;
        
        // // match showtimeId with cinemaId
        // const showtimes = await movieService.getAllShowtimes();
        
        // // use showtimeId obtained to getShowtimeById
        // const showtimeDetails = await movieService.getShowtimeById(showtimeId);

        // // Get the loggedIn status from the request object
        // const loggedIn = req.loggedIn;

        // // Render the 'moviedetails.ejs' page with the movie data
        // res.render('pages/cinemas.ejs', { showtimeDetails, loggedIn });
    } catch (error) {
        // Handle errors
        console.error("Error in getBookingForMoviePage:", error);
        // res.status(500).send('Internal Server Error: ' + error.message);
    }
}];
