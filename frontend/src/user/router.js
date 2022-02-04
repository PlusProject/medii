import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Home, DoctorList, ClinicalTrialsList, SocialNetwork, Recommend,PartialNetwork,Jstest
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
      name: "socialnetwork",
      path: "/socialnetwork",
      component: SocialNetwork,
    },
    {
      path: "/recommend",
      name: 'recommend',
      component: Recommend,
    },
    {
      name: 'PartialNetwork',
      path: '/partialnetwork',
      component: PartialNetwork,
    },
    {
      path: "/jstest",
      name: "jstest",
      component: Jstest,
    }
  ]
})

export default router