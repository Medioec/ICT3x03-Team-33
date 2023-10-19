-- Create tables
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
    currStatus VARCHAR(255) NOT NULL
);

CREATE TABLE CreditCard (
    creditCardId SERIAL PRIMARY KEY NOT NULL,
    userId UUID NOT NULL,
    blob BYTEA NOT NULL
);

CREATE TABLE Cinema (
    cinemaId SERIAL PRIMARY KEY NOT NULL,
    cinemaName VARCHAR(255) NOT NULL,
    locationName VARCHAR(255) NOT NULL
);

CREATE TABLE Theater (
    theaterNumber VARCHAR(255) PRIMARY KEY NOT NULL
);

CREATE TABLE Showtimes (
    showtimeId SERIAL PRIMARY KEY NOT NULL,
    cinemaId INT NOT NULL,
    theaterId VARCHAR(255) NOT NULL,
    movieId INT NOT NULL,
    dateAndTime TIMESTAMP NOT NULL
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
    ticketId INT UNIQUE NOT NULL
);

CREATE TABLE Seat (
    seatId VARCHAR(255) PRIMARY KEY NOT NULL
);

-- Add foreign keys
ALTER TABLE UserSessions
ADD CONSTRAINT fk_user_sessions_userId
FOREIGN KEY (userId) REFERENCES CinemaUser(userId);

ALTER TABLE CreditCard
ADD CONSTRAINT fk_credit_card_userId
FOREIGN KEY (userId) REFERENCES CinemaUser(userId);

ALTER TABLE Showtimes
ADD CONSTRAINT fk_showtimes_cinemaId
FOREIGN KEY (cinemaId) REFERENCES Cinema(cinemaId);

ALTER TABLE Showtimes
ADD CONSTRAINT fk_showtimes_theaterId
FOREIGN KEY (theaterId) REFERENCES Theater(theaterNumber);

ALTER TABLE Showtimes
ADD CONSTRAINT fk_showtimes_movieId
FOREIGN KEY (movieId) REFERENCES MovieDetails(movieId);

ALTER TABLE BookingDetails
ADD CONSTRAINT fk_booking_details_showtimeId
FOREIGN KEY (showtimeId) REFERENCES Showtimes(showtimeId);

ALTER TABLE BookingDetails
ADD CONSTRAINT fk_booking_details_userId
FOREIGN KEY (userId) REFERENCES CinemaUser(userId);

-- Insert Movie data
INSERT INTO MovieDetails (title, synopsis, genre, contentRating, lang, subtitles)
VALUES
    ('The Shawshank Redemption', 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.', 'Drama', 'R', 'English', 'English'),
    ('The Godfather', 'An organized crime dynasty''s aging patriarch transfers control of his clandestine empire to his reluctant son.', 'Crime', 'R', 'English', 'English'),
    ('Pulp Fiction', 'The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.', 'Crime', 'R', 'English', 'English'),
    ('The Dark Knight', 'When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham. The Dark Knight must accept one of the greatest psychological and physical tests of his ability to fight injustice.', 'Action', 'PG-13', 'English', 'English'),
    ('Forrest Gump', 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75.', 'Drama', 'PG-13', 'English', 'English'),
    ('Schindler''s List', 'In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis.', 'Biography', 'R', 'English', 'English'),
    ('The Matrix', 'A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.', 'Action', 'R', 'English', 'English'),
    ('Titanic', 'A seventeen-year-old aristocrat falls in love with a kind but poor artist aboard the luxurious, ill-fated R.M.S. Titanic.', 'Drama', 'PG-13', 'English', 'English'),
    ('Fight Club', 'An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much, much more.', 'Drama', 'R', 'English', 'English'),
    ('Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', 'Action', 'PG-13', 'English', 'English'),
    ('The Lord of the Rings: The Fellowship of the Ring', 'A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.', 'Adventure', 'PG-13', 'English', 'English'),
    ('Star Wars: Episode IV - A New Hope', 'Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a Wookiee, and two droids to save the galaxy from the Empire''s world-destroying battle station, while also attempting to rescue Princess Leia from the mysterious Darth Vader.', 'Adventure', 'PG', 'English', 'English'),
    ('The Green Mile', 'The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift.', 'Crime', 'R', 'English', 'English'),
    ('Forrest Gump', 'The presidencies of Kennedy and Johnson, the events of Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with an IQ of 75.', 'Drama', 'PG-13', 'English', 'English'),
    ('The Lord of the Rings: The Two Towers', 'While Frodo and Sam edge closer to Mordor with the help of the shifty Gollum, the divided fellowship makes a stand against Sauron''s new ally, Saruman, and his hordes of Isengard.', 'Adventure', 'PG-13', 'English', 'English'),
    ('The Silence of the Lambs', 'A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims.', 'Crime', 'R', 'English', 'English'),
    ('Gladiator', 'A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.', 'Action', 'R', 'English', 'English'),
    ('The Lion King', 'Lion cub and future king Simba searches for his identity. His eagerness to please others and penchant for testing his boundaries sometimes gets him into trouble.', 'Animation', 'G', 'English', 'English'),
    ('The Departed', 'An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in South Boston.', 'Crime', 'R', 'English', 'English'),
    ('The Intouchables', 'After he becomes a quadriplegic from a paragliding accident, an aristocrat hires a young man from the projects to be his caregiver.', 'Comedy', 'R', 'French', 'English');


-- Change all movie subtitles to chinese
UPDATE MovieDetails
SET subtitles = 'Chinese';

-- Prints in console the contents of the MovieDetails table
SELECT * FROM MovieDetails;

-- Insert 1 fake user data for testing
INSERT INTO CinemaUser (userId, email, username, passwordHash, userRole)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000', -- Replace with a generated UUID
    'fakeuser123@example.com', -- Replace with a fake email address
    'fake_user123', -- Replace with a fake username
    'fake_password_hash', -- Replace with a fake password hash
    'user' -- Replace with the desired user role
);


