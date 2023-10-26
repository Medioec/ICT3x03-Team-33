const express = require('express');
const router = express.Router();
const homeController = require('../controllers/homeController');
const checkHeaders = require('../middleware/checkHeaders');

router.get('/', homeController.getHomePage);

// Add other routes as needed

module.exports = router;
