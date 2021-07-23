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
              list="name-list"
              v-model="search.name"
              v-on:keydown.enter="submit"
              placeholder="의사명"
              autocomplete="off"
            ></b-form-input>
            <b-form-datalist
              id="name-list"
              :options="autoComplete.name_kor"
            />
          </b-col>
          <b-col md="2">
            <label for="belong">병원</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="belong"
              list="belong-list"
              v-model="search.hospital"
              v-on:keydown.enter="submit"
              placeholder="병원"
              autocomplete="off"
            ></b-form-input>
            <b-form-datalist
              id="belong-list"
              :options="autoComplete.belong"
            />
          </b-col> 
        </b-row>

        <b-row align-v="center" class="input-row">
          <b-col md="2">
            <label for="major">진료 분야</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="major"
              v-model="search.major"
              v-on:keydown.enter="submit"
              placeholder="심장, 폐, 동맥..."
              autocomplete="off"
            ></b-form-input>
          </b-col>

          <b-col md="2">
            <label for="disease">질병</label>
          </b-col>
          <b-col md="4">
            <b-form-input id="disease"
              v-model="search.disease"
              v-on:keydown.enter="submit"
              placeholder="I00, K00... / 동맥질환, 순환계통.."
              autocomplete="off"
            ></b-form-input>
          </b-col>
        </b-row>

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
        v-on:click="submit"
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
import api from '../api'

export default {
  name: 'SearchForm',
  data () {
    return {
      search: {
        name: '',
        hospital: '',
        major: '',
        disease: ''
      },
      autoComplete: {
        name_kor: [],
        belong: [],
        major: []
      }
    }
  },
  mounted () {
    this.init()
  },
  methods: {
    async init () {
      try {
        const res_name = await api.getNameList()
        const res_hospital = await api.getHospitalList()
        for(let n of res_name.data){
          this.autoComplete.name_kor.push(n.name_kor)
        }
        for(let h of res_hospital.data){
          this.autoComplete.belong.push(h.belong)
        }
      } catch (err) {
        console.log(err)
      }
    },
    clearAll () {
      this.search.name = '',
      this.search.hospital = ''
      this.search.major = ''
      this.search.disease = ''
      this.$store.dispatch('clearState')
      this.$router.push({name: 'home'})
    },
    async submit () {
      try {
        const res = await api.search(this.search.name, this.search.hospital, this.search.disease, this.search.major)
        console.log("data from Search")
        console.log(res.data)
        const results = res.data.person
        this.dispatchResults(results)
      } catch (err) {
        console.log(err)
      }
      
    },
    dispatchResults (data) {
      // const results = this.getResults()
      // this.splitThesis(results)
      
      this.$store.dispatch('commitSearchResults', {data: data})
      // 현재 search-results경로가 아니면 실행
      if (this.currentRouteName != 'search-results') {
        this.$router.push({name: 'search-results'})
      }
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