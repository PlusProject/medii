<template>
  <v-app id="app" style="height: 100%">


    <v-app-bar
      app
      color="#F3F5FF"
      fixed
      >
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </v-app-bar>

    <!-- Sizes your content based upon application components -->
    <v-main>

      <!-- Provides the application the proper gutter -->
      <v-container fluid>

        <!-- If using vue-router -->
        <router-view></router-view>
      </v-container>
    </v-main>

    <!-- <v-footer app>

    </v-footer> -->
  </v-app>
</template>

<script>
export default {
  name: 'App',
  components: {}
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: #F3F5FF;
}
/* div > .v-application--wrap {
  min-height: 908px;
} */
</style>
