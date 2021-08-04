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
                label="병원"
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
                autocomplete="off"
                v-model="detailSearch.major"
                @keydown.enter="showSearchResults()"
              ></v-text-field>
            </v-col>

            <v-col cols="12">
              <v-text-field
                label="질병"
                placeholder="순환계통, 신경계통... / I00, C00..."
                autocomplete="off"
                v-model="detailSearch.disease"
                @keydown.enter="showSearchResults()"
              ></v-text-field>
            </v-col>
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
      height: ''
    }
  },
  methods: {
    ...mapMutations([ 'setDetailQuery', 'clearSearchQuery' ]),
    onClick (index) {
      let autocomplete = Object.assign([], this.autocomplete);
      autocomplete[index] = !autocomplete[index]
      this.autocomplete = autocomplete
    },
    searchWithClick () {
      this.$refs["nameCombobox"].blur()
      this.$refs["hospitalCombobox"].blur()
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
      if (this.$route.name !== 'DoctorList') {
        this.$router.push({ name: 'DoctorList' })
      }
    },
    resetField (field) {
      switch (field) {
        case 0:
          this.detailSearch.name_kor=''
          break
        case 1:
          this.detailSearch.belong=''
          break
        case 2:
          this.detailSearch.major=''
          break
        case 3:
          this.detailSearch.disease=''
          break
      }
    }
  },
  computed: {
    ...mapGetters([ 'doctorList', 'hospitalList' ]),
    doctorItems () {
      const name = this.detailSearch.name_kor
      return this.doctorList.filter((cur) => {
        return cur.indexOf(name) > -1
      }).sort()
    },
    hospitalItems () {
      const name = this.detailSearch.belong
      return this.hospitalList.filter((cur) => {
        return cur.indexOf(name) > -1
      }).sort()
    },
    topPos () {
      return this.width.substring(0, 3) < 800 ? '150px' : '182px'
    },
    leftPos () {
      return this.width.substring(0, 3) / 2 + 'px'
    },
    fontSize () {
      return this.width.substring(0, 3) < 800 ? '14px' : 'medium'
    }
  }
}
</script>

<style lang="scss">
  .v-menu__content .menuable__content__active .v-autocomplete__content{
    max-height: 150px !important;
  }
</style>