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
        console.log(bookingHistory);

        return res.render('pages/memberbooking.ejs', { bookingHistory, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

exports.getMemberProfilePage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;
        const token = req.cookies.token;

        console.log("Token:", token); // Log the token for debugging

        const creditCards = await paymentService.getAllCreditCards(token);
        console.log("Credit Cards:", creditCards); // Log the credit cards data

        return res.render('pages/memberprofile.ejs', { creditCards, loggedIn });
    } catch (error) {
        console.error("Error in getMemberProfilePage:", error); // Log the error
        res.status(500).send('Internal Server Error');
    }
};


exports.getMemberPaymentPage = async (req, res) => {
    try {
        const loggedIn = req.loggedIn;
        
        // seat & movie information selected by user passed over 
        const seats = req.query.seats;
        const showtimes = req.query.showtimeId;
        
        // necessary details 
        const showtimeDetails = await movieService.getShowtimeById(showtimes);

        return res.render('pages/payment.ejs', {seats, showtimeDetails, loggedIn });
    } catch (error) {
        res.status(500).send('Internal Server Error');
    }
};

exports.postCreditCard = async (req, res) => {
    try {
        const token = req.cookies.token;
        const creditCardDetails = req.body; // Retrieve credit card details from the request body

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


