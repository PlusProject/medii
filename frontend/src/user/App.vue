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
      <div
        v-show="this.$route.name !== 'home'"
        style="z-index: 2; position: relative; height: 52px; width: 625px;"
      >
        <v-toolbar
          class="toolbar-sheet rounded-pill"
          dense
          floating
          color="white"
          elevation="0"
          height="50"
          outlined
          rounded
        >
          <!-- <v-text-field
            class="toobar-textfield"
            placeholder="질병명을 입력하세요(심장판막, 심근경색, 순환계통 / I00, C00, ...)"
            solo
            flat
            hide-details
            prepend-icon="mdi-magnify"
            single-line
            :style="{ width: '525px' }"
            :disabled="showSearchDetails"
            v-model="searchByDisease"
            autocomplete="off"
            @keydown.enter="showSearchResults()"
          ></v-text-field> -->
          <v-combobox
            class="toobar-textfield"
            placeholder="질병명을 입력하세요(심장판막, 심근경색, 순환계통 / I00, C00, ...)"
            solo
            flat
            hide-details
            prepend-icon="mdi-magnify"
            single-line
            :style="{ width: '525px' }"
            :menu-props="{ 'max-width': 500 }"
            :disabled="showSearchDetails"
            v-model="searchByDisease"
            :items="$store.getters.rareDiseaseList"
            autocomplete="off"
            @keydown.enter="searchWithClick()"
            ref="diseaseCombobox"
          />
          <!-- <v-combobox
            v-model="detailSearch.disease"
            :items="rareDiseaseList"
            label="질병"
            autocomplete="off"
            placeholder="심장판막, 심근경색, 순환계통 / I00, C00, ..."
            @keyup.enter="showSearchResults()"
            ref="diseaseCombobox"
          /> -->
          <v-btn
            icon
            ref='showDetails'
            @click="showSearchDetails = !showSearchDetails"
          >
            <v-icon> mdi-dots-vertical </v-icon>
          </v-btn>
        </v-toolbar>
        <v-expand-transition>
          <SearchDetail
            v-show="showSearchDetails"
            z-index='3'
            width='600px'
            v-on:search='showSearchDetailsTrigger()'
          />
        </v-expand-transition>
        <v-spacer></v-spacer>
      </div>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import SearchDetail from './components/SearchDetail.vue'
import { mapMutations, mapGetters } from 'vuex'

export default {
  name: 'App',
  components: {
    SearchDetail
  },
  created () {
    this.$store.dispatch('initAutocomplete')
  },
  data () {
    return {
      searchByDisease: '',
      showSearchDetails: false,
      showInfoPage: false,
      loadInfoPage: false,
    }
  },
  methods: {
    ...mapMutations([ 'setDiseaseQuery', 'clearSearchQuery' ]),
    searchWithClick () {
      this.$refs["diseaseCombobox"].blur()
      this.$nextTick(() => {
          this.showSearchResults()
      })
    },
    showSearchResults () {
      // this.showSearchDetails = !this.showSearchDetails
      this.clearSearchQuery()
      this.setDiseaseQuery(this.searchByDisease)
      this.searchByDisease = ''
      if (this.$route.name !== 'DoctorList') {
        this.$router.push({ name: 'DoctorList' })
      }
    },
    showSearchDetailsTrigger () {
      this.searchByDisease = ''
      this.$refs.showDetails.$el.click()
    }
  },
  computed: {
    ...mapGetters([ 'rareDiseaseList '])
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
</style>
