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

module.exports = {
    loginRequest,
    registerRequest,
    logoutRequest
};
