const express = require('express');
const router = express.Router();

router.get('/', require('./homeController'));

router.get('/showtimes', (req, res) => {
    res.sendFile(__dirname + '/pages/showtimes.html');
});

router.get('/movieListings', (req, res) => {
    res.sendFile(__dirname + '/pages/movielistings.html');
});

// Add other routes as needed

module.exports = router;
