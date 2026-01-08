/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        quantum: {
          primary: '#6366f1',
          secondary: '#8b5cf6',
          accent: '#06b6d4',
          dark: '#0f172a',
          darker: '#020617',
          light: '#e2e8f0',
        },
        board: {
          light: '#f0d9b5',
          dark: '#b58863',
          highlight: '#aaa23a',
          selected: '#829769',
          possible: 'rgba(99, 102, 241, 0.4)',
          superposed: 'rgba(139, 92, 246, 0.3)',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'quantum-glow': 'quantumGlow 2s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'superposition': 'superposition 1.5s ease-in-out infinite',
      },
      keyframes: {
        quantumGlow: {
          '0%, 100%': {
            boxShadow: '0 0 5px rgba(139, 92, 246, 0.5), 0 0 20px rgba(139, 92, 246, 0.3)',
          },
          '50%': {
            boxShadow: '0 0 20px rgba(139, 92, 246, 0.8), 0 0 40px rgba(139, 92, 246, 0.5)',
          },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        superposition: {
          '0%, 100%': { opacity: '0.5', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.05)' },
        },
      },
      backgroundImage: {
        'quantum-gradient': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%)',
        'dark-gradient': 'linear-gradient(180deg, #0f172a 0%, #020617 100%)',
      }
    },
  },
  plugins: [],
}
