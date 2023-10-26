async function fetchData() {
    try {
        const response = await fetch("/movielistings", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        });

        const data = await response.json();

        // TODO: Replace with login success code
        console.log(data);
        
    } catch (error) {
        // Handle errors
        console.error('Error:', error);
    }
}

// Call the async function
fetchData();

function generateImageSource(title) {
    // Replace special characters and spaces in the title with underscores
    // e.g. movie title for db: "The Lord of the Rings: The Fellowship of the Ring" 
    // -> "The Lord of the Rings_ The Fellowship of the Ring"
    // using this so to avoid issues with : in the image file path
    const formattedTitle = title.replace(/[:\s]/g, '_');
    return `/images/movies/${formattedTitle}.jpg`;
  }