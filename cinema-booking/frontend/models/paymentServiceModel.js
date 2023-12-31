// Required for https, set agent: httpsAgent in fetch
const httpsAgent = require('../middleware/httpsAgent');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

async function makePayment(token, paymentData) {
    const response = await fetch("https://payment/makePayment", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(paymentData),
        agent: httpsAgent
    });

    const responseData = await response.json();
    return responseData;
}

async function addCreditCard(token, creditCardData) {
    const response = await fetch("https://payment/addCreditCard", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(creditCardData),
        agent: httpsAgent
    });

    if (response.status === 201) {
        return response;
    } else if (response.status === 400) {
        throw new Error('Bad Request - Invalid credit card data');
    } else {
        throw new Error('Internal Server Error');
    }
}


async function getOneCreditCard(token, creditCardId) {
    const requestData = {
        creditCardId: creditCardId
    };
    
    const response = await fetch("https://payment/getOneCreditCard", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(requestData),
        agent: httpsAgent
    });

    const responseData = await response.json();
    return responseData;
}

async function getAllCreditCards(token) {
    try {
        const response = await fetch("https://payment/getAllCreditCards", {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            agent: httpsAgent
        });
        const responseData = await response.json();
        return responseData;
    } catch (error) {
        console.error("Error in getAllCreditCards:", error); 
        throw error; 
    }
}

async function updateOneCreditCard(token, creditCardData) {
    const response = await fetch("https://payment/updateOneCreditCard", {
        method: "PUT",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(creditCardData),
        agent: httpsAgent
    });

    if (response.status === 200) {
        return response;
    } else if (response.status === 400) {
        throw new Error('Bad Request - Invalid credit card data');
    } else {
        throw new Error('Internal Server Error');
    }
}

async function deleteCreditCard(token, creditSent) {

    const response = await fetch("https://payment/deleteCreditCard", {
        method: "DELETE",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(creditSent),
        agent: httpsAgent
    });

    if (response.status === 200) {
        return response;
    } else if (response.status === 400) {
        throw new Error('Bad Request - Invalid credit card data');
    } else {
        throw new Error('Internal Server Error');
    }
}

module.exports = {
    makePayment,
    addCreditCard,
    getOneCreditCard,
    getAllCreditCards,
    updateOneCreditCard,
    deleteCreditCard
};
