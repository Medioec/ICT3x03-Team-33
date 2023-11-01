const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');

// index page
router.get('/', checkLoggedIn, homeController.getHomePage);

// route to moviedetails for a specific movie
router.get('/moviedetails', checkLoggedIn, homeController.getMovieDetailsPage);

// all movies from navbar
router.get('/allmovies',checkLoggedIn, homeController.getAllMoviesPage);

// all showtimes from navbar
router.get('/allshowtimes',checkLoggedIn, homeController.getAllShowtimesPage);

// seat selection for selected movie
router.get('/booking',checkLoggedIn, homeController.getBookingForMoviePage);

// recommended cinemas
router.get('/cinemas',checkLoggedIn, homeController.getCinemasPage);

// Add other routes as needed
module.exports = router;
