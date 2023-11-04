// nodejs mvc refresher:
// routes defines mapping of url endpoints and their corresponding controller functions
// specifies http methods (GET, POST etc.)

const express = require('express');
const router = express.Router();
const identityServiceController = require('../controllers/identityServiceController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');
const isOTPVerified = require('../middleware/isOTPVerified');

// login
router.get('/login', isOTPVerified, checkLoggedIn, identityServiceController.getLogin);
router.post('/loginRequest', isOTPVerified, checkLoggedIn, checkHeaders, identityServiceController.postLogin);
router.get('/otp', checkLoggedIn, identityServiceController.getOTP);
router.post('/otpRequest', checkLoggedIn, checkHeaders, identityServiceController.postOTP);

// register
router.get('/register', isOTPVerified, checkLoggedIn, identityServiceController.getRegister);
router.post('/registerRequest', isOTPVerified, checkLoggedIn, checkHeaders, identityServiceController.postRegister);

// logout
router.put('/logout', isOTPVerified, checkLoggedIn, checkHeaders, identityServiceController.logout);

module.exports = router;