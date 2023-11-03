// mvc refresher:
// model interacts with backend services -> query for data, sends user data to backend
// if you add new requests, make sure you add to module.exports at the bottom of the page

async function loginRequest(body) {
    const response = await fetch("http://identity:8081/login", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });

    responseData = await response.json();
    return responseData;
}

async function registerRequest(body) {
    const response = await fetch("http://identity:8081/register", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });
    
    return response;
}

async function logoutRequest(token) {
    const response = await fetch("http://identity:8081/logout", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    return response;
}

async function verifyStaffActivationToken(token) {
    const response = await fetch(`http://identity:8081/activate_staff_account/${token}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    });

    return response;
}

async function setStaffPasswordRequest(token, body) {
    const response = await fetch(`http://identity:8081/staff_set_password/${token}`, {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });

    return response;
}

module.exports = {
    loginRequest,
    registerRequest,
    logoutRequest,
    verifyStaffActivationToken,
    setStaffPasswordRequest
};
