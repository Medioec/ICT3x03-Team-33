$("#logout-button").click(async function () {
    try {
        const response = await fetch("/logout", {
            method: "PUT", 
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
        });
        
        if (response.ok) {
            // TODO LOGOUT SUCCESS CODE (e.g. redirect)
            console.log('Logout successful');
        } else {
            // Handle error or show a message to the user
            console.error('Logout failed');
        }
    } catch (error) {
        console.error('Error occured', error);
    }
});