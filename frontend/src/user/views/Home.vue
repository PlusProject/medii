<template>
  <div class="app-container">
    <v-container 
      :class="showInfoPage ? 'search-container' + ' transition-move' : 'search-container'" 
      fluid 
      :style="toolbarPos"
    >
      <p :class="showInfoPage ? 'logo' + ' fade-out' : 'logo'">
        MEDIAI +
      </p>
      <v-toolbar
        dense
        floating
        class="toolbar-sheet rounded-pill"
        color="white"
        elevation="12"
        height="50"
        outlined
        rounded
        :width="styles.toobarWidth"
      >
        <v-text-field
          solo
          flat
          hide-details
          prepend-icon="mdi-magnify"
          single-line
          :style="{ width: styles.toobarWidth - 80 + 'px' }"
          v-model="search"
        ></v-text-field>
      </v-toolbar>

      <p class="btn-search-detail" v-if="!showInfoPage">
        <v-btn
          elevation="8"
          large
          rounded
          @click="showInfoPage = true"
          color="#93A2FF"
          :style="{ 'color': '#F3F5FF' }"
        >
          상세검색
          <v-icon right>
            mdi-filter-variant
          </v-icon>
        </v-btn>
      </p>

      <p class="btn-show-info" v-if="!showInfoPage">
        <v-btn
          color="primary"
          elevation="8"
          icon
          large
          @click="showInfoPageTrigger()"
        >
          <v-icon>
            mdi-vuetify
          </v-icon>
        </v-btn>
      </p>
    </v-container>
    <div style="margin-top: 20vh">
      <transition
        name="fadeInUp"
        mode="out-in"
      >
        <router-view/>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {
      search: '',
      showInfoPage: false,
      styles: {
        toobarWidth: 600,
        toolbarTop: 30
      }
    }
  },
  methods: {
    showInfoPageTrigger () {
      this.showInfoPage = true;
      setTimeout(() => {
        if (this.$route.name != 'page2'){
          this.$router.push('page2')
        }
      }, 2000)
    }
  },
  computed: {
    toolbarPos () {
      return {
        top: this.styles.toolbarTop + 'vh',
        'justify-content': 'center'
        // left: '-webkit-calc(50% - ' + this.styles.sheetWidth/2 + 'px)' 
      }
    }
  }
}
</script>

<style lang="scss" scoped>
  .search-container {
    position: relative;
  }
  .btn-search-detail {
    margin-top: 32px;
  }
  .btn-show-info {
    margin-top: 200px;
  }
  .transition-move {
    transform: translate(-5%, -300px);
    transition-property: transform;
    transition-duration: 3s;
  }
  .logo {
    height: 10vh;
    font-size: 80px;
  }
  .fade-out {
    transition: opacity 0;
    transition: all 2s;
    height: 2vh;
    opacity: 0;
    font-size: 0px;
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
