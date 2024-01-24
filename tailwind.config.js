/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './catalog/templates/**/*.html',
    ],
  theme: {
    extend: {
      colors: {
        'light-purple': '#9191b8',
        'dark-purple': '#4B3F72',
      },
      backgroundImage: theme => ({
        'gradient-to-r': 'linear-gradient(to right, var(--tw-gradient-stops))',
        'gradient-r-light-purple-dark-purple': 'linear-gradient(to right, #D1D1E9, #4B3F72)',
        'gradient-r-dark-purple-light-purple': 'linear-gradient(to right, #4B3F72, #D1D1E9)',
      })
    },
  },
  variants: {
    extend: {
      backgroundImage: ['hover', 'focus'],
    },
  },
    plugins: [],
}

