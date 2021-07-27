<template>
  <v-sheet
    fluid
    max-width="800px"
    overflow-y="auto"
    class="mx-auto rounded-xl"
    style="position: relative; margin-top: 20px; background-color: #fff"
    elevation="12"
  >
    <v-form>
      <v-container>
        <v-row>
          <v-col cols="6">
            <v-col cols="12">
              <v-combobox
                v-model="detailSearch.name_kor"
                :items="doctorItems"
                label="이름"
                @keyup.enter="showSearchResults()"
              />
            </v-col>

            <v-col cols="12">
              <v-combobox
                v-model="detailSearch.belong"
                :items="hospitalItems"
                label="병원"
                @keyup.enter="showSearchResults()"
              />
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
</template>

<script>
import { mapGetters } from 'vuex'

export default {
  name: 'SearchDetail',
  props: [ 'visible' ],
  data () {
    return {
      detailSearch: {
        name_kor: '',
        belong: '',
        major: '',
        disease: ''
      },
      autocomplete: [ false, false, false, false ]
    }
  },
  methods: {
    test (e) {
      this.detailSearch.name_kor = e.target.value
    },
    onClick (index) {
      let autocomplete = Object.assign([], this.autocomplete);
      autocomplete[index] = !autocomplete[index]
      this.autocomplete = autocomplete
    },
    showSearchResults () {
      this.$router.push({ name: 'page3', params: { elasticSearch: '', detailSearch: this.detailSearch }})
    },
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
    }
  }
}
</script>

<style lang="scss">
  .rotate {
    transform: rotate(180);
  }
  .v-menu__content .menuable__content__active .v-autocomplete__content{
    max-height: 150px !important;
  }
</style>