import plugin from 'tailwindcss/plugin';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,svelte,js,ts}'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#FBFBFD',
          100: '#F5F6FB',
          200: '#DFE2EE',
          300: '#BDC2D4',
          400: '#91949F',
          500: '#676C7E',
          600: '#474D62',
          700: '#363A48',
          800: '#272930',
          900: '#1A1B20'
        }
      }
    }
  },
  plugins: [
    plugin(function({ matchUtilities, theme }) {
      matchUtilities(
        {
          square: (value) => ({
            width: value,
            height: value
          })
        },
        { values: theme('spacing') }
      );
    })
  ]
};
