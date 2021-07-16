<template>
  <div class="container">
    <b-table
      id="result-table"
      :items="getPerson"
      :fields="personFields"
      :current-page="personCurrentPage"
      :per-page="personPerPage"
    >
      <template #cell(clinical_trials)="row">
        <b-button v-b-modal.clinical-trials-modal size="md" @click="renderClinicalTrialsTable(row.item.pid)" class="mr-1">
          show <b-badge variant="light">{{ row.item.participate_num }}</b-badge>
        </b-button>
        <!-- <b-dropdown id="clinical-trials-dropdown" dropleft class="mt-2">
          <b-card>
            <b-table
              id="clinical-trials-table"
              :items="getPerson"
              :fields="fields"
              :current-page="currentPage"
              :per-page="perPage"
            >
              <b-pagination
                v-model="currentPage"
                :total-rows="getPersonLength"
                :per-page="perPage"
                align="center"
              >
              </b-pagination>
            </b-table>
          </b-card>
        </b-dropdown> -->
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
      // searchResults: '',
      personFields: [
        { key: 'name_kor', label: '이름', sortable: true },
        { key: 'belong', label: '병원', sortable: true },
        { key: 'major', label: '진료 분야' },
        { key: 'clinical_trials', label: '임상 시험', tdClass: 'tdclass', thClass: 'thclass' },
        { key: 'thesis', label: '논문', thClass: 'thclass' },
      ],
      clinicalTrialsFields: [
        { key: 'title_kor', label: 'Title', sortable: true, thClass: 'clinicalTitle' },
        { key: 'title_eng', label: '', sortable: true }
      ],
      thesisFields: [
        { key: 'title', label: 'Title', sortable: true, thClass: 'thesisTitle' },
        { key: 'year', label: 'Year', sortable: true },
        { key: 'journal', label: 'Journal', sortable: true },
        { key: 'citation', label: 'Citation', sortable: true }
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
        this.participateItems = participateItems
      } catch (err) {
        console.log(err)
      }
    },
    async renderthesisTable (pid) {
      // api 추가
      // this.isBusy = true
      this.thesisItems = []
      try {
        const res = await api.getThesis(pid)
        const thesisData = res.data
        const thesisItems = []
        for (let data of thesisData) {
          thesisItems.push(data.thesis)
        }
        this.thesisItems = thesisItems
        // this.isBusy = false
      } catch (err) {
        console.log(err)
      }
    }
    // limitCheck (item) {
    //   if(item.length > 20){
    //     return true && this.hidedetails
    //   }
    //   return false && this.hidedetails
    // },
    // toggle () {
    //   this.hidedetails = !this.hidedetails
    // }
  }
}
</script>

<style>
  .container {
    margin-top: 32px
  }
  .table th, .table td {
    min-width: 150px;
  }
  .clinicalTitle {
    width: 50%;
  }
  .thesisTitle {
    width: 70%;
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
</style>