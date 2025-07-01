module.exports = {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(ts|tsx)$': 'babel-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],
  setupFilesAfterEnv: ['@testing-library/jest-dom'],
  transformIgnorePatterns: [
    '/node_modules/(?!(?:@fullcalendar)/)',
  ],
  moduleNameMapper: {
    '^@fullcalendar/react$': '<rootDir>/__mocks__/fullcalendar-react.js',
    '^@fullcalendar/(daygrid|timegrid|interaction)$': '<rootDir>/__mocks__/fullcalendar-plugin.js',
  },
};
