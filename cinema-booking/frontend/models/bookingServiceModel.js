async function generateBooking(bookingData) {
    const response = await fetch("http://bookingservice:8083/generateBooking", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        body: JSON.stringify(bookingData),
    });

    const responseData = await response.json();
    return responseData;
}

async function retrieveOneBooking(sessionId, ticketId) {
    const response = await fetch(`http://bookingservice:8083/retrieveOneBooking/${ticketId}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${sessionId}`
        }
    });

    const responseData = await response.json();
    return responseData;
}

async function retrieveAllBookings(sessionId) {
    const response = await fetch("http://bookingservice:8083/retrieveAllBookings", {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Authorization": `Bearer ${sessionId}`
        }
    });

    const responseData = await response.json();
    return responseData;
}

module.exports = {
    generateBooking,
    retrieveOneBooking,
    retrieveAllBookings
};
