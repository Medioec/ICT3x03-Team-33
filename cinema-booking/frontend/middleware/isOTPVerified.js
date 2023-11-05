// check if user is logged in
const isOTPVerified = (req, res, next) => {
    try {
        const token = req.cookies.token;
        console.log(token);
        if (token) {   
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
        else{
            next();
        }
    } catch (error) {
        console.log(error);
        res.status(500).send('Internal Server Error');
    }
};

module.exports = isOTPVerified;
