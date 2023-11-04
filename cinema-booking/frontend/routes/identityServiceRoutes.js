// nodejs mvc refresher:
// routes defines mapping of url endpoints and their corresponding controller functions
// specifies http methods (GET, POST etc.)

const express = require('express');
const router = express.Router();
const identityServiceController = require('../controllers/identityServiceController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');

// login
router.get('/login', checkLoggedIn, identityServiceController.getLogin);
router.post('/loginRequest', checkLoggedIn, checkHeaders, identityServiceController.postLogin);
router.get('/otp', checkLoggedIn, identityServiceController.getOTP);
router.post('/otpRequest', checkLoggedIn, checkHeaders, identityServiceController.postOTP);

// register
router.get('/register', checkLoggedIn, identityServiceController.getRegister);
router.post('/registerRequest', checkLoggedIn, checkHeaders, identityServiceController.postRegister);

// logout
router.put('/logout', checkLoggedIn, checkHeaders, identityServiceController.logout);

module.exports = router;