const express = require('express');
const router = express.Router();
const identityServiceController = require('../controllers/identityServiceController');
const checkHeaders = require('../middleware/checkHeaders');

router.get('/login', identityServiceController.getLogin);
router.post('/loginRequest', checkHeaders, identityServiceController.postLogin);
router.get('/register', identityServiceController.getRegister);
router.post('/registerRequest', checkHeaders, identityServiceController.postRegister);
router.delete('/logout', identityServiceController.logout);

module.exports = router;