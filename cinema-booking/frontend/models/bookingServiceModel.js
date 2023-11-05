async function generateBooking(token, bookingData) {
    const response = await fetch("http://booking:8083/generateBooking", {
        method: "POST",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(bookingData),
    });

    const responseData = await response.json();
    return responseData;
}

async function retrieveOneBooking(token, ticketId) {
    const response = await fetch(`http://booking:8083/retrieveOneBooking/${ticketId}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    });

    const responseData = await response.json();
    return responseData;
}

async function retrieveAllBookings(token) {
    const response = await fetch("http://booking:8083/retrieveAllBookings", {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
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
    const response = await fetch(`http://booking:8083/retrieveAllBookedSeats/${showtimeId}`, {
        method: "GET",
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
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
