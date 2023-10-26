$("#logout-button").click(async function () {
    try {
        const response = await fetch("/logout", {
            method: "DELETE", 
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
        console.error('An error occurred during logout', error);
    }
});