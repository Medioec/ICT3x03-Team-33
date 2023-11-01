const express = require('express');
const router = express.Router();
const staffController = require('../controllers/staffController');
const checkHeaders = require('../middleware/checkHeaders');
const checkUserRole = require('../middleware/checkUserRole');

staff_role = 'staff';

router.get('/staff', checkUserRole(staff_role), staffController.getStaffDashboard);

// activate account
router.get('/activate', staffController.verifyStaffActivationLink);
router.get('/setPassword', staffController.getStaffPasswordPage);
router.post('/setPasswordRequest', staffController.setStaffPassword);
// Add other routes as needed

module.exports = router;
