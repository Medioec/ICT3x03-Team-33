// get all movies from movie service
async function getAllMovies() {
    try {
        const response = await fetch("http://movie:8082/getAllMovies", {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
        });

        if (!response.ok) {
            console.error("Response not OK. Status:", response.status);
            throw new Error("Failed to get movies");
        }

        return response.json();
    } catch (error) {
        console.error("Error in getAllMovies:", error);
        throw error;
    }
}

module.exports = {
    getAllMovies
};