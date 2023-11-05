// check if user is logged in
const isOTPVerified = (req, res, next) => {
    try {
        const token = req.cookies.token;
        
        if (token) {
            // get currStatus
            const decodedToken = JSON.parse(atob(json_response.sessionToken.split('.')[1]));
            const currStatus = decodedToken.currStatus;
            
            req.status = currStatus;

            // verify against db
            if (currStatus == 'unverified') {
                fetch("http://identity:8081/isOTPTokenValid", { 
                    method: "POST",
                    headers: {
                        "Accept": "application/json",
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    }
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
        else {
            next();
        }
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

module.exports = isOTPVerified;
