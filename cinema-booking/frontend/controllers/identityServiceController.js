// mvc refresher:
// controller handles data from model (which was sent via backend)
// takes requests from frontend -> sends data to model
// receives data from model -> sends data to frontend
// handles cookies (validating jwt token in cookies, setting cookies, clearing cookies)

// models
const identityService = require('../models/identityServiceModel');
const logger = require('../middleware/logger');

const captchaKey = process.env.CAPTCHA_KEY

exports.getLogin = (req, res) => {
    // Get the loggedIn status from the request object
    const loggedIn = req.loggedIn;

    // if logged in, don't try to login again
    if (loggedIn) {
        return res.redirect('/');
    }

    res.render('login.ejs', { loggedIn, captchaKey });
};

// if username and password valid -> verify OTP
exports.postLogin = async (req, res) => {
    try {
        const data = await identityService.loginRequest(req.body);

        if (data.status === 200) {
            // get partial token
            json_response = await data.json();
            const decodedToken = JSON.parse(atob(json_response.sessionToken.split('.')[1]));
            const expiryDelta = (decodedToken.exp - decodedToken.iat) * 1000;

            res.cookie('token', json_response.sessionToken, {
                path: '/',
                maxAge: expiryDelta,
                httpOnly: true
                // TODO: add more cookie options (samesite, secure, etc.)
            });

            logger('info', 'Verifying OTP for user ' + req.body.username + ' from ' + req.socket.remoteAddress);
            return res.status(data.status).json({'status': 'success', 'message': 'Verify OTP'});
        }   

        else if (data.status == 403) {
            logger('info', 'Member account not activated' + req.body.username + ' from ' + req.socket.remoteAddress);
            return res.status(data.status).json({'status': 'fail', 'message': 'Activate your account first!' });
        }

        else {
            logger('info', 'Invalid login for user ' + req.body.username + ' from ' + req.socket.remoteAddress);
            return res.status(401).json({'status': 'fail', 'message': 'Login failed. Invalid credentials.' });
        }
    } catch (error) {
        logger('info', 'Error while logging in user ' + req.body.username +  + ' from ' + req.ip + ': ' + error.message);
        return res.status(500).json({'status': 'fail', 'message': 'Internal Server Error' });
    }
};

exports.getOTP = (req, res) => {
    // Get the loggedIn status from the request object
    const loggedIn = req.loggedIn;

    // if logged in, don't try to login again
    if (loggedIn) {
        return res.redirect('/');
    }

    res.render('pages/otp.ejs');
};

exports.postOTP = async (req, res) => {
    try {
        // get partial token
        const token = req.cookies.token;

        if (token) {
            const data = await identityService.verifyOTP(token, req.body);
        
            if (data.status === 200) {
                res.clearCookie('token');

                json_response = await data.json();
                const decodedToken = JSON.parse(atob(json_response.sessionToken.split('.')[1]));
                const expiryDelta = (decodedToken.exp - decodedToken.iat) * 1000;

                // get user role
                const userRole = decodedToken.userRole;

                res.cookie('token', json_response.sessionToken, {
                    path: '/',
                    maxAge: expiryDelta,
                    httpOnly: true
                    // TODO: add more cookie options (samesite, secure, etc.)
                });

                // set loggedIn status
                req.loggedIn = true;
                logger('info', 'Successful login for user ' + req.body.username + ' from ' + req.socket.remoteAddress);
                return res.status(200).json({'status': 'success', 'message': 'Login successful', 'userRole': userRole});
                }   

            else {
                logger('info', 'Invalid OTP for user ' + req.body.username + ' from ' + req.socket.remoteAddress);
                return res.status(401).json({'status': 'fail', 'message': 'Invalid OTP' });
            }
        }

        else {
            logger('info', 'OTP expired for user' + req.body.username + ' from ' + req.socket.remoteAddress);
            return res.status(401).json({'status': 'fail', 'message': 'OTP expired' });
        }
        
    } catch (error) {
        logger('info', 'Error while logging in user ' + req.body.username +  + ' from ' + req.socket.remoteAddress + ': ' + error.message);
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

    res.render('register.ejs', { captchaKey });
};

exports.postRegister = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // if logged in, don't try to register
        if (loggedIn) {
            return res.status(401).json({ message: 'Unauthorized request' });
        }

        const data = await identityService.registerRequest(req.body);
        // Check if the data includes a status that indicates success
        if (data.status === 201 || data.status === 200) {
            return res.status(data.status).json({ message: 'Registration successful' });
        } else {
            // If data includes a message, send that, otherwise send a generic error message
            const jresponse = await data.json();
            const message = jresponse.message || "An error occurred during registration";
            return res.status(data.status).json({ 'message': message });
        }
        
    } catch (error) {
        // Send the error message from the catch block, if available
        const message = error.message || 'Internal Server Error';
        res.status(500).json({ 'message': message });
    }
};


exports.logout = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // if not logged in, don't try to logout
        if (!loggedIn) {
            res.clearCookie('token');
            return res.status(401).json({ message: 'Not logged in.'});
        }

        // if logged in, allow logout
        const token = req.cookies.token;
        const data = await identityService.logoutRequest(token);
        
        res.clearCookie('token');

        if (data.status === 200) {
            return res.status(200).json({'message': 'Logout successful'});
        }
        
    } catch (error) {
        return res.status(500).json({ 'message': 'Internal Server Error' });
    }
};

