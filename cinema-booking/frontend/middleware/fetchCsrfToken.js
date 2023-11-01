async function fetchCsrfToken(req, res, next) {
    try {
        // Dynamically import node-fetch
        const fetch = (await import('node-fetch')).default;

        // Fetch the CSRF token from the Flask backend
        const response = await fetch('http://identity:8081/get_csrf_token', { credentials: 'include' });
        const data = await response.json();

        if (data.csrf_token) {
            // Attach the CSRF token to the response so it can be used by the client-side code
            res.locals.csrfToken = data.csrf_token;
            next();
        } else {
            throw new Error('Failed to fetch CSRF token');
        }
    } catch (error) {
        console.error('Error fetching CSRF token:', error);
        res.status(500).send('Internal Server Error');
    }
}

module.exports = fetchCsrfToken;
