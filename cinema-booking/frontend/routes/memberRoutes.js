const express = require('express');
const router = express.Router();
const memberController = require('../controllers/memberController');
const checkUserRole = require('../middleware/checkUserRole');

member_role = 'member';

router.get('/member', checkUserRole(member_role), memberController.getMembersHomePage);

// Add other routes as needed

module.exports = router;