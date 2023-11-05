const path = require('path');

module.exports = {
  mode: 'development',
  entry: './public/js/register.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  
  devtool: 'source-map', // This will generate a separate source map file instead of using eval, which is less safe.
};
