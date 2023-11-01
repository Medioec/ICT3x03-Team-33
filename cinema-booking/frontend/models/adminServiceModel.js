async function createStaffRequest(body, token) {
    const response = await fetch("http://identity:8081/create_staff", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body),
    });
    
    return response;
}

module.exports = {
    createStaffRequest
};
