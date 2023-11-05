const express = require('express');
const router = express.Router();
const memberController = require('../controllers/memberController');
const checkUserRole = require('../middleware/checkUserRole');
const isOTPVerified = require('../middleware/isOTPVerified');

member_role = 'member';

router.get('/member', isOTPVerified, checkUserRole(member_role), memberController.getMembersHomePage);

// recommended cinemas
router.get('/cinemas', isOTPVerified, checkUserRole(member_role), memberController.getCinemasPage);

// view all bookings
router.get('/viewbooking', isOTPVerified, checkUserRole(member_role), memberController.getMemberBookingPage);

// profile page for cc info
router.get('/memberprofile', isOTPVerified, checkUserRole(member_role), memberController.getMemberProfilePage);

// checkout only for members
router.get('/payment', isOTPVerified, checkUserRole(member_role), memberController.getMemberPaymentPage);

// verify account activation link
router.get('/verify', memberController.verifyAccount);

// add credit card
router.post('/addcreditcard', isOTPVerified, checkUserRole(member_role), memberController.postCreditCard);

// process booking 
router.post('/processbooking', isOTPVerified, checkUserRole(member_role), memberController.postGenerateBooking);

// add credit card
router.delete('/deletecreditcard', isOTPVerified, checkUserRole(member_role), memberController.deleteCreditCard);

// process booking 

// Add other routes as needed
module.exports = router;