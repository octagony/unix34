import type { Config } from 'tailwindcss'

export default <Config>{
  content: [
    './components/**/*.{vue,js,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
    './error.vue'
  ],
  theme: {
    extend: {
      colors: {
        nixos: '#5277C1',
        ubuntu: '#E95420',
        mangowm: '#FF6B35',
        arch: '#1793D1',
        fedora: '#294172',
        debian: '#A80030',
        kde: '#1D99F3',
        gnome: '#4A86CF',
        hyprland: '#75D5FF',
        sway: '#93A8D0',
        i3: '#5294E2',
        wayland: '#FFBC75',
      }
    },
  },
  plugins: [],
}
