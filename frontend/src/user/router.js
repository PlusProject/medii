import Vue from 'vue'
import VueRouter from 'vue-router'

import {

} from './views'
Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      name: 'home',
      path: '/',
      component: Home
    }
  ]
})

export default router