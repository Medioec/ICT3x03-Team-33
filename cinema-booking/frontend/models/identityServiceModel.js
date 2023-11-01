const https = require('https');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const httpsAgent = new https.Agent({
      rejectUnauthorized: false,
    });


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

    responseData = await response.json();
    return responseData;
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

module.exports = {
    loginRequest,
    registerRequest,
    logoutRequest
};
