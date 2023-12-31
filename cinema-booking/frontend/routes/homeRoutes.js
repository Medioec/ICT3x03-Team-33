const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');
const isOTPVerified = require('../middleware/isOTPVerified');

// index page
router.get('/', isOTPVerified, checkLoggedIn, homeController.getHomePage);

// route to moviedetails for a specific movie
router.get('/moviedetails', isOTPVerified, checkLoggedIn, homeController.getMovieDetailsPage);

// all movies page from navbar
router.get('/allmovies', isOTPVerified, checkLoggedIn, homeController.getAllMoviesPage);

// all showtimes page from navbar
router.get('/allshowtimes', isOTPVerified, checkLoggedIn, homeController.getAllShowtimesPage);

// seat selection for selected movie
router.get('/booking', isOTPVerified, checkLoggedIn, homeController.getBookingForMoviePage);

// get all movies
router.get('/getAllMovies', checkHeaders, homeController.getAllMovies);

// get all cinemas
router.get('/getAllCinemas', checkHeaders, homeController.getAllCinemas);

// get all showtimes
router.get('/getAllShowtimes', checkHeaders, homeController.getAllShowtimes);

// get showtime by id
router.get('/getShowtimeById', checkHeaders, homeController.getShowtimeById);

// get all booked seats
router.get('/getAllBookedSeats', checkHeaders, homeController.getAllBookedSeats);

// Add other routes as needed
module.exports = router;
