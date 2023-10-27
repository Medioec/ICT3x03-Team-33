// Function to retrieve all movies from the database
async function getAllMovies() {
    try {
        const response = await fetch('http://movie:8082/getAllMovies', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Response not OK. Status:', response.status);
            throw new Error('Failed to get movies');
        }

        return response.json();
    } catch (error) {
        console.error('Error in getAllMovies:', error);
        throw error;
    }
}

// Function to create a new movie entry in the database
async function createMovie(movieData) {
    try {
        const response = await fetch('http://movie:8082/createMovie', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movieData)
        });

        if (!response.ok) {
            console.error('Response not OK. Status:', response.status);
            throw new Error('Failed to create a movie');
        }

        return response.json();
    } catch (error) {
        console.error('Error in createMovie:', error);
        throw error;
    }
}

// Function to retrieve a movie by its ID
async function getMovieById(movieId) {
    try {
        const response = await fetch(`http://movie:8082/getMovieById/${movieId}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Response not OK. Status:', response.status);
            throw new Error(`Failed to get movie with ID: ${movieId}`);
        }

        return response.json();
    } catch (error) {
        console.error('Error in getMovieById:', error);
        throw error;
    }
}

// Function to update a movie entry by its ID
async function updateMovieById(movieId, movieData) {
    try {
        const response = await fetch(`http://movie:8082/updateMovieById/${movieId}`, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(movieData)
        });

        if (!response.ok) {
            console.error('Response not OK. Status:', response.status);
            throw new Error(`Failed to update movie with ID: ${movieId}`);
        }

        return response.json();
    } catch (error) {
        console.error('Error in updateMovieById:', error);
        throw error;
    }
}

// Function to delete a movie entry in the database
async function deleteMovieById(movieId) {
    try {
        const response = await fetch(`http://movie:8082/deleteMovieById/${movieId}`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            console.error('Response not OK. Status:', response.status);
            throw new Error(`Failed to delete movie with ID: ${movieId}`);
        }

        return response.json();
    } catch (error) {
        console.error('Error in deleteMovieById:', error);
        throw error;
    }
}

module.exports = {
    createMovie,
    getAllMovies,
    getMovieById,
    updateMovieById,
    deleteMovieById
};