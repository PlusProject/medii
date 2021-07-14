<template>
  <div class="container">
    <b-card>
      <div>
        <SearchForm />
      </div>
      <div class="content-app">
        <transition
          name="fadeInUp"
          mode="out-in"
        >
          <router-view />
        </transition>
      </div>
    </b-card>
  </div>
</template>
<script>
import SearchForm from './SearchForm.vue'

export default {
  name: 'Home',
  components: {
      SearchForm
  }
}
</script>

<style>
  .content-app {
    margin:0;
  }
</style>