<template>
  <div class="app-container">
    <v-container
      fluid
      :class="showInfoPage ? 'search-container' + ' transition-move' : 'search-container'" 
    >
      <p :class="showInfoPage ? 'logo' + ' fade-out' : 'logo'">
        MEDIAI +
      </p>
      <v-toolbar
        class="toolbar-sheet rounded-pill"
        dense
        floating
        color="white"
        elevation="12"
        height="50"
        outlined
        rounded
        :width="styles.toobarWidth"
      >
        <v-text-field
          class="toobar-textfield"
          placeholder="질병명을 입력하세요(고혈압, 심근경색, 순환계통 / I00, C00, ...)"
          solo
          flat
          hide-details
          prepend-icon="mdi-magnify"
          single-line
          :style="{ width: styles.toobarWidth - 80 + 'px' }"
          :disabled="showSearchDetails"
          v-model="searchByDisease"
          autocomplete="off"
          @keydown.enter="showSearchResults()"
        ></v-text-field>
        <!-- <v-combobox
            class="toobar-textfield"
            placeholder="질병명을 입력하세요(고혈압, 심근경색, 순환계통 / I00, C00, ...)"
            solo
            flat
            hide-details
            prepend-icon="mdi-magnify"
            single-line
            :style="{ width: styles.toobarWidth - 40 + 'px' }"
            :disabled="showSearchDetails"
            v-model="searchByDisease"
            autocomplete="off"
            @keydown.enter="searchWithClick()"
            :items="showRareDisease ? $store.getters.rareDiseaseList : $store.getters.diseaseList"
            :menu-props="{ 'max-width': styles.toobarWidth - 80 + 'px' }"
            ref="diseaseCombobox"
          /> -->
        <v-btn
          icon 
          v-if="showInfoPage"
          @click="showSearchDetails = !showSearchDetails"
        >
          <v-icon> mdi-dots-vertical </v-icon>
        </v-btn>
      </v-toolbar>
      <v-expand-transition>
        <SearchDetail
          v-show="showSearchDetails && showInfoPage"
          width="800px"
        />
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
          <v-icon right> mdi-filter-variant </v-icon>
        </v-btn>
        <v-expand-transition>
          <SearchDetail
            v-show="showSearchDetails"
            width="800px"
          />
        </v-expand-transition>
      </div>

      <div class="btn-show-info" v-if="false">
        <v-btn
          color="primary"
          elevation="8"
          icon
          large
          @click="showInfoPageTrigger()"
        >
          <v-icon>mdi-chevron-double-down</v-icon>
        </v-btn>
      </div>
    </v-container>
    <div style="margin-top: 20vh">
      <transition
        name="fadeInUp"
        mode="out-in"
      >
        <database-info v-if="loadInfoPage" class="infopage"/>
      </transition>
    </div>
  </div>
</template>

<script>
import DatabaseInfo from '../components/DatabaseInfo.vue'
import SearchDetail from '../components/SearchDetail.vue'
import { mapMutations } from 'vuex'

export default {
  name: 'Home',
  components: {
    SearchDetail,
    DatabaseInfo
  },
  data () {
    return {
      searchByDisease: '',
      showSearchDetails: false,
      showInfoPage: false,
      loadInfoPage: false,
      styles: {
        toobarWidth: 601
      },
      showRareDisease: false,
      showClinicalTrialsPage: false
    }
  },
  methods: {
    ...mapMutations([ 'setDiseaseQuery', 'clearSearchQuery' ]),
    showInfoPageTrigger () {
      this.showSearchDetails = false
      this.showInfoPage = true
      setTimeout(() => {
        this.loadInfoPage = true
      }, 1800)
    },
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
      if (this.$route.name !== 'DoctorList') {
        this.$router.push({ name: 'DoctorList' })
      }
    },
    showSearchDetailsTrigger () {
      this.searchByDisease = ''
      this.showSearchDetails = !this.showSearchDetails
    }
  }
}
</script>

<style lang="scss" scoped>
  $toolbar-top-pos: 20vh;

  .search-container {
    position: relative;
    top: $toolbar-top-pos;
    justify-content: center;
    z-index: 2;
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
  .switch-center {
    display: flex;
    justify-content: center;
  }
</style>
