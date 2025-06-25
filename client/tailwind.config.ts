// tailwind.config.mjs
export default {
  darkMode: 'class',

  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  
  theme: {
    extend: {
       colors: {
        // Define custom color palettes for light and dark mode.
        background: {
          light: '#ffffff',         // light background color
          dark: '#1F2937',          // dark background color (e.g., a dark gray/blue)
        },
        text: {
          light: '#111827',         // dark text color for light mode
          dark: '#F3F4F6',          // light text color for dark mode
        },
        // You can add more custom colors needed for your design:
        primary: {
          light: '#2563EB',         // blue for light mode
          dark: '#3B82F6',          // lighter blue for dark mode
        },
      },
    },
  },
  plugins: [],


}