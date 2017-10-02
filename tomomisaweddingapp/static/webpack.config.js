const webpack = require('webpack');
const config = {
    entry:  __dirname + '/js/index.js',
    output: {
        path: __dirname + '/dist',
        publicPath: '/dist/',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    cache: false,
};
module.exports = config;
