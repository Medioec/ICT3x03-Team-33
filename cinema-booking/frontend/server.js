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
    console.log(data);

    // if delete successful, unset cookie
    res.clearCookie('token');

    // Send response to the client
    res.json({ message: 'Logout successful' });
    // or if you prefer to send a plain text response
    // res.send('Logout successful');

    // TODO: add any other logout logic here (page redirection, render diff navbar, etc.)
});
// ############################## END OF IDENTITY SERVICE #########################################

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});