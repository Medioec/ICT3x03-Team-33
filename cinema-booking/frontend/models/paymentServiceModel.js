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

    if (response.status === 200) {
        // Handle a successful response
        return response;
    } else if (response.status === 400) {
        // Handle a 400 Bad Request response
        throw new Error('Bad Request - Invalid credit card data');
    } else {
        // Handle other response status codes as needed
        throw new Error('Internal Server Error');
    }
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
