// Required for https, set agent: httpsAgent in fetch
const httpsAgent = require('../middleware/httpsAgent');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

async function generateBooking(token, bookingData) {
    const response = await fetch("https://booking/generateBooking", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(bookingData),
        agent: httpsAgent
    });

    const responseData = await response.json();
    return responseData;
}

async function retrieveOneBooking(token, ticketId) {
    const response = await fetch(`https://booking/retrieveOneBooking/${ticketId}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        agent: httpsAgent
    });

    const responseData = await response.json();
    return responseData;
}

async function retrieveAllBookings(token) {
    const response = await fetch("https://booking/retrieveAllBookings", {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        agent: httpsAgent
    });
    if (response.status === 200) {
        const responseData = await response.json();
        return responseData;
    } else if (response.status === 404) {
        console.log('No bookings found');
    } else {
        throw new Error('Internal Server Error');
    }
}

async function retrieveAllBookedSeats(showtimeId) {
    const response = await fetch(`https://booking/retrieveAllBookedSeats/${showtimeId}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        agent: httpsAgent
    });

    if (response.status === 200) {
        const responseData = await response.json();
        return responseData;
    } else if (response.status === 404) {
        console.log('No bookings found');
    } else {
        throw new Error('Internal Server Error');
    }
}

module.exports = {
    generateBooking,
    retrieveOneBooking,
    retrieveAllBookings,
    retrieveAllBookedSeats
};
