CREATE TABLE CinemaUser (
    userId UUID PRIMARY KEY NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    passwordHash VARCHAR(255) NOT NULL,
    userRole VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE UserSessions (
    sessionId UUID PRIMARY KEY NOT NULL,
    userId UUID NOT NULL,
    expiryTimestamp TIMESTAMP NOT NULL,
    currStatus VARCHAR(255) NOT NULL,
    FOREIGN KEY (userId) REFERENCES CinemaUser(userId)
);

CREATE TABLE CreditCard (
    creditCardId SERIAL PRIMARY KEY NOT NULL,
    userId UUID NOT NULL,
    blob BYTEA NOT NULL,
    FOREIGN KEY (userId) REFERENCES CinemaUser(userId)
);

CREATE TABLE Showtimes (
    showtimeId SERIAL PRIMARY KEY NOT NULL,
    cinemaId INT NOT NULL,
    theaterId  VARCHAR(255) NOT NULL,
    movieId INT NOT NULL,
    dateAndTime TIMESTAMP NOT NULL,
    FOREIGN KEY (cinemaId) REFERENCES Cinema(cinemaId),
    FOREIGN KEY (theaterId) REFERENCES Theater(theaterNumber),
    FOREIGN KEY (movieId) REFERENCES MovieDetails(movieId)
);

CREATE TABLE Theater (
    theaterNumber VARCHAR(255) PRIMARY KEY NOT NULL
);

CREATE TABLE Cinema (
    cinemaId SERIAL PRIMARY KEY NOT NULL,
    cinemaName VARCHAR(255) NOT NULL,
    locationName VARCHAR(255) NOT NULL
);

CREATE TABLE MovieDetails (
    movieId SERIAL PRIMARY KEY NOT NULL,
    title VARCHAR(255) NOT NULL,
    synopsis VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    contentRating VARCHAR(255) NOT NULL,
    lang VARCHAR(255) NOT NULL,
    subtitles VARCHAR(255) NOT NULL
);

CREATE TABLE BookingDetails (
    seatId VARCHAR(255) NOT NULL,
    showtimeId INT NOT NULL,
    userId UUID NOT NULL UNIQUE,
    ticketId INT UNIQUE NOT NULL,
    FOREIGN KEY (showtimeId) REFERENCES Showtimes(showtimeId),
    FOREIGN KEY (userId) REFERENCES CinemaUser(userId),
    PRIMARY KEY(seatId, showtimeId)
);

CREATE TABLE Seat (
    seatId VARCHAR(255) PRIMARY KEY NOT NULL
);



