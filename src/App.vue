<template>
  <v-app :theme="theme">
    <v-main>
      <PlantData />
    </v-main>
  </v-app>
</template>

<script>
  import PlantData from './components/PlantData.vue'

  export default {
    name: 'App',
    components: {
      PlantData,
    },
    computed: {
      theme() {
        return 'dark';
        // return (this.$vuetify.defaultTheme.dark) ? 'dark' : 'light'
      }
    },
    data: () => ({
      //
    }),
  }
</script>
