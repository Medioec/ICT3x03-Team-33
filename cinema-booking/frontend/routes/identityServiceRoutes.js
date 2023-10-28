// nodejs mvc refresher:
// routes defines mapping of url endpoints and their corresponding controller functions
// specifies http methods (GET, POST etc.)

const express = require('express');
const router = express.Router();
const identityServiceController = require('../controllers/identityServiceController');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');

// login
router.get('/login', identityServiceController.getLogin);
router.post('/loginRequest', checkHeaders, identityServiceController.postLogin);

// register
router.get('/register', checkLoggedIn, identityServiceController.getRegister);
router.post('/registerRequest', checkLoggedIn, checkHeaders, identityServiceController.postRegister);

// logout
router.put('/logout', checkLoggedIn, checkHeaders, identityServiceController.logout);

module.exports = router;