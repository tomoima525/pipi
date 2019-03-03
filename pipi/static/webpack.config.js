// eslint-disable-next-line @typescript-eslint/no-var-requires
const path = require('path');

module.exports = {
  entry: './src/index.tsx',
  output: {
    filename: 'bundle-2.js',
    path: path.resolve(__dirname, './dist'),
    publicPath: '/dist/'
  },
  resolve: {
    extensions: ['.js', '.jsx', '.ts', '.tsx', '.css']
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: [{ loader: 'babel-loader' }, { loader: 'ts-loader' }],
        exclude: /node_modules/
      },

      // handle js file with babel
      { test: /\.js$/, loader: 'babel-loader' },

      {
        enforce: 'pre',
        test: /\.(js|tsx|ts)$/,
        loader: 'eslint-loader',
        exclude: /node_modules/,
        options: {
          failOnError: true
        }
      }
    ]
  },
  devServer: {
    port: 8080,
    historyApiFallback: true
  },
  cache: false
};
