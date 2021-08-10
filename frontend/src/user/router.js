import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Home, DoctorList, ClinicalTrialsList, Page4
} from './views'
Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      name: 'home',
      path: '/',
      component: Home
    },
    {
      name: 'DoctorList',
      path: '/doctors',
      component: DoctorList
    },
    {
      name: 'ClinicalTrialsList',
      path: '/clinicaltrials',
      component: ClinicalTrialsList
    },
    {
      name: 'page4',
      path: '/page4',
      component: Page4
    }
  ]
})

export default router