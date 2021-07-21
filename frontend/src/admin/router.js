import Vue from 'vue'
import VueRouter from 'vue-router'

import {
    Home, ResultTable
} from './views'
Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  base: '/admin/',
  routes: [
    {
      name: 'home',
      path: '/',
      component: Home,
      children: [
        {
          path: '/search-results',
          name: 'search-results',
          component: ResultTable
        }
      ]
    }
  ]
})

export default router