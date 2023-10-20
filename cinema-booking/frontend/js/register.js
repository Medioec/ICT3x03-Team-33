// make sure the DOM is loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("register-button").addEventListener("click", function (event) {
        event.preventDefault();
        
        const email = document.getElementById("email").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        
        // Create an object with the data to be sent as JSON
        const data = {
            email: email,
            username: username,
            password: password
        };

        // Send a POST request with JSON data to the identity service
        fetch("/registerRequest", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(data),
        })
        
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })

        // Handle the response from the server
        .then(data => {
            if (data.sessionID) {
                // Successful registration, display success
                // TODO: REPLACE WITH SUCCESS CODE
                document.getElementById("error-message").textContent = data.message;

            } else {
                // Registration failed, handle the error message
                document.getElementById("error-message").textContent = data.message;
            }
        })
        .catch(error => {
            // Handle errors in the request
            console.error("Error:", error);
        });
    });
});
