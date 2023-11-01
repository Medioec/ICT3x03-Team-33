// nodejs mvc refresher:
// routes defines mapping of url endpoints and their corresponding controller functions
// specifies http methods (GET, POST etc.)

const express = require('express');
const cors = require('cors');
const router = express.Router();
const app = express();

// Middleware to log headers
app.use((req, res, next) => {
  console.log('Headers:', req.headers);
  next();
});
const identityServiceController = require('../controllers/identityServiceController');
const fetchCsrfToken = require('../middleware/fetchCsrfToken');
const checkHeaders = require('../middleware/checkHeaders');
const checkLoggedIn = require('../middleware/checkLoggedIn');

const corsOptions = {
  origin: 'http://localhost:8080',
  credentials: true,
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
};

router.use(cors(corsOptions));
router.use(fetchCsrfToken);

// login
router.get('/login', checkLoggedIn, identityServiceController.getLogin);
router.post('/loginRequest', checkLoggedIn, checkHeaders, identityServiceController.postLogin);

// register
router.get('/register', checkLoggedIn, identityServiceController.getRegister);
router.post('/registerRequest', checkLoggedIn, checkHeaders, identityServiceController.postRegister);

// logout
router.put('/logout', checkLoggedIn, checkHeaders, identityServiceController.logout);

module.exports = router;

