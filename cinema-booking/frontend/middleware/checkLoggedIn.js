// check if user is logged in
const checkLoggedIn = (req, res, next) => {
    try {
        const token = req.cookies.token;

        if (token) {
            fetch("http://identity:8081/basicAuth", { 
                method: "POST",
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            })
            .then(response => {
                if (response.status === 200) {
                    req.loggedIn = true;
                } else {
                    req.loggedIn = false;
                }
                console.log("checkLoggedIn: " + req.loggedIn);
                next();
            })
            .catch(error => {
                console.error(error);
                res.status(500).send('Internal Server Error');
            });
        } else {
            req.loggedIn = false;
            next();
        }
    } catch (error) {
        console.error(error);
        res.status(500).send('Internal Server Error');
    }
};

module.exports = checkLoggedIn;
