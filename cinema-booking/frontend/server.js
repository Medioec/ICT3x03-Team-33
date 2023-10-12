const express = require('express');
const app = express();
const port = process.env.PORT || 8080;

app.use(express.static(__dirname)); // Serve static files from the root directory
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html'); // Serve the index.html from the root directory
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
