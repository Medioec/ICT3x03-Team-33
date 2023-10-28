const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');

router.get('/', checkLoggedIn, homeController.getHomePage);

// route to moviedetails for a specific movie
router.get('/moviedetails', checkLoggedIn, homeController.getMovieDetailsPage);

// Add other routes as needed

module.exports = router;
