/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#445382',
        secondary: '#1A202C',
        tertiary: "#1A100C",
        gray: {
          100: '#F7FAFC',
          200: '#EDF2F7',
          300: '#E2E8F0',
          400: '#CBD5E0',
          500: '#A0AEC0',
          600: '#718096',
          700: '#4A5568',
          800: '#2D3748',
          900: '#1A202C',
        },
        // add any other custom colors here
      },
      minHeight: {
        '90vh': '90vh'
      }
    },
    screens: {
      'tablet': '640px',
      // => @media (min-width: 640px) { ... }

      'laptop': '1024px',
      // => @media (min-width: 1024px) { ... }

      'desktop': '1600px',
      // => @media (min-width: 1600px) { ... }

      '4k': '2500px',
      // => @media (min-width: 2000px) { ... }
    },

  },
  plugins: [],
}

