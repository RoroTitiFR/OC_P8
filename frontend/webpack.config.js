const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const FixStyleOnlyEntriesPlugin = require("webpack-fix-style-only-entries");

module.exports = {
    mode: "production",
    entry: {
        "js/app": "./js/app.js",
        "js/substitutes": "./js/substitutes.js",
        "css/animate": "./scss/animate.scss",
        "css/bulma": "./scss/bulma.scss",
        "css/mini-tailwind": "./scss/tailwind.scss"
    },
    devtool: 'source-map',
    plugins: [
        new FixStyleOnlyEntriesPlugin(),
        new MiniCssExtractPlugin()
    ],
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