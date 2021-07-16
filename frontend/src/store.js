import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const state = {
  searchResults: {
    person: [],
    doctor_info: [],
    participate: [],
    writes: []
  },
  person: [],
  doctor_info: [],
  participate: [],
  writes: []
}

const getters = {
  getInfo (state) {
    return state.searchResults
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
  // getParticipateLength (state) {
  //   return state.participate.length
  // },
  // getWritesLength (state) {
  //   return state.writes.length
  // }
  // getDoctorInfoLength (state) {
  //   return state.searchResults['doctor_info'].length
  // },
  // getParticipateLength (state) {
  //   return state.searchResults.participate.length
  // },
  // getWritesLength (state) {
  //   return state.searchResults.writes.length
  // }
}

const mutations = {
  savePersonInfo (state, data) {
    state.person = data
  },
  clearState (state) {
    state.searchResults = [],
    state.person = [],
    state.doctor_info = [],
    state.participate = [],
    state.writes = []
  }
}

const actions = {
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