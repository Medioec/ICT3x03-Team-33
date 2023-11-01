const express = require('express');
const router = express.Router();
const memberController = require('../controllers/memberController');
const checkUserRole = require('../middleware/checkUserRole');
const checkLoggedIn = require('../middleware/checkLoggedIn');

member_role = 'member';

router.get('/member', checkUserRole(member_role), checkLoggedIn, memberController.getMembersHomePage);

// Add other routes as needed

module.exports = router;