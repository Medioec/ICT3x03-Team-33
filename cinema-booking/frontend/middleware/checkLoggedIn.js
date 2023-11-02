// Required for https, set agent: httpsAgent in fetch
const httpsAgent = require('../middleware/httpsAgent');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

// check if user is logged in
const checkLoggedIn = (req, res, next) => {
    try {
        const token = req.cookies.token;

        if (token) {
            fetch("https://identity/basicAuth", { 
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                agent: httpsAgent
            })
            .then(response => {
                if (response.status === 200) {
                    req.loggedIn = true;
                } else {
                    req.loggedIn = false;
                }
                next();
            })
            .catch(error => {
                res.status(500).send('Internal Server Error');
            });
        } else {
            req.loggedIn = false;
            next();
        }
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

module.exports = checkLoggedIn;
