<template>
  <div class="app-container">
    <v-container
      fluid
      :class="showInfoPage ? 'search-container' + ' transition-move' : 'search-container'" 
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
          :disabled="showSearchDetails"
          v-model="elasticSearch"
          @keydown.enter="showSearchResults()"
        ></v-text-field>
        <!-- <v-btn
          elevation="8"
          large
          rounded
          @click="showSearchDetails = !showSearchDetails"
          color="#93A2FF"
          :disabled="!showInfoPage"
          :style="{ 'color': '#F3F5FF', 'margin-left': '80px', 'height': '50px'}"
          :class="showInfoPage ? 'side-btn' + ' fade-in' : 'side-btn'"
        >
          상세검색
          <v-icon right>
            mdi-filter-variant
          </v-icon>
        </v-btn> -->
        <v-btn
          icon 
          v-if="showInfoPage"
          @click="showSearchDetails = !showSearchDetails"
        >
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-toolbar>
        <v-expand-transition>
          <v-sheet
            fluid
            v-show="showSearchDetails && showInfoPage"
            max-width="800px"
            overflow-y="auto"
            class="mx-auto rounded-xl"
            style="margin-top: 20px; background-color: #fff"
            elevation="12"
          >
            <v-form>
              <v-container>
                <v-row>
                  <v-col cols="6">
                    <v-col cols="12">
                      <v-text-field
                        label="이름"
                        v-model="detailSearch.name_kor"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12">
                      <v-text-field
                        label="병원"
                        v-model="detailSearch.belong"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>
                  </v-col>

                  <v-col cols="6">
                    <v-col cols="12">
                      <v-text-field
                        label="진료분야"
                        v-model="detailSearch.major"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12">
                      <v-text-field
                        label="질병"
                        v-model="detailSearch.disease"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-sheet>
        </v-expand-transition>
      

      <div class="btn-search-detail" v-if="!showInfoPage">
        <v-btn
          elevation="8"
          large
          rounded
          @click="showSearchDetailsTrigger()"
          color="#93A2FF"
          :style="{ 'color': '#F3F5FF' }"
        >
          상세검색
          <v-icon right>
            mdi-filter-variant
          </v-icon>
        </v-btn>
        <v-expand-transition>
          <v-sheet fluid
            v-show="showSearchDetails"
            max-width="800px"
            overflow-y="auto"
            class="mx-auto rounded-xl"
            style="margin-top: 20px; background-color: #fff"
            elevation="12"
          >
            <v-form>
              <v-container>
                <v-row>
                  <v-col cols="6">
                    <v-col cols="12">
                      <v-text-field
                        label="이름"
                        v-model="detailSearch.name_kor"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12">
                      <v-text-field
                        label="병원"
                        v-model="detailSearch.belong"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>
                  </v-col>

                  <v-col cols="6">
                    <v-col cols="12">
                      <v-text-field
                        label="진료분야"
                        v-model="detailSearch.major"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>

                    <v-col cols="12">
                      <v-text-field
                        label="질병"
                        v-model="detailSearch.disease"
                        @keydown.enter="showSearchResults()"
                      ></v-text-field>
                    </v-col>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
          </v-sheet>
        </v-expand-transition>
      </div>

      <div class="btn-show-info" v-if="!showInfoPage">
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
      </div>
    </v-container>
    <div style="margin-top: 20vh">
      <transition
        name="fadeInUp"
        mode="out-in"
      >
        <page-2 v-if="loadInfoPage" class="infopage"/>
      </transition>
    </div>
  </div>
</template>

<script>
import Page2 from './Page2.vue';

export default {
  name: 'Home',
  components: {
    Page2
  },
  data () {
    return {
      elasticSearch: '',
      detailSearch: {
        name_kor: '',
        belong: '',
        major: '',
        disease: ''
      },
      showSearchDetails: false,
      showInfoPage: false,
      loadInfoPage: false,
      styles: {
        toobarWidth: 600,
        toolbarTop: 20
      }
    }
  },
  methods: {
    showInfoPageTrigger () {
      this.showInfoPage = true;
      setTimeout(() => {
        this.loadInfoPage = true;
      }, 1800)
    },
    showSearchResults () {
      this.$router.push({ name: 'page3', params: { elasticSearch: this.elasticSearch, detailSearch: this.detailSearch }})
    },
    showSearchDetailsTrigger () {
      this.elasticSearch = ''
      this.showSearchDetails = !this.showSearchDetails
    }
  },
  computed: {
    toolbarPos () {
      return {
        top: this.styles.toolbarTop + 'vh',
        'justify-content': 'center',
        'z-index': 2
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
    position: fixed;
    bottom: 32px;
    left: -webkit-calc(50% - 22px);
  }
  .infopage {
    position: fixed;
    bottom: 70vh;
  }
  .transition-move {
    transform: translate(0, -24vh);
    transition-property: transform;
    transition-duration: 1.8s;
  }
  .logo {
    height: 14vh;
    font-size: 80px;
  }
  .side-btn {
    opacity: 0;
  }
  .fade-out {
    transition: opacity 0;
    transition: all 1.8s;
    height: 8vh;
    opacity: 0;
    font-size: 0px;
  }
  .fade-in {
    transition: opacity 0;
    transition: all 1.8s;
    opacity: 1;
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
