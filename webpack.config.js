const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
// var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    // mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
    // devtool: process.env.NODE_ENV === 'production' ? false : 'source-map',
    // watch: process.env.NODE_ENV === 'production' ? false : true,

    mode: "development",
    devtool: false,
    watch: false,

    entry: './static/static_src/js/index.js', // Your entry point for JS/CSS
    output: {
        filename: 'bundle.js', // Output JS file
        path: path.resolve(__dirname, 'static/static_build/'), // Output directory
        clean: true,  // Cleans old files
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'postcss-loader' // Use PostCSS for Tailwind
                ],
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif|webp)$/i,
                type: 'asset/resource',
            },
            {
                test: /\.(woff|woff2|eot|ttf)$/i,
                type: 'asset/resource',
                generator: {
                    filename: 'fonts/[name][ext][query][contenthash:8]', // Add contenthash
                },
            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'style.css', // Output CSS file
        }),
        // Emergency comment this for reload webpack every seccond
        // new BundleTracker({ 
        //     path: path.resolve(__dirname, './static/static_build/'),
        //     filename: 'webpack-stats.json' 
        // })
    ],
};