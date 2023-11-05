// Required for https, set agent: httpsAgent in fetch
const httpsAgent = require('../middleware/httpsAgent');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

async function createStaffRequest(body, token) {
    const response = await fetch("https://identity/create_staff", {
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

module.exports = {
    createStaffRequest
};
