//Headers checks, preventing content type attack/request forgery
function checkHeaders(req, res, next) {
    if (req.headers['content-type'] !== 'application/json' || req.headers['accept'] !== 'application/json') {
        return res.status(400).send('Server expects application/json data');
    }
    next();
}

module.exports = checkHeaders;