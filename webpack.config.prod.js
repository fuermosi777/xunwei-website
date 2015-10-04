/* global __dirname */
var webpack = require('webpack');

module.exports = {
    entry: [
        './src/entry.jsx'
    ],
    output: {
        path: __dirname + '/build/build',
        publicPath: 'https://s3-ap-southeast-1.amazonaws.com/xun-wei/build/',
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
        new webpack.NoErrorsPlugin()
    ]
};
