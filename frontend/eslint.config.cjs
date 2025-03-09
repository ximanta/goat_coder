// eslint.config.cjs
const { FlatCompat } = require('@eslint/eslintrc');
const js = require('@eslint/js');

// Initialize FlatCompat with file paths
const compat = new FlatCompat();

module.exports = [
  js.configs.recommended,
  ...compat.config({
    extends: [
      'next',
      'next/core-web-vitals',
      'plugin:@typescript-eslint/recommended'
    ],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      ecmaFeatures: { jsx: true },
    },
    settings: {
      react: { version: 'detect' },
    },
    rules: {
      'react/react-in-jsx-scope': 'off',
    },
  }),
];