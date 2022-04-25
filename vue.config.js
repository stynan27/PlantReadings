const { defineConfig } = require('@vue/cli-service')
const { VuetifyLoaderPlugin } = require('vuetify-loader')

module.exports = defineConfig({
  transpileDependencies: [
    'vuetify'
  ],

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  },
})
