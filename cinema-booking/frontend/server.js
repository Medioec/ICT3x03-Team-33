const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');
const https = require('https');
const fs = require('fs');

const app = express();

// middleware
app.use(cors());
app.use(cookieParser());
app.use(bodyParser.json());

// set up static files (css, js, images) and views
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// set trust for reverse proxy
app.set('trust proxy', true);

// routes
const identityServiceRoutes = require('./routes/identityServiceRoutes');
const homeRoutes = require('./routes/homeRoutes');
const staffRoutes = require('./routes/staffRoutes');
app.use(homeRoutes);
app.use(identityServiceRoutes);
app.use(staffRoutes);

// catch-all route for handling undefined routes
app.use((req, res) => {
    res.status(404).send('Not Found');
});

// setting up https
const privateKey = fs.readFileSync('privkey.pem', 'utf8');
const certificate = fs.readFileSync('fullchain.pem', 'utf8');
const ca = fs.readFileSync('serverca.crt', 'utf8');
const credentials = { key: privateKey, cert: certificate, ca: ca, requestCert: true, rejectUnauthorized: true };

const httpsServer = https.createServer(credentials, app);

httpsServer.on('clientError', (err, socket) => {
    console.error(err);
    socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
  });
  

const port = 443;
const hostname = 'frontend';

httpsServer.listen(port);
console.log(`Server is running at https://${hostname}:${port}/`);
