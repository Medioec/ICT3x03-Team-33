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
