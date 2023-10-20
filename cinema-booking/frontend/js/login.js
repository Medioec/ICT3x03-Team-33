// make sure the DOM is loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-button").addEventListener("click", function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // create an object with the data to be sent as JSON
        const data = {
            username: username,
            password: password
        };
        
        console.log(data);

        // send a POST request with JSON data to the identity service
        fetch("/loginRequest", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(data),
        })

         // handle the response from the server
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
       
        .then(data => {
            console.log(data);
            if (data.sessionToken) {
                // set the session token as a cookie
                document.cookie = `session_token=${data.sessionID}; path=/`;
                
                // successful login, display success
                // TODO: REPLACE WITH SUCCESS CODE
                document.getElementById("error-message").textContent = data.message;
            }
        })

        // handle errors in the request
        .catch(error => {
            console.error("Error:", error);

            // login failed, handle the error message
            document.getElementById("error-message").textContent = data.message;
        });
    });
});
