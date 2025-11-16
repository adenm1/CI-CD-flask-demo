/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#1CB5A3',
        'primary-hover': '#169A8B',
        secondary: '#1769AA',
        'secondary-hover': '#125783',
        accent: '#F5A623',
        background: '#F9FAFB',
        card: '#FFFFFF',
        tablegrey: '#E5E7EB',
        heading: '#374151',
        body: '#111827',
        success: '#2ECC71',
        error: '#E63946'
      },
      boxShadow: {
        soft: '0 10px 30px rgba(17, 24, 39, 0.08)',
        inset: 'inset 0 1px 0 rgba(255, 255, 255, 0.06)'
      },
      borderRadius: {
        xl: '1.25rem',
        // Apple-style continuous corner radius (approximation)
        'apple-sm': '0.75rem', // 12px - small elements
        'apple-md': '1rem',     // 16px - medium elements
        'apple-lg': '1.25rem',  // 20px - large elements
        'apple-xl': '1.5rem',   // 24px - extra large
        'apple-2xl': '2rem'     // 32px - cards and containers
      }
    }
  },
  plugins: [require('@tailwindcss/forms')]
};
