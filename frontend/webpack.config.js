const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserJSPlugin = require('terser-webpack-plugin');
const FixStyleOnlyEntriesPlugin = require("webpack-fix-style-only-entries");

module.exports = {
    mode: "production",
    entry: {
        "js/app": "./js/app.js",
        "css/animate": "./scss/animate.scss",
        "css/bulma": "./scss/bulma.scss",
        "css/mini-tailwind": "./scss/tailwind.scss"
    },
    devtool: 'source-map',
    plugins: [
        new FixStyleOnlyEntriesPlugin(),
        new MiniCssExtractPlugin()
    ],
    optimization: {
        minimizer: [
            new TerserJSPlugin({}),
            new OptimizeCSSAssetsPlugin({
                cssProcessorOptions: {
                    map: {
                        inline: false // set to false if you want CSS source maps
                    }
                }
            })
        ],
    },
    module: {
        rules: [
            {
                test: /\.scss$/i,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: 'postcss-loader',
                        options: {
                            plugins: [
                                require('postcss-import'),
                                require("tailwindcss"),
                                require("postcss-safe-important")({
                                    paths: p => p.indexOf("tailwind") === -1
                                }),
                                require("autoprefixer")
                            ],
                            sourceMap: true
                        },
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true
                        }
                    }
                ]
            },
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"]
                    }
                }
            }
        ],
    },
    output: {
        path: path.resolve(__dirname, "..", "assets")
    },
    externals: {
        jquery: 'jQuery'
    }
};