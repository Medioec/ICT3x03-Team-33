// mvc refresher:
// controller handles data from model (which was sent via backend)
// takes requests from frontend -> sends data to model
// receives data from model -> sends data to frontend
// handles cookies (validating jwt token in cookies, setting cookies, clearing cookies)

// models
const identityService = require('../models/identityServiceModel');

exports.getLogin = (req, res) => {
    // Get the loggedIn status from the request object
    const loggedIn = req.loggedIn;

    // if logged in, don't try to login again
    if (loggedIn) {
        return res.redirect('/');
    }

    res.render('login.ejs', { loggedIn });
};

exports.postLogin = async (req, res) => {
    try {
        const data = await identityService.loginRequest(req.body);

        if (data.sessionToken) {
            const decodedToken = JSON.parse(atob(data.sessionToken.split('.')[1]));
            const expiryDelta = (decodedToken.exp - decodedToken.iat) * 1000;

            // get user role
            const userRole = decodedToken.userRole;

            console.log("controller: ", userRole);

            res.cookie('token', data.sessionToken, {
                path: '/',
                maxAge: expiryDelta,
                httpOnly: true
                // TODO: add more cookie options (samesite, secure, etc.)
            });

            // set loggedIn status
            req.loggedIn = true;
            return res.status(200).json({'status': 'success', 'message': 'Login successful', 'userRole': userRole});

        } else {
            req.loggedIn = false;
            return res.status(401).json({'status': 'fail', 'message': 'Login failed. Invalid credentials.' });
        }
    } catch (error) {
        return res.status(500).json({'status': 'fail', 'message': 'Internal Server Error' });
    }
};

exports.getRegister = (req, res) => {
    // Get the loggedIn status from the request object
    const loggedIn = req.loggedIn;

    // if logged in, don't allow register again
    if (loggedIn) {
        return res.redirect('/');
    }

    res.render('register.ejs');
};

exports.postRegister = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // if logged in, don't try to register
        if (loggedIn) {
            return res.status(401).json({ message: 'Unauthorized request'});
        }

        const data = await identityService.registerRequest(req.body);
        return res.status(data.status).json({'message': 'Registration successful'});
        
    } catch (error) {
        res.status(500).json({ 'message': 'Internal Server Error' });
    }
};

exports.logout = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // if not logged in, don't try to logout
        if (!loggedIn) {
            res.clearCookie('token');
            return res.status(401).json({ message: 'Not logged in.' });
        }

        // if logged in, allow logout
        const token = req.cookies.token;
        const data = await identityService.logoutRequest(token);
        
        res.clearCookie('token');

        if (data.status === 200) {
            return res.status(200).json({'message': 'Logout successful'});
        }
        
    } catch (error) {
        res.status(500).json({ 'message': 'Internal Server Error' });
    }
};

