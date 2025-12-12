/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: "#3b82f6", // Blue 500
                secondary: "#6366f1", // Indigo 500
                dark: "#0f172a", // Slate 900
                darker: "#020617", // Slate 950
                surface: "#1e293b", // Slate 800
                accent: "#f43f5e", // Rose 500
                success: "#22c55e", // Green 500
                warning: "#eab308", // Yellow 500
                danger: "#ef4444", // Red 500
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            },
            animation: {
                'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
            }
        },
    },
    plugins: [],
}
