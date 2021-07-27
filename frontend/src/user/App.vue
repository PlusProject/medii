<template>
  <v-app id="app" style="height: 100%">


    <v-app-bar
      app
      color="#F3F5FF"
      fixed
      >
      <v-app-bar-nav-icon/>
      <v-toolbar-title>
        <a class="route-style" href="/">MEDIAI +</a>
      </v-toolbar-title>
    </v-app-bar>

    <!-- Sizes your content based upon application components -->
    <v-main>
      <router-view></router-view>
      <!-- Provides the application the proper gutter -->
      <!-- <v-container fluid> -->

        <!-- If using vue-router -->
        
      <!-- </v-container> -->
    </v-main>

    <!-- <v-footer app>

    </v-footer> -->
  </v-app>
</template>

<script>
export default {
  name: 'App',
  components: {},
  created () {
    this.$store.dispatch('initAutocomplete')
  }
}
</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #F3F5FF;
}
.route-style {
  &:link { color: #2c3e50; text-decoration: none;}
  &:visited { color: #2c3e50; text-decoration: none;}
  &:hover { color: #2c3e50; text-decoration: none;}
}
/* div > .v-application--wrap {
  min-height: 908px;
} */
</style>
