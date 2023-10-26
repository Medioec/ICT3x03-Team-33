async function loginRequest(body) {
    const response = await fetch("http://identity:8081/login", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(body),
    });

    return response.json();
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

    return response.json();
}

async function logoutRequest(token) {
    try {
        const response = await fetch("http://identity:8081/logout", {
            method: "DELETE",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });

        return response.json();
    } catch (error) {
        console.error(error);
        throw new Error('Internal Server Error');
    }
}

module.exports = {
    loginRequest,
    registerRequest,
    logoutRequest
};
