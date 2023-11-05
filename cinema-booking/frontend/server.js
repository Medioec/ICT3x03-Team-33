const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');

const app = express();
// Serve static files(password str meter) from the 'dist' directory
app.use(express.static(path.join(__dirname, 'dist')));

// middleware
app.use(cors());
app.use(cookieParser());
app.use(bodyParser.json());

// set up static files (css, js, images) and views
app.use(express.static(path.join(__dirname, 'public')));

// Serve the zxcvbn-ts core package as a static asset
app.use('/zxcvbn-core', express.static(path.join(__dirname, 'node_modules/@zxcvbn-ts/core/dist')));

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

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
