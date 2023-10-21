// make sure the DOM is loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("login-button").addEventListener("click", async function (event) {
        event.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        // create an object with the data to be sent as JSON
        const data = {
            username: username,
            password: password
        };

        // send a POST request with JSON data to the identity service
        await fetch("/loginRequest", { 
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify(data),
        })

        .then(response => response.json())
        .then(data => {
            // extract expiration time from jwt token
            const jwtToken = data.sessionToken;

            const decodedToken = JSON.parse(atob(jwtToken.split('.')[1])); // decode jwt payload
            const expiryDelta = decodedToken.exp - decodedToken.iat; // calculate expiration delta
            const expiryDate = new Date(decodedToken.exp * 1000);
            console.log(decodedToken);
            console.log(expiryDelta);

            // set httponly cookie with the token and expiry
            document.cookie = `token=${jwtToken};
                                expires=${expiryDate}
                                path=/;
                                `;
            console.log(document.cookie);
            // TODO REPLACE WITH LOGIN SUCCESS CODE
            document.getElementById("error-message").textContent = "Login successful!";
        })
    });
});
