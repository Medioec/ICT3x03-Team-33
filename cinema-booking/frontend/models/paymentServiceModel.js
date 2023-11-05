async function makePayment(sessionId, paymentData) {
    const response = await fetch("http://paymentservice:8084/makePayment", {
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
    const response = await fetch("http://paymentservice:8084/addCreditCard", {
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

async function getOneCreditCard(sessionId, userId, creditCardId) {
    const requestData = {
        userId: userId,
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

async function getAllCreditCards(token, userId) {
    const requestData = {
        userId: userId
    };
    
    const response = await fetch("http://payment:8084/getAllCreditCards", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(requestData),
    });

    const responseData = await response.json();
    return responseData;
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

async function deleteCreditCard(sessionId, userId, creditCardId) {
    const requestData = {
        userId: userId,
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
