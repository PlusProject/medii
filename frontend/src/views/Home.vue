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
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translate(0, 30px);
    }
    to {
      opacity: 1;
      transform: none;
    }
  }
  .fadeInUp-enter-active {
    animation: fadeInUp .8s;
  }
</style>