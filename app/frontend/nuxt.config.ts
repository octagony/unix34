import Aura from '@primeuix/themes/aura';

export default defineNuxtConfig({
  modules: ['@primevue/nuxt-module', '@nuxt/fonts', '@nuxtjs/tailwindcss'],
  typescript: {
    typeCheck: "build",
  },
  runtimeConfig: {
    public: {
      PRIMEUI_LICENSE: process.env.APP_FRONTEND_PRIMEUI_LICENSE,
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
