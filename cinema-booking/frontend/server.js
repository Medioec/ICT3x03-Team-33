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
const memberRoutes = require('./routes/memberRoutes');
const adminRoutes = require('./routes/adminRoutes');

app.use(homeRoutes);
app.use(identityServiceRoutes);
app.use(staffRoutes);
app.use(memberRoutes);
app.use(adminRoutes);

// catch-all route for handling undefined routes
app.use((req, res) => {
    res.status(404).send('Not Found');
});

// setting up https
const privateKey = fs.readFileSync('privkey.pem', 'utf8');
const certificate = fs.readFileSync('fullchain.pem', 'utf8');
const ca = fs.readFileSync('ca-cert.pem', 'utf8');
const options = { 
  key: privateKey, 
  cert: certificate, 
  ca: ca, 
  requestCert: true, 
  rejectUnauthorized: true,
  secureOptions: require('constants').SSL_OP_NO_TLSv1 | require('constants').SSL_OP_NO_TLSv1_1,
  ciphers: "TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384"
};

const httpsServer = https.createServer(options, app);

httpsServer.on('clientError', (err, socket) => {
    console.error(err);
    socket.end('HTTP/1.1 400 Bad Request\r\n\r\n');
  });
  

const port = 443;
const hostname = 'frontend';

httpsServer.listen(port);
console.log(`Server is running at https://${hostname}:${port}/`);
