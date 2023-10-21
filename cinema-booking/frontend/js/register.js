// make sure the DOM is loaded before executing the script
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("register-button").addEventListener("click", async function (event) {
        event.preventDefault();
        
        const email = document.getElementById("email").value;
        const username = document.getElementById("username").value;
        const password = document.getElementById("userPassword").value;
        
        // Create an object with the data to be sent as JSON
        const data = {
            email: email,
            username: username,
            password: password
        };

        // Send a POST request with JSON data to the identity service
        await fetch("/registerRequest", { 
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
