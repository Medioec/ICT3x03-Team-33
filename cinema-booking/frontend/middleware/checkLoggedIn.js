const https = require('https');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const httpsAgent = new https.Agent({
      rejectUnauthorized: false,
    });


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
