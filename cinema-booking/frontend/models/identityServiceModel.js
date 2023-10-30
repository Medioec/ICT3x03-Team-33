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
        credentials: 'include' 
    });

    responseData = await response.json();
    return responseData;
}

async function registerRequest(body) {
    const csrfToken = getCookie("csrf_token"); 
    const response = await fetch("http://identity:8081/register", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(body),
        credentials: 'include' 
    });
    
    return response;
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function logoutRequest(token) {
    const response = await fetch("http://identity:8081/logout", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        credentials: 'include' 
    });

    return response;
}

module.exports = {
    loginRequest,
    registerRequest,
    logoutRequest
};
