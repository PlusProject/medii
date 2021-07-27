import Vue from 'vue'
import Vuex from 'vuex'
import api from './api'

Vue.use(Vuex)
const state = {
  doctor_list: [],
  hospital_list: [],
  person: [],
  doctor_info: [],
  participate: [],
  writes: []
}

const getters = {
  doctorList (state) {
    return state.doctor_list
  },
  hospitalList (state) {
    return state.hospital_list
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