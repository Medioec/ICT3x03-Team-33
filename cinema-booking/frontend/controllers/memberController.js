const movieService = require('../models/movieServiceModel');
const bookingService = require('../models/bookingServiceModel');
const paymentService = require('../models/paymentServiceModel');

exports.getMembersHomePage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;

        // Get all movies and showtimes
        const movies = await movieService.getAllMovies();
        const showtimes = await movieService.getAllShowtimes();
        const cinemas = await movieService.getAllCinemas();

        return res.render('pages/membershome.ejs', { movies, cinemas, showtimes, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

exports.getCinemasPage = [async (req, res) => {
    try {
        const loggedIn = req.loggedIn;
        const cinemaId = req.query.cinemaId;
        const cinemaIdNumber = parseInt(cinemaId);
        const movies = await movieService.getAllMovies();
        const showtimes = await movieService.getAllShowtimes();
        const cinemaData = await movieService.getAllCinemas();

        // Filter showtimes for the selected cinemaId
        const filteredCinemaShowtimes = showtimes.filter((showtime) => showtime.cinemaId === cinemaIdNumber);

        // Find the cinema with the matching cinemaId and extract the cinemaName
        const selectedCinema = cinemaData.find((cinema) => cinema.cinemaId === cinemaIdNumber);
        const cinemaName = selectedCinema ? selectedCinema.cinemaName : 'Cinema Not Found';

        // Extract titles for each showtime
        const titles = filteredCinemaShowtimes.map((showtime) => {
            const matchingMovie = movies.find((movie) => movie.movieId === showtime.movieId);
            return matchingMovie ? matchingMovie.title : 'Movie Title Not Found';
        });

        // Render the 'cinemas.ejs' page with the movie data, cinema name, and loggedIn status
        res.render('pages/cinemas.ejs', { cinemaId, showtimes, cinemaData, titles, filteredCinemaShowtimes, cinemaName, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
}];

exports.getMemberBookingPage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;
        const token = req.cookies.token;

        const bookingHistory = await bookingService.retrieveAllBookings(token);
        const bookingShowtime = bookingHistory.map((booking) => booking.showtimeId);
        const showtimeArray = [];

        for (const showtimeId of bookingShowtime) {
            const showtime = await movieService.getShowtimeById(showtimeId);
            showtimeArray.push(showtime);
        }

        return res.render('pages/memberbooking.ejs', { showtimeArray, bookingShowtime, loggedIn });
    } catch (error) {
        console.error("Error in getMemberBookingPage:", error);
    }
};


exports.getMemberProfilePage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;
        const token = req.cookies.token;

        const creditCards = await paymentService.getAllCreditCards(token);
        console.log(creditCards);

        return res.render('pages/memberprofile.ejs', { creditCards, loggedIn });
    } catch (error) {
        console.error("Error in getMemberProfilePage:", error); 
        res.status(500).send('Internal Server Error');
    }
};


exports.getMemberPaymentPage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;
        const token = req.cookies.token;

        // seat & movie information selected by user passed over 
        const seat = req.query.seat;        
        const showtimes = req.query.showtimeId;
        
        // necessary details 
        const showtimeDetails = await movieService.getShowtimeById(showtimes);
        const creditCards = await paymentService.getAllCreditCards(token);

        return res.render('pages/payment.ejs', {seat, showtimes, showtimeDetails, creditCards, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

exports.postCreditCard = async (req, res) => {
    try {
        const token = req.cookies.token;
        const creditCardDetails = req.body; 

        // Ensure that the creditCardDetails object contains the necessary properties
        if (!creditCardDetails) {
            return res.status(400).json({ message: 'Bad Request - Missing credit card details' });
        }

        const creditCard = await paymentService.addCreditCard(token, creditCardDetails);

        if (creditCard.status === 200) {
            return res.status(200).json({ message: 'Credit Card added successfully' });
        } else if (creditCard.status === 400) {
            // Handle a 400 Bad Request response
            return res.status(400).json({ message: 'Bad Request - Invalid credit card data' });
        } else {
            // Handle other response status codes as needed
            return res.status(500).json({ message: 'Internal Server Error' });
        }
    } catch (error) {
        res.status(500).json({ message: 'Internal Server Error' });
    }
};


exports.deleteCreditCard = async (req, res) => {
    try {
        const token = req.cookies.token;
        const creditCardDetails = req.body; 

        console.log(creditCardDetails);

        // Ensure that the creditCardDetails object contains the necessary properties
        if (!creditCardDetails) {
            return res.status(400).json({ message: 'Bad Request - Missing credit card details' });
        }

        // Delete the credit card
        const creditCard = await paymentService.deleteCreditCard(token, creditCardDetails);

        // handle response
        if (creditCard.status === 200) {
            return res.status(200).json({ message: 'Credit Card deleted successfully' });
        } else if (creditCard.status === 400) {
            // Handle a 400 Bad Request response
            return res.status(400).json({ message: 'Bad Request - Invalid credit card data' });
        } else {
            // Handle other response status codes as needed
            return res.status(500).json({ message: 'Internal Server Error' });
        }

    } catch (error) {
        res.status(500).json({ message: 'Internal Server Error' });
    }
};


exports.postGenerateBooking = async (req, res) => {
    try{

        const token = req.cookies.token;
        const bookingDetails = req.body;

        // Ensure that the bookingDetails object contains the necessary properties
        if (!bookingDetails) {
            return res.status(400).json({ message: 'Bad Request - Missing booking details' });
        }

        const booking = await bookingService.generateBooking(token, bookingDetails);

        if (booking.status === 201) {
            return res.status(201).json({ message: 'Booking generated successfully' });
        } else if (booking.status === 400) {
            // Handle a 400 Bad Request response
            return res.status(400).json({ message: 'Bad Request - Invalid booking data' });
        } else {
            // Handle other response status codes as needed
            return res.status(500).json({ message: 'Internal Server Error' });
        }

    } catch(error){
        res.status(500).send('Internal Server Error');
    }
};

