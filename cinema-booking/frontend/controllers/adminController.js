// models
const adminService = require('../models/adminServiceModel');

const captchaKey = process.env.CAPTCHA_KEY;

exports.getStaffAccountCreationPage = (req, res) => {
    // Get the loggedIn status from the request object
    const loggedIn = req.loggedIn;

    // if not logged in, redirect to home page
    if (!loggedIn) {
        return res.redirect('/');
    }

    res.render('pages/admincreatestaff.ejs', {loggedIn, captchaKey});
};

exports.createStaffAccount = async (req, res) => {
    try {
        console.log("inside CreateStaffAccount request");
        const loggedIn = req.loggedIn;
        
        console.log("request: loggedin", loggedIn);

        // if not logged in, redirect to home page
        if (!loggedIn) {
            return res.redirect('/');
        }
        
        // get token
        const token = req.cookies.token;
        const data = await adminService.createStaffRequest(req.body, token);

        if (data.status === 200) {
            return res.status(200).json({'message': 'Staff added successfully'});
        }
        
    } catch (error) {
        res.status(500).json({ 'message': 'Internal Server Error' });
    }
};