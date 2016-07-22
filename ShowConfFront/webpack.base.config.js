/**
 * Created by aresn on 16/7/5.
 */
var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
    // 入口
    entry: {
        main: './src/main',
        vendors: ['vue', 'vue-router', 'jquery', 'lodash']
    },
    // 输出
    output: {
        path: path.join(__dirname, './dist'),
        filename: '[name].js',
        chunkFilename: '[name].chunk.js',
        publicPath: '/dist/'
    },
    // 加载器
    module: {
        loaders: [
            { test: /\.vue$/, loader: 'vue' },
            { test: /\.js$/, loader: 'babel', exclude: /node_modules/ },
            { test: /\.css$/, loader: 'style!css!autoprefixer'},
            { test: /\.scss$/, loader: 'style!css!sass?sourceMap'},
            { test: /\.less$/, loader: 'style!css!less?sourceMap'},
            { test: /\.(gif|jpg|png|woff|svg|eot|ttf)\??.*$/, loader: 'url-loader?limit=8192'},
            { test: /\.(html|tpl)$/, loader: 'html-loader' },

            // **IMPORTANT** This is needed so that each bootstrap js file required by
            // bootstrap-webpack has access to the jQuery object
            { test: /bootstrap\/js\//, loader: 'imports?jQuery=jquery' },
            { test : "/jquery-*\/**\/*.js$", loader : "'imports?jQuery=jquery" },

            // Needed for the css-loader when [bootstrap-webpack](https://github.com/bline/bootstrap-webpack)
            // loads bootstrap's css.
            { test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,   loader: "url?limit=10000&minetype=application/font-woff" },
            { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,    loader: "url?limit=10000&minetype=application/octet-stream" },
            { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,    loader: "file" },
            { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,    loader: "url?limit=10000&minetype=image/svg+xml" }
        ]
    },
    vue: {
        loaders: {
            css: ExtractTextPlugin.extract(
                "style-loader",
                "css-loader?sourceMap",
                {
                    publicPath: "../dist/"
                }
            )
        }
    },
    // 转es5
    babel: {
        presets: ['es2015'],
        plugins: ['transform-runtime']
    },
    resolve: {
        // require时省略的扩展名，如：require('module') 不需要module.js
        extensions: ['', '.js', '.vue'],
        // 别名，可以直接使用别名来代表设定的路径以及其他
        alias: {
            filter: path.join(__dirname, './src/filters'),
            components: path.join(__dirname, './src/components'),
            'jquery-highlight': path.join(__dirname, './node_modules/jquery-highlight/jquery.highlight.js'),
            'jquery-jsonview': path.join(__dirname, './node_modules/jquery-jsonview/dist/jquery.jsonview.js'),
            'config': path.join(__dirname, './src/config.js'),
        }
    },
    plugins: [
        new webpack.ProvidePlugin({
          $: 'jquery',
          jQuery: 'jquery',
          'window.jQuery': 'jquery',
          _: 'lodash',
        }),

        new ExtractTextPlugin("[name].css",{ allChunks : true,resolve : ['modules'] }),
        new webpack.optimize.CommonsChunkPlugin('vendors', 'vendors.js')
    ]
};