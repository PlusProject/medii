import Vue from 'vue'
import VueRouter from 'vue-router'

import {
  Home, Page2, Page3, Page4
} from './views'
Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      name: 'home',
      path: '/',
      component: Home,
      children: [
        {
          name: 'page2',
          path: '/page2',
          component: Page2
        }
      ]
    },
    {
      name: 'page3',
      path: '/page3',
      component: Page3
    },
    {
      name: 'page4',
      path: '/page4',
      component: Page4
    }
  ]
})

export default router