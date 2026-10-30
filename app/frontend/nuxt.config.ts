import Aura from '@primeuix/themes/aura';
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  modules: ['@primevue/nuxt-module', '@nuxt/fonts', '@nuxtjs/color-mode', '@nuxt/ui'],
  typescript: {
    typeCheck: "build",
  },
  runtimeConfig: {
    public: {
      PRIMEUI_LICENSE: process.env.APP_FRONTEND_PRIMEUI_LICENSE,
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL
    },
  },
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  primevue: {
    options: {
      theme: {
        preset: Aura,
        options: {
          darkModeSelector: 'system',
        },
      },
    },
  },

  alias: {
    "@": "/<rootDir>/app",
  },

  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [
      tailwindcss(),
    ],
  },

  fonts: {
    families: [
      { name: 'Fira Code', provider: 'google', global: true }
    ]
  },

  app: {
    head: {
      title: 'Unix34',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Linux of a different level' },
      ],
    },
  },
});
