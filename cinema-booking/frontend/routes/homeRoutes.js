const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');

router.get('/', checkLoggedIn, homeController.getHomePage);

// route to moviedetails for a specific movie
router.get('/moviedetails', checkLoggedIn, homeController.getMovieDetailsPage);

// all movies from navbar
router.get('/allmovies',checkLoggedIn, homeController.getAllMoviesPage);

// all showtimes from navbar
router.get('/allshowtimes',checkLoggedIn, homeController.getAllShowtimesPage);




router.get('/showtimedetails',checkLoggedIn, homeController.getShowtimesDetailsPage);


// Add other routes as needed

module.exports = router;
