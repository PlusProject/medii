<template>
  <v-sheet
    fluid
    :max-width="width"
    overflow-y="auto"
    class="mx-auto rounded-xl"
    style="position: relative; margin-top: 20px; background-color: #fff"
    elevation="12"
  >
    <!-- <p :style="{ 'position': 'absolute', 'left': leftPos, 'top': topPos }">
      <i :style="{ 'font-size': fontSize }">press Enter to search</i>
    </p> -->
    
    <v-form>
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-col cols="12">
              <v-combobox
                v-model="detailSearch.name_kor"
                :items="doctorList"
                :disabled="showClinicalTrialsPage"
                label="이름"
                autocomplete="off"
                @keyup.enter="showSearchResults()"
                ref="nameCombobox"
              />
            </v-col>

            <v-col cols="12">
              <v-combobox
                v-model="detailSearch.belong"
                :items="hospitalList"
                :disabled="showClinicalTrialsPage"
                label="소속기관"
                autocomplete="off"
                @keyup.enter="showSearchResults()"
                ref="hospitalCombobox"
              />
            </v-col>
          </v-col>

          <v-col cols="6">
            <v-col cols="12">
              <v-text-field
                label="진료분야"
                placeholder="심장, 폐, 동맥..."
                :disabled="showClinicalTrialsPage"
                autocomplete="off"
                v-model="detailSearch.major"
                @keydown.enter="showSearchResults()"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                label="질병"
                placeholder="고혈압, 심근경색, 순환계통 / I00, C00, ..."
                autocomplete="off"
                v-model="detailSearch.disease"
                @keydown.enter="showSearchResults()"
              ></v-text-field>
              <!-- <v-combobox
                v-model="detailSearch.disease"
                :items="rareDiseaseList"
                label="질병"
                autocomplete="off"
                placeholder="고혈압, 심근경색, 순환계통 / I00, C00, ..."
                @keyup.enter="showSearchResults()"
                ref="diseaseCombobox"
              /> -->
            </v-col>
            <v-row>
              <v-switch
                v-model="showRareDisease"
                label="희귀질환만 보기"
                color="indigo"
                style="margin: auto"
              ></v-switch>
              <v-switch
                v-model="showClinicalTrialsPage"
                label="임상시험 기준으로 검색"
                color="indigo"
                style="margin: auto"
              ></v-switch>
            </v-row>
          </v-col>
        </v-row>
        <v-row class="ma-0 pb-3">
          <v-spacer/>
          <v-col cols="3" class="pa-0">
            <v-btn
              class="mx-auto rounded"
              :small="width < '800'"
              plane
              @click="searchWithClick()"
            >
              search
            </v-btn>
          </v-col>
          <v-spacer/>
        </v-row>
      </v-container>
    </v-form>
  </v-sheet>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'

export default {
  name: 'SearchDetail',
  props: [ 'visible', 'width' ],
  data () {
    return {
      name_kor: '',
      detailSearch: {
        name_kor: '',
        belong: '',
        major: '',
        disease: ''
      },
      height: '',
    }
  },
  methods: {
    ...mapMutations([ 'setDetailQuery', 'clearSearchQuery' ]),
    searchWithClick () {
      this.$refs["nameCombobox"].blur()
      this.$refs["hospitalCombobox"].blur()
      // this.$refs["diseaseCombobox"].blur()
      this.$nextTick(() => {
          this.showSearchResults()
      })
    },
    showSearchResults () {
      this.$emit('search')
      this.clearSearchQuery()
      this.setDetailQuery(this.detailSearch)
      this.detailSearch.name_kor=''
      this.detailSearch.belong=''
      this.detailSearch.major=''
      this.detailSearch.disease=''
      if (this.$store.state.showClinicalTrialsPage) {
        this.$router.push({ name: 'ClinicalTrialsList' })
      }
      else if (this.$route.name !== 'DoctorList') {
        this.$router.push({ name: 'DoctorList' })
      }
    },
    removeQuery () {
      this.detailSearch.name_kor=''
      this.detailSearch.belong=''
      this.detailSearch.major=''
    }
  },
  computed: {
    ...mapGetters([ 'doctorList', 'hospitalList', 'rareDiseaseList', 'showClinicalTrialsPage' ]),
    topPos () {
      return this.width.substring(0, 3) < 800 ? '150px' : '182px'
    },
    leftPos () {
      return this.width.substring(0, 3) / 2 + 'px'
    },
    fontSize () {
      return this.width.substring(0, 3) < 800 ? '14px' : 'medium'
    },
    showRareDisease: {
      get () {
        return this.$store.state.showRareDisease
      },
      set (value) {
        this.$store.commit('setShowRareDisease', value)
      }
    },
    showClinicalTrialsPage: {
      get () {
        return this.$store.state.showClinicalTrialsPage
      },
      set (value) {
        this.$store.commit('setShowClinicalTrialsPage', value)
      }
    }
  },
  watch: {
    '$store.state.showClinicalTrialsPage' () {
      console.log("changed")
      this.detailSearch.name_kor=''
      this.detailSearch.belong=''
      this.detailSearch.major=''
    }
  }
}
</script>

<style lang="scss">
  .v-menu__content .menuable__content__active .v-autocomplete__content{
    max-height: 150px !important;
  }
</style>