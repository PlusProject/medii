<template>
  <div class="container">
    <b-table
      id="result-table"
      :items="getInfo"
      :fields="fields"
      :current-page="currentPage"
      :per-page="perPage"
    >
      <template #cell(thesis)="row">
        <b-button size="md" @click="info(row.item, row.index, $event.target)" class="mr-1">
          show
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
      v-model="currentPage"
      :total-rows="getLength"
      :per-page="perPage"
      align="center"
    >
    </b-pagination>
    <b-modal
      scrollable
      :id="infoModal.id"
      :title="infoModal.title"
      class="modal-thesis"
      size="lg"
      ok-only
      @hide="resetInfoModal"
    >
      <pre>{{ infoModal.content }}</pre>
    </b-modal>
  </div>
</template>
<script>
import { mapGetters } from 'vuex';

export default {
  name: 'ResultTable',
  data () {
    return {
      searchResults: '',
      fields: [
        { key: 'id', label: '이름', sortable: true },
        { key: 'belong', label: '병원', sortable: true },
        { key: 'major', label: '진료 분야' },
        { key: 'researchTitle_ko_field', label: '연구 제목', tdClass: 'tdclass', thClass: 'thclass' },
        // { key: 'researchtitle', label: '연구 제목' },
        { key: 'disease_code', label: '질환 분류', thClass: 'thclass' },
      ],
      infoModal: {
        id: 'info-modal',
        title: '',
        content: ''
      },
      hidedetails: true,
      perPage: 6,
      currentPage: 1
    } 
  },
  mounted () {
    this.searchResults = this.$store.getters.getInfo
  },
  computed: {
    ...mapGetters([ 'getInfo', 'getLength' ]),
    rows () {
      return this.searchResults.length
    }
    // searchData () {
    //   return this.$store.getters.getInfo
    // }
  },
  methods: {
    info(item, index, button) {
      this.infoModal.title = `${item.id}`
      this.infoModal.content = item.nameofthesis
      this.$root.$emit('bv::show::modal', this.infoModal.id, button)
    },
    resetInfoModal() {
      this.infoModal.title = ''
      this.infoModal.content = ''
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