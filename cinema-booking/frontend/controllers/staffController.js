// models
const movieService = require('../models/movieServiceModel');
const identityService = require('../models/identityServiceModel');

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

exports.verifyStaffActivationLink = async (req, res) => {
    console.log("in verify activation link req");
    try { 
        const token = req.query.token;
        console.log("can get token", token);

        // verify if the link is valid
        const response = await identityService.verifyStaffActivationToken(token);
        console.log(response);
        console.log(response.status);

        if (response.status != 200){
            res.status(403).send('Unauthorized Access');
        }
        
        res.redirect(`/setPassword/${token}`);
        // res.status(200).send('Valid link');

    } catch (error) {
        // Handle errors
        res.status(500).send('Internal Server Error');
    }    
};

exports.getStaffPasswordPage = async (req, res) => {
    try {
        res.render('pages/staffactivation.ejs')
    } catch (error) {
        // Handle errors
        res.status(500).send('Internal Server Error');
    }    
};

exports.setStaffPassword = async (req, res) => {
    try {
        const response = await identityService.setStaffPassword(req.params.token);
        console.log(response);
        res.status(200).send("test");

    } catch (error) {
        // Handle errors
        res.status(500).send('Internal Server Error');
    }    
};