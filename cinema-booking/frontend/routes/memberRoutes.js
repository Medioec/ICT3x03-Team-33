const express = require('express');
const router = express.Router();
const memberController = require('../controllers/memberController');
const checkUserRole = require('../middleware/checkUserRole');

member_role = 'member';

router.get('/member', checkUserRole(member_role), memberController.getMembersHomePage);

// recommended cinemas
router.get('/cinemas', checkUserRole(member_role), memberController.getCinemasPage);

// view all bookings
router.get('/viewbooking', checkUserRole(member_role), memberController.getMemberBookingPage);

// profile page for cc info
router.get('/memberprofile', checkUserRole(member_role), memberController.getMemberProfilePage);

// checkout only for members
router.get('/payment', checkUserRole(member_role), memberController.getMemberPaymentPage);

// Add other routes as needed

module.exports = router;