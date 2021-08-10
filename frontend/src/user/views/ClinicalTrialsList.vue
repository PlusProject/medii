<template>
  <div style="width:1185px; margin:auto; margin-top:40px">
    <v-card>
      <v-card-title>
        <v-spacer></v-spacer>
        <v-text-field
          v-model="tableSearch"
          append-icon="mdi-magnify"
          label="결과 내 검색"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="clinicalTrialsHeaders"
        :items="clinicalTrialsData"
        item-key="index+${start_date}"
        :search="clinicalTrialsSearch"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :loading="tableLoading"
        loading-text="Loading... Please wait"
        height="560px"
        fixed-header
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.name_kor !== '' && !$store.state.showClinicalTrialsPage"
            >
              {{ getQuery.name_kor }}
            </v-chip>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.belong !== '' && !$store.state.showClinicalTrialsPage"
            >
              {{ getQuery.belong }}
            </v-chip>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.major !== '' && !$store.state.showClinicalTrialsPage"
            >
              {{ getQuery.major }}
            </v-chip>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.disease !== ''"
            >
              {{ getQuery.disease }}
            </v-chip>
            <v-spacer></v-spacer>
            <v-menu offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  color="primary"
                  dark
                  v-bind="attrs"
                  v-on="on"
                >
                  {{ '정렬 기준: ' + currentSortByTitle }}
                </v-btn>
              </template>
              <v-list>
                <v-list-item
                  v-for="(item, index) in sortByItems"
                  :key="index"
                  @click="setSortBy(index)"
                >
                  <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-btn
              color="primary"
              dark
              style="margin-left: 16px"
              @click="sortDesc = !sortDesc"
            >
              {{ sortOrder }}
            </v-btn>
          </v-toolbar>
        </template>
        <template v-slot:item.rare_disease="{ item }">
          <v-icon
            small
            color="red"
            v-if="item.rare_disease===1"
          >
            mdi-circle
          </v-icon>
        </template>
        <template v-if="noData" v-slot:no-data>
          <p style="font-size: 30px; margin: 180px 0px;">
            <span v-if="checkQueryIsOne()" style="color: #f06060">'{{ noDataKeyword }}'</span>
            <span v-if="checkQueryIsOne()">에 대한 </span>
            검색 결과가 없습니다.
          </p>
        </template>
      </v-data-table>

      <!-- 다이얼로그는 연구담당자 정보 -> cid를 받아서 해당 cid의 연구담당자 정보 가져오는 API로 받아오기 간단한 데이터 테이블카드로 구성 -->
      <v-dialog
        v-model="loadingDialog"
        hide-overlay
        persistent
        width="300"
      >
        <v-card
          color="primary"
          dark
        >
          <v-card-text>
              Loading... Please wait
            <v-progress-linear
              indeterminate
              color="white"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </v-dialog>

      <v-dialog
        v-model="participateDialog"
        max-width="1000"
      >
        <v-card>
          <v-card-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="clinicalTrialsSearch"
              append-icon="mdi-magnify"
              label="결과 내 검색"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="clinicalTrialsHeaders"
            :items="clinicalTrialsData"
            item-key="title"
            :search="clinicalTrialsSearch"
          >
            <template v-slot:item.index="{ index }">
              {{ index + 1}}
            </template>
          </v-data-table>
        </v-card>
      </v-dialog>
    </v-card>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import api from '../api'

