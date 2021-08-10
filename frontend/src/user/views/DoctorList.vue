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
        :headers="tableHeaders"
        :items="tableData"
        item-key="name_kor"
        :search="tableSearch"
        :sort-by.sync="sortBy"
        :sort-desc.sync="sortDesc"
        :single-expand="true"
        :expanded.sync="expanded"
        @item-expanded="onExapnd"
        show-expand
        :loading="tableLoading"
        loading-text="Loading... Please wait"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.name_kor !== ''"
            >
              {{ getQuery.name_kor }}
            </v-chip>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.belong !== ''"
            >
              {{ getQuery.belong }}
            </v-chip>
            <v-chip
              class="ma-2"
              color='primary'
              v-if="getQuery.major !== ''"
            >
              {{ getQuery.major }}
            </v-chip>
            <v-chip
              class="ma-2"
              :color="rareDisease ? 'error' : 'primary'"
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
        <template v-slot:item.name_kor="{ item }">
          <a :href="item.doctor_info.url" target="_blank">{{ item.name_kor }}</a>
        </template>
        <template v-slot:item.participate_num="{ item }">
          <v-btn
            @click.stop="showParticipateInfo(item)"
            :disabled="item.participate_num === 0"
          >
            {{ item.participate_num }}
          </v-btn>
        </template>
        <template v-slot:item.writes_num="{ item }">
          <v-btn
            @click.stop="showWritesInfo(item)"
            :disabled="item.writes_num === 0"
          >
            {{ item.writes_num }}
          </v-btn>
        </template>
        <template v-if="noData" v-slot:no-data>
          <p style="font-size: 30px; margin: 60px 0px;">
            <span v-if="checkQueryIsOne()" style="color: #f06060">'{{ noDataKeyword }}'</span>
            <span v-if="checkQueryIsOne()">에 대한 </span>
            검색 결과가 없습니다.
          </p>
        </template>
        <template v-slot:expanded-item="{ headers }">
          <td :colspan="headers.length" style="margin-top:20px">
            <v-card>
              <v-card-title>
                임상 coworker
              </v-card-title>
              {{ crisCoworker }}
            </v-card>
            <v-card>
              <v-card-title>
                논문 coworker
              </v-card-title>
              {{ thesisCoworker }}
            </v-card>
          </td>
        </template>
      </v-data-table>

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

      <v-dialog
        v-model="writesDialog"
        max-width="1000"
      >
        <v-card>
          <v-card-title>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="thesisSearch"
              append-icon="mdi-magnify"
              label="결과 내 검색"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="thesisHeaders"
            :items="thesisData"
            item-key="title"
            :search="thesisSearch"
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
          align: 'start',
          sortable: true,
          value: 'name_kor',
          width: '80px'
        },
        { text: '병원', value: 'belong', width: '200px' },
        { text: '진료분야', value: 'major' },
        { text: '임상 시험', value: 'participate_num' },
        { text: '논문', value: 'writes_num' },
      ],
      tableData: [],
      rareDisease: '',
      tableSearch: '',
      clinicalTrialsHeaders: [
        { 
          text: 'Index',
          align: 'start',
          sortable: true,
          value: 'index'
        },
        { text: '연구제목', value: 'title_kor', width: '30%' },
        { text: 'Scientific Title', value: 'title_eng', width: '40%' },
        { text: 'Source', value: 'source_name', width: '15%' },
        { text: 'Start Date', value: 'start_date', width: '15%' }
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
        { text: 'Title', value: 'title', width: '70%' },
        { text: 'Journal', value: 'journal', width: '15%' },
        { text: 'Year', value: 'publication_date' },
        { text: 'Citation', value: 'citation' }
      ],
      thesisData: [],
      thesisSearch: '',
      thesisCoworker: '',
      crisCoworker: '',
      sortByItems: [
        { title: '이름', value: 'name_kor'},
        { title: '임상 시험 수', value: 'participate_num' },
        { title: '논문 개수', value: 'writes_num' }
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
    // tableLoading () {
    //   return this.tableData.length === 0
    // },
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
          name_kor: this.getQuery.name_kor || '',
          belong: this.getQuery.belong || '',
          major: this.getQuery.major || '',
          disease: this.getQuery.disease || ''
        }
        // console.log(params)
        const res = await api.search(params)
        this.tableData = res.data.person
        this.rareDisease = res.data.rare
        console.log(this.rareDisease)
        if (this.tableData.length === 0){
          this.noData = true
        }
      } catch (err) {
        console.log(err)
      }
      this.tableLoading = false
    },
    async getCoworker (id) {
      try {
        const res = await api.getCoworker(id)
        this.thesisCoworker = res.data
      } catch (err) {
        console.log(err)
      }
    },
    async getCrisCoworker (id) {
      try {
        const res = await api.getCrisCoworker(id)
        this.crisCoworker = res.data
      } catch (err) {
        console.log(err)
      }
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
    },
    async onExapnd (item) {
      if (this.expanded.length === 0) {
        try {
          const id = item.item.pid
          this.getCoworker(id)
          this.getCrisCoworker(id)
        } catch (err) {
          console.log(err)
        }
      }
    },
    expandParticipateInfo (item) {
      const currentRowExpanded = this.expanded[0] === item;
      this.expanded = []
      const rowExpanded = this.expanded[0] === item;
      if (rowExpanded || currentRowExpanded) {
        this.expanded.pop()
      } else {
        this.expanded.push(item);
      }
    },
    expandWritesInfo (item) {
      const currentRowExpanded = this.expanded[0] === item;
      this.expanded = []
      const rowExpanded = this.expanded[0] === item;
      if (rowExpanded || currentRowExpanded) {
        this.expanded.pop()
      } else {
        this.expanded.push(item);
      }
    }
  }
}
</script>

<style scoped>
  a:link { text-decoration: none;}
  a:visited { text-decoration: none;}
  a:hover { text-decoration: underline;}
</style>