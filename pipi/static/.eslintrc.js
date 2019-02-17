module.exports = {
  extends: ['airbnb', 'prettier', 'plugin:prettier/recommended', 'prettier/@typescript-eslint'],
  plugins: ['@typescript-eslint/tslint', 'prettier'],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    sourceType: 'module',
    project: './tsconfig.json'
  },
  rules: {
    '@typescript-eslint/tslint/config': [
      'warn',
      {
        lintFile: './tslint.json'
      }
    ],
    'react/jsx-filename-extension': [1, { extensions: ['.js', '.jsx', '.tsx'] }],
    'import/prefer-default-export': false
  },
  settings: {
    'import/resolver': {
      node: {
        extensions: ['.ts', '.tsx', '.js', '.jsx', '.json']
      }
    }
  },
  env: {
    browser: true,
    node: true
  }
};
