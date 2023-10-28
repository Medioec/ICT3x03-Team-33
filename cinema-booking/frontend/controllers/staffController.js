// models
const movieService = require('../models/movieServiceModel');

exports.getStaffDashboard = async (req, res) => {
    try {
        const movies = await movieService.getAllMovies();
        console.log(movies);
        
        // Get the loggedIn status from the request object
        const loggedIn = req.loggedIn;
        
        res.render('pages/staffdash.ejs', { movies, loggedIn });

    } catch (error) {
        // Handle errors
        res.status(500).send('Internal Server Error');
    }    
};