// Required for https, set agent: httpsAgent in fetch
const httpsAgent = require('../middleware/httpsAgent');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

// mvc refresher:
// model interacts with backend services -> query for data, sends user data to backend
// if you add new requests, make sure you add to module.exports at the bottom of the page

async function loginRequest(body) {
    const response = await fetch("https://identity/login", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
        agent: httpsAgent
    });

    return response;
}

async function verifyOTP(token, body) {
    const response = await fetch("https://identity/verify_otp", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body),
        agent: httpsAgent
    });

    return response;
}

async function registerRequest(body) {
    const response = await fetch("https://identity/register", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
        agent: httpsAgent
    });
    
    return response;
}

async function logoutRequest(token) {
    const response = await fetch("https://identity/logout", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        agent: httpsAgent
    });

    return response;
}

async function verifyStaffActivationToken(token) {
    const response = await fetch(`https://identity/activate_staff_account/${token}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        agent: httpsAgent
    });

    return response;
}

async function setStaffPasswordRequest(token, body) {
    const response = await fetch(`https://identity/staff_set_password/${token}`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
        agent: httpsAgent
    });

    return response;
}

async function verifyMemberActivationToken(token) {
    const response = await fetch(`https://identity/activate_member_account/${token}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        agent: httpsAgent
    });

    return response;
}

module.exports = {
    loginRequest,
    verifyOTP,
    registerRequest,
    logoutRequest,
    verifyStaffActivationToken,
    setStaffPasswordRequest,
    verifyMemberActivationToken
};
