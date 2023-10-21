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
            console.log(data.message);
            document.getElementById("error-message").textContent = data.message;
        })
    });
});
