// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  extends: ['@blakvghost/ui-pro'],
  modules: [
    // '@vite-pwa/nuxt',
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/ui',
    '@vueuse/nuxt',
    '@nuxtjs/i18n',
    '@nuxtjs/sitemap'
  ],
  ssr: false,

  devtools: {
    enabled: false
  },

  site: {
    enabled: true,
    urls: ['/'],
    name: 'Садоводы',
    autoI18n: 'prefix_except_default',
    debug: true
  },

  colorMode: {
    disableTransition: false
  },

  ui: {
    safelistColors: ['primary', 'red', 'orange', 'green']
  },

  routeRules: {
    // Temporary workaround for prerender regression. see https://github.com/nuxt/nuxt/issues/27490
    '/': { prerender: true }
  },

  future: {
    compatibilityVersion: 4
  },

  compatibilityDate: '2024-07-11',

  typescript: {
    strict: false
  },

  eslint: {
    config: {
      stylistic: {
        commaDangle: 'never',
        braceStyle: '1tbs'
      }
    }
  },

  i18n: {
    lazy: true,
    langDir: 'locales',
    strategy: 'prefix_except_default',
    locales: [
      { code: 'ru', language: 'ru', name: 'Русский', file: 'ru.json', cache: false },
      { code: 'uz', language: 'uz', name: 'O\'zbek', file: 'uz.json', cache: false }
    ],
    defaultLocale: 'ru'
  },
  pwa: {
    manifest: {
      name: 'Садоводы',
      short_name: 'Садоводы',
      description: 'Садоводы',
      theme_color: '#00D8A5',
      icons: [
        {
          src: '/icons/logo64.png',
          sizes: '64x64',
          type: 'image/png'
        },
        {
          src: '/icons/logo144.png',
          sizes: '144x144',
          type: 'image/png'
        },
        {
          src: '/icons/logo192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/icons/logo512.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    },
    workbox: {
      navigateFallback: '/'
    },
    // injectManifest: {
    //     globPatterns: ['**/*.{js,css,html,png,svg,ico}'],
    // },
    client: {
      installPrompt: true,
      // you don't need to include this: only for testing purposes
      // if enabling periodic sync for update use 1 hour or so (periodicSyncForUpdates: 3600)
      periodicSyncForUpdates: 20
    },
    devOptions: {
      enabled: true,
      // suppressWarnings: true,
      // navigateFallback: '/',
      // navigateFallbackAllowlist: [/^\/$/],
      type: 'module'
    }
  }
})
