// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'
import ViteComponents from 'unplugin-vue-components/vite'
import IconsResolver from 'unplugin-icons/resolver'
import { nodeResolve } from '@rollup/plugin-node-resolve';

export default defineNuxtConfig({
  // routeRules: {
  //   "/": {redirect: '/map/'}
  // },
  devtools: { enabled: false },
  experimental: {
    componentIslands: true
  },
  app: {
    head: {
      title: 'КК',
      link: [{ rel: 'icon', type: 'svg', href: '/img/icons/favicon.svg' }]
    },
  },
  css: [
    "primevue/resources/primevue.min.css",
    "primeicons/primeicons.css",
    "bootstrap/dist/css/bootstrap.min.css",
    'leaflet/dist/leaflet.css',
    '@fortawesome/fontawesome-svg-core/styles.css'
  ],
  modules: [
    '@unocss/nuxt',
    '@pinia/nuxt',
    'unplugin-icons/nuxt',
    '@vueuse/nuxt',
    'nuxt3-leaflet'
  ],
  nitro: {
    rollupConfig: {
      // external: ['ali-oss'],
      plugins: [
        nodeResolve({
          exportConditions: ['node'],
          extensions: ['.mjs', '.node'],
        }),
      ],
    },
    node: true,
  },
  vite: {
    plugins: [
      ViteComponents({
        resolvers: [
          IconsResolver({
            componentPrefix: ''
          })
        ],
        dts: true
      })
    ]
  },
  vue: {
    defineModel: true,
    propsDestructure: true
  },
  build: {
    transpile: process.env.NUXT_APP_DEBUG ? ['primevue'] : ['primevue', 'leaflet'],
  },
})
