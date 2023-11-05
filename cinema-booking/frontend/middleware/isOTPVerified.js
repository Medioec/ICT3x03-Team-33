// check if user is logged in
const isOTPVerified = (req, res, next) => {
    try {
        const token = req.cookies.token;
    
        if (token) {    
            // get currStatus
            const decodedToken = JSON.parse(atob(json_response.sessionToken.split('.')[1]));
            const currStatus = decodedToken.currStatus;
            
            req.status = currStatus;

            if (currStatus === 'unverified') {
                res.redirect('/otp');
            }

            else {
                next();
            }
        } 

        else{
            next();
        }
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

module.exports = isOTPVerified;
