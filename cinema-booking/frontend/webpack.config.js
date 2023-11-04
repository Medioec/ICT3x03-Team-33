const path = require('path');
//using module bundler webpacker
module.exports = {
  mode: 'development',
  // Entry point of your application
  entry: './public/js/register.js', 
  // Output configuration
  output: {
    path: path.resolve(__dirname, 'dist'), // The output directory
    filename: 'bundle.js' // The name of the output file
  },
};