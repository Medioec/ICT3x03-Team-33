let fetch;

import('node-fetch').then(module => {
    fetch = module.default;
});

async function fetchCsrfToken(req, res, next) {
    try {
        // Ensure fetch is available before using it
        if (!fetch) {
            throw new Error('Fetch is not initialized yet.');
        }

        const response = await fetch('http://identity:8081/get_csrf_token');
        const data = await response.json();

        if (data.csrf_token) {
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
