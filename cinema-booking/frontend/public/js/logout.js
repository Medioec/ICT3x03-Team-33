$("#logout-button").click(function () {
    fetch("/logout", {
        method: "PUT", 
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
    })

    .then(response => {
        window.location.href = "/";
    })

    .catch(error => {
        console.error('Error occurred', error);
    });
});
