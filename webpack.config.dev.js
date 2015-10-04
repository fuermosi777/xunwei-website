/* global __dirname */
var webpack = require('webpack');

module.exports = {
    entry: [
        'webpack/hot/only-dev-server',
        './src/entry.jsx'
    ],
    output: {
        path: __dirname + '/build',
        publicPath: 'http://localhost:8080/',
        filename: 'bundle.js'
    },
    module: {
        loaders: [{
            test: /\.jsx$/,
            loaders: ['react-hot', 'babel'],
            exclude: /node_modules/
        }, {
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel'
        }, {
            test: /\.less$/,
            loader: 'style!css!less'
        }, {
            test: /\.(css)$/,
            loader: 'style!css'
        }, {
            test: /\.(png|jpg|jpeg|svg)$/,
            loader: 'file'
        }]
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin()
    ]
};
