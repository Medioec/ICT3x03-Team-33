// make sure the DOM is loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-button").addEventListener("click", function (event) {
        event.preventDefault();
        console.log("clicked")

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // Create an object with the data to be sent as JSON
        const data = {
            username: username,
            password: password
        };

        console.log(data)

        // Send a POST request with JSON data to the identity service
        fetch("/login", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(data),
        })

        .then(response => {
            console.error(`Response status: ${response.status}`);
            console.log("Response text:", response.text());
            return response.json();
            // return response.json();
        })

        // Handle the response from the server
        .then(data => {
            if (data.sessionID) {
                // Successful login, generate ECDH key pair

            } else {
                // Login failed, handle the error message
                document.getElementById("error-message").textContent = "error";
            }
        })
        .catch(error => {
            // Handle errors in the request
            console.error("Error:", error);
        });
    });
});
