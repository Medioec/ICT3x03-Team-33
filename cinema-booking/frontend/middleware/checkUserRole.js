// function to check if the user is logged in and has the required role to access the page
function checkUserRole(requiredRole) {
    return (req, res, next) => {
        try {
            // get cookie
            const token = req.cookies.token;

            // if user is not logged in, redirect to login page
            if (!token) {
                res.redirect('/login');
                return res.status(401).send('Unauthorized');
            }

            // get user role from cookie
            const decodedToken = JSON.parse(atob(token.split('.')[1]));
            const userRole = decodedToken.userRole;

            // if user doesn't have permission, send forbidden error
            if (userRole !== requiredRole) {
                return res.status(403).send('Access Forbidden');
            }

            // verify their role using identity service
            const response = fetch("http://identity:8081/enhancedAuth", {
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(response => {
                console.log(response);

                // if validation fails, user doesn't have permissions
                if (response.status !== 200) {
                    req.loggedIn = false;
                    return res.status(403).send('Access Forbidden');
                }

                // if validation passes, call next middleware
                req.loggedIn = true;
                next();
            })
            
        } catch (error) {
            console.error('Error in checkUserRole middleware:', error);
            res.status(500).send('Internal Server Error');
        }
    };
}

module.exports = checkUserRole;