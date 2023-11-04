const https = require('https');
const fs = require('fs');

const httpsAgent = new https.Agent({
    cert: fs.readFileSync('fullchain.pem'),
    key: fs.readFileSync('privkey.pem'),
    ca: fs.readFileSync('ca-cert.pem'),
    rejectUnauthorized: true
  });

module.exports = httpsAgent;
