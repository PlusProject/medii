<template>
  <div class="container">
    <b-table
      id="result-table"
      :items="getPerson"
      :fields="personFields"
      :current-page="personCurrentPage"
      :per-page="personPerPage"
    >
      <template #cell(name_kor)="row">
        <b-link :href="row.item.doctor_info.url" target="_blank">
          {{ row.item.name_kor }}
        </b-link>
      </template>
      <template #cell(clinical_trials)="row">
        <b-button v-b-modal.clinical-trials-modal size="md" @click="renderClinicalTrialsTable(row.item.pid)" class="mr-1">
          show <b-badge variant="light">{{ row.item.participate_num }}</b-badge>
        </b-button>
      </template>

      <template #cell(thesis)="row">
        <b-button v-b-modal.thesis-modal size="md" @click="renderthesisTable(row.item.pid)" class="mr-1">
          show <b-badge variant="light">{{ row.item.thesis_num }}</b-badge>
        </b-button>
      </template>
      
      <!--<template #cell(specializedfield)="row">
        <span
          v-if="limitCheck(row.item.specializedfield)"
          @dblclick="toggle()"
        >
          {{ row.item.specializedfield.substr(0, 20) + '...' }}
        </span>
        <span v-else>
          {{ row.item.specializedfield }}
        </span>
      </template>-->
    </b-table>
    <b-pagination
      v-model="personCurrentPage"
      :total-rows="getPersonLength"
      :per-page="personPerPage"
      align="center"
    >
    </b-pagination>

    <b-modal
      id="clinical-trials-modal"
      title="임상 시험 목록"
      class="modal-thesis"
      size="xl"
      hide-footer
      centered
    >
      <b-table
        id="result-table"
        :items="participateItems"
        :fields="clinicalTrialsFields"
        :current-page="clinicalTrialsCurrentPage"
        :per-page="clinicalTrialsPerPage"
      >
        <template #cell(index)="row">
          {{ (clinicalTrialsCurrentPage-1) * clinicalTrialsPerPage + row.index + 1 }}
        </template>
      </b-table>
      <b-pagination
        v-model="clinicalTrialsCurrentPage"
        :total-rows="participateLength"
        :per-page="clinicalTrialsPerPage"
        align="right"
      >
      </b-pagination>
    </b-modal>

    <b-modal
      id="thesis-modal"
      title="논문"
      class="modal-thesis"
      size="xl"
      hide-footer
      centered
    >
      <b-table
        id="result-table"
        :items="thesisItems"
        :fields="thesisFields"
        :current-page="thesisCurrentPage"
        :per-page="thesisPerPage"
        busy.sync="isBusy"
      >
        <template #cell(index)="row">
          {{ (thesisCurrentPage-1) * thesisPerPage + row.index + 1 }}
        </template>
      </b-table>
      <b-spinner v-if="isBusy" variant="primary" label="Spinning" class="table-spinner"></b-spinner>
      <b-pagination
        v-model="thesisCurrentPage"
        :total-rows="thesisLength"
        :per-page="thesisPerPage"
        align="right"
      >
      </b-pagination>
    </b-modal>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';
import api from '../api'

export default {
  name: 'ResultTable',
  data () {
    return {
      personFields: [
        { key: 'name_kor', label: '이름', thClass: 'name', tdClass: 'name', sortable: true },
        { key: 'belong', label: '병원', thClass: 'belong', tdClass: 'belong', sortable: true },
        { key: 'major', label: '진료 분야', thClass: 'major', tdClass: 'major' },
        { key: 'clinical_trials', label: '임상 시험', tdClass: 'button', thClass: 'button' },
        { key: 'thesis', label: '논문', tdClass: 'button', thClass: 'button' },
      ],
      clinicalTrialsFields: [
        { key: 'index', label: 'Index', tdClass: 'index', thClass: 'index' },
        { key: 'title_kor', label: '연구제목', sortable: true, thClass: 'clinicalTitle' },
        { key: 'title_eng', label: 'Scientific Title', thClass: 'title_eng',sortable: true },
        { key: 'source_name', label: 'Source', thClass: 'source', sortable: true },
        { key: 'start_date', label: 'Start Date', thClass: 'startDate', sortable:true}
      ],
      thesisFields: [
        { key: 'index', label: 'Index', tdClass: 'index', thClass: 'index' },
        { key: 'title', label: 'Title', sortable: true, thClass: 'thesisTitle', tdClass: 'thesisTitle' },
        { key: 'journal', label: 'Journal', tdClass: 'journal', thClass: 'journal', sortable: true },
        { key: 'publication_date', label: 'Year', tdClass: 'publication_date', thClass: 'publication_date', sortable: true },
        { key: 'citation', label: 'Citation', tdClass: 'citation', thClass: 'citation', sortable: true }
      ],
      hidedetails: true,
      personPerPage: 10,
      personCurrentPage: 1,
      clinicalTrialsPerPage: 6,
      clinicalTrialsCurrentPage: 1,
      thesisPerPage: 6,
      thesisCurrentPage: 1,
      showClinicalTrials: false,
      showThesis: false,
      participateItems: [],
      thesisData: '',
      thesisItems: [],
      isBusy: false
    } 
  },
  computed: {
    ...mapGetters([ 'getInfo', 'getPerson', 'getParticipate', 'getWrites', 'getDoctorInfo', 'getPersonLength' ]),
    participateLength () {
      return this.participateItems.length
    },
    thesisLength () {
      return this.thesisItems.length
    }
  },
  methods: {
    async renderClinicalTrialsTable (pid) {
      // pid로 임상 데이터 가져오기, api 추가
      this.participateItems = []
      try {
        const res = await api.getClinicalTrials(pid)
        const participateData = res.data
        const participateItems = []
        for (let data of participateData) {
          participateItems.push(data.clinical_trials)
        }
        participateItems.sort(function(a, b) {
          if (a.start_date === '') {
            return 1;
          }
          else if (b.start_date === '') {
            return -1;
          }
          return new Date(b.start_date) - new Date(a.start_date)
        })
        this.participateItems = participateItems
      } catch (err) {
        console.log(err)
      }
    },
    async renderthesisTable (pid) {
      // this.isBusy = true
      this.thesisItems = []
      try {
        const res = await api.getThesis(pid)
        const thesisData = res.data
        const thesisItems = []
        for (let data of thesisData) {
          thesisItems.push(data.thesis)
        }
        thesisItems.sort(function (a, b) {
          if (a.publication_date === '') {
            return 1;
          }
          else if (b.publication_date === '') {
            return -1;
          }
          return b.publication_date - a.publication_date
        })
        this.thesisItems = thesisItems
        // this.isBusy = false
      } catch (err) {
        console.log(err)
      }
    }
  }
}
</script>

<style>
  .container {
    margin-top: 32px
  }
  .name {
    width: 10%;
  }
  .belong {
    width: 15%;
  }
  .major {
    width: 45%;
    word-break: break-all;
  }
  .clinicalTitle {
    width: 40%;
  }
  .startDate {
    width: 10%;
  }
  .title_eng {
    width: 30%;
  }
  .source {
    width: 15%;
  }
  .thesisTitle {
    width: 70%;
  }
  .journal {
    width: 15%;
  }
  .table-container {
    position: relative;
    width: 100%;
  }
  .b-table[aria-busy="true"] + .table-spinner {
    /* this assumes that the spinner component has a width and height */
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    z-index: 10; /* make sure spinner is over table */
  }
  .index {
    width: 5%;
  }
</style>