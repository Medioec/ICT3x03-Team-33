// check if user is logged in
const checkLoggedIn = async (req, res, next) => {
    try {
        // get cookie
        const token = req.cookies.token;

        // if token exists, query identity service to check if token is valid
        if (token) {
            const response = await fetch("http://identity:8081/basicAuth", { 
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            // get result of token validation
            if (response.status === 200) {
                // If the token is valid, set loggedIn in the request object
                req.loggedIn = true;
            } else {
                // If token is invalid, set loggedIn to false
                req.loggedIn = false;
            }
        } else {
            // if token is not present, set loggedIn to false
            req.loggedIn = false;
        }

        // Continue to the next middleware or route handler
        next();

    } catch (error) {
        // Handle any errors that might occur during the process
        console.error('Error:', error);
        res.status(500).send('Internal Server Error');
    }
};

module.exports = checkLoggedIn;