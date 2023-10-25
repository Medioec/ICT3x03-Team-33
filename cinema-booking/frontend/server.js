const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors')
const cookieParser = require('cookie-parser');

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(cookieParser());
app.use(bodyParser.json());
app.use(express.static(__dirname)); // Serve static files from the root directory

app.set('view engine', 'ejs');
app.set('views', __dirname); // Assuming your EJS files are in a folder named 'views'

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html'); // Serve the index.html from the root directory
});

//Headers checks, preventing content type attack/request forgery
function checkHeaders(req, res, next) {
    if (req.headers['content-type'] !== 'application/json' || req.headers['accept'] !== 'application/json') {
        return res.status(400).send('Server expects application/json data');
    }
    next();
}

// ############################## TESTING AUTH PAGE REDIRECTION #########################################

// testing basicAuth (check if jwt token is valid)
// used for basic pages that users can access without logging in (e.g. homepage, movie listings)
// only diff is the rendering of the navbar
app.get('/test', async (req, res) => {
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

            console.log('Response:', response);

            // get result of token validation
            if (response.status === 200) {
                // If the token is valid, user is logged in
                loggedIn = true;
                res.render('test.ejs', { loggedIn });
            } 
          
            // if token invalid, redirect to login page
            else {
                res.redirect('/login');
            }
        }
        
        // if token is not present, user is not logged in
        else {
            loggedIn = false;
            res.render('test.ejs', { loggedIn });
        }

        res.sendFile(__dirname + '/pages/movielistings.html');

    } catch (error) {
        // Handle any errors that might occur during the process
        console.error('Error:', error);
        res.status(500).send('Internal Server Error');
    }
});

app.get('/moviedetails', (req, res) => {
    res.sendFile(__dirname + '/pages/moviedetails.html');
});

// ############################## END OF TESTING AUTH PAGE REDIRECTION #########################################

// ############################## IDENTITY SERVICE #########################################
// handle GET request from login.html
app.get('/login', (req, res) => {
    res.sendFile(__dirname + '/login.html');
});

// handle POST request from login.html with header checks
app.post('/loginRequest', checkHeaders, async (req, res) => {
    // send POST request from login form to identity service
    const response = await fetch("http://identity:8081/login", { 
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(req.body),
    });

    // parse the JSON data received from identity service
    const data = await response.json();
    
    // if jwt token exists, set cookie with the token and expiry
    if (data.sessionToken) {
        const decodedToken = JSON.parse(atob(data.sessionToken.split('.')[1])); // decode jwt payload

        // calculate expiration delta in milliseconds
        const expiryDelta = (decodedToken.exp - decodedToken.iat) * 1000; 

        // Assuming "token" and "expiry" are the fields in your JSON response
        res.cookie('token', data.sessionToken, { 
            path: '/', // set the cookie path to root, so that it is accessible for all routes
            maxAge: expiryDelta, // set the cookie expiry time
            httpOnly: true, // make the cookie accessible only through HTTP(S) requests
        });

        res.send({'message': 'Login successful!'});
    }

    // if jwt token does not exist, send error message
    else {
        res.send(data);
    }
});

// handle GET request from register.html
app.get('/register', (req, res) => {
    res.sendFile(__dirname + '/register.html');
});

// handle POST request from register.html with header checks
app.post('/registerRequest', checkHeaders, async (req, res) => {
    // send POST request from register form to identity service
    const response = await fetch("http://identity:8081/register", { 
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(req.body),
    });

    // parse the JSON data received from identity service
    const data = await response.json();

    // send the parsed data as a response
    res.send(data);
});

// logout and delete cookie
app.delete('/logout', async (req, res) => {
    try {
        // get cookie
        const token = req.cookies.token;

        // send DELETE request containing jwt token to identity service to delete in db
        const response = await fetch("http://identity:8081/logout", { 
            method: "DELETE",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // send jwt token in Authorization header
            }
        });

        // parse the response received from the identity service
        const data = await response.json();

        // if delete successful, unset cookie
        res.clearCookie('token');

        // Send response to the client
        res.json({ message: data });
        
    } catch (error) {
        // Handle other errors that might occur
        console.error(error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});
// ############################## END OF IDENTITY SERVICE #########################################

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});