export default {
  name: 'DoctorList',
  data () {
    return {
      tableHeaders: [
        {
          text: '이름',
          align: 'center',
          sortable: true,
          value: 'name_kor',
          width: '80px'
        },
        { text: '병원', value: 'belong', width: '200px', align: 'center' },
        { text: '진료분야', value: 'major', width: '50%', align: 'center'},
        { text: '임상 시험', value: 'participate_num', align: 'center' },
        { text: '논문', value: 'writes_num', align: 'center' },
      ],
      tableData: [],
      rareDisease: '',
      tableSearch: '',
      clinicalTrialsHeaders: [
        { 
          text: '희귀질환',
          align: 'center',
          sortable: true,
          value: 'rare_disease',
          width: '8%'
        },
        //희귀질환 여부 동그라미 추가 필요)
        { text: '연구제목', value: 'title_kor', width: '30%', align: 'center' },
        { text: 'Scientific Title', value: 'title_eng', width: '30%', align: 'center' },
        { text: 'Source', value: 'source_name', width: '10%', align: 'center' },
        { text: 'Start Date', value: 'start_date', width: '10%', align: 'center' },
        { text: '연구담당자', value: 'chief_name', width: '10%', align: 'center' },
      ],
      clinicalTrialsData: [],
      clinicalTrialsSearch: '',
      thesisHeaders: [
        { 
          text: 'Index',
          align: 'start',
          sortable: true,
          value: 'index'
        },
        { text: 'Title', value: 'title', width: '70%', align: 'center' },
        { text: 'Journal', value: 'journal', width: '15%', align: 'center' },
        { text: 'Year', value: 'publication_date', align: 'center' },
        { text: 'Citation', value: 'citation', align: 'center' }
      ],
      thesisData: [],
      thesisSearch: '',
      thesisCoworker: '',
      crisCoworker: '',
      sortByItems: [
        { title: '이름', value: 'name_kor', align: 'center' },
        { title: '임상 시험 수', value: 'participate_num', align: 'center' },
        { title: '논문 개수', value: 'writes_num', align: 'center' }
      ],
      currentSortByTitle: '임상 시험 수',
      sortBy: 'participate_num',
      sortDesc: true,
      expanded: [],
      participateDialog: false,
      writesDialog: false,
      participateExpand: false,
      writesExpand: false,
      loadingDialog: false,
      tableLoading: true,
      resultRender: {
        name_kor: '',
        belong: '',
        major: '',
        disease: ''
      },
      noData: false,
      noDataKeyword: ''
    }
  },
  mounted () {
    this.init()
  },
  computed: {
    ...mapGetters([ 'getQuery' ]),
    sortOrder () {
      return this.sortDesc ? '내림차순' : '오름차순'
    }
  },
  watch: {
    'getQuery' () {
      this.resultRender = JSON.parse(JSON.stringify(this.getQuery))
      this.init()
    }
  },
  methods: {
    async init () {
      this.tableData = []
      this.getSearchResults()
    },
    async getSearchResults () {
      this.tableLoading = true
      try {
        const params = {
          disease: this.getQuery.disease,
          rare: this.$store.state.showRareDisease
        }
        console.log(params)
        const res = await api.searchClinicalTrials(params)
        this.clinicalTrialsData = res.data
        if (this.clinicalTrialsData.length === 0){
          this.noData = true
        }
      } catch (err) {
        console.log(err)
      }
      this.tableLoading = false
    },
    setSortBy (index) {
      this.currentSortByTitle = this.sortByItems[index].title
      this.sortBy = this.sortByItems[index].value
    },
    async showParticipateInfo (item) {
      this.clinicalTrialsSearch = ''
      this.loadingDialog = true
      try {
        const res = await api.getClinicalTrials(item.pid)
        const clinicalTrialsData = res.data
        const clinicalTrialsItems = []
        for (let data of clinicalTrialsData) {
          clinicalTrialsItems.push(data.clinical_trials)
        }
        clinicalTrialsItems.sort(function(a, b) {
          if (a.start_date === '') {
            return 1;
          }
          else if (b.start_date === '') {
            return -1;
          }
          return new Date(b.start_date) - new Date(a.start_date)
        })
        this.clinicalTrialsData = clinicalTrialsItems
        this.loadingDialog = false
        this.participateDialog = true
      } catch (err) {
        console.log(err)
      }
    },
    async showWritesInfo (item) {
      this.thesisSearch = ''
      this.loadingDialog = true
      try {
        const res = await api.getThesis(item.pid)
        const thesisData = res.data
        const thesisItems = []
        for (let data of thesisData) {
          thesisItems.push(data.thesis)
        }
        thesisItems.sort(function (a, b) {
          if (a.citation === '') {
            return 1;
          }
          else if (b.citation === '') {
            return -1;
          }
          return b.citation - a.citation
        })
        this.thesisData = thesisItems
        this.loadingDialog = false
        this.writesDialog = true
      } catch (err) {
        console.log(err)
      }
    },
    checkQueryIsOne () {
      let query = JSON.parse(JSON.stringify(this.getQuery))
      let flag = 0
      for (let keyword in query) {
        if (query[keyword] && flag === 1) {
          return false
        }
        if (query[keyword]) {
          this.noDataKeyword = query[keyword]
          flag = 1
        }
      }
      return true
    }
  }
}
</script>

<style scoped>
  a:link { text-decoration: none;}
  a:visited { text-decoration: none;}
  a:hover { text-decoration: underline;}
</style>