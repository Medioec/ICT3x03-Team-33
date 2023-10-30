const winston = require('winston');
const { combine, timestamp, json } = winston.format

function createLog(level, message) {
    const logger = winston.createLogger({
        level: 'info',
        format: combine(timestamp(), json()),
        transports: [new winston.transports.Console()],
      });
    logger.log(level, message);
}
module.exports = createLog;
