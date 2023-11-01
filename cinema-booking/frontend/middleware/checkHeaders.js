//Headers checks, preventing content type attack/request forgery
function checkHeaders(req, res, next) {
    if (req.headers['content-type'] !== 'application/json' || req.headers['accept'] !== 'application/json') {
        return res.status(400).send('Server expects application/json data');
    }

    // Check for CSRF token in headers
    if (!req.headers['X-CSRFTokeen']) {
        return res.status(403).send('CSRF token is missing');
    }

    next();
}

module.exports = checkHeaders;