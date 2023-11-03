async function makePayment(sessionId, paymentData) {
    const response = await fetch("http://payment:8084/makePayment", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionId}`
        },
        body: JSON.stringify(paymentData),
    });

    const responseData = await response.json();
    return responseData;
}

async function addCreditCard(token, creditCardData) {
    const response = await fetch("http://payment:8084/addCreditCard", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(creditCardData),
    });

    return response;
}

async function getOneCreditCard(sessionId, creditCardId) {
    const requestData = {
        creditCardId: creditCardId
    };
    
    const response = await fetch("http://payment:8084/getOneCreditCard", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionId}`
        },
        body: JSON.stringify(requestData),
    });

    const responseData = await response.json();
    return responseData;
}

async function getAllCreditCards(token) {
    try {
        const response = await fetch("http://payment:8084/getAllCreditCards", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
        });
        const responseData = await response.json();
        console.log("API Response Data:", responseData); // Log the API response data
        return responseData;
    } catch (error) {
        console.error("Error in getAllCreditCards:", error); // Log the error
        throw error; // Rethrow the error to handle it in your controller.
    }
}

async function updateOneCreditCard(sessionId, creditCardData) {
    const response = await fetch("http://payment:8084/updateOneCreditCard", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionId}`
        },
        body: JSON.stringify(creditCardData),
    });

    const responseData = await response.json();
    return responseData;
}

async function deleteCreditCard(sessionId, creditCardId) {
    const requestData = {
        creditCardId: creditCardId
    };

    const response = await fetch("http://payment:8084/deleteCreditCard", {
        method: "DELETE",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${sessionId}`
        },
        body: JSON.stringify(requestData),
    });

    const responseData = await response.json();
    return responseData;
}

module.exports = {
    makePayment,
    addCreditCard,
    getOneCreditCard,
    getAllCreditCards,
    updateOneCreditCard,
    deleteCreditCard
};
