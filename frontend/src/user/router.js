import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Home, DoctorList, Page4
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
      path: '/doctor-list',
      component: DoctorList,
      props: true
    },
    {
      name: 'page4',
      path: '/page4',
      component: Page4
    }
  ]
})

export default router