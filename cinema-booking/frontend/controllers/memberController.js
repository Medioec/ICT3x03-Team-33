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