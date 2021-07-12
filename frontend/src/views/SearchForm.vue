<template>
  <div>
    <b-card bg-variant="light" class="card">
      <b-container>
        <b-row align-v="center" class="input-row">
          <b-col md="2">
            <label for="name">이름</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="name"
              v-model="search.id"
              v-on:keydown.enter="dispatchResults"
              placeholder="의사명"
            ></b-form-input>
          </b-col>
          <b-col md="2">
            <label for="belong">병원</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="belong"
              v-model="search.belong"
              v-on:keydown.enter="dispatchResults"
              placeholder="병원"
            ></b-form-input>
          </b-col> 
        </b-row>

        <b-row align-v="center" class="input-row">
          <b-col md="2">
            <label for="major">진료 분야</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="major"
              v-model="search.major"
              v-on:keydown.enter="dispatchResults"
              placeholder="심장, 폐, 동맥..."
            ></b-form-input>
          </b-col>

          <b-col md="2">
            <label for="disease_code">질환 분류</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="disease_code"
              v-model="search.disease_code"
              v-on:keydown.enter="dispatchResults"
              placeholder="I00, K00... / 동맥질환, 순환계통.."
            ></b-form-input>
          </b-col>
        </b-row>
        
        <!--<b-row align-v="center" class="input-row">
          <b-col md="2">
            <label for="researchtitle">연구 제목</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="researchtitle"
              v-model="search.researchtitle"
              v-on:keydown.enter="dispatchResults"
            ></b-form-input>
          </b-col>
          <b-col md="2">
            <label for="diseasecode">질환 분류</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="diseasecode"
              v-model="search.diseasecode"
              v-on:keydown.enter="dispatchResults"
            ></b-form-input>
          </b-col> 
        </b-row>-->

        <!--<b-row align-v="center" class="input-row">
          <b-col md="4">
            <b-form-checkbox>
              checkbox
            </b-form-checkbox>
          </b-col>
          <b-col md="4">
            <b-form-checkbox>
              checkbox2
            </b-form-checkbox>
          </b-col>
          <b-col md="4">
            <b-form-checkbox>
              checkbox3
            </b-form-checkbox>
          </b-col>
        </b-row>-->
      </b-container>
    </b-card>
    <p>
      <b-button
        variant="outline-success"
        v-on:click="dispatchResults"
        style="margin: 0px 4px;"
      >
        Search
      </b-button>
      <b-button
        variant="outline-primary"
        v-on:click="clearAll"
        style="margin: 0px 4px;"
      >
        Clear all
      </b-button>
    </p>
  </div>
</template>
<script>
import api from '../api.js'

export default {
  name: 'SearchForm',
  data () {
    return {
      search: {
        id: '권현철',
        belong: '삼성병원',
        major: '심장',
        // researchTitle_ko_field: '',
        disease_code: 'I00'
      },
      wholeData: null
    }
  },
  created() {
    //api call, save data
    this.getData()
  },
  methods: {
    clearAll () {
      this.search.id = '',
      this.search.belong = ''
      // this.search.researchTitle_ko_field = '',
      this.search.major = ''
      this.search.disease_code = ''
      this.$store.dispatch('clearState')
    },
    async getData () {
      const res = await api.getData()
      console.log(res.data)
      this.wholeData = res.data
    },
    dispatchResults () {
      const results = this.getResults()
      this.splitThesis(results)
      this.$store.dispatch('callMutation', {inputData: results})
      // 현재 search-results경로가 아니면 실행
      if (this.currentRouteName != 'search-results') {
        this.$router.push({name: 'search-results'})
      }
    },
    splitThesis (results) {
      for(var i=0; i<results.length; i++){
        results[i].researchTitle_ko_field = results[i].researchTitle_ko_field.replace(/,/gi,"\n\n")
      }
    },
    isSearchEmpty () {
      for(var key in this.search){
        if(this.search[key] !== ''){
          return false
        }
      }
      return true
    },
    getResults () {
      var results = []
      var isEmpty = this.isSearchEmpty()
      for(var i=0; i<this.wholeData.length; i++){
        let flag = 0
        if(!isEmpty){
          for(let key in this.search){
            if(this.search[key] === '' || this.wholeData[i][key].indexOf(this.search[key]) !== -1){
              continue;
            }
            flag = 1
            break;
          }
        }
        this.wholeData[i].major = this.wholeData[i].major.replace("진료분야: ","")
        if(flag !== 1){
          results.push(this.wholeData[i])
        }
      }
      return results
    }
  },
  computed: {
    currentRouteName() {
      return this.$route.name
    }
  }
}
</script>
<style>
label {
  margin: 0
}
.input-row {
  margin: 32px 8px
}
.card {
  margin: 32px
}
</style>