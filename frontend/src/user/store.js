import Vue from 'vue'
import Vuex from 'vuex'
import api from './api'

Vue.use(Vuex)
const state = {
  search: {
    name_kor: '',
    belong: '',
    major: '',
    disease: ''
  },
  doctor_list: [],
  hospital_list: [],
  person: [],
  doctor_info: [],
  participate: [],
  writes: []
}

const getters = {
  getQuery (state) {
    return state.search
  },
  doctorList (state) {
    return state.doctor_list.sort()
  },
  hospitalList (state) {
    return state.hospital_list.sort()
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
    state.doctor_list = data.doctor_list
    state.hospital_list = data.hospital_list
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
  }
}

const actions = {
  async initAutocomplete ({ commit }) {
    const doctor = await api.getDoctorList()
    const hospital = await api.getHospitalList()
    const doctor_list = []
    const hospital_list = []
    for (let name of doctor.data) {
      doctor_list.push(name.name_kor)
    }
    for (let name of hospital.data) {
      hospital_list.push(name.belong)
    }
    const data = {
      doctor_list,
      hospital_list
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
    state: state,
    getters: getters,
    mutations: mutations,
    actions: actions
})