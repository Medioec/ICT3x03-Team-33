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

// all movies from navbar
router.get('/allmovies', isOTPVerified, checkLoggedIn, homeController.getAllMoviesPage);

// all showtimes from navbar
router.get('/allshowtimes', isOTPVerified, checkLoggedIn, homeController.getAllShowtimesPage);

// seat selection for selected movie
router.get('/booking', isOTPVerified, checkLoggedIn, homeController.getBookingForMoviePage);

// Add other routes as needed
module.exports = router;
