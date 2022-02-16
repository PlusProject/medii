import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Home, DoctorList, ClinicalTrialsList,Recommend,Jstest,Vvis,Choice,AllNetwork
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
      path: "/vvis",
      name: "vvis",
      component: Vvis,
    },
    {
      path: "/recommend",
      name: 'recommend',
      component: Recommend,
    },
    {
      path: "/jstest",
      name: "jstest",
      component: Jstest,
    },
    {
      path: "/choice",
      name: "choice",
      component: Choice,
    },
    {
      path: "/allnetwork",
      name: "allnetwork",
      component: AllNetwork,
    }
  ]
})

export default router