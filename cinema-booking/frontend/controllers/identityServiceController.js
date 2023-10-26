const identityService = require('../models/identityServiceModel');

exports.getLogin = (req, res) => {
    // TODO: ADD IN LOGGED IN STATUS FOR NAVBAR
    res.render('login.ejs');
};

exports.postLogin = async (req, res) => {
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

            res.send({ message: 'Login successful!' });
        } else {
            res.send(data);
        }
    } catch (error) {
        console.error('Error in postLogin:', error);
        res.status(500).send('Internal Server Error');
    }
};

exports.getRegister = (req, res) => {
    // TODO: ADD IN LOGGED IN STATUS FOR NAVBAR
    res.render('register.ejs');
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
