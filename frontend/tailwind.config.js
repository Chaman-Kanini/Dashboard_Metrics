/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        kanini: {
          blue: '#0088CE',
          cyan: '#00A8E4',
          lime: '#BDDA57',
          lightCyan: '#68CEF2',
        },
        primary: {
          50: '#f0fce5',
          100: '#ddf7c2',
          200: '#c9f29b',
          300: '#b5ed74',
          400: '#a5e857',
          500: '#BDDA57',
          600: '#a8c44d',
          700: '#8fa942',
          800: '#768e37',
          900: '#5d6e2c',
        },
        secondary: {
          50: '#e0f5ff',
          100: '#b3e5ff',
          200: '#80d4ff',
          300: '#4dc3ff',
          400: '#26b7ff',
          500: '#00A8E4',
          600: '#0088CE',
          700: '#0066a1',
          800: '#004d7a',
          900: '#003353',
        },
      },
    },
  },
  plugins: [],
}
