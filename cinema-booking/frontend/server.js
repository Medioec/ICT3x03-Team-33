const express = require('express');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 8080;

// middleware
app.use(cors());
app.use(cookieParser());
app.use(bodyParser.json());

// set up static files (css, js, images) and views
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// routes
const identityServiceRoutes = require('./routes/identityServiceRoutes');
const homeRoutes = require('./routes/homeRoutes');
app.use(homeRoutes);
app.use(identityServiceRoutes);

// catch-all route for handling undefined routes
app.use((req, res) => {
    res.status(404).send('Not Found');
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
