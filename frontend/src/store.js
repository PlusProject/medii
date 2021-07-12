import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
const state = {
  searchResults: []
}

const getters = {
  getInfo (state) {
    return state.searchResults
  },
  getLength (state) {
    return state.searchResults.length
  }
}

const mutations = {
  changeName (state, inputData) {
    state.searchResults = []
    for(var i=0; i<inputData.length; i++){
      state.searchResults.push(inputData[i])
    }
  },
  clearState (state) {
    state.searchResults = []
  }
}

const actions = {
  callMutation ({ state, commit }, {inputData}) {
      state
      commit('changeName', inputData)
  },
  clearState ({ state, commit }) {
    state
    commit('clearState')
  }
}

export default new Vuex.Store({
    state: state,
    getters: getters,
    mutations: mutations,
    actions: actions
})