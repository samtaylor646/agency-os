/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primitive Tokens
        'atlassian-blue': {
          100: '#E6F0FF',
          300: '#4C9AFF',
          500: '#0052CC',
          700: '#003E99',
          900: '#002966',
        },
        'atlassian-gray': {
          50: '#F4F5F7',
          100: '#EBECF0',
          200: '#DFE1E6',
          300: '#C1C7D0',
          400: '#97A0AF',
          500: '#7A869A',
          600: '#5E6C84',
          700: '#42526E',
          800: '#172B4D',
          900: '#091E42',
        },
        'atlassian-red': { 500: '#DE350B' },
        'atlassian-green': { 500: '#00875A' },
        'atlassian-yellow': { 500: '#FF991F' },
        
        // Semantic Tokens - Backgrounds
        'bg-default': '#FFFFFF',
        'bg-subtle': '#F4F5F7',
        'bg-inverse': '#172B4D',
        'bg-primary': '#0052CC',
        'bg-primary-hover': '#003E99',
        
        // Semantic Tokens - Text
        'text-default': '#172B4D',
        'text-subtle': '#5E6C84',
        'text-muted': '#7A869A',
        'text-inverse': '#FFFFFF',
        'text-brand': '#0052CC',
        
        // Semantic Tokens - Borders
        'border-default': '#DFE1E6',
        'border-focused': '#4C9AFF',
        
        // Semantic Tokens - Interactive
        'action-primary': '#0052CC',
        'action-primary-hover': '#003E99',
        'action-primary-active': '#002966',
        'action-secondary': '#EBECF0',
        'action-secondary-hover': '#DFE1E6',
        'action-secondary-active': '#E6F0FF',
        
        // Semantic Tokens - Feedback
        'feedback-error': '#DE350B',
        'feedback-success': '#00875A',
        'feedback-warning': '#FF991F',
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        'atlassian-sm': '0 1px 1px rgba(9, 30, 66, 0.25), 0 0 1px rgba(9, 30, 66, 0.31)',
        'atlassian-md': '0 4px 8px -2px rgba(9, 30, 66, 0.25), 0 0 1px rgba(9, 30, 66, 0.31)',
      },
      transitionTimingFunction: {
        'snappy': 'cubic-bezier(0.4, 0, 0.2, 1)',
        'smooth': 'cubic-bezier(0.4, 0, 0.2, 1)',
      },
      transitionDuration: {
        'snappy': '200ms',
        'smooth': '300ms',
      }
    },
  },
  plugins: [],
}