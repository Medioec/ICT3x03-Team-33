// mvc refresher:
// controller handles data from model (which was sent via backend)
// takes requests from frontend -> sends data to model
// receives data from model -> sends data to frontend
// handles cookies (validating jwt token in cookies, setting cookies, clearing cookies)

// models
const identityService = require('../models/identityServiceModel');

// custom middleware
const checkLoggedIn = require('../middleware/checkLoggedIn');
const checkHeaders = require('../middleware/checkHeaders'); 

exports.getLogin = [checkLoggedIn, async (req, res) => {
    // Get the loggedIn status from the request object
    const loggedIn = req.loggedIn;

    // TODO: ADD IN LOGGED IN STATUS FOR NAVBAR
    res.render('login.ejs', { loggedIn });
}];

exports.postLogin = [checkHeaders, async (req, res) => {
    try {
        const data = await identityService.loginRequest(req.body);

        if (data.sessionToken) {
            const decodedToken = JSON.parse(atob(data.sessionToken.split('.')[1]));
            const expiryDelta = (decodedToken.exp - decodedToken.iat) * 1000;

            res.cookie('token', data.sessionToken, {
                path: '/',
                maxAge: expiryDelta,
                httpOnly: true
            });

            // Set loggedIn status
            req.loggedIn = true;

            // on login, redirect to home page
            res.redirect("/");

        } else {
            req.loggedIn = false;
            res.status(401).json({ message: 'Login failed. Invalid credentials.' });
        }
    } catch (error) {
        console.error('Error in postLogin:', error);
        res.status(500).send('Internal Server Error');
    }
}];

exports.getRegister = (req, res) => {
    const loggedIn = req.loggedIn;

    // TODO: ADD IN LOGGED IN STATUS FOR NAVBAR
    res.render('register.ejs', { loggedIn });

};

exports.postRegister = async (req, res) => {
    try {
        const data = await identityService.registerRequest(req.body);
        res.send(data);
    } catch (error) {
        console.error('Error in postRegister:', error);
        res.status(500).send('Internal Server Error');
    }
};

exports.logout = async (req, res) => {
    try {
        const token = req.cookies.token;
        const data = await identityService.logoutRequest(token);

        res.clearCookie('token');
        res.json({ message: data });
    } catch (error) {
        console.error('Error in logout:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
};
