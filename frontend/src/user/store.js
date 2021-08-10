import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import api from './api'

Vue.use(Vuex)
const state = {
  search: {
    name_kor: '',
    belong: '',
    major: '',
    disease: ''
  },
  doctorList: [],
  hospitalList: [],
  diseaseList: [],
  rareDiseaseList: [],
  person: [],
  doctor_info: [],
  participate: [],
  writes: [],
  showRareDisease: false,
  showClinicalTrialsPage: false
}

const getters = {
  getQuery (state) {
    return state.search
  },
  doctorList (state) {
    return state.doctorList.sort()
  },
  hospitalList (state) {
    return state.hospitalList.sort()
  },
  diseaseList (state) {
    return state.diseaseList.sort()
  },
  rareDiseaseList (state) {
    return state.rareDiseaseList.sort()
  },
  getPerson (state) {
    return state.person
  },
  getParticipate (state) {
    return state.participate
  },
  getWrites (state) {
    return state.writes
  },
  getDoctorInfo (state) {
    return state.doctor_info
  },
  getPersonLength (state) {
    return state.person.length
  },
  getDoctorInfoLength (state) {
    return state.doctor_info.length
  },
  showRareDisease (state) {
    return state.showRareDisease
  },
  showClinicalTrialsPage (state) {
    return state.showClinicalTrialsPage
  }
}

const mutations = {
  setDetailQuery (state, data) {
    state.search.name_kor = data.name_kor || '',
    state.search.belong = data.belong || '',
    state.search.major = data.major || '',
    state.search.disease = data.disease || ''
  },
  setDiseaseQuery (state, data) {
    state.search.disease = data
  },
  initAutocomplete (state, data) {
    state.doctorList = data.doctorList
    state.hospitalList = data.hospitalList
    state.diseaseList = data.diseaseList
    state.rareDiseaseList = data.rareDiseaseList
  },
  savePersonInfo (state, data) {
    state.person = data
  },
  clearState (state) {
    state.person = [],
    state.doctor_info = [],
    state.participate = [],
    state.writes = []
  },
  clearSearchQuery (state) {
    const data = {
      name_kor: '',
      belong: '',
      major: '',
      disease: ''
    }
    state.search = data
  },
  setShowRareDisease (state, data) {
    state.showRareDisease = data
  },
  setShowClinicalTrialsPage (state, data) {
    state.showClinicalTrialsPage = data
  }
}

const actions = {
  async initAutocomplete ({ commit }) {
    const doctor = await api.getDoctorList()
    const hospital = await api.getHospitalList()
    const disease = await api.getDiseaseList()
    const rareDisease = await api.getRareDiseaseList()
    const doctorList = []
    const hospitalList = []
    const diseaseList = []
    const rareDiseaseList = []
    for (let name of doctor.data) {
      doctorList.push(name.name_kor)
    }
    for (let name of hospital.data) {
      hospitalList.push(name.belong)
    }
    for (let name of disease.data) {
      diseaseList.push(name.name_kor)
    }
    for (let name of rareDisease.data) {
      rareDiseaseList.push(name.name_kor)
    }
    const data = {
      doctorList,
      hospitalList,
      diseaseList,
      rareDiseaseList
    }
    commit('initAutocomplete', data)
  },
  commitSearchResults ({ commit }, { data }) {
      commit('savePersonInfo', data)
  },
  clearState ({ commit }) {
    commit('clearState')
  }
}

export default new Vuex.Store({
    plugins: [createPersistedState()],
    state: state,
    getters: getters,
    mutations: mutations,
    actions: actions
})