const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');

// custom middleware
const checkHeaders = require('./middleware/checkHeaders');
const checkLoggedIn = require('./middleware/checkLoggedIn');
const checkUserRole = require('./middleware/checkUserRole');

const app = express();
const port = process.env.PORT || 8080;

// middleware
app.use(cors());
app.use(cookieParser());
app.use(bodyParser.json());

// app.use(checkHeaders);
// app.use(checkLoggedIn);
// app.use(checkUserRole);

// set up static files (css, js, images) and views
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// routes
const identityServiceRoutes = require('./routes/identityServiceRoutes');
const homeRoutes = require('./routes/homeRoutes');


// app.use('/pages', pageRoutes);
app.use('/', homeRoutes);
app.use('/', identityServiceRoutes);

// catch-all route for handling undefined routes
app.use((req, res) => {
    res.status(404).send('Not Found');
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
            httpOnly: true, // ensures that the cookie is only accessible by the server and not by client-side scripts running in the browser
			// TODO: Uncomment the following line when HTTPS is enabled
			//secure: true,
        });

        res.send({'message': 'Login successful!'});
    }

    // if jwt token does not exist, send error message
    else {
        res.send(data);
    }
});

// TODO: Uncomment the following line when HTTPS is enabled
// Implement the HTTP Strict Transport Security (HSTS) header
// app.use((req, res, next) => {
    // res.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
    // next();
// });


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
