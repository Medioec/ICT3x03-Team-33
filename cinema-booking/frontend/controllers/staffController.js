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
        return res.status(500).send('Internal Server Error');
    }    
};

exports.verifyStaffActivationLink = async (req, res) => {
    try { 
        const token = req.query.token;

        // verify if the link is valid
        const response = await identityService.verifyStaffActivationToken(token);

        if (response.status != 200){
            return res.status(403).send('Unauthorized Access');
        }
        
        res.redirect(`/setPassword?token=${token}`);

    } catch (error) {
        // Handle errors
        return res.status(500).send('Internal Server Error');
    }    
};

exports.getStaffPasswordPage = async (req, res) => {
    try {
        const token = req.query.token;

        // verify if the link is valid
        const response = await identityService.verifyStaffActivationToken(token);

        if (response.status != 200){
            return res.status(403).send('Unauthorized Access');
        }

        res.render('pages/staffactivateaccount.ejs')
        
    } catch (error) {
        // Handle errors
        return res.status(500).send('Internal Server Error');
    }    
};

exports.setStaffPasswordRequest = async (req, res) => {
    try {
        const token = req.query.token;
        console.log(token);
        console.log("set password");

        const response = await identityService.setStaffPasswordRequest(token, req.body);
        console.log(response); 
        if (response.status == 200) {
            return res.status(200).send('Success');
        }

        res.status(500).send('Internal Server Error'); 

    } catch (error) {
        // Handle errors
        res.status(500).send('Internal Server Error');
    }    
};