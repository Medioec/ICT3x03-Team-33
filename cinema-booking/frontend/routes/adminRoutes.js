const express = require('express');
const router = express.Router();
const adminController = require('../controllers/adminController');
const checkHeaders = require('../middleware/checkHeaders');
const checkUserRole = require('../middleware/checkUserRole');
const isOTPVerified = require('../middleware/isOTPVerified');

admin_role = 'admin';

// create staff acc
router.get('/createStaff', isOTPVerified, checkUserRole(admin_role), adminController.getStaffAccountCreationPage);
router.post('/createStaffRequest', isOTPVerified, checkUserRole(admin_role), checkHeaders, adminController.createStaffAccount);

// Add other routes as needed

module.exports = router;
