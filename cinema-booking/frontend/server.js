const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors')

const app = express();
const port = process.env.PORT || 8080;

app.use(cors());
app.use(bodyParser.json());

app.use(express.static(__dirname)); // Serve static files from the root directory
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html'); // Serve the index.html from the root directory
});


// ############################## IDENTITY SERVICE #########################################
// handle GET request from login.html
app.get('/login', (req, res) => {
    res.sendFile(__dirname + '/login.html');
});

// handle POST request from login.html
app.post('/loginRequest', async (req, res) => {
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

    // send the parsed data as a response
    res.send(data);
});

// handle GET request from register.html
app.get('/register', (req, res) => {
    res.sendFile(__dirname + '/register.html');
});

// handle POST request from register.html
app.post('/registerRequest', async (req, res) => {
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
// ############################## END OF IDENTITY SERVICE #########################################

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});