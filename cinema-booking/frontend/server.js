const express = require('express');
const axios = require('axios');
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

// handle GET request from login.html
app.get('/loginPage', (req, res) => {
    res.sendFile(__dirname + '/login.html'); // Serve the index.html from the root directory
});

// handle POST request from login.html
app.post('/loginRequest', async (req, res) => {
    try {
        // send POST request from login form to identity service
         const response = await axios.post('http://identity:8081/login', req.body, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log("Returning from backend " + response.data)
        // Handle the response from the identity service
        res.send(response.data);

    } catch (error) {
        // Handle errors here and send an error response
        console.error(error.message);
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});