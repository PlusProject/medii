<template>
  <div class="container">
    <b-table
      id="result-table"
      :items="getPerson"
      :fields="personFields"
      :current-page="personCurrentPage"
      :per-page="personPerPage"
    >
      <!-- <template #cell(thesis)="row">
        <b-button size="md" @click="info(row.item, row.index, $event.target)" class="mr-1">
          show
        </b-button>
      </template> -->

      <template #cell(clinical_trials)="row">
        <b-button v-b-modal.clinical-trials-modal size="md" @click="renderClinicalTrialsTable(row.item.pid)" class="mr-1">
          show
          <!-- show <b-badge variant="light">pid</b-badge> -->
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
          show
          <!-- show <b-badge variant="light">pid</b-badge> -->
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
      align="right"
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
      >
      </b-table>
      <b-pagination
        v-model="thesisCurrentPage"
        :total-rows="thesisLength"
        :per-page="thesisPerPage"
        align="center"
      >
      </b-pagination>
    </b-modal>

  </div>
</template>
<script>
import { mapGetters } from 'vuex';

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
        { key: 'title_kor', label: 'Title', sortable: true },
        { key: 'title_eng', label: '', sortable: true }
      ],
      thesisFields: [
        { key: 'title', label: 'Title', sortable: true },
        { key: 'year', label: 'Year', sortable: true },
        { key: 'journal', label: 'Journal', sortable: true },
        { key: 'citation', label: 'Citation', sortable: true }
      ],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: ''
      },
      hidedetails: true,
      personPerPage: 10,
      personCurrentPage: 1,
      clinicalTrialsPerPage: 6,
      clinicalTrialsCurrentPage: 1,
      thesisPerPage: 6,
      thesisCurrentPage: 1,
      showClinicalTrials: false,
      showThesis: false,
      participateData: '',
      participateItems: [],
      thesisData: '',
      thesisItems: []
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
  // watch: {
  //   'getParticipate' () {
  //     this.participateData = JSON.parse(JSON.stringify(this.getParticipate))
  //   }
  // },
  methods: {
    info(item, index, button) {
      this.infoModal.title = `${item.id}`
      this.infoModal.content = item.nameofthesis
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    resetInfoModal () {
      this.infoModal.title = ''
      this.infoModal.content = ''
    },
    renderClinicalTrialsTable (pid) {
      // pid로 임상 데이터 가져오기
      let participateItems = []
      this.participateData = JSON.parse(JSON.stringify(this.getParticipate))
      console.log(this.participateData)
      for (let i=0; i<this.participateData.length; i++) {
        if (this.participateData[i].pid == pid) {
          participateItems.push(this.participateData[i].clinical_trials)
        }
      }
      this.participateItems = participateItems
    },
    renderthesisTable (pid) {
      let thesisItems = []
      this.thesisData = JSON.parse(JSON.stringify(this.getWrites))
      for (let i=0; i<this.thesisData.length; i++) {
        if (this.thesisData[i].pid == pid) {
          thesisItems.push(this.thesisData[i].thesis)
        }
      }
      this.thesisItems = thesisItems
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
</style>