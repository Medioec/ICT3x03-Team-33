// models
const movieService = require('../models/movieServiceModel');

// custom middleware
const checkLoggedIn = require('../middleware/checkLoggedIn');
const checkHeaders = require('../middleware/checkHeaders'); 

exports.getHomePage = [checkLoggedIn, async (req, res) => {
    try {
        // get all movies from movie service
        const movies = await movieService.getAllMovies();
        console.log(movies);
        
        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;
        
        res.render('index.ejs', { movies, loggedIn });

    } catch (error) {
        // Handle errors
        console.error("Error in getHomePage:", error);
        res.status(500).send('Internal Server Error: ' + error.message);

        // res.status(500).send('Internal Server Error');
    }
}];