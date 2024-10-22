/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '/home/skye/FRASystem/FaceCheckIn/FaceCheckInApp/templates/**.html', // Include all HTML files
  ],
  theme: {
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },
    variants: {
      textAlign: ['responsive'], // Ensure this is present
    },
    extend: {
      // Add any customizations here
    },
  },
  plugins: [],
}
