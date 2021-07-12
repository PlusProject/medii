<template>
  <div class="container">
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