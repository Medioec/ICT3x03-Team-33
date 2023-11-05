// Required for https, set agent: httpsAgent in fetch
const httpsAgent = require('../middleware/httpsAgent');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

// check if user is logged in
const isOTPVerified = (req, res, next) => {
    try {
        const token = req.cookies.token;

        if (token) {   
            // get currStatus
            const decodedToken = JSON.parse(atob(json_response.sessionToken.split('.')[1]));
            const currStatus = decodedToken.currStatus;
            
            req.status = currStatus;

            if (currStatus == 'unverified') {
                fetch("https://identity/isOTPTokenValid", { 
                    method: "POST",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    agent: httpsAgent
                })
                .then(response => {      
                    // if otp token is valid          
                    if (response.status === 200) {
                        res.redirect('/otp');
                    } 
                    
                    // if otp token is invalid
                    else {
                        res.clearCookie('token');
                        next();
                    }
                })
            }

            else {
                next();
            }
        } 
        else{
            next();
        }
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
};

module.exports = isOTPVerified;
